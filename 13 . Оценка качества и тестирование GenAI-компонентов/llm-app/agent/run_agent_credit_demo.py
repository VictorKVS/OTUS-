from __future__ import annotations

import argparse
import json
import logging
import re
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rag.rag_demo_common import (
    DEFAULT_CHAT_MODEL,
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_KNOWLEDGE_PATH,
    DEFAULT_OLLAMA_API_KEY,
    DEFAULT_OLLAMA_BASE_URL,
    DEFAULT_QDRANT_COLLECTION,
    DEFAULT_QDRANT_HOST,
    DEFAULT_QDRANT_PORT,
    DEFAULT_TOP_K,
    build_context,
    load_knowledge_chunks,
    make_ollama_client,
    parse_optional_float,
    search_chunks,
    seed_collection,
    setup_logging,
)


PACKAGE_ROOT = Path(__file__).resolve().parent
DEFAULT_CASES_PATH = PACKAGE_ROOT / "data" / "mock_credit_cases.json"
ALLOWED_STATUSES = {"ok", "blocked", "manual_review", "insufficient"}
MAX_RERUN_CHECKS = 2
LOG_BLOCK_WIDTH = 72

INTERACTIVE_HELP = """Команды:
- `exit`, `quit`, `q`, `выход` — завершить диалог.
- `:help` — показать эту подсказку.
- `:cases` — показать все mock-кейсы.
- `:case` — показать текущий кейс.
- `:use CASE_ID` — переключиться на другой кейс.
"""

CHECK_CATALOG: dict[str, dict[str, str]] = {
    "eligibility": {
        "label": "Допуск к заявке",
        "description": "Проверка возраста, резидентства, регистрации, телефона и правила повторной заявки после отказа.",
    },
    "income_employment": {
        "label": "Доход и занятость",
        "description": "Проверка минимального дохода, стажа на текущем месте и срока деятельности для самозанятых и ИП.",
    },
    "auto_decline": {
        "label": "Автоотказ",
        "description": "Проверка условий автоматического отказа по просрочке, PTI, BKI mismatch и device swap.",
    },
    "manual_review": {
        "label": "Ручная проверка",
        "description": "Проверка условий передачи заявки андеррайтеру.",
    },
    "documents": {
        "label": "Документы",
        "description": "Проверка набора документов и дополнительных подтверждений.",
    },
    "pricing": {
        "label": "Ставка и срок",
        "description": "Проверка диапазона ставки и допустимого срока по продукту.",
    },
    "offer_validity": {
        "label": "Срок жизни оферты",
        "description": "Проверка срока действия одобренной оферты.",
    },
    "disbursement": {
        "label": "Выдача",
        "description": "Проверка, когда клиент получает деньги или товар.",
    },
    "payments": {
        "label": "Платежи",
        "description": "Проверка даты платежа, автосписания и поведения на выходных.",
    },
    "early_repayment": {
        "label": "Досрочное погашение",
        "description": "Проверка правил полного и частичного досрочного погашения.",
    },
    "hardship": {
        "label": "Реструктуризация",
        "description": "Проверка доступности программы снижения платежа и её ограничений.",
    },
    "collections": {
        "label": "Просрочка и штрафы",
        "description": "Проверка напоминаний, контактов и штрафов при просрочке.",
    },
}

KEYWORD_CHECK_MAP: dict[str, tuple[str, ...]] = {
    "eligibility": ("подать", "заявк", "возраст", "регистрац", "резидент", "отказ", "телефон"),
    "income_employment": ("доход", "стаж", "самозан", "ип", "работ", "занятост"),
    "auto_decline": ("автоотказ", "отклон", "pti", "просроч", "долгов"),
    "manual_review": ("ручн", "андеррайт", "видео", "проверк"),
    "documents": ("документ", "паспорт", "справк", "выписк", "селфи"),
    "pricing": ("ставк", "процент", "срок", "зарплатн"),
    "offer_validity": ("оферт", "действ"),
    "disbursement": ("выдач", "получ", "зачисл", "товар"),
    "payments": ("платеж", "автоспис", "5-е", "15-е", "25-е"),
    "early_repayment": ("досроч", "погаш"),
    "hardship": ("реструктур", "каникул", "снижени", "больнич"),
    "collections": ("штраф", "взыск", "напоминан", "email", "push"),
}

DEFAULT_BROAD_CHECKS = [
    "eligibility",
    "income_employment",
    "auto_decline",
    "manual_review",
    "documents",
    "pricing",
    "offer_validity",
    "early_repayment",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Запускает controlled-agent demo поверх локального RAG, Qdrant и Ollama."
    )
    parser.add_argument(
        "--knowledge-file",
        default=str(DEFAULT_KNOWLEDGE_PATH),
        help="Путь до JSON-файла со знаниями.",
    )
    parser.add_argument(
        "--cases-file",
        default=str(DEFAULT_CASES_PATH),
        help="Путь до JSON-файла с mock-кейсами.",
    )
    parser.add_argument(
        "--collection",
        default=DEFAULT_QDRANT_COLLECTION,
        help="Имя коллекции в Qdrant.",
    )
    parser.add_argument(
        "--qdrant-host",
        default=DEFAULT_QDRANT_HOST,
        help="Хост Qdrant.",
    )
    parser.add_argument(
        "--qdrant-port",
        type=int,
        default=DEFAULT_QDRANT_PORT,
        help="REST-порт Qdrant.",
    )
    parser.add_argument(
        "--ollama-base-url",
        default=DEFAULT_OLLAMA_BASE_URL,
        help="OpenAI-compatible URL локального Ollama.",
    )
    parser.add_argument(
        "--ollama-api-key",
        default=DEFAULT_OLLAMA_API_KEY,
        help="API key для Ollama.",
    )
    parser.add_argument(
        "--chat-model",
        default=DEFAULT_CHAT_MODEL,
        help="Локальная chat-модель через Ollama.",
    )
    parser.add_argument(
        "--embedding-model",
        default=DEFAULT_EMBEDDING_MODEL,
        help="Локальная embedding-модель через Ollama.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_TOP_K,
        help="Сколько top-k чанков брать из Qdrant для одной подзадачи.",
    )
    parser.add_argument(
        "--score-threshold",
        default="",
        help="Минимальный score Qdrant. По умолчанию фильтр отключен.",
    )
    parser.add_argument(
        "--case-id",
        default="C-102",
        help="Какой mock-кейс использовать по умолчанию.",
    )
    parser.add_argument(
        "--question",
        default="",
        help="Если передан, будет выполнен один запрос без интерактивного цикла.",
    )
    parser.add_argument(
        "--list-cases",
        action="store_true",
        help="Показать все mock-кейсы и завершиться.",
    )
    parser.add_argument(
        "--reindex",
        action="store_true",
        help="Перед запуском пересоздать коллекцию и заново залить знания.",
    )
    parser.add_argument(
        "--hide-chunks",
        action="store_true",
        help="Не печатать каталог чанков при переиндексации.",
    )
    return parser


def load_mock_cases(cases_path: Path) -> dict[str, dict[str, Any]]:
    if not cases_path.exists():
        raise FileNotFoundError(f"Файл mock-кейсов не найден: {cases_path}")

    raw_items = json.loads(cases_path.read_text(encoding="utf-8"))
    if not isinstance(raw_items, list) or not raw_items:
        raise ValueError(f"Ожидался непустой JSON-список в {cases_path}")

    cases: dict[str, dict[str, Any]] = {}
    for index, raw_item in enumerate(raw_items, start=1):
        if not isinstance(raw_item, dict):
            raise ValueError(f"Элемент #{index} в {cases_path} должен быть объектом.")
        case_id = str(raw_item.get("case_id") or "").strip()
        title = str(raw_item.get("title") or "").strip()
        application = raw_item.get("application")
        if not case_id:
            raise ValueError(f"У mock-кейса #{index} пустой case_id.")
        if not title:
            raise ValueError(f"У mock-кейса {case_id} пустой title.")
        if not isinstance(application, dict):
            raise ValueError(f"У mock-кейса {case_id} поле application должно быть объектом.")
        if case_id in cases:
            raise ValueError(f"Дублируется case_id: {case_id}")
        cases[case_id] = raw_item

    return cases


def ordered_unique(items: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def bool_text(value: Any) -> str:
    return "да" if bool(value) else "нет"


def optional_text(value: Any) -> str:
    if value is None or value == "":
        return "неизвестно"
    if isinstance(value, bool):
        return bool_text(value)
    if isinstance(value, list):
        return ", ".join(str(item) for item in value) if value else "нет"
    return str(value)


def humanize_product(product_type: str) -> str:
    mapping = {
        "cash_loan": "кредит наличными",
        "pos": "POS-кредит",
        "refinance": "рефинансирование",
    }
    return mapping.get(product_type, product_type)


def humanize_city_type(city_type: str) -> str:
    return "город-миллионник" if city_type == "million_plus" else "не-миллионник"


def humanize_employment(employment_type: str) -> str:
    mapping = {
        "salary": "наёмный сотрудник",
        "self_employed": "самозанятый",
        "ip": "ИП",
    }
    return mapping.get(employment_type, employment_type)


def render_case_summary(case: dict[str, Any]) -> str:
    app = case["application"]
    return (
        f"{case['case_id']} | {case['title']} | "
        f"product={humanize_product(str(app.get('product_type') or ''))} | "
        f"amount={optional_text(app.get('requested_amount_rub'))} RUB | "
        f"income={optional_text(app.get('monthly_income_rub'))} RUB | "
        f"pti={optional_text(app.get('pti_percent'))}% | "
        f"payroll={bool_text(app.get('payroll_client'))}"
    )


def render_case_facts(case: dict[str, Any]) -> str:
    app = case["application"]
    return "\n".join(
        [
            f"case_id: {case['case_id']}",
            f"title: {case['title']}",
            f"summary: {case.get('summary') or '-'}",
            f"product_type: {humanize_product(str(app.get('product_type') or ''))}",
            f"requested_amount_rub: {optional_text(app.get('requested_amount_rub'))}",
            f"term_months: {optional_text(app.get('term_months'))}",
            f"city_type: {humanize_city_type(str(app.get('city_type') or ''))}",
            f"age_years: {optional_text(app.get('age_years'))}",
            f"monthly_income_rub: {optional_text(app.get('monthly_income_rub'))}",
            f"employment_type: {humanize_employment(str(app.get('employment_type') or ''))}",
            f"current_job_months: {optional_text(app.get('current_job_months'))}",
            f"business_activity_months: {optional_text(app.get('business_activity_months'))}",
            f"payroll_client: {bool_text(app.get('payroll_client'))}",
            f"internal_rating: {optional_text(app.get('internal_rating'))}",
            f"pti_percent: {optional_text(app.get('pti_percent'))}",
            f"has_current_delinquency: {bool_text(app.get('has_current_delinquency'))}",
            f"max_dpd_last_180_days: {optional_text(app.get('max_dpd_last_180_days'))}",
            f"passport_bki_mismatch: {bool_text(app.get('passport_bki_mismatch'))}",
            f"remote_device_swap_signs: {bool_text(app.get('remote_device_swap_signs'))}",
            f"tax_resident_rf: {bool_text(app.get('tax_resident_rf'))}",
            f"registration_in_company_region: {bool_text(app.get('registration_in_company_region'))}",
            f"phone_registered_days: {optional_text(app.get('phone_registered_days'))}",
            f"last_rejection_days_ago: {optional_text(app.get('last_rejection_days_ago'))}",
            f"income_mismatch: {bool_text(app.get('income_mismatch'))}",
            f"nonstandard_income_source: {bool_text(app.get('nonstandard_income_source'))}",
            f"fraud_flags: {optional_text(app.get('fraud_flags'))}",
        ]
    )


def print_case_catalog(cases: dict[str, dict[str, Any]], logger: logging.Logger) -> None:
    logger.info("Доступные mock-кейсы:")
    for case_id in sorted(cases):
        logger.info("%s", render_case_summary(cases[case_id]))


def get_mock_application(
    case_id: str,
    *,
    cases: dict[str, dict[str, Any]],
    logger: logging.Logger,
) -> dict[str, Any]:
    normalized_case_id = case_id.strip().upper()
    if normalized_case_id not in cases:
        raise KeyError(f"Mock-кейс не найден: {case_id}")

    logger.info("TOOL get_mock_application(case_id=%s)", normalized_case_id)
    case = cases[normalized_case_id]
    logger.info("TOOL RESULT %s", render_case_summary(case))
    logger.info("TOOL CASE FACTS\n%s", render_case_facts(case))
    return case


def parse_json_response(raw_text: str) -> Any | None:
    candidates: list[str] = []
    stripped = raw_text.strip()
    if stripped:
        candidates.append(stripped)

    fenced_match = re.search(r"```(?:json)?\s*(.*?)```", stripped, re.DOTALL)
    if fenced_match:
        candidates.append(fenced_match.group(1).strip())

    for opening, closing in (("{", "}"), ("[", "]")):
        start = stripped.find(opening)
        end = stripped.rfind(closing)
        if start != -1 and end != -1 and end > start:
            candidates.append(stripped[start : end + 1].strip())

    for candidate in ordered_unique(candidates):
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue

    return None


def log_block(
    logger: logging.Logger,
    title: str,
    *,
    cycle: int | None = None,
    suffix: str = "",
    char: str = "=",
) -> None:
    line = char * LOG_BLOCK_WIDTH
    header = title if cycle is None else f"{title} | cycle={cycle}"
    if suffix:
        header = f"{header} | {suffix}"
    logger.info(line)
    logger.info(header)
    logger.info(line)


def log_text_block(
    logger: logging.Logger,
    title: str,
    text: str,
    *,
    cycle: int | None = None,
    suffix: str = "",
    char: str = "=",
) -> None:
    log_block(logger, title, cycle=cycle, suffix=suffix, char=char)
    logger.info("%s", text)


def log_json_block(
    logger: logging.Logger,
    title: str,
    payload: Any,
    *,
    cycle: int | None = None,
    suffix: str = "",
    char: str = "=",
) -> None:
    log_text_block(
        logger,
        title,
        json.dumps(payload, ensure_ascii=False, indent=2),
        cycle=cycle,
        suffix=suffix,
        char=char,
    )


def render_plan_outline(plan: dict[str, Any]) -> str:
    lines = [
        f"goal: {plan['goal']}",
        "required_checks:",
    ]
    for index, check_id in enumerate(plan["required_checks"], start=1):
        label = CHECK_CATALOG.get(check_id, {}).get("label", check_id)
        lines.append(f"{index}. {check_id} | {label}")

    if plan.get("missing_case_fields"):
        lines.append("missing_case_fields:")
        for field_name in plan["missing_case_fields"]:
            lines.append(f"- {field_name}")

    lines.append("subquestions:")
    for index, item in enumerate(plan["subquestions"], start=1):
        lines.append(f"{index}. {item['check_id']} -> {item['question']}")
    return "\n".join(lines)


def render_records_outline(records: list[dict[str, Any]]) -> str:
    if not records:
        return "Пока нет результатов проверок."

    lines: list[str] = []
    for index, record in enumerate(records, start=1):
        lines.append(
            f"{index}. {record['check_id']} | status={record['status']} | "
            f"hits={record.get('hit_count', 0)} | sources={', '.join(record.get('sources', [])) or 'нет'}"
        )
        lines.append(f"   answer: {record['answer']}")
        uncertainty = str(record.get("uncertainty") or "").strip()
        if not is_no_uncertainty(uncertainty):
            lines.append(f"   uncertainty: {uncertainty}")
    return "\n".join(lines)


def render_rerun_outline(rerun_checks: list[dict[str, str]]) -> str:
    if not rerun_checks:
        return "Self-check не запросил дополнительный retrieval."

    lines: list[str] = []
    for index, item in enumerate(rerun_checks, start=1):
        check_id = item["check_id"]
        label = CHECK_CATALOG.get(check_id, {}).get("label", check_id)
        lines.append(f"{index}. {check_id} | {label}")
        lines.append(f"   follow_up_question: {item['follow_up_question']}")
    return "\n".join(lines)


def evaluate_result(records: list[dict[str, Any]], review: dict[str, Any]) -> dict[str, Any]:
    counters = {
        "ok": 0,
        "blocked": 0,
        "manual_review": 0,
        "insufficient": 0,
    }
    for record in records:
        status = str(record.get("status") or "")
        if status in counters:
            counters[status] += 1

    return {
        "checks_total": len(records),
        "status_counters": counters,
        "needs_revision": bool(review.get("needs_revision")),
        "issues_count": len(review.get("issues", [])),
        "rerun_count": len(review.get("rerun_checks", [])),
        "uncertainty_count": len(review.get("extra_uncertainties", [])),
        "overall_summary": build_overall_summary(records),
    }


def llm_text_call(
    *,
    system_prompt: str,
    user_prompt: str,
    model: str,
    ollama_base_url: str,
    ollama_api_key: str,
    logger: logging.Logger,
    step_name: str,
    max_tokens: int,
) -> str:
    logger.info("LLM step=%s | model=%s", step_name, model)
    client = make_ollama_client(base_url=ollama_base_url, api_key=ollama_api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
        max_tokens=max_tokens,
    )
    text = (response.choices[0].message.content or "").strip()
    logger.info("LLM step=%s | response_chars=%d", step_name, len(text))
    logger.info("LLM RAW %s\n%s", step_name, text)
    return text


def llm_json_call(
    *,
    system_prompt: str,
    user_prompt: str,
    model: str,
    ollama_base_url: str,
    ollama_api_key: str,
    logger: logging.Logger,
    step_name: str,
    max_tokens: int,
) -> Any | None:
    raw_text = llm_text_call(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model=model,
        ollama_base_url=ollama_base_url,
        ollama_api_key=ollama_api_key,
        logger=logger,
        step_name=step_name,
        max_tokens=max_tokens,
    )
    parsed = parse_json_response(raw_text)
    if parsed is None:
        logger.warning("LLM step=%s вернул невалидный JSON, включаю fallback.", step_name)
    return parsed


def infer_checks_from_question(question: str) -> list[str]:
    lowered = question.lower()
    selected: list[str] = []

    if any(token in lowered for token in ("проверь кейс", "разбери кейс", "сделай вывод", "общий вывод")):
        return DEFAULT_BROAD_CHECKS.copy()

    for check_id, keywords in KEYWORD_CHECK_MAP.items():
        if any(keyword in lowered for keyword in keywords):
            selected.append(check_id)

    if any(token in lowered for token in ("может ли", "можно ли", "подать заявку")):
        selected.extend(["eligibility", "income_employment", "auto_decline", "manual_review"])

    if not selected:
        return DEFAULT_BROAD_CHECKS.copy()

    return ordered_unique(selected)


def infer_missing_case_fields(case: dict[str, Any]) -> list[str]:
    app = case["application"]
    missing: list[str] = []

    if app.get("payroll_client") and not app.get("internal_rating"):
        missing.append("internal_rating")

    employment_type = str(app.get("employment_type") or "")
    if employment_type in {"self_employed", "ip"}:
        if app.get("business_activity_months") is None or app.get("business_activity_months") == "":
            missing.append("business_activity_months")
    else:
        if app.get("current_job_months") is None or app.get("current_job_months") == "":
            missing.append("current_job_months")

    return missing


def build_subquestion(check_id: str, case: dict[str, Any], user_question: str) -> str:
    app = case["application"]
    amount = optional_text(app.get("requested_amount_rub"))
    product = humanize_product(str(app.get("product_type") or ""))
    payroll = "зарплатный" if app.get("payroll_client") else "не зарплатный"

    templates = {
        "eligibility": "Может ли клиент подать заявку с точки зрения возраста, резидентства, регистрации, телефона и правила 14 дней после отказа?",
        "income_employment": "Проходит ли клиент требования по доходу и стажу или сроку деятельности для продукта?",
        "auto_decline": "Есть ли для этого кейса условия автоматического отказа по PTI, текущей просрочке, давней просрочке, BKI mismatch или device swap?",
        "manual_review": "Нужно ли отправлять заявку в ручную проверку из-за нестандартного дохода или расхождений в данных?",
        "documents": f"Какие документы нужны клиенту по {product} на сумму {amount} рублей с учётом того, что клиент {payroll}?",
        "pricing": f"Какой диапазон ставки и допустимый срок применимы к этому {payroll} клиенту по продукту {product}?",
        "offer_validity": "Сколько дней действует одобренная оферта?",
        "disbursement": "Когда клиент получит деньги или товар после одобрения?",
        "payments": "Какой график платежей и что происходит, если дата платежа попадает на выходной?",
        "early_repayment": "Можно ли сделать частичное досрочное погашение, есть ли комиссия и какой минимальный порог?",
        "hardship": "Доступна ли клиенту программа реструктуризации и какие для неё условия?",
        "collections": "Как идут напоминания и какой штраф при просрочке?",
    }
    return templates.get(check_id, user_question)


def build_default_plan(question: str, case: dict[str, Any]) -> dict[str, Any]:
    required_checks = infer_checks_from_question(question)
    return {
        "goal": f"Разобрать кейс {case['case_id']} и ответить на вопрос пользователя.",
        "required_checks": required_checks,
        "missing_case_fields": infer_missing_case_fields(case),
        "subquestions": [
            {"check_id": check_id, "question": build_subquestion(check_id, case, question)}
            for check_id in required_checks
        ],
        "answer_sections": [CHECK_CATALOG[check_id]["label"] for check_id in required_checks],
    }


def validate_plan(raw_plan: Any, *, question: str, case: dict[str, Any]) -> dict[str, Any]:
    fallback = build_default_plan(question, case)
    if not isinstance(raw_plan, dict):
        return fallback

    required_checks_raw = raw_plan.get("required_checks") or []
    required_checks = [
        str(item).strip()
        for item in required_checks_raw
        if str(item).strip() in CHECK_CATALOG
    ]

    if not required_checks:
        required_checks = fallback["required_checks"]

    for check_id in fallback["required_checks"]:
        if check_id not in required_checks and check_id in infer_checks_from_question(question):
            required_checks.append(check_id)

    subquestions_map: dict[str, str] = {}
    for item in raw_plan.get("subquestions") or []:
        if not isinstance(item, dict):
            continue
        check_id = str(item.get("check_id") or "").strip()
        prompt = str(item.get("question") or "").strip()
        if check_id in CHECK_CATALOG and prompt:
            subquestions_map[check_id] = prompt

    subquestions = []
    for check_id in required_checks:
        subquestions.append(
            {
                "check_id": check_id,
                "question": subquestions_map.get(check_id) or build_subquestion(check_id, case, question),
            }
        )

    missing_case_fields = ordered_unique(
        [
            str(item).strip()
            for item in (raw_plan.get("missing_case_fields") or [])
            if str(item).strip()
        ]
        + fallback["missing_case_fields"]
    )

    answer_sections = [
        str(item).strip()
        for item in (raw_plan.get("answer_sections") or [])
        if str(item).strip()
    ]
    if not answer_sections:
        answer_sections = [CHECK_CATALOG[check_id]["label"] for check_id in required_checks]

    goal = str(raw_plan.get("goal") or "").strip() or fallback["goal"]

    return {
        "goal": goal,
        "required_checks": ordered_unique(required_checks),
        "missing_case_fields": missing_case_fields,
        "subquestions": subquestions,
        "answer_sections": answer_sections,
    }


def plan_case(
    *,
    case: dict[str, Any],
    question: str,
    model: str,
    ollama_base_url: str,
    ollama_api_key: str,
    logger: logging.Logger,
) -> dict[str, Any]:
    system_prompt = (
        "Ты planner-узел controlled-agent demo по внутренним кредитным политикам. "
        "Нельзя отвечать по существу на вопрос пользователя. "
        "Нужно только разложить задачу на компактный план и вернуть JSON."
    )
    checks_text = "\n".join(
        f"- {check_id}: {payload['description']}"
        for check_id, payload in CHECK_CATALOG.items()
    )
    user_prompt = (
        "Верни только JSON-объект вида:\n"
        "{\n"
        '  "goal": "...",\n'
        '  "required_checks": ["eligibility", "documents"],\n'
        '  "missing_case_fields": ["internal_rating"],\n'
        '  "subquestions": [{"check_id": "eligibility", "question": "..."}],\n'
        '  "answer_sections": ["Допуск к заявке", "Документы"]\n'
        "}\n\n"
        "Правила:\n"
        "- используй только допустимые check_id;\n"
        "- выбери от 3 до 8 проверок;\n"
        "- подзадачи должны быть короткими;\n"
        "- добавляй missing_case_fields только если поле реально влияет на ответ;\n"
        "- никаких пояснений вне JSON.\n\n"
        f"Допустимые check_id:\n{checks_text}\n\n"
        f"Вопрос пользователя:\n{question}\n\n"
        f"Факты кейса:\n{render_case_facts(case)}"
    )
    raw_plan = llm_json_call(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model=model,
        ollama_base_url=ollama_base_url,
        ollama_api_key=ollama_api_key,
        logger=logger,
        step_name="planner",
        max_tokens=900,
    )
    plan = validate_plan(raw_plan, question=question, case=case)
    logger.info("AGENT PLAN\n%s", json.dumps(plan, ensure_ascii=False, indent=2))
    return plan


def parse_check_answer(raw_text: str, known_sources: list[str]) -> dict[str, Any]:
    parsed: dict[str, str] = {}
    for line in raw_text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        parsed[key.strip().lower()] = value.strip()

    status = parsed.get("статус", "").strip().lower().replace("-", "_")
    if status not in ALLOWED_STATUSES:
        lowered = raw_text.lower()
        if "manual_review" in lowered or "ручн" in lowered:
            status = "manual_review"
        elif "blocked" in lowered or "нельзя" in lowered or "автоотказ" in lowered:
            status = "blocked"
        elif "insufficient" in lowered or "недостаточно" in lowered or "неизвест" in lowered:
            status = "insufficient"
        else:
            status = "ok"

    answer = parsed.get("вывод", "").strip() or raw_text.strip()
    uncertainty = parsed.get("неопределенности", "").strip() or "нет"
    sources_raw = parsed.get("источники", "").strip()
    sources = [
        chunk_id.strip()
        for chunk_id in re.split(r"[,\s]+", sources_raw)
        if chunk_id.strip() in known_sources
    ]
    if not sources:
        sources = known_sources[:2]

    return {
        "status": status,
        "answer": answer,
        "uncertainty": uncertainty,
        "sources": ordered_unique(sources),
        "raw_text": raw_text,
    }


def answer_policy_check(
    *,
    case: dict[str, Any],
    check_id: str,
    subquestion: str,
    hits,
    model: str,
    ollama_base_url: str,
    ollama_api_key: str,
    logger: logging.Logger,
) -> dict[str, Any]:
    if check_id not in CHECK_CATALOG:
        raise KeyError(f"Неизвестный check_id: {check_id}")

    system_prompt = (
        "Ты узел policy-check в controlled-agent demo. "
        "Отвечай только по данным кейса и найденным policy-фрагментам. "
        "Не используй внешние знания. Верни ровно 4 строки и ничего больше:\n"
        "Статус: ok|blocked|manual_review|insufficient\n"
        "Вывод: ...\n"
        "Неопределенности: ...\n"
        "Источники: chunk-id-1, chunk-id-2"
    )
    user_prompt = (
        f"Проверка: {check_id} ({CHECK_CATALOG[check_id]['description']})\n\n"
        f"Факты кейса:\n{render_case_facts(case)}\n\n"
        f"Найденные policy-фрагменты:\n{build_context(hits)}\n\n"
        "Сделай краткий вывод именно по подзадаче. "
        "Если данных кейса или контекста не хватает, честно укажи это в строке Неопределенности. "
        "Не придумывай новые правила.\n\n"
        f"Подзадача: {subquestion}"
    )
    raw_text = llm_text_call(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model=model,
        ollama_base_url=ollama_base_url,
        ollama_api_key=ollama_api_key,
        logger=logger,
        step_name=f"check::{check_id}",
        max_tokens=320,
    )
    parsed = parse_check_answer(raw_text, [hit.chunk_id for hit in hits])
    parsed.update(
        {
            "check_id": check_id,
            "label": CHECK_CATALOG[check_id]["label"],
            "subquestion": subquestion,
            "hit_count": len(hits),
        }
    )
    logger.info(
        "CHECK RESULT %s\n%s",
        check_id,
        json.dumps(
            {
                "status": parsed["status"],
                "answer": parsed["answer"],
                "uncertainty": parsed["uncertainty"],
                "sources": parsed["sources"],
                "subquestion": subquestion,
            },
            ensure_ascii=False,
            indent=2,
        ),
    )
    return parsed


def is_no_uncertainty(value: str) -> bool:
    normalized = (value or "").strip().lower()
    return normalized in {"", "нет", "none", "n/a", "нет.", "-"}


def collect_uncertainties(records: list[dict[str, Any]]) -> list[str]:
    notes: list[str] = []
    for record in records:
        uncertainty = str(record.get("uncertainty") or "").strip()
        if is_no_uncertainty(uncertainty):
            continue
        notes.append(f"{record['label']}: {uncertainty}")
    return ordered_unique(notes)


def build_overall_summary(records: list[dict[str, Any]]) -> str:
    blocked = [record["answer"] for record in records if record["status"] == "blocked"]
    manual_review = [record["answer"] for record in records if record["status"] == "manual_review"]
    insufficient = [record["answer"] for record in records if record["status"] == "insufficient"]

    if blocked:
        return "Есть блокирующие условия: " + "; ".join(blocked[:2])
    if manual_review:
        return "Прямого блокера не видно, но заявку нужно отправить в ручную проверку: " + "; ".join(
            manual_review[:2]
        )
    if insufficient:
        return "Часть ответа требует дополнительных данных кейса: " + "; ".join(insufficient[:2])
    return "По доступным данным прямых блокеров не видно."


def build_draft_answer(
    *,
    case: dict[str, Any],
    question: str,
    plan: dict[str, Any],
    records: list[dict[str, Any]],
    extra_uncertainties: list[str] | None = None,
    review_notes: list[str] | None = None,
) -> str:
    records_by_check = {record["check_id"]: record for record in records}
    ordered_records = [records_by_check[check_id] for check_id in plan["required_checks"] if check_id in records_by_check]
    uncertainties = ordered_unique(collect_uncertainties(ordered_records) + (extra_uncertainties or []))
    all_sources = ordered_unique(
        [
            chunk_id
            for record in ordered_records
            for chunk_id in record.get("sources", [])
        ]
    )

    lines: list[str] = [
        f"Кейс {case['case_id']} — {case['title']}",
        f"Вопрос: {question}",
        "",
        "Итог:",
        f"- {build_overall_summary(ordered_records)}",
        "",
        "Проверки:",
    ]

    for index, record in enumerate(ordered_records, start=1):
        lines.append(f"{index}. {record['label']} [{record['status']}]")
        lines.append(f"   {record['answer']}")
        if not is_no_uncertainty(str(record.get("uncertainty") or "")):
            lines.append(f"   Неопределенности: {record['uncertainty']}")
        lines.append(f"   Источники: {', '.join(record.get('sources', [])) or 'нет'}")

    if uncertainties:
        lines.extend(["", "Неопределенности:"])
        for note in uncertainties:
            lines.append(f"- {note}")

    if review_notes:
        lines.extend(["", "Self-check:"])
        for note in review_notes:
            lines.append(f"- {note}")

    lines.extend(["", "Источники:"])
    for chunk_id in all_sources:
        lines.append(f"- {chunk_id}")

    return "\n".join(lines)


def validate_review(raw_review: Any) -> dict[str, Any]:
    if not isinstance(raw_review, dict):
        return {
            "needs_revision": False,
            "issues": [],
            "rerun_checks": [],
            "extra_uncertainties": [],
        }

    issues: list[str] = []
    for item in raw_review.get("issues") or []:
        if isinstance(item, dict):
            problem = str(item.get("problem") or "").strip()
            check_id = str(item.get("check_id") or "").strip()
            if problem:
                issues.append(f"{check_id or 'general'}: {problem}")
        else:
            problem = str(item).strip()
            if problem:
                issues.append(problem)

    rerun_checks: list[dict[str, str]] = []
    for item in raw_review.get("rerun_checks") or []:
        if not isinstance(item, dict):
            continue
        check_id = str(item.get("check_id") or "").strip()
        follow_up_question = str(item.get("follow_up_question") or "").strip()
        if check_id in CHECK_CATALOG and follow_up_question:
            rerun_checks.append(
                {
                    "check_id": check_id,
                    "follow_up_question": follow_up_question,
                }
            )

    extra_uncertainties = [
        str(item).strip()
        for item in (raw_review.get("extra_uncertainties") or [])
        if str(item).strip()
    ]

    needs_revision = bool(raw_review.get("needs_revision")) or bool(issues) or bool(rerun_checks)
    return {
        "needs_revision": needs_revision,
        "issues": ordered_unique(issues),
        "rerun_checks": rerun_checks[:MAX_RERUN_CHECKS],
        "extra_uncertainties": ordered_unique(extra_uncertainties),
    }


def llm_self_check(
    *,
    case: dict[str, Any],
    question: str,
    plan: dict[str, Any],
    records: list[dict[str, Any]],
    draft_answer: str,
    model: str,
    ollama_base_url: str,
    ollama_api_key: str,
    logger: logging.Logger,
) -> dict[str, Any]:
    system_prompt = (
        "Ты critic-узел controlled-agent demo. "
        "Проверь черновой ответ на unsupported claims, потерю части вопроса и игнорирование неизвестных полей кейса. "
        "Верни только JSON."
    )
    user_prompt = (
        "Верни JSON-объект вида:\n"
        "{\n"
        '  "needs_revision": true,\n'
        '  "issues": [{"check_id": "documents", "problem": "..." }],\n'
        '  "rerun_checks": [{"check_id": "documents", "follow_up_question": "..."}],\n'
        '  "extra_uncertainties": ["..."]\n'
        "}\n\n"
        "Правила:\n"
        "- issue добавляй только если проблема существенна;\n"
        "- rerun_checks заполняй только если нужен новый retrieval по конкретной подзадаче;\n"
        "- если достаточно просто подчеркнуть неопределенность, заполни extra_uncertainties без rerun;\n"
        "- используй только существующие check_id;\n"
        "- никаких пояснений вне JSON.\n\n"
        f"Вопрос пользователя:\n{question}\n\n"
        f"Факты кейса:\n{render_case_facts(case)}\n\n"
        f"План:\n{json.dumps(plan, ensure_ascii=False, indent=2)}\n\n"
        f"Результаты подзадач:\n{json.dumps(records, ensure_ascii=False, indent=2)}\n\n"
        f"Черновой ответ:\n{draft_answer}"
    )
    raw_review = llm_json_call(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model=model,
        ollama_base_url=ollama_base_url,
        ollama_api_key=ollama_api_key,
        logger=logger,
        step_name="critic",
        max_tokens=700,
    )
    return validate_review(raw_review)


def rule_based_self_check(plan: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    issues: list[str] = []
    extra_uncertainties: list[str] = []
    records_by_check = {record["check_id"]: record for record in records}

    for check_id in plan["required_checks"]:
        if check_id not in records_by_check:
            issues.append(f"{check_id}: отсутствует результат подзадачи.")
            continue
        if not records_by_check[check_id].get("sources"):
            issues.append(f"{check_id}: нет подтверждённых источников в результате подзадачи.")

    for record in records:
        uncertainty = str(record.get("uncertainty") or "").strip()
        if is_no_uncertainty(uncertainty):
            continue
        extra_uncertainties.append(f"{record['label']}: {uncertainty}")

    return {
        "needs_revision": bool(issues),
        "issues": ordered_unique(issues),
        "rerun_checks": [],
        "extra_uncertainties": ordered_unique(extra_uncertainties),
    }


def merge_reviews(*reviews: dict[str, Any]) -> dict[str, Any]:
    merged_issues: list[str] = []
    merged_reruns: list[dict[str, str]] = []
    merged_uncertainties: list[str] = []

    for review in reviews:
        merged_issues.extend(review.get("issues", []))
        merged_uncertainties.extend(review.get("extra_uncertainties", []))
        for rerun in review.get("rerun_checks", []):
            if rerun not in merged_reruns:
                merged_reruns.append(rerun)

    return {
        "needs_revision": bool(merged_issues or merged_reruns),
        "issues": ordered_unique(merged_issues),
        "rerun_checks": merged_reruns[:MAX_RERUN_CHECKS],
        "extra_uncertainties": ordered_unique(merged_uncertainties),
    }


def run_single_turn(
    *,
    case_id: str,
    question: str,
    cases: dict[str, dict[str, Any]],
    qdrant_host: str,
    qdrant_port: int,
    collection_name: str,
    ollama_base_url: str,
    ollama_api_key: str,
    embedding_model: str,
    chat_model: str,
    top_k: int,
    score_threshold: float | None,
    logger: logging.Logger,
) -> str:
    review_cycle = 1
    log_block(logger, "AGENT REQUEST", suffix=f"case_id={case_id}")
    logger.info("question: %s", question)

    log_block(logger, "CONTEXT LOAD", char="-")
    case = get_mock_application(case_id, cases=cases, logger=logger)

    log_block(logger, "PLAN BUILD", cycle=review_cycle)
    plan = plan_case(
        case=case,
        question=question,
        model=chat_model,
        ollama_base_url=ollama_base_url,
        ollama_api_key=ollama_api_key,
        logger=logger,
    )
    log_text_block(logger, "PLAN OUTLINE", render_plan_outline(plan), cycle=review_cycle, char="-")

    records_by_check: dict[str, dict[str, Any]] = {}
    total_subtasks = len(plan["subquestions"])
    log_block(
        logger,
        "PLAN EXECUTION",
        cycle=review_cycle,
        suffix=f"subtasks={total_subtasks}",
    )
    for index, item in enumerate(plan["subquestions"], start=1):
        check_id = item["check_id"]
        subquestion = item["question"]
        log_block(
            logger,
            "PLAN STEP",
            cycle=review_cycle,
            suffix=f"step={index}/{total_subtasks} | check_id={check_id}",
            char="-",
        )
        logger.info("subquestion: %s", subquestion)
        hits = search_chunks(
            question=subquestion,
            qdrant_host=qdrant_host,
            qdrant_port=qdrant_port,
            collection_name=collection_name,
            ollama_base_url=ollama_base_url,
            ollama_api_key=ollama_api_key,
            embedding_model=embedding_model,
            top_k=top_k,
            score_threshold=score_threshold,
            logger=logger,
        )
        records_by_check[check_id] = answer_policy_check(
            case=case,
            check_id=check_id,
            subquestion=subquestion,
            hits=hits,
            model=chat_model,
            ollama_base_url=ollama_base_url,
            ollama_api_key=ollama_api_key,
            logger=logger,
        )

    records = [records_by_check[check_id] for check_id in plan["required_checks"] if check_id in records_by_check]
    log_text_block(logger, "PLAN EXECUTION SUMMARY", render_records_outline(records), cycle=review_cycle, char="-")
    draft_answer = build_draft_answer(
        case=case,
        question=question,
        plan=plan,
        records=records,
    )
    log_text_block(logger, "DRAFT ANSWER", draft_answer, cycle=review_cycle)

    log_block(logger, "SELF-CHECK", cycle=review_cycle)
    llm_review = llm_self_check(
        case=case,
        question=question,
        plan=plan,
        records=records,
        draft_answer=draft_answer,
        model=chat_model,
        ollama_base_url=ollama_base_url,
        ollama_api_key=ollama_api_key,
        logger=logger,
    )
    rule_review = rule_based_self_check(plan, records)
    review = merge_reviews(llm_review, rule_review)
    log_json_block(logger, "SELF-CHECK REVIEW", review, cycle=review_cycle, char="-")
    log_text_block(
        logger,
        "SELF-CHECK ACTIONS",
        render_rerun_outline(review["rerun_checks"]),
        cycle=review_cycle,
        char="-",
    )

    if review["needs_revision"]:
        review_cycle += 1
        log_block(logger, "REVISION", cycle=review_cycle, suffix="targeted correction")
        if not review["rerun_checks"]:
            logger.info("Self-check нашёл замечания, но дополнительный retrieval не потребовался.")
        for index, rerun in enumerate(review["rerun_checks"], start=1):
            check_id = rerun["check_id"]
            follow_up_question = rerun["follow_up_question"]
            log_block(
                logger,
                "REVISION STEP",
                cycle=review_cycle,
                suffix=f"step={index}/{len(review['rerun_checks'])} | check_id={check_id}",
                char="-",
            )
            logger.info("follow_up_question: %s", follow_up_question)
            hits = search_chunks(
                question=follow_up_question,
                qdrant_host=qdrant_host,
                qdrant_port=qdrant_port,
                collection_name=collection_name,
                ollama_base_url=ollama_base_url,
                ollama_api_key=ollama_api_key,
                embedding_model=embedding_model,
                top_k=top_k,
                score_threshold=score_threshold,
                logger=logger,
            )
            records_by_check[check_id] = answer_policy_check(
                case=case,
                check_id=check_id,
                subquestion=follow_up_question,
                hits=hits,
                model=chat_model,
                ollama_base_url=ollama_base_url,
                ollama_api_key=ollama_api_key,
                logger=logger,
            )

    final_records = [records_by_check[check_id] for check_id in plan["required_checks"] if check_id in records_by_check]
    log_text_block(
        logger,
        "POST-REVISION SUMMARY",
        render_records_outline(final_records),
        cycle=review_cycle,
        char="-",
    )
    final_answer = build_draft_answer(
        case=case,
        question=question,
        plan=plan,
        records=final_records,
        extra_uncertainties=review["extra_uncertainties"],
        review_notes=review["issues"] if review["needs_revision"] else None,
    )
    result_evaluation = evaluate_result(final_records, review)
    log_json_block(logger, "RESULT EVALUATION", result_evaluation, cycle=review_cycle, char="-")
    log_text_block(logger, "FINAL ANSWER", final_answer, cycle=review_cycle)
    return final_answer


def interactive_loop(
    *,
    initial_case_id: str,
    cases: dict[str, dict[str, Any]],
    qdrant_host: str,
    qdrant_port: int,
    collection_name: str,
    ollama_base_url: str,
    ollama_api_key: str,
    embedding_model: str,
    chat_model: str,
    top_k: int,
    score_threshold: float | None,
    logger: logging.Logger,
) -> None:
    current_case_id = initial_case_id.strip().upper()
    if current_case_id not in cases:
        raise KeyError(f"Mock-кейс не найден: {current_case_id}")

    print("Интерактивный agent demo запущен.")
    print(INTERACTIVE_HELP)
    print(f"Текущий кейс: {render_case_summary(cases[current_case_id])}")

    while True:
        try:
            question = input(f"{current_case_id}> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход.")
            break

        if not question:
            continue

        lowered = question.lower()
        if lowered in {"exit", "quit", "q", "выход"}:
            print("Выход.")
            break
        if question == ":help":
            print(INTERACTIVE_HELP)
            continue
        if question == ":cases":
            for case_id in sorted(cases):
                print(render_case_summary(cases[case_id]))
            continue
        if question == ":case":
            print(render_case_facts(cases[current_case_id]))
            continue
        if question.startswith(":use "):
            candidate = question.split(" ", 1)[1].strip().upper()
            if candidate not in cases:
                print(f"Неизвестный кейс: {candidate}")
                continue
            current_case_id = candidate
            print(f"Текущий кейс: {render_case_summary(cases[current_case_id])}")
            continue

        answer = run_single_turn(
            case_id=current_case_id,
            question=question,
            cases=cases,
            qdrant_host=qdrant_host,
            qdrant_port=qdrant_port,
            collection_name=collection_name,
            ollama_base_url=ollama_base_url,
            ollama_api_key=ollama_api_key,
            embedding_model=embedding_model,
            chat_model=chat_model,
            top_k=top_k,
            score_threshold=score_threshold,
            logger=logger,
        )
        print("\nАгент>\n" + answer + "\n")


def main() -> None:
    args = build_parser().parse_args()
    logger = setup_logging()
    knowledge_path = Path(args.knowledge_file).expanduser().resolve()
    cases_path = Path(args.cases_file).expanduser().resolve()
    score_threshold = parse_optional_float(args.score_threshold)

    load_knowledge_chunks(knowledge_path)
    cases = load_mock_cases(cases_path)

    if args.list_cases:
        print_case_catalog(cases, logger)
        return

    if args.reindex:
        seed_collection(
            knowledge_path=knowledge_path,
            qdrant_host=args.qdrant_host,
            qdrant_port=args.qdrant_port,
            collection_name=args.collection,
            ollama_base_url=args.ollama_base_url,
            ollama_api_key=args.ollama_api_key,
            embedding_model=args.embedding_model,
            logger=logger,
            show_chunks=not args.hide_chunks,
        )

    logger.info(
        "Agent demo готов: collection=%s, qdrant=%s:%d, chat_model=%s, embedding_model=%s, default_case=%s",
        args.collection,
        args.qdrant_host,
        args.qdrant_port,
        args.chat_model,
        args.embedding_model,
        args.case_id,
    )

    if args.question.strip():
        answer = run_single_turn(
            case_id=args.case_id,
            question=args.question.strip(),
            cases=cases,
            qdrant_host=args.qdrant_host,
            qdrant_port=args.qdrant_port,
            collection_name=args.collection,
            ollama_base_url=args.ollama_base_url,
            ollama_api_key=args.ollama_api_key,
            embedding_model=args.embedding_model,
            chat_model=args.chat_model,
            top_k=args.top_k,
            score_threshold=score_threshold,
            logger=logger,
        )
        print("\nАгент>\n" + answer)
        return

    interactive_loop(
        initial_case_id=args.case_id,
        cases=cases,
        qdrant_host=args.qdrant_host,
        qdrant_port=args.qdrant_port,
        collection_name=args.collection,
        ollama_base_url=args.ollama_base_url,
        ollama_api_key=args.ollama_api_key,
        embedding_model=args.embedding_model,
        chat_model=args.chat_model,
        top_k=args.top_k,
        score_threshold=score_threshold,
        logger=logger,
    )


if __name__ == "__main__":
    main()

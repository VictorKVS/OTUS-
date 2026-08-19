from __future__ import annotations

import json
import logging
import os
import re
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models


PACKAGE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_ROOT.parent
load_dotenv(REPO_ROOT / ".env")

DEFAULT_KNOWLEDGE_PATH = PACKAGE_ROOT / "data" / "credit_policy_chunks.json"

DEFAULT_OLLAMA_API_KEY = (os.getenv("OLLAMA_API_KEY") or "ollama").strip()
DEFAULT_OLLAMA_BASE_URL = (os.getenv("OLLAMA_BASE_URL") or "http://localhost:11434/v1").strip()
DEFAULT_CHAT_MODEL = (os.getenv("RAG_CHAT_MODEL") or "hf.co/Qwen/Qwen3-4B-GGUF:Q4_K_M").strip()
DEFAULT_EMBEDDING_MODEL = (os.getenv("RAG_EMBEDDING_MODEL") or "nomic-embed-text").strip()

DEFAULT_QDRANT_HOST = (os.getenv("RAG_QDRANT_HOST") or "localhost").strip()
DEFAULT_QDRANT_PORT = int((os.getenv("RAG_QDRANT_PORT") or "6333").strip())
DEFAULT_QDRANT_COLLECTION = (os.getenv("RAG_QDRANT_COLLECTION") or "credit_policy_demo").strip()
DEFAULT_TOP_K = int((os.getenv("RAG_TOP_K") or "4").strip())
DEFAULT_VECTOR_CANDIDATES = int((os.getenv("RAG_VECTOR_CANDIDATES") or "50").strip())
DEFAULT_VECTOR_WEIGHT = float((os.getenv("RAG_VECTOR_WEIGHT") or "0.35").strip())
DEFAULT_LEXICAL_WEIGHT = float((os.getenv("RAG_LEXICAL_WEIGHT") or "0.65").strip())


RU_STOPWORDS = {
    "а",
    "без",
    "бы",
    "в",
    "во",
    "все",
    "для",
    "до",
    "если",
    "есть",
    "же",
    "за",
    "и",
    "из",
    "или",
    "как",
    "какая",
    "какие",
    "какой",
    "когда",
    "ли",
    "мне",
    "на",
    "не",
    "нет",
    "но",
    "нужен",
    "нужна",
    "нужны",
    "о",
    "об",
    "от",
    "по",
    "под",
    "после",
    "при",
    "про",
    "с",
    "со",
    "сколько",
    "такой",
    "то",
    "у",
    "что",
    "это",
}


TOKEN_SUFFIXES = (
    "иями",
    "ями",
    "ами",
    "ией",
    "ией",
    "ого",
    "ему",
    "ому",
    "ыми",
    "ими",
    "иях",
    "иях",
    "иях",
    "иям",
    "ием",
    "иях",
    "ий",
    "ый",
    "ой",
    "ая",
    "яя",
    "ое",
    "ее",
    "ые",
    "ие",
    "ам",
    "ям",
    "ах",
    "ях",
    "ов",
    "ев",
    "ей",
    "ом",
    "ем",
    "им",
    "ым",
    "ую",
    "юю",
    "ия",
    "ья",
    "ию",
    "ью",
    "ия",
    "а",
    "я",
    "ы",
    "и",
    "е",
    "о",
    "у",
    "ю",
)


SYSTEM_PROMPT = (
    "Ты демонстрационный RAG-ассистент по внутренним кредитным политикам вымышленной компании. "
    "Отвечай только по найденным фрагментам базы знаний. "
    "Если в найденных фрагментах нет ответа, так и скажи: "
    "«В базе знаний не нашёл ответа». "
    "Не придумывай новые правила, сроки, ставки или исключения. "
    "В конце ответа обязательно добавь строку вида "
    "«Источники: chunk-id-1, chunk-id-2»."
)


@dataclass(frozen=True)
class KnowledgeChunk:
    point_id: int
    chunk_id: str
    section: str
    title: str
    text: str
    keywords: tuple[str, ...]

    @classmethod
    def from_raw(cls, raw: dict[str, object], point_id: int) -> "KnowledgeChunk":
        chunk_id = str(raw.get("chunk_id") or "").strip()
        section = str(raw.get("section") or "").strip()
        title = str(raw.get("title") or "").strip()
        text = str(raw.get("text") or "").strip()
        keywords_raw = raw.get("keywords") or []

        if not chunk_id:
            raise ValueError(f"У чанка #{point_id} пустой chunk_id.")
        if not section:
            raise ValueError(f"У чанка {chunk_id} пустой section.")
        if not title:
            raise ValueError(f"У чанка {chunk_id} пустой title.")
        if not text:
            raise ValueError(f"У чанка {chunk_id} пустой text.")
        if not isinstance(keywords_raw, list):
            raise ValueError(f"У чанка {chunk_id} поле keywords должно быть списком.")

        keywords = tuple(str(item).strip() for item in keywords_raw if str(item).strip())
        return cls(
            point_id=point_id,
            chunk_id=chunk_id,
            section=section,
            title=title,
            text=text,
            keywords=keywords,
        )

    def payload(self) -> dict[str, object]:
        return {
            "chunk_id": self.chunk_id,
            "section": self.section,
            "title": self.title,
            "text": self.text,
            "keywords": list(self.keywords),
            "searchable_text": self.searchable_text(),
        }

    def searchable_text(self) -> str:
        keywords_text = ", ".join(self.keywords)
        return (
            f"Раздел: {self.section}\n"
            f"Заголовок: {self.title}\n"
            f"Ключевые слова: {keywords_text}\n"
            f"Содержимое: {self.text}"
        )


@dataclass(frozen=True)
class RetrievedChunk:
    point_id: int | str
    chunk_id: str
    section: str
    title: str
    text: str
    keywords: tuple[str, ...]
    score: float
    vector_score: float
    lexical_score: float
    matched_terms: tuple[str, ...]


def normalize_text(text: str) -> str:
    return text.lower().replace("ё", "е")


def tokenize(text: str) -> list[str]:
    return re.findall(r"[0-9a-zа-я]+", normalize_text(text))


def stem_token(token: str) -> str:
    normalized = normalize_text(token)
    for suffix in TOKEN_SUFFIXES:
        if normalized.endswith(suffix) and len(normalized) - len(suffix) >= 4:
            return normalized[: -len(suffix)]
    return normalized


def extract_terms(text: str) -> tuple[str, ...]:
    seen: set[str] = set()
    terms: list[str] = []

    for token in tokenize(text):
        if token in RU_STOPWORDS:
            continue
        stemmed = stem_token(token)
        if len(stemmed) < 3 or stemmed in RU_STOPWORDS or stemmed in seen:
            continue
        seen.add(stemmed)
        terms.append(stemmed)

    return tuple(terms)


def lexical_match_score(
    *,
    question_terms: tuple[str, ...],
    section: str,
    title: str,
    text: str,
    keywords: tuple[str, ...],
) -> tuple[float, tuple[str, ...]]:
    if not question_terms:
        return 0.0, ()

    fields = {
        "keywords": set(extract_terms(" ".join(keywords))),
        "title": set(extract_terms(title)),
        "section": set(extract_terms(section)),
        "text": set(extract_terms(text)),
    }
    field_weights = {
        "keywords": 4.0,
        "title": 3.0,
        "section": 2.0,
        "text": 1.0,
    }

    matched_terms: list[str] = []
    weighted_hits = 0.0
    max_weight = max(field_weights.values())

    for term in question_terms:
        best_weight = 0.0
        for field_name, field_terms in fields.items():
            if term in field_terms:
                best_weight = max(best_weight, field_weights[field_name])
        if best_weight > 0.0:
            matched_terms.append(term)
            weighted_hits += best_weight

    score = weighted_hits / (len(question_terms) * max_weight)
    return min(1.0, score), tuple(matched_terms)


def setup_logging(*, verbose: bool = True) -> logging.Logger:
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        force=True,
    )
    return logging.getLogger("rag_demo")


def normalize_ollama_base_url(base_url: str) -> str:
    value = base_url.strip().rstrip("/")
    if value.endswith("/v1"):
        return value
    return f"{value}/v1"


def parse_optional_float(value: str | None) -> float | None:
    raw = (value or "").strip()
    if not raw:
        return None
    return float(raw)


def load_knowledge_chunks(knowledge_path: Path = DEFAULT_KNOWLEDGE_PATH) -> list[KnowledgeChunk]:
    if not knowledge_path.exists():
        raise FileNotFoundError(f"Файл знаний не найден: {knowledge_path}")

    raw_items = json.loads(knowledge_path.read_text(encoding="utf-8"))
    if not isinstance(raw_items, list) or not raw_items:
        raise ValueError(f"Ожидался непустой JSON-список в {knowledge_path}")

    chunks: list[KnowledgeChunk] = []
    seen_chunk_ids: set[str] = set()

    for index, raw_item in enumerate(raw_items, start=1):
        if not isinstance(raw_item, dict):
            raise ValueError(f"Элемент #{index} в {knowledge_path} должен быть объектом.")
        chunk = KnowledgeChunk.from_raw(raw_item, point_id=index)
        if chunk.chunk_id in seen_chunk_ids:
            raise ValueError(f"Дублируется chunk_id: {chunk.chunk_id}")
        seen_chunk_ids.add(chunk.chunk_id)
        chunks.append(chunk)

    return chunks


def print_chunk_catalog(chunks: Iterable[KnowledgeChunk], logger: logging.Logger) -> None:
    logger.info("Каталог чанков, который будет отправлен в Qdrant:")
    for chunk in chunks:
        logger.info(
            "chunk=%s | section=%s | title=%s | keywords=%s",
            chunk.chunk_id,
            chunk.section,
            chunk.title,
            ", ".join(chunk.keywords) if chunk.keywords else "-",
        )
        logger.info("text=%s", chunk.text)


def make_ollama_client(
    *,
    base_url: str = DEFAULT_OLLAMA_BASE_URL,
    api_key: str = DEFAULT_OLLAMA_API_KEY,
) -> OpenAI:
    return OpenAI(
        api_key=api_key,
        base_url=normalize_ollama_base_url(base_url),
    )


def make_qdrant_client(
    *,
    host: str = DEFAULT_QDRANT_HOST,
    port: int = DEFAULT_QDRANT_PORT,
) -> QdrantClient:
    return QdrantClient(host=host, port=port, timeout=30)


def embed_text(*, client: OpenAI, model: str, text: str) -> list[float]:
    response = client.embeddings.create(
        model=model,
        input=text,
        encoding_format="float",
    )
    return list(response.data[0].embedding)


def recreate_collection(
    *,
    client: QdrantClient,
    collection_name: str,
    vector_size: int,
    logger: logging.Logger,
) -> None:
    if client.collection_exists(collection_name):
        logger.info("Удаляю существующую коллекцию Qdrant: %s", collection_name)
        client.delete_collection(collection_name=collection_name)

    logger.info(
        "Создаю коллекцию Qdrant: name=%s, vector_size=%d, distance=cosine",
        collection_name,
        vector_size,
    )
    client.create_collection(
        collection_name=collection_name,
        vectors_config=qdrant_models.VectorParams(
            size=vector_size,
            distance=qdrant_models.Distance.COSINE,
        ),
    )


def seed_collection(
    *,
    knowledge_path: Path = DEFAULT_KNOWLEDGE_PATH,
    qdrant_host: str = DEFAULT_QDRANT_HOST,
    qdrant_port: int = DEFAULT_QDRANT_PORT,
    collection_name: str = DEFAULT_QDRANT_COLLECTION,
    ollama_base_url: str = DEFAULT_OLLAMA_BASE_URL,
    ollama_api_key: str = DEFAULT_OLLAMA_API_KEY,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    logger: logging.Logger,
    show_chunks: bool = True,
) -> list[KnowledgeChunk]:
    chunks = load_knowledge_chunks(knowledge_path)
    if show_chunks:
        print_chunk_catalog(chunks, logger)

    openai_client = make_ollama_client(base_url=ollama_base_url, api_key=ollama_api_key)
    qdrant_client = make_qdrant_client(host=qdrant_host, port=qdrant_port)

    points: list[qdrant_models.PointStruct] = []
    vector_size: int | None = None

    for chunk in chunks:
        searchable_text = chunk.searchable_text()
        vector = embed_text(client=openai_client, model=embedding_model, text=searchable_text)
        if vector_size is None:
            vector_size = len(vector)
            logger.info("Первая размерность embedding-вектора: %d", vector_size)

        logger.info(
            "Подготовлен чанк для индексации: point_id=%d, chunk=%s, chars=%d",
            chunk.point_id,
            chunk.chunk_id,
            len(searchable_text),
        )
        points.append(
            qdrant_models.PointStruct(
                id=chunk.point_id,
                vector=vector,
                payload=chunk.payload(),
            )
        )

    if vector_size is None:
        raise RuntimeError("Не удалось определить размерность embedding-вектора.")

    recreate_collection(
        client=qdrant_client,
        collection_name=collection_name,
        vector_size=vector_size,
        logger=logger,
    )
    qdrant_client.upsert(collection_name=collection_name, points=points, wait=True)
    logger.info(
        "Коллекция заполнена: collection=%s, points=%d, embedding_model=%s",
        collection_name,
        len(points),
        embedding_model,
    )
    return chunks


def search_chunks(
    *,
    question: str,
    qdrant_host: str,
    qdrant_port: int,
    collection_name: str,
    ollama_base_url: str,
    ollama_api_key: str,
    embedding_model: str,
    top_k: int,
    score_threshold: float | None,
    logger: logging.Logger,
) -> list[RetrievedChunk]:
    openai_client = make_ollama_client(base_url=ollama_base_url, api_key=ollama_api_key)
    qdrant_client = make_qdrant_client(host=qdrant_host, port=qdrant_port)

    question_terms = extract_terms(question)
    candidate_limit = max(top_k, DEFAULT_VECTOR_CANDIDATES)
    query_vector = embed_text(client=openai_client, model=embedding_model, text=question)
    logger.info(
        "Поиск в Qdrant: host=%s, port=%d, collection=%s, top_k=%d, vector_candidates=%d, score_threshold=%s",
        qdrant_host,
        qdrant_port,
        collection_name,
        top_k,
        candidate_limit,
        "disabled" if score_threshold is None else f"{score_threshold:.4f}",
    )
    logger.info("Вопрос пользователя: %s", question)
    logger.info(
        "Термы вопроса для lexical rerank: %s",
        ", ".join(question_terms) if question_terms else "-",
    )
    logger.info("Размерность вектора вопроса: %d", len(query_vector))

    response = qdrant_client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=candidate_limit,
        with_payload=True,
        score_threshold=score_threshold,
    )

    hits: list[RetrievedChunk] = []
    for point in response.points:
        payload = point.payload or {}
        keywords_raw = payload.get("keywords") or []
        keywords = tuple(str(item).strip() for item in keywords_raw if str(item).strip())
        lexical_score, matched_terms = lexical_match_score(
            question_terms=question_terms,
            section=str(payload.get("section") or ""),
            title=str(payload.get("title") or ""),
            text=str(payload.get("text") or ""),
            keywords=keywords,
        )
        vector_score = float(point.score)
        final_score = vector_score * DEFAULT_VECTOR_WEIGHT + lexical_score * DEFAULT_LEXICAL_WEIGHT
        hits.append(
            RetrievedChunk(
                point_id=point.id,
                chunk_id=str(payload.get("chunk_id") or point.id),
                section=str(payload.get("section") or ""),
                title=str(payload.get("title") or ""),
                text=str(payload.get("text") or ""),
                keywords=keywords,
                score=final_score,
                vector_score=vector_score,
                lexical_score=lexical_score,
                matched_terms=matched_terms,
            )
        )

    if not hits:
        logger.warning("Qdrant не вернул ни одного релевантного чанка.")
        return hits

    hits.sort(
        key=lambda item: (
            item.score,
            item.lexical_score,
            item.vector_score,
        ),
        reverse=True,
    )
    hits = hits[:top_k]
    logger.info(
        "После гибридного rerank: vector_weight=%.2f, lexical_weight=%.2f, final_top_k=%d",
        DEFAULT_VECTOR_WEIGHT,
        DEFAULT_LEXICAL_WEIGHT,
        len(hits),
    )
    for index, hit in enumerate(hits, start=1):
        logger.info(
            "hit #%d | final_score=%.4f | vector_score=%.4f | lexical_score=%.4f | chunk=%s | section=%s | title=%s | keywords=%s | matched_terms=%s",
            index,
            hit.score,
            hit.vector_score,
            hit.lexical_score,
            hit.chunk_id,
            hit.section,
            hit.title,
            ", ".join(hit.keywords) if hit.keywords else "-",
            ", ".join(hit.matched_terms) if hit.matched_terms else "-",
        )
        logger.info(
            "hit #%d text=%s",
            index,
            textwrap.shorten(hit.text.replace("\n", " "), width=220, placeholder="..."),
        )

    return hits


def build_context(hits: Iterable[RetrievedChunk]) -> str:
    blocks: list[str] = []
    for index, hit in enumerate(hits, start=1):
        blocks.append(
            f"[{index}] chunk_id={hit.chunk_id}; section={hit.section}; title={hit.title}\n{hit.text}"
        )

    if not blocks:
        return "Найденные фрагменты отсутствуют."
    return "\n\n---\n\n".join(blocks)


def build_history_text(history: list[dict[str, str]]) -> str:
    if not history:
        return "История пока пуста."

    role_names = {
        "user": "Пользователь",
        "assistant": "Ассистент",
    }
    rendered: list[str] = []
    for item in history[-6:]:
        role = role_names.get(item.get("role", ""), item.get("role", "unknown"))
        content = (item.get("content") or "").strip()
        if not content:
            continue
        rendered.append(f"{role}: {content}")

    return "\n".join(rendered) if rendered else "История пока пуста."


def answer_with_rag(
    *,
    question: str,
    history: list[dict[str, str]],
    hits: list[RetrievedChunk],
    ollama_base_url: str,
    ollama_api_key: str,
    chat_model: str,
    logger: logging.Logger,
) -> str:
    context = build_context(hits)
    logger.info(
        "Передаю в LLM %d чанков, model=%s, context_chars=%d",
        len(hits),
        chat_model,
        len(context),
    )

    prompt = (
        "История диалога:\n"
        f"{build_history_text(history)}\n\n"
        "Найденные фрагменты:\n"
        f"{context}\n\n"
        "Задача:\n"
        "1. Ответь на текущий вопрос пользователя только по найденным фрагментам.\n"
        "2. Если данных недостаточно, честно скажи, что ответа нет в базе знаний.\n"
        "3. В конце приведи строку с chunk_id источников.\n\n"
        f"Текущий вопрос пользователя: {question}"
    )

    client = make_ollama_client(base_url=ollama_base_url, api_key=ollama_api_key)
    response = client.chat.completions.create(
        model=chat_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        max_tokens=450,
    )

    answer = (response.choices[0].message.content or "").strip()
    logger.info("Ответ модели готов: chars=%d", len(answer))
    logger.info("Ответ RAG:\n%s", answer)
    return answer

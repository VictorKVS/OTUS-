from __future__ import annotations

import hashlib
import os
from pathlib import Path

import qrcode
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing, Line, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from svglib.svglib import svg2rlg


ROOT = Path(__file__).resolve().parents[1]
HW = ROOT / "5. Низкоуровневое проектирование (LLD) компоненты и взаимодействия  ДЗ" / "ДЗ_05_OSINT_KB_Agent_LLD"
OUT = HW / "DZ05_LLD_OSINT_KB_AGENT_SUBMISSION.pdf"
SHA = HW / "SHA256SUMS.txt"
TMP = HW / ".pdf-build"
TMP.mkdir(exist_ok=True)

REPO_URL = "https://github.com/VictorKVS/OTUS-"
FOLDER_URL = "https://github.com/VictorKVS/OTUS-/tree/main/5.%20%D0%9D%D0%B8%D0%B7%D0%BA%D0%BE%D1%83%D1%80%D0%BE%D0%B2%D0%BD%D0%B5%D0%B2%D0%BE%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20(LLD)%20%D0%BA%D0%BE%D0%BC%D0%BF%D0%BE%D0%BD%D0%B5%D0%BD%D1%82%D1%8B%20%D0%B8%20%D0%B2%D0%B7%D0%B0%D0%B8%D0%BC%D0%BE%D0%B4%D0%B5%D0%B9%D1%81%D1%82%D0%B2%D0%B8%D1%8F%20%20%D0%94%D0%97/%D0%94%D0%97_05_OSINT_KB_Agent_LLD"
README_URL = FOLDER_URL + "/README.md"
PDF_URL = FOLDER_URL + "/DZ05_LLD_OSINT_KB_AGENT_SUBMISSION.pdf"
PR_URL = "https://github.com/VictorKVS/OTUS-/pull/12"
MERGE_COMMIT = "d39000c866c9b51b19801f30a95a5ea16d37605c"

NAVY = colors.HexColor("#17365D")
BLUE = colors.HexColor("#2F6FED")
LIGHT_BLUE = colors.HexColor("#EAF2FF")
PALE = colors.HexColor("#F6F8FB")
GREEN = colors.HexColor("#198754")
ORANGE = colors.HexColor("#D97706")
RED = colors.HexColor("#B42318")
GRAY = colors.HexColor("#5F6B7A")
DARK = colors.HexColor("#172033")
BORDER = colors.HexColor("#CBD5E1")


def register_fonts() -> None:
    choices = [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ("/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf", "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"),
    ]
    for regular, bold in choices:
        if Path(regular).exists() and Path(bold).exists():
            pdfmetrics.registerFont(TTFont("Body", regular))
            pdfmetrics.registerFont(TTFont("BodyBold", bold))
            return
    raise RuntimeError("Cyrillic-capable font not found")


register_fonts()

styles = getSampleStyleSheet()
BODY = ParagraphStyle("body", parent=styles["BodyText"], fontName="Body", fontSize=9.6, leading=14, textColor=DARK, spaceAfter=6)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=8.2, leading=11.2, textColor=GRAY)
H1 = ParagraphStyle("h1", parent=styles["Heading1"], fontName="BodyBold", fontSize=23, leading=28, textColor=NAVY, spaceAfter=10)
H2 = ParagraphStyle("h2", parent=styles["Heading2"], fontName="BodyBold", fontSize=15, leading=19, textColor=NAVY, spaceBefore=4, spaceAfter=8)
H3 = ParagraphStyle("h3", parent=styles["Heading3"], fontName="BodyBold", fontSize=11.2, leading=14, textColor=BLUE, spaceBefore=4, spaceAfter=5)
CENTER = ParagraphStyle("center", parent=BODY, alignment=TA_CENTER)
TITLE = ParagraphStyle("title", parent=styles["Title"], fontName="BodyBold", fontSize=28, leading=34, alignment=TA_CENTER, textColor=NAVY, spaceAfter=8)
SUBTITLE = ParagraphStyle("subtitle", parent=BODY, fontName="Body", fontSize=14, leading=18, alignment=TA_CENTER, textColor=GRAY)
CODE = ParagraphStyle("code", parent=BODY, fontName="Courier", fontSize=7.6, leading=10, backColor=PALE, borderColor=BORDER, borderWidth=0.5, borderPadding=6)
CALLOUT = ParagraphStyle("callout", parent=BODY, fontName="BodyBold", fontSize=10.2, leading=15, backColor=LIGHT_BLUE, borderColor=BLUE, borderWidth=0.7, borderPadding=8, textColor=NAVY)


def p(text: str, style=BODY):
    return Paragraph(text, style)


def link(label: str, url: str) -> Paragraph:
    return p(f'<link href="{url}" color="#2F6FED"><u>{label}</u></link>')


def qr(url: str, name: str) -> Path:
    path = TMP / name
    img = qrcode.make(url)
    img.save(path)
    return path


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.35)
    canvas.line(18 * mm, h - 15 * mm, w - 18 * mm, h - 15 * mm)
    canvas.setFont("Body", 7.5)
    canvas.setFillColor(GRAY)
    canvas.drawString(18 * mm, h - 11.5 * mm, "OTUS · ДЗ 05 · LLD · Knowledge Base Filling Agent")
    canvas.drawRightString(w - 18 * mm, 10 * mm, f"VictorKVS / OTUS- · стр. {doc.page}")
    canvas.line(18 * mm, 14 * mm, w - 18 * mm, 14 * mm)
    canvas.restoreState()


class Doc(BaseDocTemplate):
    def __init__(self, filename: str):
        super().__init__(filename, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=22 * mm, bottomMargin=20 * mm, title="ДЗ 05 — LLD: OSINT Knowledge Base Filling Agent", author="VictorKVS")
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")
        self.addPageTemplates(PageTemplate(id="main", frames=frame, onPage=header_footer))


def scaled_svg(path: Path, max_w: float, max_h: float):
    drawing = svg2rlg(str(path))
    if drawing is None:
        raise RuntimeError(f"Cannot read SVG: {path}")
    sx = max_w / drawing.width
    sy = max_h / drawing.height
    scale = min(sx, sy, 1.0)
    drawing.width *= scale
    drawing.height *= scale
    drawing.scale(scale, scale)
    return drawing


def section_title(number: str, title: str):
    return [p(f"{number}. {title}", H1), Spacer(1, 2 * mm)]


def overview_drawing() -> Drawing:
    d = Drawing(500, 112)
    labels = [
        ("SOURCE", "публичный / официальный"),
        ("CAPTURE", "URL · UTC · SHA-256"),
        ("CHUNK", "stable locator"),
        ("CANDIDATE", "ENTITY · CLAIM · RELATION"),
        ("REVIEW", "APPROVE / REWORK / REJECT"),
        ("KNOWLEDGE", "KB · Graph · Audit"),
    ]
    x = 3
    widths = [68, 72, 63, 90, 82, 82]
    colors_fill = [colors.HexColor("#F8FAFC"), LIGHT_BLUE, colors.HexColor("#F8FAFC"), colors.HexColor("#FFF7ED"), colors.HexColor("#FFF7ED"), colors.HexColor("#ECFDF5")]
    for i, ((a, b), ww, fill) in enumerate(zip(labels, widths, colors_fill)):
        d.add(Rect(x, 34, ww, 48, rx=7, ry=7, fillColor=fill, strokeColor=BORDER, strokeWidth=0.8))
        d.add(String(x + ww / 2, 62, a, fontName="BodyBold", fontSize=7.6, fillColor=NAVY, textAnchor="middle"))
        d.add(String(x + ww / 2, 47, b, fontName="Body", fontSize=5.5, fillColor=GRAY, textAnchor="middle"))
        if i < len(labels) - 1:
            d.add(Line(x + ww, 58, x + ww + 10, 58, strokeColor=BLUE, strokeWidth=1.1))
            d.add(Line(x + ww + 6, 55, x + ww + 10, 58, strokeColor=BLUE, strokeWidth=1.1))
            d.add(Line(x + ww + 6, 61, x + ww + 10, 58, strokeColor=BLUE, strokeWidth=1.1))
        x += ww + 10
    d.add(String(250, 97, "Доказательный конвейер Knowledge Base Filling Agent", fontName="BodyBold", fontSize=11, fillColor=NAVY, textAnchor="middle"))
    d.add(String(250, 14, "Автоматический компонент не имеет права выполнять переход CLAIM → FACT", fontName="BodyBold", fontSize=8, fillColor=RED, textAnchor="middle"))
    return d


def sequence_drawing() -> Drawing:
    d = Drawing(500, 285)
    participants = ["Collector", "Ingest API", "Policy", "Validator", "Extractor", "Review", "Publisher"]
    xs = [35, 105, 175, 245, 315, 385, 455]
    for x, name in zip(xs, participants):
        d.add(Rect(x - 29, 245, 58, 24, rx=4, ry=4, fillColor=LIGHT_BLUE if name != "Review" else colors.HexColor("#FFF7ED"), strokeColor=BORDER, strokeWidth=0.7))
        d.add(String(x, 253, name, fontName="BodyBold", fontSize=6.3, fillColor=NAVY, textAnchor="middle"))
        d.add(Line(x, 242, x, 20, strokeColor=colors.HexColor("#AAB4C3"), strokeWidth=0.55))
    events = [
        (0, 1, 222, "POST EvidencePackage"),
        (1, 2, 190, "purpose + access + legal basis"),
        (2, 3, 158, "ADMITTED"),
        (3, 4, 126, "capture + chunks + candidates"),
        (4, 5, 94, "review item + provenance"),
        (5, 6, 62, "APPROVE"),
    ]
    for a, b, y, label in events:
        x1, x2 = xs[a], xs[b]
        d.add(Line(x1, y, x2 - 5, y, strokeColor=BLUE, strokeWidth=1.1))
        d.add(Line(x2 - 9, y - 3, x2 - 5, y, strokeColor=BLUE, strokeWidth=1.1))
        d.add(Line(x2 - 9, y + 3, x2 - 5, y, strokeColor=BLUE, strokeWidth=1.1))
        d.add(String((x1 + x2) / 2, y + 5, label, fontName="Body", fontSize=5.8, fillColor=DARK, textAnchor="middle"))
    d.add(String(250, 277, "Ключевой сценарий: Evidence Package → Human Review → Knowledge Base", fontName="BodyBold", fontSize=10, fillColor=NAVY, textAnchor="middle"))
    d.add(String(250, 5, "REWORK и REJECT фиксируются в Audit Journal и не публикуются как FACT", fontName="BodyBold", fontSize=7.4, fillColor=RED, textAnchor="middle"))
    return d


def endpoint_table():
    data = [
        [p("Метод", H3), p("Endpoint", H3), p("Назначение", H3)],
        ["POST", "/evidence-packages", "Регистрация evidence package"],
        ["GET", "/evidence-packages/{packageId}", "Статус обработки"],
        ["POST", "/evidence-packages/{packageId}/process", "Запуск deterministic pipeline"],
        ["GET", "/review-items", "Очередь human review"],
        ["POST", "/review-items/{id}/decision", "Решение APPROVE / REWORK / REJECT"],
        ["GET", "/cases/{caseId}/coverage", "Coverage и research gaps"],
        ["GET", "/cases/{caseId}/lineage/{objectId}", "Трассировка до capture/chunk"],
    ]
    t = Table(data, colWidths=[20 * mm, 72 * mm, 78 * mm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), LIGHT_BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), NAVY),
        ("FONTNAME", (0, 0), (-1, 0), "BodyBold"),
        ("FONTNAME", (0, 1), (-1, -1), "Body"),
        ("FONTSIZE", (0, 1), (-1, -1), 7.8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def component_table():
    rows = [
        ("Ingest API", "Принимает EvidencePackage и обеспечивает idempotency"),
        ("Policy & Admission Gate", "Проверяет purpose, legal basis и access class"),
        ("Evidence Validator", "Проверяет manifest, lineage, hash и сохраняет оригинал"),
        ("Stable Chunk Builder", "Создаёт воспроизводимые chunks с локаторами"),
        ("Candidate Extractor", "ENTITY / EVENT / CLAIM / DEFINITION / RELATION"),
        ("Provenance Binder", "Связывает candidate с source/capture/chunk/tool version"),
        ("Entity Resolution", "Exact merge; fuzzy merge требует review"),
        ("Contradiction Engine", "Конфликты, supersession, stale и research gaps"),
        ("Review Queue", "Human gate: APPROVE / REWORK / REJECT"),
        ("Knowledge Publisher", "Versioned write в KB и проекция в graph"),
        ("Audit Writer", "Append-only audit trail"),
    ]
    data = [[p("Компонент", H3), p("Ответственность", H3)]] + [[p(a, BODY), p(b, BODY)] for a, b in rows]
    t = Table(data, colWidths=[54 * mm, 116 * mm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), LIGHT_BLUE),
        ("GRID", (0, 0), (-1, -1), 0.35, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def build() -> None:
    doc = Doc(str(OUT))
    story = []

    # 1. Title
    story += [Spacer(1, 24 * mm), p("OTUS · ИИ-архитектор", ParagraphStyle("top", parent=H2, alignment=TA_CENTER, textColor=BLUE)), p("Домашнее задание №5", TITLE), p("Низкоуровневое проектирование (LLD)", TITLE), Spacer(1, 4 * mm), p("Knowledge Base Filling Agent", ParagraphStyle("sub", parent=H1, alignment=TA_CENTER, fontSize=21)), p("C3 · OpenAPI 3.1 · Sequence · BPMN · DFD", SUBTITLE), Spacer(1, 10 * mm), overview_drawing(), Spacer(1, 9 * mm), p("Архитектурный принцип", H2), p("SOURCE → CAPTURE → CHUNK → CLAIM / CANDIDATE → HUMAN REVIEW → VERIFIED KNOWLEDGE", CALLOUT), Spacer(1, 8 * mm), link("Репозиторий: github.com/VictorKVS/OTUS-", REPO_URL), link("Папка сдачи: ДЗ_05_OSINT_KB_Agent_LLD", FOLDER_URL), p(f"PR #12 · merge commit {MERGE_COMMIT[:10]}…", SMALL), PageBreak()]

    # 2. Task
    story += section_title("1", "Условие и результат")
    story += [p("Цель занятия: детализировать высокоуровневый контейнер до компонентов, спроектировать API и показать последовательность взаимодействий. Для практической части выбран контейнер <b>Knowledge Base Filling Agent</b>."), Spacer(1, 2 * mm)]
    req = [
        [p("Требование", H3), p("Артефакт", H3)],
        [p("LLD одного контейнера"), p("Knowledge Base Filling Agent")],
        [p("C3 Component Diagram"), p("architecture/C3_KB_AGENT_COMPONENTS.svg")],
        [p("OpenAPI"), p("api/openapi.yaml · OpenAPI 3.1")],
        [p("Sequence Diagram"), p("architecture/SEQUENCE_EVIDENCE_TO_KB.md")],
        [p("Дополнительные потоки"), p("BPMN + DFD")],
    ]
    t = Table(req, colWidths=[72 * mm, 98 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), LIGHT_BLUE), ("GRID", (0, 0), (-1, -1), 0.4, BORDER), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]), ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    story += [t, Spacer(1, 7 * mm), p("Что делает агент", H2), p("Агент принимает доказательственный пакет от OSINT/Screening-контура, проверяет целостность и допустимость, создаёт устойчивые chunks, извлекает кандидатов сущностей/утверждений/связей, сохраняет provenance, выявляет противоречия и направляет спорные объекты на человеческую проверку."), p("Критическая архитектурная граница: <b>автоматический компонент не имеет endpoint и полномочия для прямого CLAIM → FACT</b>.", CALLOUT), PageBreak()]

    # 3. C3
    story += section_title("2", "C3 Component Diagram")
    c3 = scaled_svg(HW / "architecture" / "C3_KB_AGENT_COMPONENTS.svg", doc.width, 155 * mm)
    story += [c3, Spacer(1, 4 * mm), p("Диаграмма показывает внутренние компоненты контейнера и связи с OSINT Collectors, Main Analyst и хранилищами. Evidence Vault является доказательственным слоем; Knowledge Base получает только утверждённые знания."), PageBreak()]

    # 4. Components
    story += section_title("3", "Ответственность компонентов")
    story += [component_table(), Spacer(1, 5 * mm), p("Принцип проектирования", H2), p("Компоненты разделены по ответственности: admission, evidence integrity, extraction, provenance, entity resolution, contradiction analysis, review и publication. Это позволяет отдельно тестировать каждый этап и не смешивать добычу материала с утверждением факта."), PageBreak()]

    # 5. OpenAPI
    story += section_title("4", "OpenAPI 3.1")
    story += [p("Контракт API оформлен в <b>api/openapi.yaml</b>. Основные операции:"), endpoint_table(), Spacer(1, 6 * mm), p("Ключевые ограничения", H2), p("• Bearer authentication для внутреннего API.<br/>• 403 при нарушении policy/access class.<br/>• 409 для idempotency/state conflicts.<br/>• Отдельный human-review endpoint.<br/>• Отдельный lineage endpoint для трассировки производного объекта до source capture и stable chunks."), p("OpenAPI намеренно не содержит операции, которая позволяет автоматической модели присвоить объекту статус FACT.", CALLOUT), PageBreak()]

    # 6. Sequence
    story += section_title("5", "Sequence Diagram")
    story += [sequence_drawing(), Spacer(1, 5 * mm), p("Ключевой сценарий", H2), p("Collector регистрирует EvidencePackage. Policy Gate проверяет основание и класс доступа. Validator фиксирует оригинал и SHA-256. Extractor формирует кандидатов. Review Queue передаёт их аналитику. Только решение APPROVE позволяет Knowledge Publisher выполнить versioned write в Knowledge Base и Entity Graph; REWORK/REJECT остаются в Audit Journal."), link("Исходная Mermaid sequence diagram", README_URL.replace("README.md", "architecture/SEQUENCE_EVIDENCE_TO_KB.md")), PageBreak()]

    # 7. BPMN
    story += section_title("6", "BPMN — бизнес-процесс")
    bpmn = scaled_svg(HW / "architecture" / "BPMN" / "OSINT_KB_AGENT_BPMN_V1_READABLE.svg", doc.width, 165 * mm)
    story += [bpmn, Spacer(1, 4 * mm), p("BPMN дополняет LLD процессным взглядом: admission, параллельный сбор, нормализация, проверка достаточности, Research Gap, Red Team, Human Review и публикация. Возврат REWORK формирует управляемый цикл доисследования вместо заполнения пробелов предположениями."), PageBreak()]

    # 8. DFD
    story += section_title("7", "DFD — потоки информации")
    dfd = scaled_svg(HW / "architecture" / "DFD" / "OSINT_KB_AGENT_DFD_V1_READABLE.svg", doc.width, 165 * mm)
    story += [dfd, Spacer(1, 4 * mm), p("DFD показывает физическое движение данных между источниками, агентом и хранилищами. Evidence Vault хранит оригиналы и hashes; Operational DB — состояние процесса; Entity Graph — производную сеть связей; Knowledge Base — проверенный экспертный слой; Audit Journal — неизменяемый след действий."), PageBreak()]

    # 9. Data contracts
    story += section_title("8", "Информационная модель и доказательность")
    story += [overview_drawing(), Spacer(1, 6 * mm), p("Разделение объектов", H2)]
    classes = [
        ("SOURCE", "источник как объект происхождения"),
        ("SOURCE_CAPTURE", "сохранённая копия + URL + UTC + SHA-256"),
        ("STABLE_CHUNK", "воспроизводимый фрагмент материала"),
        ("CLAIM", "утверждение источника"),
        ("FACT", "объект, утверждённый после review"),
        ("INFERENCE", "аналитический вывод из фактов"),
        ("HYPOTHESIS", "версия, требующая проверки"),
        ("RELATION", "типизированная связь с evidence refs"),
        ("REVIEW", "APPROVE / REWORK / REJECT"),
        ("AUDIT_EVENT", "кто, когда и что изменил"),
    ]
    data = [[p("Класс", H3), p("Назначение", H3)]] + [[p(a, BODY), p(b, BODY)] for a, b in classes]
    tab = Table(data, colWidths=[50 * mm, 120 * mm])
    tab.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), LIGHT_BLUE), ("GRID", (0, 0), (-1, -1), 0.35, BORDER), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    story += [tab, PageBreak()]

    # 10. Addresses
    story += section_title("9", "Адреса, проверка и сдача")
    qr_repo = qr(REPO_URL, "repo.png")
    qr_folder = qr(FOLDER_URL, "folder.png")
    qr_pr = qr(PR_URL, "pr.png")
    qtable = Table([
        [Image(str(qr_repo), 32 * mm, 32 * mm), Image(str(qr_folder), 32 * mm, 32 * mm), Image(str(qr_pr), 32 * mm, 32 * mm)],
        [p("Репозиторий", CENTER), p("Папка ДЗ", CENTER), p("PR #12", CENTER)],
    ], colWidths=[55 * mm] * 3)
    qtable.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BOX", (0, 0), (-1, -1), 0.35, BORDER), ("INNERGRID", (0, 0), (-1, -1), 0.35, BORDER), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    story += [qtable, Spacer(1, 6 * mm), p("GitHub-адреса", H2), link("Репозиторий VictorKVS/OTUS-", REPO_URL), link("Папка ДЗ_05_OSINT_KB_Agent_LLD", FOLDER_URL), link("README — точка входа для преподавателя", README_URL), link("PDF для сдачи", PDF_URL), link("Pull Request #12", PR_URL), p(f"Merge commit: {MERGE_COMMIT}", CODE), Spacer(1, 6 * mm), p("Что отправить преподавателю", H2), p("1. Ссылку на папку ДЗ.<br/>2. PDF <b>DZ05_LLD_OSINT_KB_AGENT_SUBMISSION.pdf</b>.<br/>3. При необходимости — прямую ссылку на OpenAPI и C3."), p("Комплект самодостаточен: README → C3 → OpenAPI → Sequence → BPMN/DFD → исходники.", CALLOUT)]

    doc.build(story)
    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    SHA.write_text(f"{digest}  {OUT.name}\n", encoding="utf-8")
    print(f"Built {OUT} ({OUT.stat().st_size} bytes)")
    print(f"SHA-256 {digest}")


if __name__ == "__main__":
    build()

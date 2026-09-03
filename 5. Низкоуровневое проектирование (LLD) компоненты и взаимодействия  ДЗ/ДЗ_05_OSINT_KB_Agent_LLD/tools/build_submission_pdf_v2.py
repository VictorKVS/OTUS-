from __future__ import annotations

import hashlib
from pathlib import Path

from reportlab.graphics.shapes import Drawing, Line, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from svglib.svglib import svg2rlg


HW = Path(__file__).resolve().parents[1]
OUT = HW / "DZ05_LLD_OSINT_KB_AGENT_SUBMISSION.pdf"
SHA = HW / "SHA256SUMS.txt"

REPO_URL = "https://github.com/VictorKVS/OTUS-"
FOLDER_URL = (
    "https://github.com/VictorKVS/OTUS-/tree/main/"
    "5.%20%D0%9D%D0%B8%D0%B7%D0%BA%D0%BE%D1%83%D1%80%D0%BE%D0%B2%D0%BD%D0%B5%D0%B2%D0%BE%D0%B5%20"
    "%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20(LLD)%20"
    "%D0%BA%D0%BE%D0%BC%D0%BF%D0%BE%D0%BD%D0%B5%D0%BD%D1%82%D1%8B%20%D0%B8%20%D0%B2%D0%B7%D0%B0%D0%B8%D0%BC%D0%BE%D0%B4%D0%B5%D0%B9%D1%81%D1%82%D0%B2%D0%B8%D1%8F%20%20%D0%94%D0%97/"
    "%D0%94%D0%97_05_OSINT_KB_Agent_LLD"
)

NAVY = colors.HexColor("#17365D")
BLUE = colors.HexColor("#2F6FED")
LIGHT_BLUE = colors.HexColor("#EAF2FF")
PALE = colors.HexColor("#F6F8FB")
GREEN = colors.HexColor("#198754")
RED = colors.HexColor("#B42318")
GRAY = colors.HexColor("#5F6B7A")
DARK = colors.HexColor("#172033")
BORDER = colors.HexColor("#CBD5E1")


def register_fonts() -> None:
    regular = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    bold = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    if not regular.exists():
        regular = Path("/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf")
        bold = Path("/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf")
    pdfmetrics.registerFont(TTFont("Body", str(regular)))
    pdfmetrics.registerFont(TTFont("BodyBold", str(bold)))


register_fonts()
styles = getSampleStyleSheet()
BODY = ParagraphStyle("body", parent=styles["BodyText"], fontName="Body", fontSize=9.5, leading=13.5, textColor=DARK)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=8, leading=11, textColor=GRAY)
H1 = ParagraphStyle("h1", parent=styles["Heading1"], fontName="BodyBold", fontSize=22, leading=27, textColor=NAVY, spaceAfter=8)
H2 = ParagraphStyle("h2", parent=styles["Heading2"], fontName="BodyBold", fontSize=14, leading=18, textColor=NAVY, spaceAfter=6)
TITLE = ParagraphStyle("title", parent=styles["Title"], fontName="BodyBold", fontSize=27, leading=33, alignment=TA_CENTER, textColor=NAVY)
CENTER = ParagraphStyle("center", parent=BODY, alignment=TA_CENTER)
CALLOUT = ParagraphStyle("callout", parent=BODY, fontName="BodyBold", fontSize=10, leading=15, backColor=LIGHT_BLUE, borderColor=BLUE, borderWidth=0.7, borderPadding=8, textColor=NAVY)


def p(text: str, style=BODY):
    return Paragraph(text, style)


def link(label: str, url: str):
    return p(f'<link href="{url}" color="#2F6FED"><u>{label}</u></link>')


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setStrokeColor(BORDER)
    canvas.line(18 * mm, h - 15 * mm, w - 18 * mm, h - 15 * mm)
    canvas.setFont("Body", 7.5)
    canvas.setFillColor(GRAY)
    canvas.drawString(18 * mm, h - 11.5 * mm, "OTUS · ДЗ 05 · C4 → C3 → Sequence → OpenAPI")
    canvas.drawRightString(w - 18 * mm, 10 * mm, f"VictorKVS / OTUS- · стр. {doc.page}")
    canvas.line(18 * mm, 14 * mm, w - 18 * mm, 14 * mm)
    canvas.restoreState()


class Doc(BaseDocTemplate):
    def __init__(self, filename: str):
        super().__init__(filename, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=22 * mm, bottomMargin=20 * mm, title="ДЗ 05 — Многоуровневое проектирование AI Service", author="VictorKVS")
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")
        self.addPageTemplates(PageTemplate(id="main", frames=frame, onPage=header_footer))


def scaled_svg(path: Path, max_w: float, max_h: float):
    drawing = svg2rlg(str(path))
    if drawing is None:
        raise RuntimeError(f"Cannot render SVG: {path}")
    scale = min(max_w / drawing.width, max_h / drawing.height, 1.0)
    drawing.width *= scale
    drawing.height *= scale
    drawing.scale(scale, scale)
    return drawing


def sequence_drawing() -> Drawing:
    d = Drawing(500, 310)
    parts = ["User", "Frontend", "Backend", "Controller", "RAG", "Vector/SQL", "LLM", "Guard", "Formatter"]
    xs = [25, 80, 140, 205, 265, 325, 385, 440, 485]
    for x, name in zip(xs, parts):
        d.add(Rect(x - 22, 270, 44, 22, rx=4, ry=4, fillColor=LIGHT_BLUE if name not in {"User", "Vector/SQL", "LLM"} else PALE, strokeColor=BORDER, strokeWidth=0.7))
        d.add(String(x, 278, name, fontName="BodyBold", fontSize=5.5, fillColor=NAVY, textAnchor="middle"))
        d.add(Line(x, 267, x, 22, strokeColor=colors.HexColor("#AAB4C3"), strokeWidth=0.5))

    events = [
        (0, 1, 246, "request recommendation"),
        (1, 2, 220, "POST case/recommendation"),
        (2, 3, 194, "POST /get_recommendation"),
        (3, 4, 168, "normalize + retrieve"),
        (4, 5, 142, "semantic + structured context"),
        (4, 6, 116, "prompt + context"),
        (6, 7, 90, "draft recommendation"),
        (7, 8, 64, "evidence + confidence"),
        (8, 3, 40, "RecommendationResponse"),
    ]
    for a, b, y, label in events:
        x1, x2 = xs[a], xs[b]
        direction = 1 if x2 >= x1 else -1
        target = x2 - direction * 4
        d.add(Line(x1, y, target, y, strokeColor=BLUE, strokeWidth=1.0))
        d.add(String((x1 + x2) / 2, y + 5, label, fontName="Body", fontSize=5.2, fillColor=DARK, textAnchor="middle"))
    d.add(String(250, 302, "Sequence — Пользователь запрашивает рекомендацию", fontName="BodyBold", fontSize=10, fillColor=NAVY, textAnchor="middle"))
    return d


def requirement_table():
    rows = [
        ["C2 Container Diagram", "Frontend · Backend · AI Service · Vector DB · SQL DB", "✅"],
        ["C3 AI Service", "Controller · RAG · Prompt Factory · LLM Client · Guard · Evaluator", "✅"],
        ["Sequence", "Пользователь запрашивает рекомендацию", "✅"],
        ["OpenAPI", "POST /get_recommendation", "✅"],
        ["API quality", "types + request/response examples + error codes", "✅"],
    ]
    data = [[p("Требование", H2), p("Реализация", H2), p("", H2)]] + [[p(a), p(b), p(c, CENTER)] for a, b, c in rows]
    t = Table(data, colWidths=[48 * mm, 108 * mm, 14 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), LIGHT_BLUE), ("GRID", (0, 0), (-1, -1), 0.35, BORDER), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return t


def api_table():
    rows = [
        ["200", "RecommendationResponse", "recommendation + confidence + evidence_refs"],
        ["400", "INVALID_REQUEST", "ошибка контракта"],
        ["401", "UNAUTHORIZED", "authentication"],
        ["404", "CASE_NOT_FOUND", "case отсутствует"],
        ["422", "INSUFFICIENT_EVIDENCE", "недостаточно доказательств"],
        ["429", "RATE_LIMITED", "rate limit"],
        ["500", "INTERNAL_ERROR", "ошибка AI Service"],
        ["503", "DEPENDENCY_UNAVAILABLE", "LLM / Vector DB недоступны"],
    ]
    data = [[p("HTTP", H2), p("Код", H2), p("Смысл", H2)]] + [[p(a), p(b), p(c)] for a, b, c in rows]
    t = Table(data, colWidths=[22 * mm, 63 * mm, 85 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), LIGHT_BLUE), ("GRID", (0, 0), (-1, -1), 0.35, BORDER), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return t


def build() -> None:
    doc = Doc(str(OUT))
    story = []

    story += [Spacer(1, 24 * mm), p("OTUS · ИИ-архитектор", ParagraphStyle("top", parent=H2, alignment=TA_CENTER, textColor=BLUE)), p("Домашнее задание №5", TITLE), p("Многоуровневое проектирование", TITLE), Spacer(1, 3 * mm), p("от C4 Model до спецификации API", ParagraphStyle("sub", parent=H1, alignment=TA_CENTER, fontSize=20)), Spacer(1, 10 * mm), p("OSINT / Due Diligence AI Platform", ParagraphStyle("case", parent=H2, alignment=TA_CENTER, fontSize=15)), Spacer(1, 10 * mm), p("C2 → C3 AI Service → Sequence → OpenAPI /get_recommendation", CALLOUT), Spacer(1, 10 * mm), link("Репозиторий: github.com/VictorKVS/OTUS-", REPO_URL), link("Папка сдачи: ДЗ_05_OSINT_KB_Agent_LLD", FOLDER_URL), PageBreak()]

    story += [p("1. Соответствие условию", H1), requirement_table(), Spacer(1, 6 * mm), p("Работа использует собственный кейс, что допускается условием задания. Один сценарий проходит через все уровни: пользователь запрашивает рекомендацию → Backend вызывает AI Service → AI Service выполняет RAG и LLM inference → возвращает recommendation с evidence refs."), PageBreak()]

    story += [p("2. C2 — Container Diagram", H1), scaled_svg(HW / "architecture" / "C2_SYSTEM_CONTAINERS.svg", doc.width, 175 * mm), Spacer(1, 4 * mm), p("На C2 явно выделены обязательные контейнеры: <b>Frontend, Backend, AI Service, Vector DB и SQL DB</b>. Evidence Vault и External OSINT Sources добавлены как доменно необходимые контейнеры/внешние системы."), PageBreak()]

    story += [p("3. C3 — AI Service", H1), scaled_svg(HW / "architecture" / "C3_KB_AGENT_COMPONENTS.svg", doc.width, 175 * mm), Spacer(1, 3 * mm), p("AI Service детализирован до компонентов Recommendation Controller, Query Normalizer, RAG Manager, Prompt Template Factory, LLM Client, Citation & Evidence Guard, Confidence Evaluator и Recommendation Formatter. Эти же компоненты участвуют в Sequence Diagram."), PageBreak()]

    story += [p("4. Sequence — пользователь запрашивает рекомендацию", H1), sequence_drawing(), Spacer(1, 5 * mm), p("Backend вызывает <b>POST /get_recommendation</b>. RAG Manager получает semantic context из Vector DB и structured context из SQL DB. LLM формирует draft; Citation Guard проверяет evidence; Confidence Evaluator оценивает ограничения; Formatter возвращает RecommendationResponse."), p("Если доказательств недостаточно, API возвращает 422 INSUFFICIENT_EVIDENCE вместо выдуманного ответа.", CALLOUT), PageBreak()]

    story += [p("5. OpenAPI 3.1", H1), p("Файл: <b>api/openapi.yaml</b>"), Spacer(1, 2 * mm), p("Главный контракт Backend ↔ AI Service:", H2), p("POST /get_recommendation", CALLOUT), Spacer(1, 5 * mm), p("RecommendationRequest содержит request_id, case_id, query, recommendation_type, language, top_k, include_evidence и constraints. RecommendationResponse содержит recommendation, rationale, confidence, evidence_refs, limitations, research_gaps и model_info."), Spacer(1, 4 * mm), api_table(), Spacer(1, 5 * mm), p("В OpenAPI приведены полноценные request/response examples и примеры ошибок, что закрывает критерий качества API."), PageBreak()]

    story += [p("6. Связность C3 ↔ Sequence ↔ API", H1), p("<b>C3:</b> Recommendation Controller → Query Normalizer → RAG Manager → Prompt Template Factory → LLM Client → Citation Guard → Confidence Evaluator → Recommendation Formatter."), Spacer(1, 5 * mm), p("<b>Sequence:</b> использует те же компоненты в той же логической последовательности."), Spacer(1, 5 * mm), p("<b>API:</b> Recommendation Controller реализует POST /get_recommendation и возвращает объект, собранный Recommendation Formatter."), Spacer(1, 8 * mm), p("Таким образом, диаграммы не являются независимыми картинками: они описывают один и тот же сценарий на разных уровнях детализации.", CALLOUT), PageBreak()]

    story += [p("7. Дополнительные архитектурные материалы", H1), p("BPMN и DFD не заменяют обязательные C2/C3/Sequence, а показывают более широкий evidence/knowledge pipeline OSINT-платформы."), Spacer(1, 4 * mm), scaled_svg(HW / "architecture" / "BPMN" / "OSINT_KB_AGENT_BPMN_V1_READABLE.svg", doc.width, 90 * mm), Spacer(1, 3 * mm), scaled_svg(HW / "architecture" / "DFD" / "OSINT_KB_AGENT_DFD_V1_READABLE.svg", doc.width, 90 * mm), PageBreak()]

    story += [p("8. Адреса для проверки", H1), link("Репозиторий", REPO_URL), Spacer(1, 3 * mm), link("Папка ДЗ", FOLDER_URL), Spacer(1, 7 * mm), p("Основные файлы", H2), p("• README.md — точка входа.<br/>• architecture/C2_SYSTEM_CONTAINERS.svg — C2.<br/>• architecture/C3_KB_AGENT_COMPONENTS.svg — C3.<br/>• architecture/SEQUENCE_GET_RECOMMENDATION.md — Sequence.<br/>• api/openapi.yaml — OpenAPI 3.1.<br/>• DZ05_LLD_OSINT_KB_AGENT_SUBMISSION.pdf — единый PDF."), Spacer(1, 8 * mm), p("Итог", H2), p("Работа соответствует заданной цепочке C2 → C3 AI Service → Sequence «Пользователь запрашивает рекомендацию» → OpenAPI POST /get_recommendation. API содержит типы, примеры и коды ошибок."),]

    doc.build(story)
    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    SHA.write_text(f"{digest}  {OUT.name}\n", encoding="utf-8")
    print(f"Built {OUT} ({OUT.stat().st_size} bytes)")
    print(f"SHA-256 {digest}")


if __name__ == "__main__":
    build()

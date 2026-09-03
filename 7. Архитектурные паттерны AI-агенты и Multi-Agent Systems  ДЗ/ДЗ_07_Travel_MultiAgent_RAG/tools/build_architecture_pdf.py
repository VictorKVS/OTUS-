from pathlib import Path
import math

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "architecture" / "DZ07_TRAVEL_MULTIAGENT_ARCHITECTURE.pdf"

W, H = landscape(A4)
NAVY = colors.HexColor("#17365D")
BLUE = colors.HexColor("#2F6FED")
GREEN = colors.HexColor("#198754")
ORANGE = colors.HexColor("#D97706")
PALE = colors.HexColor("#F6F8FB")
LIGHT = colors.HexColor("#EAF2FF")
BORDER = colors.HexColor("#CBD5E1")
DARK = colors.HexColor("#172033")
GRAY = colors.HexColor("#5F6B7A")


def register_fonts():
    pairs = [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ("/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf", "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"),
    ]
    for regular, bold in pairs:
        if Path(regular).exists() and Path(bold).exists():
            pdfmetrics.registerFont(TTFont("Body", regular))
            pdfmetrics.registerFont(TTFont("BodyBold", bold))
            return
    raise RuntimeError("Cyrillic-capable font not found")


def box(c, x, y, w, h, label, subtitle="", fill=colors.white, stroke=BORDER):
    c.setFillColor(fill); c.setStrokeColor(stroke); c.setLineWidth(1)
    c.roundRect(x, y, w, h, 4*mm, fill=1, stroke=1)
    c.setFillColor(NAVY); c.setFont("BodyBold", 8.5)
    c.drawCentredString(x+w/2, y+h/2+2, label)
    if subtitle:
        c.setFillColor(GRAY); c.setFont("Body", 6.3)
        c.drawCentredString(x+w/2, y+h/2-9, subtitle)


def arrow(c, x1, y1, x2, y2, color=BLUE, width=1.2):
    c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(width)
    c.line(x1, y1, x2, y2)
    ang = math.atan2(y2-y1, x2-x1)
    al, aw = 8, 3.5
    bx, by = x2-al*math.cos(ang), y2-al*math.sin(ang)
    lx, ly = bx+aw*math.cos(ang+math.pi/2), by+aw*math.sin(ang+math.pi/2)
    rx, ry = bx+aw*math.cos(ang-math.pi/2), by+aw*math.sin(ang-math.pi/2)
    path = c.beginPath(); path.moveTo(x2, y2); path.lineTo(lx, ly); path.lineTo(rx, ry); path.close()
    c.drawPath(path, fill=1, stroke=0)


def title(c, text, subtitle, size=19):
    c.setFillColor(NAVY); c.setFont("BodyBold", size)
    c.drawString(18*mm, H-22*mm, text)
    c.setFillColor(GRAY); c.setFont("Body", 9.5)
    c.drawString(18*mm, H-29*mm, subtitle)


def footer(c, page):
    c.setStrokeColor(BORDER); c.setLineWidth(0.5)
    c.line(16*mm, 13*mm, W-16*mm, 13*mm)
    c.setFillColor(GRAY); c.setFont("Body", 7)
    c.drawCentredString(W/2, 7.5*mm, f"OTUS · DZ 07 · Multi-Agent Travel Assistant · M1.1 · VictorKVS · page {page}/3")


def build():
    register_fonts()
    c = canvas.Canvas(str(OUT), pagesize=(W, H))
    c.setTitle("OTUS DZ07 - Multi-Agent Travel Assistant M1.1")
    c.setAuthor("VictorKVS")

    # Page 1: Supervisor + typed messages
    title(c, "DZ 07 - Supervisor Multi-Agent Architecture", "Typed LangChain messages + explicit Command handoffs", 17.5)
    y = H-70*mm
    box(c, 18*mm, y, 36*mm, 20*mm, "Employee", "HumanMessage", LIGHT)
    box(c, 70*mm, y, 40*mm, 20*mm, "Manager Agent", "Supervisor / context", colors.HexColor("#FFF7ED"), ORANGE)
    arrow(c, 54*mm, y+10*mm, 70*mm, y+10*mm)
    box(c, 132*mm, y+25*mm, 42*mm, 18*mm, "Policy RAG", "hybrid retrieval", colors.white, BLUE)
    box(c, 132*mm, y-3*mm, 42*mm, 18*mm, "Flight Search", "read-only mock", colors.white, BLUE)
    box(c, 196*mm, y-3*mm, 42*mm, 18*mm, "Hotel Search", "read-only mock", colors.white, BLUE)
    box(c, 196*mm, y+25*mm, 42*mm, 18*mm, "Budget Analyst", "cost + policy", colors.white, BLUE)
    arrow(c, 110*mm, y+10*mm, 132*mm, y+34*mm)
    arrow(c, 153*mm, y+25*mm, 153*mm, y+15*mm)
    arrow(c, 174*mm, y+6*mm, 196*mm, y+6*mm)
    arrow(c, 217*mm, y+15*mm, 217*mm, y+25*mm)
    arrow(c, 196*mm, y+34*mm, 110*mm, y+10*mm, ORANGE)

    for x, title_text, lines, fill, stroke in [
        (18*mm, "TravelState(MessagesState)", [
            "messages: SystemMessage / HumanMessage / AIMessage",
            "request · policy_hits · expanded_policy_chunks",
            "flight_options · hotel_options · budget · final_answer",
            "trace: every explicit handoff",
        ], PALE, BORDER),
        (150*mm, "Agent communication gate", [
            "✓ typed messages are stored in shared state",
            "✓ Manager delegates through Command(goto=...)",
            "✓ each agent has Single Responsibility",
            "✓ final response returns to Manager",
        ], colors.HexColor("#ECFDF5"), GREEN),
    ]:
        c.setFillColor(fill); c.setStrokeColor(stroke)
        c.roundRect(x, 39*mm, 120*mm, 38*mm, 4*mm, fill=1, stroke=1)
        c.setFillColor(stroke if stroke == GREEN else NAVY); c.setFont("BodyBold", 10)
        c.drawString(x+6*mm, 67*mm, title_text)
        c.setFillColor(DARK); c.setFont("Body", 7.3)
        for i, line in enumerate(lines): c.drawString(x+6*mm, (59-i*6)*mm, line)
    footer(c, 1); c.showPage()

    # Page 2: Hybrid RAG
    title(c, "Hybrid RAG Flow - Corporate Travel Policy", "Dense + lexical retrieval, dedup, reranking, chunk expansion and evidence refs")
    xs = [18, 70, 122, 174, 226]
    rows = [
        (H-59*mm, [("Travel Policy","source"),("Structure-aware","chunking"),("Metadata","id/version/ACL"),("Dense Embeddings","demo hash / prod model"),("Vector DB","Pinecone/pgvector")]),
        (H-102*mm, [("Trip Request","query"),("Normalize","RU aliases"),("Dense Search","semantic"),("Lexical Search","sparse"),("Hybrid Merge","0.55/0.35/0.10")]),
        (H-145*mm, [("Dedup","chunk_id"),("Rerank","hybrid score"),("Top-k","primary hits"),("Chunk Expansion","section ±1"),("Evidence Pack","refs + scores")]),
    ]
    for row_idx, (yy, items) in enumerate(rows):
        for (lab, sub), x in zip(items, xs):
            fill = colors.HexColor("#FFF7ED") if lab == "Rerank" else (colors.HexColor("#ECFDF5") if lab == "Vector DB" else colors.white)
            stroke = ORANGE if lab == "Rerank" else (GREEN if lab == "Vector DB" else (BLUE if row_idx == 1 else BORDER))
            box(c, x*mm, yy, 42*mm, 18*mm, lab, sub, fill, stroke)
        for i in range(4): arrow(c, (xs[i]+42)*mm, yy+9*mm, xs[i+1]*mm, yy+9*mm)
    box(c, 112*mm, 29*mm, 75*mm, 20*mm, "Policy RAG Agent", "Grounded answer / POLICY_GAP", colors.HexColor("#ECFDF5"), GREEN)
    arrow(c, 247*mm, H-145*mm, 187*mm, 49*mm, GREEN)
    c.setFillColor(DARK); c.setFont("Body", 6.7)
    c.drawString(18*mm, 20.5*mm, "Normalization: отель→гостиница · Москве→москва · перелета→перелёт · согласования→согласование")
    footer(c, 2); c.showPage()

    # Page 3: Quality gate + production boundary
    title(c, "Verification & Production Boundary", "What the demo proves, and what remains a production replacement")
    c.setFillColor(NAVY); c.setFont("BodyBold", 9)
    c.drawString(18*mm, H-58*mm, "Layer"); c.drawString(60*mm, H-58*mm, "Demo"); c.drawString(123*mm, H-58*mm, "Production")
    rows = [
        ("Embeddings","deterministic hash","dedicated embedding model"),
        ("Vector store","in-memory chunks","Pinecone / pgvector"),
        ("Lexical","token overlap","sparse/BM25-like index"),
        ("Reranker","hybrid score","cross-encoder / managed"),
        ("Messages","LangChain typed","typed + persistence/observability"),
        ("Handoff","Command(goto)","policy-aware supervisor"),
        ("Eval","5 synthetic cases","versioned representative set"),
    ]
    yy = H-66*mm
    for layer, demo, prod in rows:
        c.setStrokeColor(BORDER); c.line(18*mm, yy-2*mm, W-18*mm, yy-2*mm)
        c.setFillColor(DARK); c.setFont("BodyBold", 7.2); c.drawString(18*mm, yy, layer)
        c.setFont("Body", 7.2); c.drawString(60*mm, yy, demo); c.drawString(123*mm, yy, prod)
        yy -= 9*mm

    for x, heading, lines, fill, stroke in [
        (18*mm, "CI quality gate", ["pytest: typed messages + explicit handoffs","hybrid retrieval: dense + lexical + rerank + expansion","HitRate@2 >= 0.80","MRR@2 >= 0.70","demo run: no API key / no network"], colors.HexColor("#ECFDF5"), GREEN),
        (150*mm, "Final response contract", ["status + estimated_total_rub","flight_id + hotel_id","evidence_refs with dense/lexical/hybrid scores","retrieval_metrics","expanded_context_chunk_ids"], LIGHT, BLUE),
    ]:
        c.setFillColor(fill); c.setStrokeColor(stroke)
        c.roundRect(x, 35*mm, 120*mm, 44*mm, 4*mm, fill=1, stroke=1)
        c.setFillColor(stroke); c.setFont("BodyBold", 11); c.drawString(x+6*mm, 68*mm, heading)
        c.setFillColor(DARK); c.setFont("Body", 8)
        for i, line in enumerate(lines): c.drawString(x+6*mm, (60-i*6)*mm, line)
    footer(c, 3); c.save()


if __name__ == "__main__":
    build()
    print(OUT)

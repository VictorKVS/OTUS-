from __future__ import annotations

from pathlib import Path
from urllib.parse import quote

import fitz

HW = Path(__file__).resolve().parents[1]
PDF = HW / "DZ05_LLD_OSINT_KB_AGENT_SUBMISSION.pdf"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

REPO = "https://github.com/VictorKVS/OTUS-"
BASE_PATH = "5. Низкоуровневое проектирование (LLD) компоненты и взаимодействия  ДЗ/ДЗ_05_OSINT_KB_Agent_LLD"


def gh_blob(rel: str) -> str:
    return f"{REPO}/blob/main/{quote(BASE_PATH + '/' + rel, safe='/()_-')}"


def gh_tree(rel: str = "") -> str:
    path = BASE_PATH + ("/" + rel if rel else "")
    return f"{REPO}/tree/main/{quote(path, safe='/()_-')}"


LINKS = {
    1: [("GitHub: репозиторий", REPO), ("папка ДЗ", gh_tree())],
    2: [("GitHub: README", gh_blob("README.md")), ("условие ДЗ", gh_blob("УСЛОВИЕ_ДЗ.md"))],
    3: [("GitHub: C2", gh_blob("architecture/C2_SYSTEM_CONTAINERS.svg")), ("Draw.io", gh_blob("architecture/DIAGRAMS.drawio"))],
    4: [("GitHub: C3", gh_blob("architecture/C3_KB_AGENT_COMPONENTS.svg")), ("C3 source", gh_blob("architecture/C3_KB_AGENT_COMPONENTS.md"))],
    5: [("GitHub: Sequence", gh_blob("architecture/SEQUENCE_GET_RECOMMENDATION.md"))],
    6: [("GitHub: OpenAPI 3.1", gh_blob("api/openapi.yaml"))],
    7: [("GitHub: Draw.io", gh_blob("architecture/DIAGRAMS.drawio")), ("README", gh_blob("README.md"))],
    8: [("GitHub: готовая папка ДЗ", gh_tree()), ("OpenAPI", gh_blob("api/openapi.yaml"))],
}


def main() -> None:
    src = fitz.open(PDF)
    font = fitz.Font(fontfile=FONT)
    page_count = len(src)

    for page_no, page in enumerate(src, start=1):
        rect = page.rect
        page.insert_font(fontname="DejaVuSans", fontfile=FONT)

        # Clean the old footer area only. The report body is left untouched.
        page.draw_rect(
            fitz.Rect(0, rect.height - 66, rect.width, rect.height),
            color=(1, 1, 1),
            fill=(1, 1, 1),
            overlay=True,
        )

        # Contextual GitHub links immediately above the footer.
        x = 36
        y = rect.height - 58
        fontsize = 6.5
        for label, url in LINKS.get(page_no, [("GitHub: папка ДЗ", gh_tree())]):
            width = font.text_length(label, fontsize=fontsize)
            if x + width > rect.width - 36:
                x = 36
                y += 11
            link_rect = fitz.Rect(x, y, min(x + width + 4, rect.width - 36), y + 11)
            page.insert_text(
                fitz.Point(x, y + 8.5),
                label,
                fontname="DejaVuSans",
                fontsize=fontsize,
                color=(0.18, 0.42, 0.86),
                overlay=True,
            )
            page.draw_line(
                fitz.Point(x, y + 10),
                fitz.Point(x + width, y + 10),
                color=(0.18, 0.42, 0.86),
                width=0.35,
                overlay=True,
            )
            page.insert_link({"kind": fitz.LINK_URI, "from": link_rect, "uri": url})
            x += width + 14

        # Exactly one informative footer row per page.
        page.draw_line(
            fitz.Point(36, rect.height - 29),
            fitz.Point(rect.width - 36, rect.height - 29),
            color=(0.78, 0.81, 0.86),
            width=0.55,
            overlay=True,
        )
        footer = (
            f"OTUS · ИИ-архитектор · ДЗ 05 · Многоуровневое проектирование C4 → API "
            f"· VictorKVS · стр. {page_no} из {page_count}"
        )
        page.insert_textbox(
            fitz.Rect(36, rect.height - 24, rect.width - 36, rect.height - 8),
            footer,
            fontsize=6.7,
            fontname="DejaVuSans",
            color=(0.32, 0.36, 0.43),
            align=fitz.TEXT_ALIGN_CENTER,
            overlay=True,
        )

    tmp = PDF.with_suffix(".postprocessed.pdf")
    src.save(tmp, garbage=4, deflate=True)
    src.close()
    tmp.replace(PDF)
    print(f"Postprocessed: {PDF} ({PDF.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

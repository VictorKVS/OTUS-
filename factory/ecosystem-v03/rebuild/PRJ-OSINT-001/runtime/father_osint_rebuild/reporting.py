"""BLOCK: preliminary Markdown report builder."""


DISCLAIMER = "**Not verified infringements or accusations. Human review required.**"


def build_report(con):
    rows = con.execute(
        "SELECT id,category,score,title,url,status "
        "FROM findings ORDER BY score DESC,id"
    ).fetchall()

    lines = [
        "# Preliminary OSINT signals",
        "",
        DISCLAIMER,
        "",
        f"Unique signals: {len(rows)}",
        "",
    ]

    for case_id, category, score, title, url, status in rows:
        lines.extend(
            [
                f"## CASE-{case_id:05d} · {category} · priority {score}/100",
                f"- Title: {title}",
                f"- URL: {url}",
                f"- Review: {status}",
                "- Next: verify rights, context, and licensing with a qualified specialist.",
                "",
            ]
        )

    return "\n".join(lines)

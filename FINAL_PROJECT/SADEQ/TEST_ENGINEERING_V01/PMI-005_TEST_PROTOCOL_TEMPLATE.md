# ПМИ-005 — Протокол испытания (шаблон)
**NOT A TEST RESULT / NO PASS CLAIM**

1. Протокол № / TEST-ID / ПМИ revision:
2. Заказчик / комиссия / исполнитель / reviewer:
3. Дата и время начала/окончания в UTC:
4. Цель / исходное требование ТЗ / источник и пункт:
5. Испытуемый артефакт: git SHA; source/tree/build/container digest; dependency lock; model & embedding digest; prompt/policy/source schema/dataset version:
6. Среда: OS/version/CPU/RAM/GPU, network firewall/offline controls, PostgreSQL/Qdrant/ITSM test version:
7. Сведения о предшествующих испытаниях, test run ID:
8. Preconditions checklist / blocked conditions:
9. Expected / Actual table (each step):
10. HTTP/DB/ITSM source-of-truth before-after states with SHA256:
11. Security decisions, missing/forbidden effects and audit receipt:
12. Deviations, severity, ticket/incident/rollback:
13. Status: PASS / FAIL / BLOCKED / NOT_RUN / INCONCLUSIVE:
14. Raw evidence list, storage URI, SHA256, provenance and redaction:
15. Repeatability: command, start seed, clean-state and replay steps:
16. Conclusion, acceptance restrictions, recommendations:
17. Signatures: developer / QA / security reviewer / independent POLYGON / release owner (required according to test class).

**Note:** automated pytest output can be attached under point 14, but cannot replace the entire programme/methodology or business acceptance act.

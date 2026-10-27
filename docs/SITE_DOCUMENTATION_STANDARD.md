# FATHER Site Documentation Pack Standard

Статус: **CANONICAL DESIGN v1**

Сайт FATHER считается инженерным изделием и имеет собственное документальное досье. Документы создаются и поддерживаются вместе с кодом.

## Rule

```text
SITE IDEA / CHANGE
→ REQUIREMENTS
→ UX / INFORMATION ARCHITECTURE
→ ARCHITECTURE / DATA CONTRACTS
→ SECURITY / PRIVACY
→ IMPLEMENTATION
→ QA / ACCESSIBILITY / PERFORMANCE
→ RELEASE / OPERATIONS
→ EVIDENCE
→ NEXT CHANGE
```

Ни один release не считается полным, если обязательный документ отсутствует, не имеет owner/approver, находится в FAIL/BLOCKED или не связан с требуемым evidence.

## Automation

Source of truth: `site/data/site-document-pack.json`.

- `tools/generate_site_document_pack.py` восстанавливает недостающие controlled documents;
- `tools/validate_site_document_pack.py` проверяет completeness/metadata/status;
- CI workflow выполняет validator на изменениях сайта/Factory/doc pack;
- `site/document-center.html` отображает состояние пакета.

Документы живут в `docs/site/` и не заменяют специализированные FATHER standards; они ссылаются на них.

"""SADEQ TP-001 design-time JSON Schema tests.
Runnable after installing pytest and jsonschema[format]. Not POLYGON qualification.
"""
import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


def read_json(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def validator(schema_name):
    schema = read_json(f"contracts/{schema_name}.schema.json")
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


@pytest.mark.parametrize(
    "fixture,expected_valid",
    [
        ("inc_001_valid.json", True),
        ("inc_001_reject_unknown_nested.json", False),
        ("inc_001_reject_spoofed_tenant.json", False),
    ],
)
def test_incident_fixtures(fixture, expected_valid):
    data = read_json(f"fixtures/{fixture}")
    assert validator("InboundIncidentV1").is_valid(data) == expected_valid


def test_required_source_and_priority_enum():
    original = read_json("fixtures/inc_001_valid.json")
    missing = copy.deepcopy(original)
    del missing["source_system"]
    bad_priority = copy.deepcopy(original)
    bad_priority["priority"] = "P0"
    v = validator("InboundIncidentV1")
    assert not v.is_valid(missing)
    assert not v.is_valid(bad_priority)


def test_invalid_timestamp_rejected_with_format_checker():
    data = read_json("fixtures/inc_001_valid.json")
    data["observed_at"] = "not-a-timestamp"
    assert not validator("InboundIncidentV1").is_valid(data)


def test_action_contract_rejects_extra_nested_and_unsafe_tool():
    import uuid
    good = {
        "schema_version": "1.0.0",
        "proposal_id": str(uuid.UUID(int=1)),
        "tenant_id": "tenant-a",
        "target_ticket_id": "INC-001",
        "object_state_version": 1,
        "tool_name": "mock_itsm.update_ticket_status",
        "arguments": {"new_status": "IN_PROGRESS"},
        "expected_postcondition": {"status": "IN_PROGRESS"},
        "evidence_refs": [
            {"source_id": "SOP-01", "chunk_id": "SOP-01-CH1", "source_sha256": "a" * 64}
        ],
        "reason": "Факт подтверждён регламентом",
        "expires_at": "2026-12-01T12:00:00Z",
    }
    v = validator("ActionProposalV1")
    assert v.is_valid(good)
    injected = copy.deepcopy(good)
    injected["arguments"]["shell_command"] = "echo no"
    assert not v.is_valid(injected)
    tool = copy.deepcopy(good)
    tool["tool_name"] = "admin_export_all"
    assert not v.is_valid(tool)
    # Business rule: exact action and expected postcondition must match.
    mismatched = copy.deepcopy(good)
    mismatched["expected_postcondition"]["status"] = "WAITING_FOR_SUPPORT"
    assert v.is_valid(mismatched)  # Schema alone is insufficient!
    assert mismatched["arguments"]["new_status"] != mismatched["expected_postcondition"]["status"]


def test_approval_is_bound_to_exact_digest_shape():
    approval = {
        "schema_version": "1.0.0",
        "proposal_id": "00000000-0000-0000-0000-000000000001",
        "proposal_sha256": "b" * 64,
        "decision": "APPROVE",
        "reason": "Допустимое тестовое действие",
        "approved_state_version": 1,
    }
    v = validator("ApprovalDecisionV1")
    assert v.is_valid(approval)
    approval["principal_id"] = "admin-from-body"
    assert not v.is_valid(approval)  # Identity only server-side.


def test_internal_observation_not_a_client_request():
    internal = {
        "schema_version": "1.0.0",
        "tenant_id": "tenant-a",
        "principal_id": "svc-ingress-01",
        "source_system": "mock-itsm",
        "external_ticket_id": "INC-001",
        "object_key": "SVC-X",
        "event_id": "00000000-0000-0000-0000-000000000002",
        "idempotency_key": "0" * 64,
        "observed_at": "2026-11-28T09:00:00+03:00",
        "source_sha256": "a" * 64,
        "trace_id": "TRACE-INC-001",
    }
    assert validator("ValidatedObservationV1").is_valid(internal)
    assert not validator("InboundIncidentV1").is_valid(internal)

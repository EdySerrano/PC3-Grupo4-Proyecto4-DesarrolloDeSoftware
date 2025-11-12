import json
from audit_cli import reporting
from audit_cli.models import AuditResult


def make_sample_result() -> AuditResult:
    return {
        "host": "example.com",
        "port": 443,
        "check_type": "tls_version",
        "status": "OK",
        "details": "TLSv1.2 detected",
        "timestamp_utc": "2025-01-01T00:00:00Z",
    }


def test_results_to_json_and_back():
    results = [make_sample_result()]
    j = reporting.results_to_json(results)
    parsed = json.loads(j)
    assert isinstance(parsed, list)
    assert parsed[0]["host"] == results[0]["host"]
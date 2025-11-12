import json
import csv
from audit_cli import reporting
from audit_cli.models import AuditResult
from io import StringIO


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


def test_results_to_csv_and_reader():
    results = [make_sample_result()]
    csv_text = reporting.results_to_csv(results)

    f = StringIO(csv_text)
    reader = csv.DictReader(f)
    rows = list(reader)
    assert len(rows) == 1
    row = rows[0]
    assert row["host"] == "example.com"
    assert int(row["port"]) == 443


def test_results_to_csv_empty():
    """Verifica que una lista vacia produzca un CSV vacio."""
    results = []
    csv_text = reporting.results_to_csv(results)
    assert csv_text == ""
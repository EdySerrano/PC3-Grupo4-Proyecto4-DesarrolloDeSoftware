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


def test_save_report_writes_file_and_reports_message(tmp_path, capsys):
    results = [make_sample_result()]
    content = reporting.results_to_json(results)

    out_file = tmp_path / "out.json"
    reporting.save_report(content, str(out_file))

    # Verificar que el archivo existe y que el contenido coincide
    assert out_file.exists()
    loaded = json.loads(out_file.read_text(encoding="utf-8"))
    assert loaded[0]["host"] == "example.com"

    captured = capsys.readouterr()
    assert out_file.name in captured.err


def test_save_report_prints_to_stdout(capsys):
    results = [make_sample_result()]
    content = reporting.results_to_json(results)

    reporting.save_report(content, None)

    captured = capsys.readouterr()
    assert json.loads(captured.out)[0]["host"] == "example.com"


def test_save_report_handles_io_error(tmp_path, capsys):
    content = "Estos son datos de prueba"

    failing_path = str(tmp_path)

    reporting.save_report(content, failing_path)

    # Verifica que el mensaje de error se imprimio en stderr
    captured = capsys.readouterr()

    assert "Error al escribir archivo" in captured.err

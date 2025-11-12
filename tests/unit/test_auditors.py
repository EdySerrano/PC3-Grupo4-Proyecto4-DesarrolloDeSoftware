import pytest
from audit_cli import auditors

MOCK_SUCCESS_OUTPUT = """
Protocol  : TLSv1.2
Cipher    : ECDHE-RSA-AES256-GCM-SHA384
"""

MOCK_REFUSED_OUTPUT = "connect:errno=111 Connection refused"
MOCK_TIMEOUT_EXCEPTION = TimeoutError("Comando openssl timed out")


@pytest.mark.parametrize(
    "stub_simulation, expected_status, expected_details_fragment",
    [
        (MOCK_SUCCESS_OUTPUT, "OK", "TLSv1.2 detectado"),
        (MOCK_REFUSED_OUTPUT, "ERROR", "Conexion rechazada"),
        (MOCK_TIMEOUT_EXCEPTION, "ERROR", "timed out"),
        ("some other random output", "FAIL", "no detectado"),
    ],
)
def test_check_tls_parametrized(
    monkeypatch, stub_simulation, expected_status, expected_details_fragment
):
    def mock_run_openssl(host: str, port: int) -> str:
        if isinstance(stub_simulation, Exception):
            raise stub_simulation
        return stub_simulation

    monkeypatch.setattr(auditors.runners, "run_openssl_s_client", mock_run_openssl)

    result = auditors.check_tls_version("fake-host.com", 443)

    assert result["status"] == expected_status
    assert expected_details_fragment in result["details"]
    assert result["host"] == "fake-host.com"


def test_check_tls_handles_unknown_exception(monkeypatch):
    def raise_value_error(host: str, port: int) -> str:
        raise ValueError("error")

    monkeypatch.setattr(auditors.runners, "run_openssl_s_client", raise_value_error)

    result = auditors.check_tls_version("fake-host.com", 443)

    assert result["status"] == "ERROR"
    assert "Unknown error" in result["details"]
    assert "error" in result["details"]

import subprocess
import pytest
from audit_cli import runners

def test_run_openssl_success(monkeypatch):
    def fake_run(args, capture_output, text, timeout, check):
        # comprueba que el comando se construye correctamente
        assert any("-tls1_2" in token or "tls1_2" in token for token in args) 
        # simula una ejecucion exitosa
        return subprocess.CompletedProcess(args, 0, stdout="REAL STDOUT", stderr="")
    monkeypatch.setattr(subprocess, "run", fake_run)
    out = runners.run_openssl_s_client("host.test", 443)
    assert out == "REAL STDOUT"
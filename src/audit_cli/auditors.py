import datetime

from . import runners
from .models import AuditResult  # Importamos nuestro contrato


def check_tls_version(host: str, port: int = 443) -> AuditResult:
    """
    Lógica de auditoría para verificar TLS.
    AHORA retorna un diccionario que cumple el contrato AuditResult.
    """

    # Función para generar el timestamp
    def get_timestamp() -> str:
        return datetime.datetime.utcnow().isoformat() + "Z"

    # Función para construir la respuesta
    def build_response(status: str, details: str) -> AuditResult:
        return {
            "host": host,
            "port": port,
            "check_type": "tls_version",
            "status": status,
            "details": details,
            "timestamp_utc": get_timestamp(),
        }

    try:
        output = runners.run_openssl_s_client(host, port)

        if "TLSv1.2" in output and "Cipher" in output:
            return build_response("OK", "TLSv1.2 detectado")

        if "Connection refused" in output:
            return build_response("ERROR", "Conexion rechazada")

        return build_response("FAIL", "TLSv1.2 no detectado o handshake fallido")

    except TimeoutError as e:
        return build_response("ERROR", str(e))
    except Exception as e:
        return build_response("ERROR", f"Unknown error: {e}")

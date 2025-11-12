from typing import Literal, TypedDict


# Este TypedDict es el "Contrato de Salida"
# Define la estructura que todas las auditorías van a retornar.
class AuditResult(TypedDict):
    host: str
    port: int
    check_type: Literal["tls_version"]
    status: Literal["OK", "FAIL", "ERROR"]
    details: str
    timestamp_utc: str

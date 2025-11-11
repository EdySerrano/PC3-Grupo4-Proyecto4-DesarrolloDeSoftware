from typing import Literal, TypedDict


# Este TypedDict ES el "Contrato de Salida"
# Define la estructura que todas las auditorías DEBEN retornar.
class AuditResult(TypedDict):
    host: str
    port: int
    check_type: Literal["tls_version"]  # Literal nos ayuda a forzar valores
    status: Literal["OK", "FAIL", "ERROR"]
    details: str
    timestamp_utc: str

import csv
import json
import sys
from io import StringIO
from typing import List

from .models import AuditResult  # Importamos nuestro contrato


def results_to_json(results: List[AuditResult]) -> str:
    """Convierte una lista de resultados de auditoría a una cadena JSON."""
    return json.dumps(results, indent=2)


def results_to_csv(results: List[AuditResult]) -> str:
    """Convierte una lista de resultados de auditoría a una cadena CSV."""
    if not results:
        return ""  # Retorna vacío si no hay resultados

    # Usamos StringIO para escribir el CSV en memoria (como cadena)
    output = StringIO()

    # Los encabezados del CSV vienen de las llaves de nuestro contrato
    fieldnames = AuditResult.__annotations__.keys()

    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

    return output.getvalue()

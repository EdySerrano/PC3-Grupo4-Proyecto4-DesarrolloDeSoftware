import csv
import json
import sys
from io import StringIO
from typing import List

from .models import AuditResult  # Importamos nuestro contrato


def results_to_json(results: List[AuditResult]) -> str:
    """Convierte una lista de resultados de auditoría a una cadena JSON."""
    return json.dumps(results, indent=2)

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


def save_report(content: str, output_file: str = None):
    """
    Guarda el contenido del reporte en un archivo o lo imprime en consola.
    """
    if output_file:
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Reporte guardado en: {output_file}", file=sys.stderr)
        except IOError as e:
            print(f"Error al escribir archivo: {e}", file=sys.stderr)
    else:
        # Si no hay --output, imprime el reporte a stdout
        print(content)

import click

from . import (
    auditors,
    reporting,  # Importamos el nuevo modulo de reportes
)


@click.group()
def cli():
    """Herramienta Audit-CLI para auditorías de seguridad."""
    pass


@cli.command()
@click.argument("host")
@click.option("--port", default=443, help="Puerto a escanear.")
@click.option(
    "--format",
    "output_format",  # La variable se llamará 'output_format'
    type=click.Choice(["json", "csv", "console"], case_sensitive=False),
    default="console",
    help="Formato de salida.",
)
@click.option(
    "--output",
    "output_file",  # La variable se llamará 'output_file'
    type=click.Path(dir_okay=False, writable=True),
    default=None,
    help="Archivo de salida. Si no se especifica, se imprime en consola.",
)
def check_tls(host: str, port: int, output_format: str, output_file: str):
    """
    Ejecuta una auditoría de versión mínima de TLS.
    """
    if output_format != "console":
        # Modo reporte
        result = auditors.check_tls_version(host, port)

        # Por ahora solo tenemos un resultado y lo ponemos en una lista
        results_list = [result]

        report_content = ""
        if output_format == "json":
            report_content = reporting.results_to_json(results_list)
        elif output_format == "csv":
            report_content = reporting.results_to_csv(results_list)

        reporting.save_report(report_content, output_file)

    else:
        # Modo consola
        click.echo(f"Auditando TLS en {host}:{port}...")
        result = auditors.check_tls_version(host, port)
        # Imprime en consola
        click.echo(f"  Host: {result['host']}:{result['port']}")
        click.echo(f"  Status: {result['status']}")
        click.echo(f"  Details: {result['details']}")


if __name__ == "__main__":
    cli()

import click
import json
from . import auditors

@click.group()
def cli():
    """Herramienta Audit-CLI para auditoria de seguridad"""
    pass

@cli.command()
@click.argument("host")
@click.option("--port", default=443, help="Puerto a escanear.")
def check_tls(host: str, port: int):
    click.echo(f"Auditando TLS en {host}:{port}...")
    result = auditors.check_tls_version(host, port)

    # Imprimir resultado
    click.echo(json.dumps(result, indent=2))

if __name__ == "__main__":
    cli()

import subprocess
import shlex

def run_openssl_s_client(host: str, port: int) -> str:
    """
    Ejecuta el comando 'openssl s_client' real.
    Esta es la funcion que vamos a reemplazar (stub) en los tests.
    """
    cmd = f"openssl s_client -connect {host}:{port} -tls1_2"

    result = subprocess.run(
        shlex.split(cmd),
        capture_output=True,
        text=True
    )
    return result.stdout

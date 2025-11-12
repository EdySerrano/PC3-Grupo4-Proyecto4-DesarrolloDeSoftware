import shlex
import subprocess


def run_openssl_s_client(host: str, port: int) -> str:
    """
    Ejecuta el comando 'openssl s_client' real.
    Esta es la función que se va a reemplazar (stub) en los tests.
    """
    cmd = f"openssl s_client -connect {host}:{port} -tls1_2"

    try:
        result = subprocess.run(
            shlex.split(cmd),
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
            input=""
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        raise TimeoutError(f"Comando openssl timed out para {host}:{port}")
    except subprocess.CalledProcessError as e:
        return e.stderr
    except FileNotFoundError:
        return "ERROR: 'openssl' binary no encontrado."

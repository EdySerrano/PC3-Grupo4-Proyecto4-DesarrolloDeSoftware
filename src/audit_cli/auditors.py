from . import runners

def check_tls_version(host: str, port: int = 443) -> dict:

    try:
        # Delegamos llamada al runner
        output = runners.run_openssl_s_client(host, port)
        
        if "TLSv1.2" in output and "Cipher" in output:
            return {"host": host, "status": "OK", "details": "TLSv1.2 detectado"}
        if "Connection refused" in output:
            return {"host": host, "status": "ERROR", "details": "Conexion rechazada"}

        return {"host": host, "status": "FAIL", "details": "TLSv1.2 no detectado o handshake fallido"}

    except TimeoutError as e:
        return {"host": host, "status": "ERROR", "details": str(e)}
    except Exception as e:
        return {"host": host, "status": "ERROR", "details": f"Unknown error: {e}"}
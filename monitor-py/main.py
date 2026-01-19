import ssl
import socket
from datetime import datetime

def get_ssl_info(host: str, port: int = 443):
    context = ssl.create_default_context()

    with socket.create_connection((host, port), timeout=5) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            cert = ssock.getpeercert()

    not_before = datetime.strptime(cert['notBefore'], "%b %d %H:%M:%S %Y %Z")
    not_after = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")

    return {
        "host": host,
        "valid_from": not_before.isoformat(),
        "valid_until": not_after.isoformat(),
        "days_remaining": (not_after - datetime.utcnow()).days,
        "issuer": dict(x[0] for x in cert['issuer']),
        "subject": dict(x[0] for x in cert['subject'])
    }
print(get_ssl_info('wilsonnascimentocosta.com.br'))
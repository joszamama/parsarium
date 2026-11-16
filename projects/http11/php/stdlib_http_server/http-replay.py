"""Feed local HTTP bytes through PHP's built-in server on loopback."""

import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
import time


def parse_http(path: Path) -> dict:
    raw = path.read_bytes()
    if not raw or len(raw) > 1 << 20:
        return {}
    with socket.socket() as reservation:
        reservation.bind(('127.0.0.1', 0))
        port = reservation.getsockname()[1]
    server = subprocess.Popen(
        ['/opt/php/bin/php', '-S', f'127.0.0.1:{port}', '/work/router.php'],
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, env=os.environ.copy(),
    )
    try:
        deadline = time.monotonic() + 5
        while True:
            if server.poll() is not None:
                raise RuntimeError(f'PHP server exited before request: {server.stderr.read()[-1000:]}')
            try:
                client = socket.create_connection(('127.0.0.1', port), timeout=2)
                break
            except OSError:
                if time.monotonic() >= deadline:
                    raise RuntimeError('PHP server did not start')
                time.sleep(0.02)
        with client:
            client.settimeout(5)
            client.sendall(raw)
            client.shutdown(socket.SHUT_WR)
            chunks = []
            while True:
                chunk = client.recv(65536)
                if not chunk:
                    break
                chunks.append(chunk)
        response = b''.join(chunks)
        if b'\r\n\r\n' not in response:
            return {}
        body = response.split(b'\r\n\r\n', 1)[1]
        try:
            parsed = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return {}
        return parsed if isinstance(parsed, dict) else {}
    finally:
        if server.poll() is None:
            server.send_signal(signal.SIGINT)
        try:
            server.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
            server.communicate()


if __name__ == '__main__':
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if input_path is None:
        raise SystemExit('HTTP file path required')
    print(json.dumps(parse_http(input_path)))

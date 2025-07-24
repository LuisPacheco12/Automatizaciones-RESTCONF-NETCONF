
import http.server
import socketserver

PORT = 8000
DIRECTORY = "/home/developer"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"[+] Sirviendo 'metricas_red.db' en http://localhost:{PORT}/metricas_red.db")
    httpd.serve_forever()

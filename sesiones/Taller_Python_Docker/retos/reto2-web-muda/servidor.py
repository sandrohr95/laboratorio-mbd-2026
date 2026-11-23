"""Un servidor web mínimo que responde con un saludo."""
from http.server import BaseHTTPRequestHandler, HTTPServer


class Saludo(BaseHTTPRequestHandler):
    def do_GET(self):
        cuerpo = "<h1>Hola desde el contenedor</h1>".encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(cuerpo)


if __name__ == "__main__":
    print("Escuchando en el puerto 8000...", flush=True)
    HTTPServer(("127.0.0.1", 8000), Saludo).serve_forever()

"""API mínima con Flask: un saludo y la información del entorno en el que se ejecuta."""
import os
import platform
import socket

from flask import Flask

app = Flask(__name__)


@app.get("/")
def inicio():
    nombre = os.environ.get("NOMBRE", "mundo")
    return {"mensaje": f"Hola, {nombre}", "python": platform.python_version()}


@app.get("/info")
def info():
    return {
        "sistema": platform.system(),
        "contenedor": socket.gethostname(),
        "en_docker": os.path.exists("/.dockerenv"),
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

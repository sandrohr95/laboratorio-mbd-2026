# Chuleta · Taller práctico de Python y Docker

## Entornos virtuales

| Qué hago | bash / zsh | PowerShell |
|---|---|---|
| Crear el entorno en la carpeta actual | `python3 -m venv .venv` | `python -m venv .venv` |
| Activarlo | `source .venv/bin/activate` | `.venv\Scripts\Activate.ps1` |
| Instalar dependencias (con el entorno activado) | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| ¿Qué Python estoy usando? | `which python` | `Get-Command python` |
| Desactivarlo | `deactivate` | `deactivate` |
| Variable de entorno para un solo comando | `AUTOR="Ana" python informe.py` | `$env:AUTOR = "Ana"; python informe.py` |

Con el entorno activado, el *prompt* empieza por `(.venv)`.

## Python: clases en un vistazo

```python
from dataclasses import dataclass, field
from enum import StrEnum

class Formato(StrEnum):
    CSV = "csv"

@dataclass(frozen=True)              # inmutable: se puede meter en un set
class Ficha:
    id: str
    filas: int
    etiquetas: tuple[str, ...] = ()  # los campos con valor por defecto, al final

    def __post_init__(self):         # validar
        if self.filas < 0:
            raise ValueError("filas negativas")

    @property
    def es_grande(self):             # se usa sin paréntesis: f.es_grande
        return self.filas >= 100_000

    @classmethod
    def desde_dict(cls, d):          # constructor alternativo
        return cls(d["id"], int(d["filas"]), tuple(d.get("etiquetas", [])))

class Coleccion:
    def __init__(self):
        self._fichas = {}            # las colecciones, SIEMPRE en __init__
    def __len__(self):               # len(c)
        return len(self._fichas)
    def __iter__(self):              # for f in c
        return iter(self._fichas.values())
    def __contains__(self, id):      # "x" in c
        return id in self._fichas
```

## Dockerfile

| Instrucción | Para qué |
|---|---|
| `FROM imagen:etiqueta` | Imagen de partida |
| `WORKDIR /ruta` | Carpeta de trabajo dentro de la imagen (la crea si no existe) |
| `COPY origen destino` | Copia archivos de tu carpeta a la imagen. `COPY a.py b.py ./` copia varios |
| `RUN comando` | Ejecuta un comando **al construir** (instalar dependencias) |
| `ENV CLAVE=valor` | Variable de entorno con un valor por defecto |
| `CMD ["programa", "arg"]` | Lo que se ejecuta **al arrancar** el contenedor |

**Orden para aprovechar la caché:** primero lo que menos cambia (imagen base, dependencias) y al final lo que más cambia (tu código).

**`.dockerignore`:** una ruta o patrón por línea. Lo que aparece aquí no se envía a `docker build`, así que ningún `COPY` lo puede copiar.

```text
.venv/
__pycache__/
```

## Comandos de Docker

| Qué hago | Comando |
|---|---|
| Descargar una imagen | `docker pull python:3.13-slim` |
| Construir una imagen con la carpeta actual | `docker build -t nombre:etiqueta .` |
| Listar imágenes | `docker image ls` |
| Ejecutar un contenedor | `docker run [opciones] imagen [comando]` |
| Contenedores en marcha / todos | `docker ps` · `docker ps -a` |
| Ejecutar algo en un contenedor en marcha | `docker exec -it nombre comando` |
| Parar / borrar un contenedor | `docker stop nombre` · `docker rm nombre` |
| Ver la salida de un contenedor | `docker logs nombre` |

## Opciones de `docker run`

| Opción | Qué hace |
|---|---|
| `--rm` | Borra el contenedor al terminar |
| `--name web` | Le da un nombre |
| `-d` | Lo ejecuta en segundo plano |
| `-it` | Modo interactivo, con terminal |
| `-e CLAVE=valor` | Variable de entorno dentro del contenedor |
| `-p 8080:80` | Publica un puerto: `ordenador:contenedor` |
| `-v "ruta_ordenador:ruta_contenedor"` | Monta una carpeta de tu ordenador (*bind mount*) |
| `-v "...:...:ro"` | La monta en solo lectura |

La ruta del ordenador en `-v` tiene que ser **absoluta**: usa `"$(pwd)/carpeta"` en bash/zsh y `"${PWD}/carpeta"` en PowerShell, siempre **entre comillas**.

Lo que va **después** del nombre de la imagen sustituye al `CMD`: `docker run --rm imagen python --version`.

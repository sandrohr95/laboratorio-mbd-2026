"""Comprueba la práctica «El catálogo en un contenedor».

Ejecútalo en tu ordenador (no dentro del contenedor), desde tu carpeta catalogo-datasets:
    python3 comprobar_docker.py        (en Windows: python comprobar_docker.py)

Puedes ejecutarlo tantas veces como quieras: después de cada parte, las
comprobaciones de esa parte deberían pasar a [OK].
"""
import json
import re
import shutil
import subprocess
from pathlib import Path

IMAGEN = "catalogo:1.0"
DATASETS = 26
DESCARTADOS = 4
BUSQUEDA_AIRE = {"calidad-aire-horaria", "calidad-aire-diaria", "zonas-juego"}

aciertos = 0
total = 0


def comprobar(descripcion: str, ok: bool, pista: str = "") -> bool:
    global aciertos, total
    total += 1
    aciertos += ok
    print(f"  [{'OK' if ok else '  '}] {descripcion}")
    if not ok and pista:
        print(f"         Pista: {pista}")
    return ok


def instrucciones(dockerfile: str) -> list[tuple[str, str]]:
    """Devuelve las instrucciones del Dockerfile como (INSTRUCCIÓN, argumentos), sin comentarios."""
    resultado = []
    for linea in dockerfile.splitlines():
        linea = linea.strip()
        if linea and not linea.startswith("#"):
            partes = linea.split(maxsplit=1)
            resultado.append((partes[0].upper(), partes[1] if len(partes) > 1 else ""))
    return resultado


def docker(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["docker", *args], capture_output=True, text=True, encoding="utf-8")


if not Path("catalogo.py").is_file() or not Path("informe.py").is_file():
    raise SystemExit("\nEjecuta comprobar_docker.py desde tu carpeta catalogo-datasets, "
                     "junto a catalogo.py e informe.py.")

print("\nParte A · En tu ordenador")
venv = Path(".venv")
comprobar("Hay un entorno virtual .venv en la carpeta", (venv / "pyvenv.cfg").is_file(),
          "créalo con: python3 -m venv .venv  (en Windows: python -m venv .venv)")
rich_en_venv = any(venv.glob("lib/python3*/site-packages/rich")) or (venv / "Lib/site-packages/rich").is_dir()
comprobar("rich está instalado en ese entorno virtual", rich_en_venv,
          "activa el entorno y ejecuta: pip install -r requirements.txt")
try:
    from catalogo import Catalogo
    cat = Catalogo.desde_json("datos/datasets.json")
    catalogo_ok = len(cat) == DATASETS and cat.descartados == DESCARTADOS
except Exception:
    catalogo_ok = False
comprobar(f"Tu catalogo.py carga {DATASETS} datasets y descarta {DESCARTADOS}", catalogo_ok,
          "termina catalogo.py (comprobar.py debe dar 26 de 26) o pide la versión resuelta")

print("\nParte B · El Dockerfile y el .dockerignore")
ruta = Path("Dockerfile")
if comprobar("Existe un archivo llamado Dockerfile", ruta.is_file(),
             "créalo en la carpeta catalogo-datasets, sin extensión (ni .txt ni .docker)"):
    pasos = instrucciones(ruta.read_text(encoding="utf-8"))
    nombres = [p[0] for p in pasos]
    desde = next((arg for ins, arg in pasos if ins == "FROM"), "")
    comprobar("Parte de una imagen oficial de Python 3.13", bool(re.match(r"python:3\.13", desde)),
              "usa FROM python:3.13-slim")
    comprobar("Fija la carpeta de trabajo con WORKDIR", "WORKDIR" in nombres)
    i_req = next((i for i, (ins, arg) in enumerate(pasos) if ins == "COPY" and "requirements" in arg), None)
    i_pip = next((i for i, (ins, arg) in enumerate(pasos)
                  if ins == "RUN" and "pip install" in arg and "-r" in arg), None)
    i_cod = next((i for i, (ins, arg) in enumerate(pasos) if ins == "COPY"
                  and ("informe.py" in arg or "catalogo.py" in arg or arg.split()[0] in (".", "./"))), None)
    comprobar("Instala las dependencias con RUN pip install -r requirements.txt", i_pip is not None)
    comprobar("Copia requirements.txt e instala antes de copiar el código (aprovecha la caché)",
              None not in (i_req, i_pip, i_cod) and i_req < i_pip < i_cod,
              "primero COPY requirements.txt y RUN pip install; después COPY del código")
    arranque = " ".join(arg for ins, arg in pasos if ins in ("CMD", "ENTRYPOINT"))
    comprobar("Arranca ejecutando informe.py", "informe.py" in arranque,
              'termina con CMD ["python", "informe.py"]')
ignorar = Path(".dockerignore")
lineas = ignorar.read_text(encoding="utf-8").split() if ignorar.is_file() else []
comprobar("Hay un .dockerignore que excluye el entorno virtual",
          any(l.strip("/") == ".venv" for l in lineas),
          "crea .dockerignore (con el punto delante) y añade una línea .venv/")

print("\nParte C · La imagen")
if not shutil.which("docker"):
    comprobar("Docker está disponible en la terminal", False, "abre Docker Desktop y vuelve a probar")
elif comprobar(f"Existe la imagen {IMAGEN}", docker("image", "inspect", IMAGEN).returncode == 0,
               f"constrúyela con: docker build -t {IMAGEN} .  (¿está Docker Desktop abierto?)"):
    r = docker("run", "--rm", "--entrypoint", "python", IMAGEN, "-c",
               "import sys, rich; print(sys.version_info[0], sys.version_info[1])")
    comprobar("La imagen tiene Python 3.13 y rich instalado", r.stdout.split() == ["3", "13"],
              "revisa el FROM y el RUN pip install")
    contenido = docker("run", "--rm", "--entrypoint", "ls", IMAGEN, "-A").stdout.split()
    comprobar("La imagen contiene tu código (catalogo.py e informe.py)",
              {"catalogo.py", "informe.py"} <= set(contenido))
    sobra = sorted({".venv", "datos", "salida"} & set(contenido))
    comprobar("La imagen NO contiene .venv, datos ni salida", not sobra,
              f"sobra {', '.join(sobra)}: añádelo al .dockerignore o copia solo los .py, "
              "y vuelve a construir la imagen")

print("\nParte D · La ejecución")
ruta = Path("salida/informe.json")
if comprobar("Existe salida/informe.json en tu ordenador", ruta.is_file(),
             "ejecuta informe.py (primero en tu ordenador, después en el contenedor)"):
    r = json.loads(ruta.read_text(encoding="utf-8"))
    if comprobar("Se ha generado dentro de un contenedor", r.get("en_docker") is True,
                 "el informe actual es el de tu ordenador: ahora ejecútalo con docker run, "
                 "montando la carpeta salida con -v para que el resultado salga del contenedor"):
        comprobar("Con Python 3.13 (la versión de la imagen)", str(r.get("python", "")).startswith("3.13"))
        comprobar("Lleva tu nombre (variable AUTOR)", bool(r.get("autor")), 'pásalo con -e AUTOR="Tu nombre"')
        comprobar("Ha leído los datos montados desde tu ordenador",
                  r.get("datasets") == DATASETS and r.get("descartados") == DESCARTADOS,
                  "monta tu carpeta datos en la carpeta de trabajo del contenedor con -v")
        comprobar("Los datos se han montado en solo lectura", r.get("datos_solo_lectura") is True,
                  "añade :ro al final del -v de la carpeta datos")
        busqueda = r.get("busqueda", {})
        comprobar("Ha buscado «aire» (variable BUSCAR) y ha encontrado 3 datasets",
                  busqueda.get("texto", "").lower() == "aire" and set(busqueda.get("resultados", [])) == BUSQUEDA_AIRE,
                  "pásalo con -e BUSCAR=aire")
        if len(r.get("mas_recientes", [])) == 3:
            print("  [++] Reto extra: has usado TOP=3")

print(f"\n{aciertos} de {total} comprobaciones correctas.")
if aciertos == total:
    print("¡Práctica completa! Tu catálogo funciona igual en cualquier ordenador con Docker.")

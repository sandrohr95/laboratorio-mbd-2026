"""Comprueba el ejercicio «Dockeriza el análisis de bicis».

Ejecútalo en tu ordenador (no dentro del contenedor), desde la carpeta bicis-docker:
    python3 comprobar.py        (en Windows: python comprobar.py)
"""
import json
import re
import shutil
import subprocess
from pathlib import Path

IMAGEN = "bicis-analisis:1.0"
TOP_ESPERADO = ["Alameda Principal", "Estación María Zambrano", "Plaza de la Merced",
                "Muelle Uno", "Paseo del Parque"]

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


print("\nParte A · El Dockerfile")
ruta = Path("Dockerfile")
if comprobar("Existe un archivo llamado Dockerfile", ruta.is_file(),
             "créalo en la carpeta bicis-docker, sin extensión (ni .txt ni .docker)"):
    pasos = instrucciones(ruta.read_text(encoding="utf-8"))
    nombres = [p[0] for p in pasos]
    desde = next((arg for ins, arg in pasos if ins == "FROM"), "")
    comprobar("Parte de una imagen oficial de Python 3.13", bool(re.match(r"python:3\.13", desde)),
              "usa FROM python:3.13-slim")
    comprobar("Fija la carpeta de trabajo con WORKDIR", "WORKDIR" in nombres)
    comprobar("Instala las dependencias con RUN pip install",
              any(ins == "RUN" and "pip install" in arg for ins, arg in pasos))
    comprobar("Arranca con CMD", "CMD" in nombres)
    copias = [arg for ins, arg in pasos if ins == "COPY"]
    i_req = next((i for i, a in enumerate(copias) if "requirements" in a), None)
    i_cod = next((i for i, a in enumerate(copias) if "analisis.py" in a or a.split()[0] == "."), None)
    comprobar("Copia requirements.txt antes que el código (aprovecha la caché)",
              i_req is not None and i_cod is not None and i_req < i_cod,
              "primero COPY requirements.txt y RUN pip install; después COPY analisis.py")
    comprobar("No mete los datos dentro de la imagen",
              not any("datos" in a for a in copias),
              "los datos se montan al ejecutar con -v, no se copian en la imagen")

print("\nParte B · La imagen")
if shutil.which("docker") is None:
    comprobar("Docker está disponible en la terminal", False, "abre Docker Desktop y vuelve a probar")
else:
    r = subprocess.run(["docker", "image", "inspect", IMAGEN], capture_output=True, text=True)
    comprobar(f"Existe la imagen {IMAGEN}", r.returncode == 0,
              f"constrúyela con: docker build -t {IMAGEN} .  (¿está Docker Desktop abierto?)")

print("\nParte C · La ejecución")
ruta = Path("salida/resumen.json")
if comprobar("Existe salida/resumen.json en tu ordenador", ruta.is_file(),
             "monta la carpeta salida con -v para que el resultado salga del contenedor"):
    r = json.loads(ruta.read_text(encoding="utf-8"))
    comprobar("Se ha generado dentro de un contenedor", r.get("en_docker") is True,
              "ejecútalo con docker run, no con python analisis.py")
    comprobar("Con Python 3.13 (la versión de la imagen)", str(r.get("python", "")).startswith("3.13"))
    comprobar("Lleva tu nombre (variable AUTOR)", bool(r.get("autor")),
              'pásalo con -e AUTOR="Tu nombre"')
    comprobar("Los resultados son correctos",
              r.get("viajes_validos") == 1940 and r.get("filas_descartadas") == 60
              and r.get("duracion_media") == 16.82,
              "¿has montado la carpeta datos completa?")
    top = r.get("top_origen", [])
    if len(top) == 5 and top == TOP_ESPERADO:
        print("  [++] Reto extra: has usado TOP=5")

print(f"\n{aciertos}/{total} comprobaciones superadas.")
if aciertos == total:
    print("Ejercicio completado. Tu análisis funciona igual en cualquier ordenador con Docker.")

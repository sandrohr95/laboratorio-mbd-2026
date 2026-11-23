"""Diagnóstico del entorno de Python.

Muestra qué Python se está ejecutando, si está dentro de un entorno virtual,
dónde se instalan sus paquetes y cuáles hay instalados.

Uso:
    python comprobar_entorno.py              # diagnóstico general
    python comprobar_entorno.py requests     # además, comprueba si se puede importar "requests"
"""
import importlib
import importlib.metadata
import os
import sys
import sysconfig


def titulo(texto):
    print(f"\n{texto}\n{'-' * len(texto)}")


def main():
    en_entorno = sys.prefix != sys.base_prefix

    titulo("Intérprete")
    print(f"Versión:     Python {sys.version.split()[0]}")
    print(f"Ejecutable:  {sys.executable}")

    titulo("Entorno virtual")
    if en_entorno:
        print("Estás DENTRO de un entorno virtual.")
        print(f"Carpeta del entorno:  {sys.prefix}")
        print(f"Python de origen:     {sys.base_prefix}")
    else:
        print("NO estás en un entorno virtual: es el Python del sistema.")
        print("Para trabajar en un proyecto, crea y activa un entorno (.venv).")
    activo = os.environ.get("VIRTUAL_ENV")
    if activo and os.path.normcase(os.path.realpath(activo)) != os.path.normcase(os.path.realpath(sys.prefix)):
        print(f"\nAVISO: la terminal tiene activado {activo},")
        print("pero este programa se está ejecutando con otro Python.")

    titulo("Dónde se instalan los paquetes")
    print(sysconfig.get_paths()["purelib"])

    titulo("Paquetes instalados")
    paquetes = sorted(
        (d.metadata["Name"], d.version) for d in importlib.metadata.distributions()
        if d.metadata["Name"]
    )
    for nombre, version in paquetes:
        print(f"  {nombre}=={version}")
    print(f"Total: {len(paquetes)}")

    for modulo in sys.argv[1:]:
        titulo(f"¿Se puede importar '{modulo}'?")
        try:
            m = importlib.import_module(modulo)
        except ModuleNotFoundError:
            print("NO. No está instalado en ESTE Python.")
            print(f"Instálalo con:  {sys.executable} -m pip install {modulo}")
        else:
            print(f"Sí. Versión: {getattr(m, '__version__', 'desconocida')}")
            print(f"Se carga desde: {getattr(m, '__file__', 'módulo interno')}")


if __name__ == "__main__":
    main()

"""Análisis del servicio de bicicletas de Málaga (datos simulados).

Lee datos/viajes.csv y datos/estaciones.json, muestra un resumen en una tabla
y lo guarda en salida/resumen.json.

Variables de entorno que acepta:
    AUTOR  nombre que se guarda en el resumen (obligatoria)
    TOP    cuántas estaciones de origen mostrar (por defecto, 3)
"""
import csv
import json
import os
import platform
import sys
from collections import Counter
from pathlib import Path

from tabulate import tabulate

DATOS = Path("datos")
SALIDA = Path("salida")


def cargar_estaciones() -> dict[int, str]:
    with open(DATOS / "estaciones.json", encoding="utf-8") as f:
        return {e["id"]: e["nombre"] for e in json.load(f)["estaciones"]}


def cargar_viajes(estaciones: dict[int, str]) -> tuple[list[dict], int]:
    validos, descartados = [], 0
    with open(DATOS / "viajes.csv", encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f):
            try:
                fila["duracion_min"] = float(fila["duracion_min"])
                fila["estacion_origen"] = int(fila["estacion_origen"])
            except (ValueError, TypeError):
                descartados += 1
                continue
            if fila["duracion_min"] <= 0 or fila["estacion_origen"] not in estaciones:
                descartados += 1
                continue
            validos.append(fila)
    return validos, descartados


def main() -> None:
    autor = os.environ.get("AUTOR", "").strip()
    if not autor:
        sys.exit("ERROR: falta la variable de entorno AUTOR (pásala con -e AUTOR=\"Tu nombre\")")
    top = int(os.environ.get("TOP", "3"))

    if not DATOS.is_dir():
        sys.exit(f"ERROR: no encuentro la carpeta {DATOS.resolve()}. ¿Has montado los datos con -v?")

    estaciones = cargar_estaciones()
    viajes, descartados = cargar_viajes(estaciones)
    origenes = Counter(estaciones[v["estacion_origen"]] for v in viajes)

    resumen = {
        "autor": autor,
        "viajes_validos": len(viajes),
        "filas_descartadas": descartados,
        "duracion_media": round(sum(v["duracion_min"] for v in viajes) / len(viajes), 2),
        "viajes_por_tipo": dict(Counter(v["tipo_usuario"] for v in viajes)),
        "top_origen": [nombre for nombre, _ in origenes.most_common(top)],
        "python": platform.python_version(),
        "en_docker": Path("/.dockerenv").exists(),
    }

    print(f"Análisis de {autor} · Python {resumen['python']}\n")
    print(tabulate(origenes.most_common(top), headers=["Estación de origen", "Viajes"]))
    print(f"\nViajes válidos: {resumen['viajes_validos']} · descartados: {descartados}")
    print(f"Duración media: {resumen['duracion_media']} min")

    SALIDA.mkdir(exist_ok=True)
    with open(SALIDA / "resumen.json", "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=2)
    print(f"\nResumen guardado en {SALIDA / 'resumen.json'}")


if __name__ == "__main__":
    main()

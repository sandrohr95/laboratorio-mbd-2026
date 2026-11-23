"""Informe del catálogo de datasets.

Carga datos/datasets.json con tu clase Catalogo (catalogo.py), muestra un
resumen en la terminal y lo guarda en salida/informe.json.

No tienes que modificar este archivo.

Variables de entorno que acepta:
    AUTOR   tu nombre, que se guarda en el informe (obligatoria)
    BUSCAR  texto que se busca en el catálogo (opcional)
    TOP     cuántos datasets recientes mostrar (por defecto, 5)
"""
import json
import os
import platform
import sys
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.table import Table

from catalogo import Catalogo

DATOS = Path("datos")
SALIDA = Path("salida")


def main() -> None:
    consola = Console()

    autor = os.environ.get("AUTOR", "").strip()
    if not autor:
        sys.exit('ERROR: falta la variable de entorno AUTOR (en Docker, pásala con -e AUTOR="Tu nombre")')
    buscar = os.environ.get("BUSCAR", "").strip()
    top = int(os.environ.get("TOP", "5"))

    if not (DATOS / "datasets.json").is_file():
        sys.exit(f"ERROR: no encuentro {(DATOS / 'datasets.json').resolve()}. "
                 "¿Estás en la carpeta correcta? En Docker, ¿has montado la carpeta datos con -v?")

    catalogo = Catalogo.desde_json(DATOS / "datasets.json", "Málaga")
    recientes = catalogo.mas_recientes(top)
    encontrados = catalogo.buscar(buscar) if buscar else []

    informe = {
        "autor": autor,
        "generado": datetime.now().isoformat(timespec="seconds"),
        "python": platform.python_version(),
        "en_docker": Path("/.dockerenv").exists(),
        "datos_solo_lectura": not os.access(DATOS, os.W_OK),
        "datasets": len(catalogo),
        "descartados": catalogo.descartados,
        "por_formato": catalogo.resumen(),
        "grandes": sorted(d.id for d in catalogo if d.es_grande),
        "mas_recientes": [d.id for d in recientes],
        "busqueda": {"texto": buscar, "resultados": [d.id for d in encontrados]},
    }

    lugar = "un contenedor" if informe["en_docker"] else "tu ordenador"
    consola.print(f"\n[bold]{catalogo!r}[/bold] · informe de {autor} en {lugar} (Python {informe['python']})")
    consola.print(f"Fichas descartadas: {catalogo.descartados} · por formato: {informe['por_formato']}\n")

    tabla = Table(title=f"Los {top} datasets actualizados más recientemente")
    tabla.add_column("Fecha")
    tabla.add_column("Título")
    tabla.add_column("Formato")
    tabla.add_column("Filas", justify="right")
    for d in recientes:
        tabla.add_row(d.actualizado.isoformat(), d.titulo, str(d.formato), f"{d.filas:,}".replace(",", "."))
    consola.print(tabla)

    if buscar:
        consola.print(f"\nBúsqueda «{buscar}»: {len(encontrados)} resultado(s)")
        for d in encontrados:
            consola.print(f"  - {d.titulo}")

    SALIDA.mkdir(exist_ok=True)
    with open(SALIDA / "informe.json", "w", encoding="utf-8") as f:
        json.dump(informe, f, ensure_ascii=False, indent=2)
    consola.print(f"\nInforme guardado en {SALIDA / 'informe.json'}")


if __name__ == "__main__":
    main()

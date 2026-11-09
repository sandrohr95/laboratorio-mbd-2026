"""Catálogo de datasets.

Modela las fichas de un catálogo de datos abiertos con clases:
  - Formato:  los formatos admitidos (Enum)
  - Dataset:  una ficha del catálogo (dataclass inmutable)
  - Catalogo: una colección de fichas que se puede recorrer, consultar y guardar

Completa las partes A a E en orden. Después de cada parte, ejecuta:
    python3 comprobar.py        (en Windows: python comprobar.py)
"""
import json
from collections import Counter
from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from pathlib import Path

UMBRAL_GRANDE = 100_000


# --------------------------------------------------------------------- Parte A
# 1. Completa el Enum Formato con cuatro miembros: CSV, JSON, GEOJSON y XLSX.
#    Su valor es el nombre en minúsculas: CSV = "csv".
class Formato(StrEnum):
    CSV = "csv"
    # ...


# 2. Convierte Dataset en una dataclass inmutable (frozen=True) con estos campos,
#    en este orden:
#       id: str, titulo: str, organismo: str, formato: Formato, filas: int,
#       actualizado: date, etiquetas: tuple[str, ...] = ()
# 3. Añade __post_init__: lanza ValueError si el id está vacío o si filas es negativo.
# 4. Añade la propiedad es_grande: True si filas >= UMBRAL_GRANDE.
class Dataset:
    ...

    # ----------------------------------------------------------------- Parte B
    # 5. Método de clase desde_dict(cls, d): crea un Dataset a partir de un diccionario
    #    como los de datos/datasets.json. Convierte cada valor a su tipo:
    #    Formato(d["formato"]), date.fromisoformat(...), tuple(...).
    #    Si la ficha no trae etiquetas, usa una tupla vacía.
    # 6. Método a_dict(self): lo contrario. Devuelve un diccionario que se pueda
    #    guardar en JSON: el formato como str, la fecha en formato ISO y las etiquetas como lista.


# --------------------------------------------------------------------- Parte C
# 7. Crea la excepción DatasetDuplicado, que hereda de Exception.


class Catalogo:
    def __init__(self, nombre: str):
        # 8. Guarda el nombre, un diccionario vacío self._datasets (id → Dataset)
        #    y un contador self.descartados = 0.
        ...

    # 9. agregar(self, dataset): lo añade al diccionario. Si el id ya existe,
    #    lanza DatasetDuplicado.

    # 10. Métodos especiales:
    #     __len__        → número de datasets
    #     __iter__       → recorre los Dataset (no los ids)
    #     __contains__   → "paradas-emt" in catalogo
    #     __getitem__    → catalogo["paradas-emt"] devuelve el Dataset
    #     __repr__       → Catalogo('Datos abiertos', 26 datasets)

    # ----------------------------------------------------------------- Parte D
    # 11. buscar(self, texto): lista de Dataset cuyo título o alguna etiqueta contiene
    #     el texto, sin distinguir mayúsculas de minúsculas.
    # 12. por_formato(self, formato): lista de Dataset con ese formato.
    # 13. mas_recientes(self, n=5): los n Dataset actualizados más recientemente,
    #     del más nuevo al más antiguo.
    # 14. resumen(self): diccionario {formato: número de datasets}, con las claves
    #     como str y ordenadas alfabéticamente: {"csv": ..., "geojson": ..., ...}

    # ----------------------------------------------------------------- Parte E
    # 15. Método de clase desde_json(cls, ruta, nombre="Catálogo"): crea un catálogo,
    #     lee el JSON y añade cada ficha con Dataset.desde_dict(). Las fichas con
    #     errores lanzan KeyError o ValueError: captúralas, no las añadas y súmalas
    #     en descartados.
    # 16. guardar_json(self, ruta): guarda todos los datasets (con a_dict) en un JSON.
    #     Crea la carpeta de destino si no existe.


if __name__ == "__main__":
    catalogo = Catalogo.desde_json("datos/datasets.json", "Málaga")
    print(catalogo, "·", catalogo.descartados, "fichas descartadas")
    print(catalogo.resumen())
    for d in catalogo.mas_recientes(3):
        print(f"  {d.actualizado}  {d.titulo}")

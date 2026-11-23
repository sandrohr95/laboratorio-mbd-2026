"""Catálogo de datasets.

Modela las fichas de un catálogo de datos abiertos con clases:
  - Formato:  los formatos admitidos (Enum)
  - Dataset:  una ficha del catálogo (dataclass inmutable)
  - Catalogo: una colección de fichas que se puede recorrer, consultar y guardar

Lee ENUNCIADO.md antes de empezar: explica cada TODO con ejemplos.
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


# ===================================================================== Parte A
class Formato(StrEnum):
    """Formatos de archivo admitidos en el catálogo."""
    CSV = "csv"
    # TODO 1: añade los miembros JSON, GEOJSON y XLSX, con su nombre en minúsculas como valor


# TODO 2: convierte Dataset en una dataclass inmutable con @dataclass(frozen=True)
class Dataset:
    """Una ficha del catálogo. Cada campo corresponde a una clave del JSON."""

    # TODO 2: declara los campos con su tipo, en este orden:
    #   id: str
    #   titulo: str
    #   organismo: str
    #   formato: Formato            ¡un Formato, no un str!
    #   filas: int
    #   actualizado: date           ¡un date, no un str!
    #   etiquetas: tuple[str, ...] = ()

    def __post_init__(self):
        """Se ejecuta justo después del __init__ que genera la dataclass."""
        # TODO 3: lanza ValueError si el id está vacío o si filas es negativo
        pass

    @property
    def es_grande(self) -> bool:
        """True si el dataset tiene UMBRAL_GRANDE filas o más."""
        raise NotImplementedError("TODO 4")

    # ================================================================= Parte B
    @classmethod
    def desde_dict(cls, d: dict) -> "Dataset":
        """Crea un Dataset a partir de una ficha del JSON, convirtiendo cada valor a su tipo.

        No captures errores aquí: si la ficha está mal, deja que salte el KeyError o el ValueError.
        """
        raise NotImplementedError("TODO 5")

    def a_dict(self) -> dict:
        """Devuelve la ficha como un diccionario que se puede guardar en JSON."""
        raise NotImplementedError("TODO 6")


# ===================================================================== Parte C
# TODO 7: crea la excepción DatasetDuplicado, una clase que hereda de Exception


class Catalogo:
    """Un catálogo de datasets: los guarda por su id y permite consultarlos."""

    def __init__(self, nombre: str):
        # TODO 8: guarda el nombre, un diccionario vacío self._datasets (id → Dataset)
        #         y el contador self.descartados = 0
        raise NotImplementedError("TODO 8")

    def agregar(self, dataset: Dataset) -> None:
        """Añade un dataset. Si su id ya existe, lanza DatasetDuplicado."""
        raise NotImplementedError("TODO 9")

    # TODO 10: los métodos especiales
    def __len__(self) -> int:
        """len(catalogo): el número de datasets."""
        raise NotImplementedError("TODO 10")

    def __iter__(self):
        """for d in catalogo: recorre los Dataset (no los ids)."""
        raise NotImplementedError("TODO 10")

    def __contains__(self, id_dataset: str) -> bool:
        """id in catalogo: True si hay un dataset con ese id."""
        raise NotImplementedError("TODO 10")

    def __getitem__(self, id_dataset: str) -> Dataset:
        """catalogo["paradas-emt"]: el Dataset con ese id."""
        raise NotImplementedError("TODO 10")

    def __repr__(self) -> str:
        """Catalogo('Prueba', 2 datasets)"""
        raise NotImplementedError("TODO 10")

    # ================================================================= Parte D
    def buscar(self, texto: str) -> list[Dataset]:
        """Datasets cuyo título o alguna etiqueta contienen el texto, sin distinguir mayúsculas."""
        raise NotImplementedError("TODO 11")

    def por_formato(self, formato: Formato) -> list[Dataset]:
        """Datasets con ese formato."""
        raise NotImplementedError("TODO 12")

    def mas_recientes(self, n: int = 5) -> list[Dataset]:
        """Los n datasets actualizados más recientemente, del más nuevo al más antiguo."""
        raise NotImplementedError("TODO 13")

    def resumen(self) -> dict[str, int]:
        """{formato: número de datasets}, con las claves como texto y ordenadas alfabéticamente."""
        raise NotImplementedError("TODO 14")

    # ================================================================= Parte E
    @classmethod
    def desde_json(cls, ruta: str | Path, nombre: str = "Catálogo") -> "Catalogo":
        """Crea un catálogo a partir de un JSON. Descarta las fichas con errores y las cuenta."""
        raise NotImplementedError("TODO 15")

    def guardar_json(self, ruta: str | Path) -> None:
        """Guarda todos los datasets en un JSON, creando la carpeta de destino si no existe."""
        raise NotImplementedError("TODO 16")


if __name__ == "__main__":
    catalogo = Catalogo.desde_json("datos/datasets.json", "Málaga")
    print(catalogo, "·", catalogo.descartados, "fichas descartadas")
    print(catalogo.resumen())
    for d in catalogo.mas_recientes(3):
        print(f"  {d.actualizado}  {d.titulo}")

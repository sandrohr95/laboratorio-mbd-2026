"""Catálogo de datasets.

Modela las fichas de un catálogo de datos abiertos con clases:
  - Formato:  los formatos admitidos (Enum)
  - Dataset:  una ficha del catálogo (dataclass inmutable)
  - Catalogo: una colección de fichas que se puede recorrer, consultar y guardar
"""
import json
from collections import Counter
from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from pathlib import Path

UMBRAL_GRANDE = 100_000


# --------------------------------------------------------------------- Parte A
class Formato(StrEnum):
    CSV = "csv"
    JSON = "json"
    GEOJSON = "geojson"
    XLSX = "xlsx"


@dataclass(frozen=True)
class Dataset:
    id: str
    titulo: str
    organismo: str
    formato: Formato
    filas: int
    actualizado: date
    etiquetas: tuple[str, ...] = ()

    def __post_init__(self):
        if not self.id:
            raise ValueError("El id no puede estar vacío")
        if self.filas < 0:
            raise ValueError(f"{self.id}: el número de filas no puede ser negativo ({self.filas})")

    @property
    def es_grande(self) -> bool:
        return self.filas >= UMBRAL_GRANDE

    # ----------------------------------------------------------------- Parte B
    @classmethod
    def desde_dict(cls, d: dict) -> "Dataset":
        return cls(
            id=d["id"],
            titulo=d["titulo"],
            organismo=d["organismo"],
            formato=Formato(d["formato"]),
            filas=int(d["filas"]),
            actualizado=date.fromisoformat(d["actualizado"]),
            etiquetas=tuple(d.get("etiquetas", [])),
        )

    def a_dict(self) -> dict:
        return {
            "id": self.id,
            "titulo": self.titulo,
            "organismo": self.organismo,
            "formato": str(self.formato),
            "filas": self.filas,
            "actualizado": self.actualizado.isoformat(),
            "etiquetas": list(self.etiquetas),
        }


# --------------------------------------------------------------------- Parte C
class DatasetDuplicado(Exception):
    """Se intenta añadir un dataset cuyo id ya está en el catálogo."""


class Catalogo:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self._datasets: dict[str, Dataset] = {}
        self.descartados = 0

    def agregar(self, dataset: Dataset) -> None:
        if dataset.id in self._datasets:
            raise DatasetDuplicado(dataset.id)
        self._datasets[dataset.id] = dataset

    def __len__(self) -> int:
        return len(self._datasets)

    def __iter__(self):
        return iter(self._datasets.values())

    def __contains__(self, id_dataset: str) -> bool:
        return id_dataset in self._datasets

    def __getitem__(self, id_dataset: str) -> Dataset:
        return self._datasets[id_dataset]

    def __repr__(self) -> str:
        return f"Catalogo({self.nombre!r}, {len(self)} datasets)"

    # ----------------------------------------------------------------- Parte D
    def buscar(self, texto: str) -> list[Dataset]:
        texto = texto.lower()
        return [d for d in self
                if texto in d.titulo.lower() or any(texto in e.lower() for e in d.etiquetas)]

    def por_formato(self, formato: Formato) -> list[Dataset]:
        return [d for d in self if d.formato == formato]

    def mas_recientes(self, n: int = 5) -> list[Dataset]:
        return sorted(self, key=lambda d: d.actualizado, reverse=True)[:n]

    def resumen(self) -> dict[str, int]:
        return dict(sorted(Counter(str(d.formato) for d in self).items()))

    # ----------------------------------------------------------------- Parte E
    @classmethod
    def desde_json(cls, ruta: str | Path, nombre: str = "Catálogo") -> "Catalogo":
        catalogo = cls(nombre)
        fichas = json.loads(Path(ruta).read_text(encoding="utf-8"))
        for ficha in fichas:
            try:
                catalogo.agregar(Dataset.desde_dict(ficha))
            except (KeyError, ValueError):
                catalogo.descartados += 1
        return catalogo

    def guardar_json(self, ruta: str | Path) -> None:
        ruta = Path(ruta)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(json.dumps([d.a_dict() for d in self], ensure_ascii=False, indent=2),
                        encoding="utf-8")


if __name__ == "__main__":
    catalogo = Catalogo.desde_json("datos/datasets.json", "Málaga")
    print(catalogo, "·", catalogo.descartados, "fichas descartadas")
    print(catalogo.resumen())
    for d in catalogo.mas_recientes(3):
        print(f"  {d.actualizado}  {d.titulo}")

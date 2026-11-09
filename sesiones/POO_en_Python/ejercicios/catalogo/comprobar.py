"""Comprueba el ejercicio «Catálogo de datasets».

Ejecútalo desde la carpeta del ejercicio, junto a catalogo.py:
    python3 comprobar.py        (en Windows: python comprobar.py)

Puedes ejecutarlo tantas veces como quieras: después de cada parte, las
comprobaciones de esa parte deberían pasar a [OK].
"""
import dataclasses
import json
import tempfile
import traceback
from datetime import date
from pathlib import Path

ESPERADO = {
 "total_fichas": 30,
 "validos": 26,
 "descartados": 4,
 "grandes": ["arbolado", "calidad-aire-horaria", "ocupacion-aparcamientos", "validaciones-emt"],
 "por_formato": {"csv": 11, "geojson": 6, "json": 5, "xlsx": 4},
 "buscar_aire": ["calidad-aire-horaria", "calidad-aire-diaria", "zonas-juego"],
 "buscar_bici": ["estaciones-bici", "carril-bici"],
 "mas_recientes_3": ["ocupacion-aparcamientos", "temperaturas-diarias", "calidad-aire-horaria"],
 "organismos": ["AEMET", "Ayuntamiento de Málaga", "EMT Málaga", "INE", "Junta de Andalucía"],
 "etiquetas": 27,
}
DATOS = Path("datos/datasets.json")
FICHA = {"id": "paradas-emt", "titulo": "Paradas de autobús", "organismo": "EMT Málaga",
         "formato": "geojson", "filas": 1120, "actualizado": "2026-07-15",
         "etiquetas": ["movilidad", "transporte"]}

aciertos = 0
total = 0


def comprobar(descripcion: str, prueba, pista: str = "") -> bool:
    """Ejecuta prueba() y muestra [OK] si devuelve True. Un error cuenta como fallo."""
    global aciertos, total
    total += 1
    try:
        ok = bool(prueba())
        error = ""
    except Exception as e:
        ok = False
        ultima = traceback.extract_tb(e.__traceback__)[-1]
        donde = f" (catalogo.py, línea {ultima.lineno})" if ultima.filename.endswith("catalogo.py") else ""
        error = f"{type(e).__name__}: {e}{donde}"
    aciertos += ok
    print(f"  [{'OK' if ok else '  '}] {descripcion}")
    if not ok:
        if error:
            print(f"         Error: {error}")
        if pista:
            print(f"         Pista: {pista}")
    return ok


def lanza(excepcion, funcion, *args, **kwargs) -> bool:
    try:
        funcion(*args, **kwargs)
    except excepcion:
        return True
    return False


try:
    import catalogo as c
except Exception as e:
    raise SystemExit(f"\nNo se puede importar catalogo.py: {type(e).__name__}: {e}\n"
                     "Ejecuta comprobar.py desde la carpeta del ejercicio y revisa que catalogo.py no tenga errores.")

if not DATOS.is_file():
    raise SystemExit(f"\nNo encuentro {DATOS}. Ejecuta comprobar.py desde la carpeta del ejercicio.")


def dataset(**cambios):
    """Crea un Dataset de prueba, con los campos que se indiquen cambiados."""
    campos = dict(id="prueba", titulo="Prueba", organismo="Laboratorio", formato=c.Formato.CSV,
                  filas=10, actualizado=date(2026, 1, 1), etiquetas=("a", "b"))
    return c.Dataset(**(campos | cambios))


print("\nParte A · Formato y Dataset")
comprobar("Formato tiene CSV, JSON, GEOJSON y XLSX, con valores en minúsculas",
          lambda: [(f.name, f.value) for f in c.Formato] ==
          [("CSV", "csv"), ("JSON", "json"), ("GEOJSON", "geojson"), ("XLSX", "xlsx")])
comprobar("Dataset es una dataclass", lambda: dataclasses.is_dataclass(c.Dataset),
          "pon @dataclass(frozen=True) encima de class Dataset")
comprobar("Dataset tiene los 7 campos en el orden indicado",
          lambda: [f.name for f in dataclasses.fields(c.Dataset)] ==
          ["id", "titulo", "organismo", "formato", "filas", "actualizado", "etiquetas"])
comprobar("Las etiquetas son opcionales (por defecto, una tupla vacía)",
          lambda: c.Dataset("x", "X", "Org", c.Formato.CSV, 1, date(2026, 1, 1)).etiquetas == ())
comprobar("Dataset es inmutable", lambda: lanza(dataclasses.FrozenInstanceError, setattr, dataset(), "filas", 5),
          "usa @dataclass(frozen=True)")
comprobar("Un id vacío lanza ValueError", lambda: lanza(ValueError, dataset, id=""),
          "valida en __post_init__ con: if not self.id: raise ValueError(...)")
comprobar("Unas filas negativas lanzan ValueError", lambda: lanza(ValueError, dataset, filas=-1))
comprobar("es_grande es una propiedad que funciona",
          lambda: isinstance(c.Dataset.es_grande, property)
          and dataset(filas=100_000).es_grande and not dataset(filas=99_999).es_grande,
          "usa @property y compara con UMBRAL_GRANDE (>=)")

print("\nParte B · Convertir desde y hacia diccionarios")
comprobar("Dataset.desde_dict() crea un Dataset con los tipos correctos",
          lambda: (d := c.Dataset.desde_dict(FICHA)).formato is c.Formato.GEOJSON
          and d.actualizado == date(2026, 7, 15) and d.etiquetas == ("movilidad", "transporte"),
          "convierte con Formato(...), date.fromisoformat(...) y tuple(...)")
comprobar("desde_dict() funciona con una ficha sin etiquetas",
          lambda: c.Dataset.desde_dict({k: v for k, v in FICHA.items() if k != "etiquetas"}).etiquetas == (),
          "usa d.get(\"etiquetas\", [])")
comprobar("desde_dict() lanza ValueError con un formato desconocido",
          lambda: lanza(ValueError, c.Dataset.desde_dict, FICHA | {"formato": "pdf"}))
comprobar("a_dict() devuelve la ficha original y se puede guardar en JSON",
          lambda: json.loads(json.dumps(c.Dataset.desde_dict(FICHA).a_dict())) == FICHA,
          "el formato como str, la fecha con .isoformat() y las etiquetas como list")

print("\nParte C · Catalogo")
comprobar("Existe la excepción DatasetDuplicado y hereda de Exception",
          lambda: issubclass(c.DatasetDuplicado, Exception))


def catalogo_de_prueba():
    cat = c.Catalogo("Prueba")
    cat.agregar(dataset(id="uno"))
    cat.agregar(dataset(id="dos", filas=20))
    return cat


comprobar("agregar() añade datasets y len() los cuenta", lambda: len(catalogo_de_prueba()) == 2)
comprobar("Añadir un id repetido lanza DatasetDuplicado",
          lambda: lanza(c.DatasetDuplicado, catalogo_de_prueba().agregar, dataset(id="uno")))
comprobar("Recorrer el catálogo con for da objetos Dataset",
          lambda: [d.id for d in catalogo_de_prueba()] == ["uno", "dos"]
          and all(isinstance(d, c.Dataset) for d in catalogo_de_prueba()),
          "__iter__ debe devolver iter(self._datasets.values())")
comprobar("Funcionan 'id' in catalogo y catalogo['id']",
          lambda: "uno" in catalogo_de_prueba() and "tres" not in catalogo_de_prueba()
          and catalogo_de_prueba()["dos"].filas == 20)
comprobar("repr() muestra Catalogo('Prueba', 2 datasets)",
          lambda: repr(catalogo_de_prueba()) == "Catalogo('Prueba', 2 datasets)",
          "usa {self.nombre!r} en el f-string para que salgan las comillas")


def cargar_a_mano():
    """Carga el catálogo sin usar desde_json(), para probar la parte D por separado."""
    cat = c.Catalogo("Datos abiertos")
    for ficha in json.loads(DATOS.read_text(encoding="utf-8")):
        try:
            cat.agregar(c.Dataset.desde_dict(ficha))
        except (KeyError, ValueError):
            pass
    return cat


print("\nParte D · Consultas")
comprobar("buscar('aire') encuentra 3 datasets (en el título o en las etiquetas)",
          lambda: sorted(d.id for d in cargar_a_mano().buscar("aire")) == sorted(ESPERADO["buscar_aire"]))
comprobar("buscar() no distingue mayúsculas de minúsculas",
          lambda: sorted(d.id for d in cargar_a_mano().buscar("BICI")) == sorted(ESPERADO["buscar_bici"]),
          "pasa a minúsculas el texto buscado y el título con .lower()")
comprobar("por_formato(Formato.XLSX) devuelve los 4 datasets en Excel",
          lambda: len(cargar_a_mano().por_formato(c.Formato.XLSX)) == ESPERADO["por_formato"]["xlsx"])
comprobar("mas_recientes(3) devuelve los 3 más nuevos, del más nuevo al más antiguo",
          lambda: [d.id for d in cargar_a_mano().mas_recientes(3)] == ESPERADO["mas_recientes_3"],
          "sorted(..., key=lambda d: d.actualizado, reverse=True)[:n]")
comprobar("resumen() cuenta los datasets por formato, con las claves ordenadas",
          lambda: (r := cargar_a_mano().resumen()) == ESPERADO["por_formato"]
          and list(r) == sorted(r))

print("\nParte E · Cargar y guardar en JSON")
comprobar(f"desde_json() carga {ESPERADO['validos']} datasets y descarta {ESPERADO['descartados']}",
          lambda: (len(cat := c.Catalogo.desde_json(DATOS)), cat.descartados)
          == (ESPERADO["validos"], ESPERADO["descartados"]),
          "captura KeyError y ValueError al crear cada Dataset y suma 1 a descartados")
comprobar("desde_json() admite un nombre para el catálogo",
          lambda: c.Catalogo.desde_json(DATOS, "Málaga").nombre == "Málaga")


def ida_y_vuelta():
    original = c.Catalogo.desde_json(DATOS)
    with tempfile.TemporaryDirectory() as tmp:
        ruta = Path(tmp) / "salida" / "catalogo.json"
        original.guardar_json(ruta)
        copia = c.Catalogo.desde_json(ruta)
    return copia.descartados == 0 and list(copia) == list(original)


comprobar("guardar_json() crea la carpeta y el archivo se vuelve a cargar igual", ida_y_vuelta,
          "crea la carpeta con ruta.parent.mkdir(parents=True, exist_ok=True)")

print(f"\n{aciertos} de {total} comprobaciones correctas.")
if aciertos == total:
    print("¡Ejercicio completo! Ejecuta python3 catalogo.py para ver el catálogo.")

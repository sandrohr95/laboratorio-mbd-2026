# Catálogo de datasets · Enunciado

Un **catálogo de datos abiertos** es una lista de fichas, una por cada conjunto de datos (*dataset*) que publica una administración: las paradas de autobús, la calidad del aire, el padrón... Cada ficha dice cómo se llama el dataset, quién lo publica, en qué formato está, cuántas filas tiene y cuándo se actualizó por última vez.

Vas a escribir en `catalogo.py` las clases que permiten **cargar ese catálogo desde un JSON, consultarlo y guardarlo**. Los datos están en `datos/datasets.json` y **son simulados**.

---

## 0. Antes de empezar

### Los datos

Abre `datos/datasets.json` en VS Code. Es una **lista de diccionarios**, uno por ficha. Esta es una de ellas:

```json
{
  "id": "paradas-emt",
  "titulo": "Paradas de autobús",
  "organismo": "EMT Málaga",
  "formato": "geojson",
  "filas": 1120,
  "actualizado": "2026-07-15",
  "etiquetas": ["movilidad", "transporte"]
}
```

En el JSON **todo son textos, números y listas**: la fecha es un `str` y el formato también. Una parte importante del ejercicio es convertir cada valor a un tipo con más sentido: la fecha a `date` y el formato a un `Formato`.

De las 30 fichas, **4 tienen errores a propósito**, como pasa con los datos reales. Tu código tendrá que detectarlas y descartarlas (parte E).

### El diseño: tres clases

| Clase | Qué representa | Tipo de clase |
|---|---|---|
| `Formato` | Los formatos de archivo admitidos: `csv`, `json`, `geojson` y `xlsx` | `StrEnum` |
| `Dataset` | **Una** ficha del catálogo | *Dataclass* inmutable |
| `Catalogo` | El catálogo **completo**: guarda muchos `Dataset` y permite consultarlos | Clase normal |

Su relación:

- Un `Dataset` **tiene un** `Formato`: su campo `formato` es un miembro del `Enum`.
- Un `Catalogo` **tiene muchos** `Dataset`: los guarda en un diccionario `{id: Dataset}`. Es **composición**: el catálogo no *es* un diccionario, *tiene* uno.

### Cómo trabajar

- Haz las partes **en orden**. Cada una usa lo de la anterior.
- En `catalogo.py`, cada cosa que tienes que hacer está marcada con `TODO` y un número del 1 al 16. Los métodos ya están declarados: sustituye `raise NotImplementedError(...)` por tu código.
- Después de cada parte, ejecuta `python3 comprobar.py` (en Windows, `python comprobar.py`). Las comprobaciones de esa parte deberían pasar a `[OK]`.
- Para probar tu código sobre la marcha, abre una consola de Python con tu archivo cargado y juega con él:

  ```bash
  $ python3 -i catalogo.py
  >>> Formato("csv")
  >>> d = Dataset.desde_dict({...})
  ```

  Si `catalogo.py` todavía no está completo, el bloque final del archivo dará un error: es normal, y la consola se abre igualmente. Sal con `exit()`.

---

## Parte A · `Formato` y `Dataset`

### TODO 1 · El `Enum` `Formato`

Un `Enum` es un conjunto **cerrado** de valores con nombre. Usarlo en lugar de cadenas sueltas evita erratas: `"csv "`, `"CSV"` o `"cvs"` serían cadenas válidas, pero no formatos válidos.

`Formato` ya tiene el miembro `CSV = "csv"`. Añade `JSON`, `GEOJSON` y `XLSX`, con su nombre en minúsculas como valor.

Como hereda de `StrEnum`, cada miembro **también es un `str`**, y se puede crear a partir del texto que viene en el JSON:

```python
>>> Formato("csv")              # del texto al miembro
<Formato.CSV: 'csv'>
>>> Formato("csv") is Formato.CSV
True
>>> str(Formato.GEOJSON)        # del miembro al texto
'geojson'
>>> Formato("pdf")              # un formato que no existe
ValueError: 'pdf' is not a valid Formato
```

Ese `ValueError` es útil: es lo que permitirá detectar la ficha con un formato que no existe.

### TODO 2 · La *dataclass* `Dataset`

Un `Dataset` es una ficha. Conviértelo en una *dataclass* **inmutable** poniendo `@dataclass(frozen=True)` encima de la clase, y declara sus campos con su tipo, **en este orden**:

| Campo | Tipo | Ejemplo | Nota |
|---|---|---|---|
| `id` | `str` | `"paradas-emt"` | Identifica la ficha. No puede repetirse ni estar vacío |
| `titulo` | `str` | `"Paradas de autobús"` | |
| `organismo` | `str` | `"EMT Málaga"` | |
| `formato` | `Formato` | `Formato.GEOJSON` | **Un `Formato`, no un `str`** |
| `filas` | `int` | `1120` | |
| `actualizado` | `date` | `date(2026, 7, 15)` | **Un `date`, no un `str`** |
| `etiquetas` | `tuple[str, ...]` | `("movilidad", "transporte")` | Por defecto, una tupla vacía: `= ()` |

Por qué así:

- **Inmutable** (`frozen=True`): una ficha cargada no debería cambiar por accidente. Si alguien intenta `d.filas = 5`, Python lanza `FrozenInstanceError`.
- **`etiquetas` es una tupla y no una lista**: en una *dataclass* inmutable no tiene sentido un campo modificable, y además una lista como valor por defecto está prohibida.
- **`etiquetas` va la última**: en una *dataclass*, los campos con valor por defecto van siempre al final.

Con esto, `@dataclass` te genera solo el `__init__`, el `__repr__` y el `__eq__`:

```python
>>> d = Dataset("paradas-emt", "Paradas de autobús", "EMT Málaga",
...             Formato.GEOJSON, 1120, date(2026, 7, 15), ("movilidad", "transporte"))
>>> d.titulo
'Paradas de autobús'
>>> d
Dataset(id='paradas-emt', titulo='Paradas de autobús', ..., etiquetas=('movilidad', 'transporte'))
```

### TODO 3 · Validar en `__post_init__`

`__post_init__` es un método que la *dataclass* ejecuta **justo después** de su `__init__`. Es el sitio para comprobar que los datos tienen sentido. Lanza un `ValueError`, con un mensaje que explique el problema, si:

- el `id` está vacío (`""`), o
- `filas` es negativo.

```python
>>> Dataset("", "Sin id", "X", Formato.CSV, 10, date(2026, 1, 1))
ValueError: El id no puede estar vacío
>>> Dataset("x", "Filas raras", "X", Formato.CSV, -1, date(2026, 1, 1))
ValueError: x: el número de filas no puede ser negativo (-1)
```

### TODO 4 · La propiedad `es_grande`

Un dataset es "grande" si tiene **100 000 filas o más** (la constante `UMBRAL_GRANDE`). Escríbelo como **propiedad**: se usa como si fuera un atributo, **sin paréntesis**, pero se calcula cada vez a partir de `filas`.

```python
>>> d.es_grande          # 1120 filas
False
```

**Comprobación:** ejecuta `comprobar.py`. Deberían salir en `[OK]` las 8 comprobaciones de la parte A.

---

## Parte B · Convertir desde y hacia diccionarios

### TODO 5 · `Dataset.desde_dict(d)`

Es un **método de clase** (`@classmethod`): un **constructor alternativo**, que recibe una ficha tal como viene del JSON (un diccionario) y devuelve un `Dataset`. Recibe `cls`, la propia clase, y termina con `return cls(...)`.

Lo que tiene que hacer es **convertir cada valor a su tipo** antes de crear el objeto:

| Clave del diccionario | Cómo se convierte |
|---|---|
| `id`, `titulo`, `organismo` | Tal cual |
| `formato` | `Formato(d["formato"])` |
| `filas` | `int(d["filas"])` |
| `actualizado` | `date.fromisoformat(d["actualizado"])`, que convierte `"2026-07-15"` en `date(2026, 7, 15)` |
| `etiquetas` | `tuple(...)` de la lista. **Puede no venir**: usa `d.get("etiquetas", [])` |

```python
>>> ficha = {"id": "paradas-emt", "titulo": "Paradas de autobús", "organismo": "EMT Málaga",
...          "formato": "geojson", "filas": 1120, "actualizado": "2026-07-15",
...          "etiquetas": ["movilidad", "transporte"]}
>>> d = Dataset.desde_dict(ficha)
>>> d.formato, d.actualizado
(<Formato.GEOJSON: 'geojson'>, datetime.date(2026, 7, 15))
```

**No captures errores aquí.** Si la ficha no tiene fecha (`KeyError`), o el formato no existe o las filas son negativas (`ValueError`), deja que el error salga: quien carga el catálogo entero decidirá qué hacer con él (parte E).

### TODO 6 · `a_dict()`

El camino inverso: devuelve un diccionario **que se pueda guardar en JSON**, con las mismas claves que la ficha original. JSON no entiende de `Formato` ni de `date`, así que hay que volver a convertirlos:

- el formato, a texto: `str(self.formato)`;
- la fecha, a texto: `self.actualizado.isoformat()`;
- las etiquetas, a lista: `list(self.etiquetas)`.

La prueba de que está bien: si conviertes una ficha a `Dataset` y otra vez a diccionario, obtienes **la misma ficha**.

```python
>>> Dataset.desde_dict(ficha).a_dict() == ficha
True
```

**Comprobación:** 4 comprobaciones de la parte B.

---

## Parte C · La clase `Catalogo`

### TODO 7 · La excepción `DatasetDuplicado`

Una **excepción propia** para cuando se intenta añadir un dataset cuyo `id` ya está en el catálogo. Es una clase vacía que **hereda de `Exception`**. Basta con un *docstring* como cuerpo.

### TODO 8 · `__init__(self, nombre)`

Un catálogo guarda tres cosas:

| Atributo | Valor inicial | Para qué |
|---|---|---|
| `self.nombre` | El que recibe | Para mostrarlo |
| `self._datasets` | `{}`, un diccionario **vacío** | Guarda los datasets por su `id`: `{"paradas-emt": Dataset(...), ...}` |
| `self.descartados` | `0` | Cuántas fichas con errores se descartaron al cargar (parte E) |

El guion bajo de `_datasets` indica que es **interno**: desde fuera nadie debería tocarlo directamente, sino usar los métodos del catálogo.

¿Por qué un diccionario y no una lista? Porque así buscar un dataset por su `id` es inmediato, y saber si un `id` ya existe es tan fácil como `id in self._datasets`.

### TODO 9 · `agregar(self, dataset)`

Añade el dataset al diccionario, con su `id` como clave. Si ese `id` **ya existe**, lanza `DatasetDuplicado` y no añadas nada.

### TODO 10 · Los métodos especiales

Hacen que el catálogo se comporte como una colección de Python. Cada uno es una o dos líneas:

| Método | Hace que funcione... | Debe devolver |
|---|---|---|
| `__len__(self)` | `len(catalogo)` | El número de datasets |
| `__iter__(self)` | `for d in catalogo:` | `iter(...)` de los **`Dataset`**, no de los ids. Pista: `.values()` |
| `__contains__(self, id_dataset)` | `"paradas-emt" in catalogo` | `True` o `False` |
| `__getitem__(self, id_dataset)` | `catalogo["paradas-emt"]` | El `Dataset` con ese id. Si no existe, que salte el `KeyError` |
| `__repr__(self)` | Mostrar el catálogo en la consola | **Exactamente** `Catalogo('Prueba', 2 datasets)` |

```python
>>> cat = Catalogo("Prueba")
>>> cat.agregar(d)
>>> len(cat), "paradas-emt" in cat, cat["paradas-emt"].titulo
(1, True, 'Paradas de autobús')
>>> cat
Catalogo('Prueba', 1 datasets)
>>> cat.agregar(d)
DatasetDuplicado: paradas-emt
```

En `__repr__`, para que el nombre salga **con comillas**, usa `{self.nombre!r}` dentro del *f-string*. Y recuerda: `__repr__` **devuelve** el texto con `return`, no lo imprime.

Una vez tienes `__iter__`, el resto de métodos del catálogo pueden recorrerlo con `for d in self`.

**Comprobación:** 6 comprobaciones de la parte C.

---

## Parte D · Consultas

Todos estos métodos devuelven **objetos `Dataset`**, no sus ids ni sus títulos, salvo `resumen()`. Los ejemplos usan el catálogo completo de `datos/datasets.json`.

### TODO 11 · `buscar(self, texto)`

Devuelve una **lista** con los datasets cuyo **título** o **alguna de sus etiquetas** contienen el texto, **sin distinguir mayúsculas de minúsculas**.

- Pasa a minúsculas el texto buscado y lo que compares: `.lower()`.
- "Contiene" significa que es una **parte** del texto: `"aire" in "calidad del aire"` es `True`.
- Para las etiquetas, te sirve `any(...)`.

```python
>>> [d.titulo for d in cat.buscar("aire")]
['Calidad del aire: mediciones horarias', 'Calidad del aire: medias diarias', 'Zonas de juego al aire libre']
>>> len(cat.buscar("BICI"))
2
```

### TODO 12 · `por_formato(self, formato)`

Devuelve una **lista** con los datasets de ese formato.

```python
>>> len(cat.por_formato(Formato.XLSX))
4
```

### TODO 13 · `mas_recientes(self, n=5)`

Devuelve una **lista** con los `n` datasets actualizados más recientemente, **del más nuevo al más antiguo**. Ordena con `sorted(..., key=..., reverse=True)` usando la fecha como criterio, y quédate con los `n` primeros.

```python
>>> [(str(d.actualizado), d.id) for d in cat.mas_recientes(3)]
[('2026-10-30', 'ocupacion-aparcamientos'), ('2026-10-29', 'temperaturas-diarias'), ('2026-10-28', 'calidad-aire-horaria')]
```

### TODO 14 · `resumen(self)`

Devuelve un **diccionario** `{formato: número de datasets}`, con los formatos como texto y las claves **ordenadas alfabéticamente**. Puedes contar con `Counter` (ya está importado) y ordenar con `dict(sorted(...items()))`.

```python
>>> cat.resumen()
{'csv': 11, 'geojson': 6, 'json': 5, 'xlsx': 4}
```

**Comprobación:** 5 comprobaciones de la parte D. El comprobador carga el catálogo a su manera, así que esta parte funciona aunque todavía no hayas hecho la E.

---

## Parte E · Cargar y guardar en JSON

### TODO 15 · `Catalogo.desde_json(ruta, nombre="Catálogo")`

Otro **método de clase**: crea un catálogo completo a partir del archivo JSON. Los pasos:

1. Crea un catálogo vacío con `cls(nombre)`.
2. Lee el archivo y conviértelo en una lista de diccionarios: `json.loads(Path(ruta).read_text(encoding="utf-8"))`.
3. Recorre las fichas. Para cada una, crea el `Dataset` con `Dataset.desde_dict(ficha)` y añádelo con `agregar()`.
4. Si al crear un `Dataset` salta un **`KeyError` o un `ValueError`**, captúralo con `try`/`except`, **no** lo añadas y suma 1 a `descartados`. El programa debe seguir con la siguiente ficha.
5. Devuelve el catálogo.

Las 4 fichas con errores, y lo que debería pasar con cada una:

| Ficha | Problema | Error que salta |
|---|---|---|
| `callejero` | Formato `"pdf"`, que no está en `Formato` | `ValueError` en `Formato("pdf")` |
| `accidentes-trafico` | `filas` vale `-1` | `ValueError` en tu `__post_init__` |
| (sin id) | `id` vacío | `ValueError` en tu `__post_init__` |
| `ruido` | No tiene la clave `actualizado` | `KeyError` en `d["actualizado"]` |

```python
>>> cat = Catalogo.desde_json("datos/datasets.json", "Málaga")
>>> cat, cat.descartados
(Catalogo('Málaga', 26 datasets), 4)
```

### TODO 16 · `guardar_json(self, ruta)`

Guarda todos los datasets del catálogo en un archivo JSON, como una lista de diccionarios (usa `a_dict()`):

1. Crea la carpeta de destino si no existe: `ruta.parent.mkdir(parents=True, exist_ok=True)`. Convierte antes `ruta` en un `Path`.
2. Escribe la lista con `json.dumps(..., ensure_ascii=False, indent=2)`. `ensure_ascii=False` conserva las tildes.

La prueba de que está bien: si guardas el catálogo y lo vuelves a cargar con `desde_json`, obtienes los mismos 26 datasets y ningún descartado.

**Comprobación:** 3 comprobaciones de la parte E. En total, **26 de 26**.

---

## Al terminar

Ejecuta el propio módulo:

```bash
$ python3 catalogo.py
Catalogo('Málaga', 26 datasets) · 4 fichas descartadas
{'csv': 11, 'geojson': 6, 'json': 5, 'xlsx': 4}
  2026-10-30  Ocupación de aparcamientos en tiempo real
  2026-10-29  Temperaturas diarias del aeropuerto
  2026-10-28  Calidad del aire: mediciones horarias
```

## Fallos frecuentes

| Síntoma | Causa |
|---|---|
| `TypeError: non-default argument 'filas' follows default argument` | Un campo con valor por defecto (`etiquetas`) no está al final |
| `TypeError: Dataset() takes no arguments` | Falta `@dataclass(frozen=True)` encima de `class Dataset` |
| `AttributeError: 'Catalogo' object has no attribute '_datasets'` | No lo has creado en `__init__`, o le falta el guion bajo |
| `TypeError: __repr__ returned non-string` | `__repr__` usa `print` en lugar de `return` |
| `RecursionError` | Dentro de `__len__` llamas a `len(self)`, o dentro de `__iter__` haces `for d in self`. Usa `self._datasets` |
| `desde_json` descarta 3 en lugar de 4 | No capturas el `KeyError` de la ficha sin fecha |
| `desde_json` se detiene con un error | La ficha con errores no está dentro del `try` |
| `mas_recientes` sale al revés | Falta `reverse=True` |

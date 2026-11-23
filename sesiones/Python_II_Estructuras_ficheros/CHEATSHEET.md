# Chuleta · Estructuras de datos, ficheros y errores

## ¿Qué estructura uso?

| Estructura | Sintaxis | Ordenada | Modificable | Duplicados | Úsala para |
|---|---|---|---|---|---|
| Lista `list` | `[1, 2, 3]` | Sí | Sí | Sí | Secuencias de elementos del mismo tipo |
| Tupla `tuple` | `(36.7, -4.4)` | Sí | No | Sí | Registros fijos: coordenadas, pares, valores de retorno |
| Diccionario `dict` | `{"id": 1, "nombre": "Soho"}` | Sí (orden de inserción) | Sí | Claves no | Datos con nombre, búsquedas por clave, JSON |
| Conjunto `set` | `{"Centro", "Este"}` | No | Sí | No | Quitar duplicados, comprobar pertenencia, operaciones de conjuntos |

## Listas

| Qué hago | Código |
|---|---|
| Añadir al final / varios / en una posición | `l.append(x)` · `l.extend([x, y])` · `l.insert(0, x)` |
| Quitar por valor / por posición | `l.remove(x)` · `l.pop()` · `l.pop(0)` |
| Ordenar en el sitio / obtener una copia ordenada | `l.sort()` · `sorted(l)` · `sorted(l, reverse=True)` |
| Copiar (no `b = a`) | `b = a.copy()` |
| Longitud, suma, mínimo, máximo | `len(l)` · `sum(l)` · `min(l)` · `max(l)` |
| ¿Está? | `x in l` |

## Tuplas y desempaquetado

```python
lat, lon = (36.7178, -4.4254)
a, b = b, a                     # intercambio
primero, *resto = [1, 2, 3, 4]
for nombre, capacidad in [("Soho", 16), ("Muelle Uno", 20)]:
    ...
```

## Diccionarios

| Qué hago | Código |
|---|---|
| Leer (error si no existe) / leer con valor por defecto | `d["clave"]` · `d.get("clave", 0)` |
| Añadir o modificar / borrar | `d["clave"] = valor` · `del d["clave"]` |
| Recorrer claves y valores | `for k, v in d.items():` |
| Claves / valores | `d.keys()` · `d.values()` |
| Contar apariciones a mano | `d[x] = d.get(x, 0) + 1` |

## Conjuntos

| Operación | Código |
|---|---|
| Crear quitando duplicados | `set(lista)` |
| Unión / intersección / diferencia | `a \| b` · `a & b` · `a - b` |
| Añadir / ¿está? | `s.add(x)` · `x in s` |

## Comprensiones

```python
[x ** 2 for x in numeros]                     # lista
[x for x in numeros if x % 2 == 0]            # lista con filtro
{c: len(c) for c in ciudades}                 # diccionario
{c[0] for c in ciudades}                      # conjunto
```

## Ordenar con criterio

```python
sorted(estaciones, key=lambda e: e["capacidad"], reverse=True)
max(estaciones, key=lambda e: e["capacidad"])
sorted(palabras, key=str.lower)
```

## Ficheros

```python
from pathlib import Path

ruta = Path("datos") / "viajes.csv"
ruta.exists()
Path("salida").mkdir(exist_ok=True)

with open("salida/notas.txt", "w", encoding="utf-8") as f:   # "r" leer · "w" escribir · "a" añadir
    f.write("texto\n")
```

### CSV

```python
import csv

with open("datos/viajes.csv", encoding="utf-8", newline="") as f:
    filas = list(csv.DictReader(f))           # lista de diccionarios; todo es str

with open("salida/limpio.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["col1", "col2"])
    w.writeheader()
    w.writerows(filas)
```

### JSON

```python
import json

with open("datos/estaciones.json", encoding="utf-8") as f:
    datos = json.load(f)                      # JSON → dict / list

with open("salida/resumen.json", "w", encoding="utf-8") as f:
    json.dump(datos, f, ensure_ascii=False, indent=2)
```

## Excepciones

```python
try:
    valor = float(texto)
except ValueError:              # captura solo el error que esperas
    valor = None
else:
    print("Sin errores")        # solo si no hubo excepción
finally:
    print("Siempre")            # haya error o no

raise ValueError("mensaje")     # lanzar un error


class DatoInvalido(Exception):  # excepción propia
    pass
```

| Excepción | Cuándo |
|---|---|
| `ValueError` | `int("N/D")` |
| `TypeError` | `"3" + 4` |
| `KeyError` | Clave que no existe |
| `IndexError` | Posición que no existe |
| `FileNotFoundError` | Archivo que no existe |
| `ZeroDivisionError` | División entre cero |

## Biblioteca estándar

```python
from collections import Counter, defaultdict, namedtuple
Counter(lista).most_common(3)                 # los 3 más frecuentes
grupos = defaultdict(list); grupos[k].append(x)

from datetime import date, datetime, timedelta
datetime.strptime("2026-09-18 08:45", "%Y-%m-%d %H:%M")
fecha.weekday()                               # 0 = lunes ... 6 = domingo
fecha + timedelta(days=7)
(date(2026, 12, 25) - date(2026, 10, 1)).days

import math, random, statistics
math.sqrt(16) · random.seed(42) · statistics.mean(l) · statistics.median(l)
```

## Módulos propios

```python
# utilidades.py
def mi_funcion():
    ...

if __name__ == "__main__":      # solo al ejecutar: python utilidades.py
    mi_funcion()
```

```python
import utilidades               # desde otro archivo de la misma carpeta
from utilidades import mi_funcion
```

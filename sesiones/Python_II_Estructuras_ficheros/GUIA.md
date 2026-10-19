# Python II · Estructuras de datos, ficheros y errores

> **Guía de laboratorio.** Síguela durante la clase a la vez que las diapositivas. La práctica se hace en un notebook; esta guía te explica cómo prepararlo y qué contiene.

**Material:** [diapositivas](https://sandrohr95.github.io/laboratorio-mbd-2026/slides/Python_II_Estructuras_ficheros.html) · [chuleta](CHEATSHEET.md) · [`notebooks/estructuras_ficheros.ipynb`](notebooks/estructuras_ficheros.ipynb) · [`notebooks/datos/`](notebooks/datos)

**Qué vas a aprender:** a organizar datos con listas, tuplas, diccionarios y conjuntos; a escribir comprensiones; a leer y escribir ficheros CSV y JSON; a manejar errores con excepciones; y a usar la biblioteca estándar de Python. Al final lo aplicarás todo a analizar los datos de un servicio de bicicletas **sin librerías externas**.

En los bloques de comandos, los que empiezan por `$` son para **bash/zsh** (macOS, Linux y WSL) y los que empiezan por `>` son para **PowerShell** (Windows). No copies el `$` ni el `>`.

---

## 1. Prepara el notebook

### 1.1 Trae el material nuevo

```bash
$ cd ~/proyectos/master/laboratorio-mbd-2026
$ git pull
```

### 1.2 Copia la carpeta `notebooks` a tu carpeta de trabajo

Esta vez el notebook viene acompañado de una carpeta `datos/` con los archivos de la práctica. Copia **la carpeta completa**, no solo el notebook: el notebook busca los datos en `datos/`, junto a él.

```bash
$ cd ~/proyectos/master
$ cp -r laboratorio-mbd-2026/sesiones/Python_II_Estructuras_ficheros/notebooks python-estructuras
$ cd python-estructuras
$ ls                                  # estructuras_ficheros.ipynb y datos/
$ code .
```

```powershell
> cd ~\proyectos\master
> cp -r laboratorio-mbd-2026\sesiones\Python_II_Estructuras_ficheros\notebooks python-estructuras
> cd python-estructuras
> ls
> code .
```

### 1.3 Elige el *kernel*

1. Abre `estructuras_ficheros.ipynb` en VS Code.
2. Arriba a la derecha, pulsa **Seleccionar kernel** (*Select Kernel*) → **Entornos de Python...** (*Python Environments...*) → **Crear entorno de Python** (*Create Python Environment*) → **Venv**, y elige tu Python 3.13 o posterior.
3. Si VS Code pregunta si quieres instalar `ipykernel`, responde **Instalar**.

Ejecuta la primera celda de código con `Shift+Intro`. Debe mostrar tu versión de Python y la lista `['estaciones.json', 'viajes.csv']`. Si en lugar de eso aparece un error `FileNotFoundError`, el notebook no encuentra la carpeta `datos/`: revisa que la copiaste junto a él.

> **Plan B:** si algo falla, abre <https://colab.research.google.com>, sube el notebook y después sube los dos archivos de datos desde el panel de archivos (icono de carpeta de la izquierda), dentro de una carpeta llamada `datos`.

**Punto de control 1:** la primera celda muestra tu versión de Python y los dos archivos de datos.

---

## 2. Trabaja el notebook

Recórrelo de arriba abajo, ejecutando las celdas **en orden**. En cada ejercicio, sustituye los `...` por tu código y ejecuta la celda de **comprobación** de debajo: si muestra `Correcto`, lo tienes.

| Apartado | Contenido |
|---|---|
| 1. Listas | Métodos, ordenar con `sort` y `sorted`, la trampa de copiar con `=` y listas anidadas |
| 2. Tuplas | Inmutabilidad, desempaquetado y funciones que devuelven varios valores |
| 3. Diccionarios | Acceso con `[]` y `get`, recorrer con `items()`, diccionarios anidados y contar apariciones |
| 4. Conjuntos | Quitar duplicados, unión, intersección y diferencia. Por qué buscar en un conjunto es tan rápido |
| 5. Comprensiones y ordenación | Comprensiones de listas, diccionarios y conjuntos. Funciones `lambda`. Ordenar con `key` |
| 6. Ficheros | Rutas con `pathlib`, `open` con `with`, CSV con `csv.DictReader` y `DictWriter`, JSON con `json.load` y `json.dump` |
| 7. Errores y excepciones | `try`/`except`/`else`/`finally`, lanzar errores con `raise` y excepciones propias |
| 8. Biblioteca estándar y módulos | `collections`, `datetime`, `math`, `random`, `statistics` y crear tu propio módulo |
| 9. Práctica final | Analizar el servicio de bicicletas: cargar, limpiar, agregar y exportar un resumen |

Los archivos que crees al ejecutar el notebook (en `salida/` y el módulo `utilidades.py`) se guardan en tu carpeta de trabajo, junto al notebook.

**Punto de control 2:** las comprobaciones de los apartados 1 a 7 muestran `Correcto`.

---

## 3. Práctica final · Servicio de bicicletas de Málaga

La carpeta `datos/` contiene los registros de un mes de un servicio de alquiler de bicicletas. **Son datos simulados**, creados para esta práctica:

| Archivo | Contenido |
|---|---|
| `viajes.csv` | 2.000 viajes: fecha, hora de inicio, estación de origen y de destino (por su `id`), duración en minutos, tipo de usuario (`abonado` u `ocasional`) y temperatura |
| `estaciones.json` | 12 estaciones con su `id`, nombre, barrio, capacidad y coordenadas |

Antes de empezar, **mira los datos**: abre `viajes.csv` en VS Code o en la terminal (`head datos/viajes.csv` o `gc datos\viajes.csv -Head 10`). Igual que en los datos reales, hay **filas con errores** que tendrás que descartar: duraciones vacías o con el texto `N/D`, duraciones negativas y estaciones que no existen.

El apartado 9 del notebook te guía paso a paso:

1. Cargar el CSV en una lista de diccionarios y el JSON en un diccionario por `id`.
2. Escribir una función que decida si un viaje es válido, usando `try`/`except`.
3. Calcular la duración media.
4. Encontrar las 3 estaciones con más salidas.
5. Contar los viajes por tipo de usuario y encontrar la hora punta.
6. Contar los viajes por barrio y encontrar el día de la semana con más uso.
7. Guardar todos los resultados en `salida/resumen.json`.

Cada paso usa los resultados del anterior, así que hazlos en orden.

**Punto de control 3:** las comprobaciones del apartado 9 muestran `Correcto` y existe el archivo `salida/resumen.json`.

---

## Problemas frecuentes

| Problema | Solución |
|---|---|
| `FileNotFoundError: 'datos/...'` | El notebook no está junto a la carpeta `datos/`. Copia la carpeta `notebooks` completa (apartado 1.2) |
| Una celda da `NameError` con una variable que sí existe | No has ejecutado las celdas anteriores, o has reiniciado el kernel. Ejecuta desde arriba: botón **Ejecutar todo** (*Run All*) |
| `TypeError: '>' not supported between instances of 'str' and 'int'` | Los valores leídos de un CSV son texto: conviértelos con `int()` o `float()` |
| Al cambiar `b`, también cambia `a` | `b = a` no copia la lista: usa `b = a.copy()` |
| `KeyError` al leer un diccionario | La clave no existe, o no es del tipo que crees (`1` no es lo mismo que `"1"`). Usa `get()` o revisa el tipo |
| Las tildes salen mal al leer o escribir | Añade `encoding="utf-8"` a `open()` |
| En Windows aparecen líneas en blanco de más en el CSV que escribes | Abre el archivo con `newline=""` |

## Para practicar en casa (opcional)

- Termina los retos del final del notebook, en el apartado «Para seguir practicando».
- **Exercism**, itinerario de Python: <https://exercism.org/tracks/python>. Los ejercicios sobre diccionarios, conjuntos y listas encajan con lo de hoy.
- Busca un CSV de datos abiertos que te interese (por ejemplo, en <https://datosabiertos.malaga.eu> o en <https://datos.gob.es>) y repite el análisis de la práctica sobre él.

# Programación orientada a objetos en Python

> **Guía de laboratorio.** Síguela durante la clase a la vez que las diapositivas. La teoría y los ejercicios cortos están en un notebook; la práctica final, en archivos de Python. Esta guía te explica cómo preparar los dos y qué contiene cada uno.

**Material:** [diapositivas](https://sandrohr95.github.io/laboratorio-mbd-2026/slides/POO_en_Python.html) · [chuleta](CHEATSHEET.md) · [`notebooks/poo.ipynb`](notebooks/poo.ipynb) · [`ejercicios/catalogo/`](ejercicios/catalogo)

**Qué vas a aprender:** a crear tus propias clases en Python y a traducir lo que ya sabes de Java: `self` frente a `this`, la ausencia de `public` y `private`, las propiedades en lugar de *getters* y *setters*, los métodos especiales, la herencia, las clases abstractas y el *duck typing*. Terminarás con la forma moderna de escribir clases: *dataclasses*, `Enum` y anotaciones de tipo. Al final lo aplicarás todo para modelar un **catálogo de datasets**.

En los bloques de comandos, los que empiezan por `$` son para **bash/zsh** (macOS, Linux y WSL) y los que empiezan por `>` son para **PowerShell** (Windows). No copies el `$` ni el `>`.

---

## 1. Prepara el material

### 1.1 Trae el material nuevo

```bash
$ cd ~/proyectos/master/laboratorio-mbd-2026
$ git pull
```

### 1.2 Copia el notebook y el ejercicio a tu carpeta de trabajo

Copia las dos carpetas **fuera del repositorio del curso**, para que tus cambios no choquen con el próximo `git pull`:

```bash
$ cd ~/proyectos/master
$ cp -r laboratorio-mbd-2026/sesiones/POO_en_Python/notebooks python-poo
$ cp -r laboratorio-mbd-2026/sesiones/POO_en_Python/ejercicios/catalogo catalogo-datasets
$ ls python-poo catalogo-datasets
```

```powershell
> cd ~\proyectos\master
> cp -r laboratorio-mbd-2026\sesiones\POO_en_Python\notebooks python-poo
> cp -r laboratorio-mbd-2026\sesiones\POO_en_Python\ejercicios\catalogo catalogo-datasets
> ls python-poo, catalogo-datasets
```

### 1.3 Abre el notebook y elige el *kernel*

```bash
$ cd ~/proyectos/master/python-poo
$ code .
```

1. Abre `poo.ipynb` en VS Code.
2. Arriba a la derecha, pulsa **Seleccionar kernel** (*Select Kernel*) → **Entornos de Python...** (*Python Environments...*) → **Crear entorno de Python** (*Create Python Environment*) → **Venv**, y elige tu Python 3.13 o posterior.
3. Si VS Code pregunta si quieres instalar `ipykernel`, responde **Instalar**.

Ejecuta la primera celda de código con `Shift+Intro`. Debe mostrar tu versión de Python sin ningún error.

> **Plan B:** si algo falla, abre <https://colab.research.google.com> y sube el notebook. No necesita ningún archivo más.

**Punto de control 1:** la primera celda del notebook muestra tu versión de Python.

---

## 2. Trabaja el notebook

Recórrelo de arriba abajo, ejecutando las celdas **en orden**. En cada ejercicio, sustituye los `...` por tu código y ejecuta la celda de **comprobación** de debajo: si muestra `Correcto`, lo tienes.

| Apartado | Contenido |
|---|---|
| 1. De Java a Python | Clases y objetos, `self`, convenciones `_` y `__` en lugar de modificadores de acceso, y "todo es un objeto" |
| 2. Clases | Atributos de instancia y de clase, `@property`, `@classmethod`, `@staticmethod` y métodos especiales (`__repr__`, `__str__`, `__eq__`, `__lt__`, `__len__`, `__iter__`...) |
| 3. Herencia y diseño | `super()`, polimorfismo, *duck typing*, clases abstractas con `abc`, composición frente a herencia y *mixins* |
| 4. Clases modernas | `@dataclass` (`field`, `frozen`, `order`, `__post_init__`), `Enum` y `StrEnum`, anotaciones de tipo, mypy y `Protocol` |
| 5. Práctica final | Qué hay que hacer en el ejercicio del catálogo de datasets |

Muchas celdas **vuelven a definir** una clase para ampliarla con algo nuevo; es normal. Si una celda falla con un `NameError` o se comporta de forma rara, ejecuta de nuevo las de arriba.

Una de las celdas del apartado 4 instala **mypy** con `pip`. Necesita conexión a internet; si no la tienes, sáltala.

**Punto de control 2:** las comprobaciones de los apartados 1 a 4 muestran `Correcto`.

---

## 3. Práctica final · Catálogo de datasets

En un proyecto real, las clases no viven en un notebook, sino en **archivos `.py`**. La práctica se hace así: en la carpeta `catalogo-datasets` que copiaste en el apartado 1.2.

| Archivo | Contenido |
|---|---|
| `catalogo.py` | El esqueleto que tienes que completar. Las instrucciones están en los comentarios, numeradas del 1 al 16 |
| `datos/datasets.json` | 30 fichas de un catálogo de datos abiertos: título, organismo, formato, número de filas, fecha de actualización y etiquetas. **Son datos simulados** |
| `comprobar.py` | Comprueba tu solución parte a parte. **No lo modifiques** |

Ábrelo en VS Code y ejecuta el comprobador desde la terminal integrada (`` Ctrl+` ``):

```bash
$ cd ~/proyectos/master/catalogo-datasets
$ code .
$ python3 comprobar.py
```

```powershell
> cd ~\proyectos\master\catalogo-datasets
> code .
> python comprobar.py
```

Al principio todas las comprobaciones salen vacías (`[  ]`). Completa `catalogo.py` **por partes** y vuelve a ejecutar `comprobar.py` después de cada una:

| Parte | Qué haces | Lo que practicas |
|---|---|---|
| A | El `Enum` `Formato` y la *dataclass* inmutable `Dataset`, con validación y la propiedad `es_grande` | `StrEnum`, `@dataclass(frozen=True)`, `__post_init__`, `@property` |
| B | `Dataset.desde_dict()` y `a_dict()`, para convertir desde y hacia JSON | `@classmethod`, conversión de tipos |
| C | La clase `Catalogo`, que guarda los datasets en un diccionario, y la excepción `DatasetDuplicado` | Composición, excepciones propias, métodos especiales |
| D | Las consultas: `buscar()`, `por_formato()`, `mas_recientes()` y `resumen()` | Comprensiones, `sorted` con `key`, `Counter` |
| E | `Catalogo.desde_json()`, que descarta las fichas con errores, y `guardar_json()` | `try`/`except`, `json`, `pathlib` |

Igual que en los datos reales, **4 de las 30 fichas tienen errores**: un formato que no existe, un número de filas negativo, un `id` vacío y una ficha a la que le falta la fecha. Tu `Dataset` debe rechazarlas con un `ValueError` o un `KeyError`, y `desde_json()` debe descartarlas sin detenerse.

Cuando `comprobar.py` diga que está todo correcto, ejecuta el propio módulo para ver el catálogo:

```bash
$ python3 catalogo.py
```

Este catálogo es el punto de partida de un proyecto que irá creciendo durante el curso: guarda bien la carpeta `catalogo-datasets`. Si ya usas Git, haz un commit cuando termines.

**Punto de control 3:** `comprobar.py` muestra `26 de 26 comprobaciones correctas`.

---

## Problemas frecuentes

| Problema | Solución |
|---|---|
| `TypeError: Bicicleta() takes no arguments` | El método se llama `__init__`, con **dos** guiones bajos a cada lado. Con `_init_` o `__init` Python no lo reconoce |
| `TypeError: recorrer() takes 1 positional argument but 2 were given` | Te falta `self` como primer parámetro del método |
| `NameError: name 'km' is not defined` dentro de un método | Los atributos se leen con `self.km`, no con `km` a secas |
| Todas las estaciones comparten las mismas bicicletas | Has creado la lista como atributo de clase. Créala en `__init__` con `self.bicis = []` |
| `RecursionError` al usar una propiedad | Dentro del *getter* o del *setter* de `bicis` usa otro nombre para guardar el valor: `self._bicis` |
| `ValueError: mutable default <class 'list'> for field ... is not allowed` | En una *dataclass*, una lista por defecto se escribe `field(default_factory=list)` |
| `TypeError: non-default argument 'filas' follows default argument` | En una *dataclass*, los campos con valor por defecto van **al final** |
| `comprobar.py` dice `No se puede importar catalogo.py` | Hay un error de sintaxis en `catalogo.py`: ejecútalo con `python3 catalogo.py` para ver la línea, o ejecuta `comprobar.py` desde la carpeta del ejercicio |
| `ImportError: cannot import name 'StrEnum'` | Tu Python es anterior a la 3.11. Comprueba la versión con `python3 --version` |

## Para practicar en casa (opcional)

- Termina los retos del final del notebook, en el apartado «Para seguir practicando».
- **Exercism**, itinerario de Python: <https://exercism.org/tracks/python>. Los ejercicios del concepto *Classes* encajan con lo de hoy.
- Lee la documentación oficial de las *dataclasses*: <https://docs.python.org/es/3/library/dataclasses.html>.
- Coge una clase que hayas escrito en Java y tradúcela a Python. Después, intenta reescribirla como *dataclass*: ¿cuántas líneas te ahorras?

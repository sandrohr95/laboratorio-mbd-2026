# Material adicional · Entornos virtuales y dependencias

> Esta guía explica qué es el `.venv` que crea VS Code para los notebooks, para qué sirven los entornos virtuales y cómo se gestionan las librerías de un proyecto. Al final tienes un resumen de comandos.

**Material:** [diapositivas](https://sandrohr95.github.io/laboratorio-mbd-2026/slides/Entornos_virtuales.html) · [`entornos/comprobar_entorno.py`](entornos/comprobar_entorno.py)

En los bloques de comandos, los que empiezan por `$` son para **bash/zsh** (macOS, Linux y WSL) y los que empiezan por `>` son para **PowerShell** (Windows). No copies el `$` ni el `>`.

---

## 1. El problema

Python trae una biblioteca estándar enorme, pero tarde o temprano necesitarás **librerías de terceros**: `pandas`, `requests`, `matplotlib`, `scikit-learn`... Si las instalas todas en el Python de tu sistema, aparecen tres problemas:

1. **Conflictos de versiones.** Un proyecto antiguo necesita `pandas` 1.5 y uno nuevo, `pandas` 2.2. En una misma instalación de Python solo puede haber **una** versión de cada librería: al actualizar para un proyecto, rompes el otro.
2. **"En mi máquina funciona".** Si no sabes exactamente qué librerías, y en qué versiones, usa tu proyecto, nadie más podrá ejecutarlo. Ni siquiera tú, dentro de seis meses, en otro ordenador.
3. **Romper el sistema.** macOS y Linux usan Python para sus propias herramientas. Por eso, en macOS con Homebrew y en los Linux recientes, `pip install` en el Python del sistema da el error `externally-managed-environment`: el sistema **te impide** hacerlo.

La solución es un **entorno virtual**: una instalación de Python aislada para cada proyecto, con sus propias librerías.

```
Python del sistema (no se toca)
├── proyecto-a/.venv  →  requests 2.31
└── proyecto-b/.venv  →  requests 2.32
```

---

## 2. Vocabulario mínimo

| Término | Qué es |
|---|---|
| **Módulo** | Un archivo `.py` que se puede importar |
| **Paquete** o **librería** | Un conjunto de módulos que se distribuye e instala junto, como `requests` |
| **PyPI** | *Python Package Index* (<https://pypi.org>): el repositorio público de donde se descargan los paquetes, con más de medio millón |
| **pip** | El instalador de paquetes que viene con Python: descarga de PyPI e instala |
| **Dependencia** | Un paquete que tu proyecto necesita |
| **Dependencia transitiva** | Un paquete que necesita otro paquete. Al instalar `requests` se instalan también `urllib3`, `idna`, `certifi` y `charset-normalizer` |

### Versiones

Casi todos los paquetes siguen el **versionado semántico**, `MAYOR.MENOR.PARCHE`:

| Cambia... | Ejemplo | Significa |
|---|---|---|
| PARCHE | `2.32.3` → `2.32.4` | Corrige errores. Seguro actualizar |
| MENOR | `2.31` → `2.32` | Añade funciones sin romper nada |
| MAYOR | `1.5` → `2.0` | Cambios incompatibles: tu código puede dejar de funcionar |

Y así se indica qué versión quieres:

| Especificador | Significa |
|---|---|
| `requests` | La más reciente |
| `requests==2.31.0` | Exactamente esa |
| `requests>=2.31` | Esa o posterior |
| `requests~=2.31.0` | Compatible: `2.31.x`, pero no `2.32` |

---

## 3. Qué es un entorno virtual, por dentro

Un entorno virtual es **solo una carpeta**, normalmente llamada `.venv`, dentro de tu proyecto:

```
.venv/
├── pyvenv.cfg       ← de qué Python se creó
├── bin/             ← en Windows: Scripts\
│   ├── python       ← un enlace al Python original
│   ├── pip
│   └── activate     ← en Windows: Activate.ps1
└── lib/python3.13/site-packages/   ← en Windows: Lib\site-packages\
    └── ...          ← aquí se instalan las librerías de ESTE entorno
```

No es una máquina virtual ni una copia completa de Python. Es un Python que, en lugar de buscar las librerías en la carpeta del sistema, las busca en su propio `site-packages`.

### Activar = cambiar el `PATH`

Cuando escribes `python`, la terminal busca ese programa en las carpetas del `PATH`, en orden. **Activar un entorno** solo añade su carpeta `bin` (o `Scripts`) **al principio** del `PATH`. A partir de ahí, `python` y `pip` son los del entorno.

```bash
$ which python3              # antes: /opt/homebrew/bin/python3 (o /usr/bin/python3)
$ source .venv/bin/activate
(.venv) $ which python       # después: /ruta/a/tu-proyecto/.venv/bin/python
```

El `(.venv)` delante del *prompt* te recuerda que el entorno está activo. `deactivate` lo desactiva.

### Entornos y notebooks

Un notebook se ejecuta con un **kernel**, que es un Python concreto. Cuando en VS Code eliges **Seleccionar kernel → Crear entorno de Python → Venv**, VS Code crea un `.venv` en la carpeta e instala en él `ipykernel`, el paquete que necesita Jupyter. Por eso, si instalas una librería en otro Python, el notebook no la encuentra.

---

## 4. Práctica · Dos proyectos, dos versiones

### 4.1 Crea dos proyectos con versiones distintas de la misma librería

```bash
$ mkdir -p ~/proyectos/master/entornos/proyecto-a ~/proyectos/master/entornos/proyecto-b
$ cd ~/proyectos/master/entornos/proyecto-a
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ python -m pip install "requests==2.31.0"
(.venv) $ python -m pip list
(.venv) $ deactivate
```

```powershell
> mkdir ~\proyectos\master\entornos\proyecto-a, ~\proyectos\master\entornos\proyecto-b
> cd ~\proyectos\master\entornos\proyecto-a
> python -m venv .venv
> .venv\Scripts\Activate.ps1
(.venv) > python -m pip install "requests==2.31.0"
(.venv) > python -m pip list
(.venv) > deactivate
```

> **Windows:** si `Activate.ps1` da un error de que la ejecución de scripts está deshabilitada, ejecuta una vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y responde que sí. También puedes no activar el entorno y llamar directamente a su Python: `.venv\Scripts\python -m pip install ...`.

`pip list` muestra `requests` **y cuatro paquetes más**: son sus dependencias transitivas.

Repite lo mismo en `proyecto-b`, pero con la versión `2.32.3`. Después, comprueba que cada proyecto tiene la suya, **a la vez**:

```bash
$ cd ~/proyectos/master/entornos
$ proyecto-a/.venv/bin/python -c "import requests; print(requests.__version__)"
$ proyecto-b/.venv/bin/python -c "import requests; print(requests.__version__)"
```

```powershell
> cd ~\proyectos\master\entornos
> proyecto-a\.venv\Scripts\python -c "import requests; print(requests.__version__)"
> proyecto-b\.venv\Scripts\python -c "import requests; print(requests.__version__)"
```

Fíjate en que no hace falta activar un entorno para usarlo: basta con llamar a **su** `python`.

### 4.2 Diagnostica con `comprobar_entorno.py`

Copia el script a la carpeta `entornos` y ejecútalo con tres Python distintos:

```bash
$ cp ~/proyectos/master/laboratorio-mbd-2026/sesiones/Python_II_Estructuras_ficheros/entornos/comprobar_entorno.py .
$ python3 comprobar_entorno.py requests                   # el Python del sistema
$ proyecto-a/.venv/bin/python comprobar_entorno.py requests
$ proyecto-b/.venv/bin/python comprobar_entorno.py requests
```

```powershell
> cp ~\proyectos\master\laboratorio-mbd-2026\sesiones\Python_II_Estructuras_ficheros\entornos\comprobar_entorno.py .
> python comprobar_entorno.py requests
> proyecto-a\.venv\Scripts\python comprobar_entorno.py requests
> proyecto-b\.venv\Scripts\python comprobar_entorno.py requests
```

Compara las salidas: el ejecutable, si estás dentro de un entorno, dónde se instalan los paquetes y la versión de `requests`. Con el Python del sistema, el script te dirá que `requests` **no está instalado**: es exactamente el error `ModuleNotFoundError` que aparece cuando ejecutas tu código con un Python distinto del que tiene las librerías.

> Guarda este script: cuando algo "no encuentre" una librería, ejecútalo con el mismo Python con el que ejecutas tu código.

### 4.3 Reproduce un entorno con `requirements.txt`

`pip freeze` lista **todos** los paquetes del entorno con su versión exacta. Guardado en un archivo, cualquiera puede recrear el mismo entorno:

```bash
$ cd proyecto-a
$ source .venv/bin/activate
(.venv) $ python -m pip freeze > requirements.txt
(.venv) $ cat requirements.txt
(.venv) $ deactivate
$ cd ..
$ mkdir proyecto-a-copia && cd proyecto-a-copia
$ python3 -m venv .venv
$ .venv/bin/python -m pip install -r ../proyecto-a/requirements.txt
$ .venv/bin/python -m pip list
```

```powershell
> cd proyecto-a
> .venv\Scripts\Activate.ps1
(.venv) > python -m pip freeze > requirements.txt
(.venv) > cat requirements.txt
(.venv) > deactivate
> cd ..
> mkdir proyecto-a-copia ; cd proyecto-a-copia
> python -m venv .venv
> .venv\Scripts\python -m pip install -r ..\proyecto-a\requirements.txt
> .venv\Scripts\python -m pip list
```

`proyecto-a-copia` tiene exactamente las mismas versiones que `proyecto-a`. Esa es la idea clave:

> **Lo que se guarda y se comparte es `requirements.txt`, no el `.venv`.** El entorno es desechable: si se rompe, se borra y se vuelve a crear en un minuto.

> **Windows:** si `cat requirements.txt` muestra caracteres raros, PowerShell 5 lo ha guardado en UTF-16. `pip` lo lee igualmente; para evitarlo, usa `python -m pip freeze | Out-File -Encoding utf8 requirements.txt`.

### 4.4 Usa una librería en tu notebook (opcional)

Vuelve al notebook de la práctica de las bicicletas. Para instalar un paquete en el **mismo Python que ejecuta el notebook**, lo más seguro es hacerlo desde una celda con `%pip`:

```python
%pip install rich
```

Después, reinicia el kernel (botón **Reiniciar** de la barra superior), ejecuta todo de nuevo y muestra el resultado de la práctica como una tabla:

```python
from rich.console import Console
from rich.table import Table

tabla = Table(title="Viajes por barrio de origen")
tabla.add_column("Barrio")
tabla.add_column("Viajes", justify="right")
for barrio, n in sorted(viajes_por_barrio.items(), key=lambda kv: kv[1], reverse=True):
    tabla.add_row(barrio, str(n))
Console().print(tabla)
```

`%pip` (con `%`) instala en el Python del kernel. Un `!pip` o un `pip` en la terminal podrían instalar en otro Python distinto.

**Punto de control:** tienes `proyecto-a` y `proyecto-b` con versiones distintas de `requests`, un `requirements.txt` y una copia del entorno creada a partir de él.

---

## 5. Panorama de herramientas

`venv` y `pip` son el estándar y vienen con Python, pero no son las únicas opciones. Estas son las que te encontrarás:

| Herramienta | Qué es | Cuándo tiene sentido |
|---|---|---|
| **`venv` + `pip`** | El estándar, incluido en Python | Casi siempre: es lo que usamos en el curso |
| **conda** (Anaconda, Miniconda, Miniforge) | Gestor de entornos y paquetes que también instala dependencias que **no son de Python** (librerías en C, CUDA para GPU...) y la propia versión de Python | Ciencia de datos con dependencias complejas. Anaconda tiene condiciones de licencia para su uso en organizaciones; **Miniforge** es la alternativa libre |
| **uv** | Herramienta moderna escrita en Rust: crea entornos, instala paquetes muchísimo más rápido que `pip`, gestiona versiones de Python y fija versiones exactas con un *lockfile* | Proyectos nuevos. Se está convirtiendo en el estándar de facto |
| **Poetry**, **PDM** | Gestores de proyecto completos: dependencias, entornos y publicación de paquetes | Proyectos que se publican como librerías |
| **pyenv** | Instala y alterna entre varias versiones de Python | Cuando necesitas, por ejemplo, Python 3.11 y 3.13 a la vez |
| **pipx**, **uv tool** | Instalan herramientas de terminal (como `ruff` o `httpie`) en un entorno propio cada una, disponibles en todas partes | Para herramientas, no para librerías de un proyecto |

### Más allá de `requirements.txt`

En los proyectos modernos, las dependencias se declaran en un archivo **`pyproject.toml`**, el estándar actual para describir un proyecto de Python, y las herramientas como `uv` generan un ***lockfile*** con las versiones exactas de todo. La idea es la misma que la de `requirements.txt`, pero más completa: lo verás cuando trabajemos con proyectos profesionales.

---

## 6. Buenas prácticas

- **Un entorno por proyecto**, dentro de la carpeta del proyecto y llamado `.venv`.
- **Nunca `sudo pip install`** ni instales paquetes en el Python del sistema.
- **No subas el `.venv` a Git** (añádelo al `.gitignore`) y **no lo muevas** de carpeta: contiene rutas absolutas. Si mueves el proyecto, borra el `.venv` y vuelve a crearlo.
- **Guarda las dependencias** en `requirements.txt` (o en `pyproject.toml`) y súbelas a Git.
- **Usa `python -m pip`** en lugar de `pip` a secas: así instalas seguro en el Python que vas a usar.
- **Ante un `ModuleNotFoundError`, pregúntate qué Python estás usando:** en la terminal (`which python` o `Get-Command python`), en VS Code (el intérprete o el kernel seleccionado) y con `comprobar_entorno.py`.

---

## Resumen de comandos

| Qué hago | bash / zsh | PowerShell |
|---|---|---|
| Crear un entorno | `python3 -m venv .venv` | `python -m venv .venv` |
| Activarlo | `source .venv/bin/activate` | `.venv\Scripts\Activate.ps1` |
| Desactivarlo | `deactivate` | `deactivate` |
| ¿Qué Python estoy usando? | `which python` | `Get-Command python` |
| Instalar un paquete | `python -m pip install requests` | igual |
| Instalar una versión concreta | `python -m pip install "requests==2.31.0"` | igual |
| Actualizar un paquete | `python -m pip install --upgrade requests` | igual |
| Desinstalar | `python -m pip uninstall requests` | igual |
| Ver los instalados / un paquete | `python -m pip list` · `python -m pip show requests` | igual |
| Guardar las dependencias | `python -m pip freeze > requirements.txt` | igual |
| Instalar desde un archivo | `python -m pip install -r requirements.txt` | igual |
| Usar un entorno sin activarlo | `.venv/bin/python script.py` | `.venv\Scripts\python script.py` |
| Borrar un entorno | `rm -rf .venv` | `Remove-Item -Recurse -Force .venv` |
| Instalar desde un notebook | `%pip install rich` | igual |

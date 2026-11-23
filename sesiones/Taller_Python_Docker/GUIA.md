# Taller práctico: Python y Docker

> **Guía de laboratorio.** Hoy no hay teoría nueva: vas a **practicar** lo que ya conoces. Son dos prácticas encadenadas sobre el mismo proyecto, el catálogo de datasets: primero lo terminas en Python y después lo metes en un contenedor. Si te sobra tiempo, tienes unos retos de depuración.

**Material:** [diapositivas](https://sandrohr95.github.io/laboratorio-mbd-2026/slides/Taller_Python_Docker.html) · [chuleta](CHEATSHEET.md) · [`ejercicios/catalogo-docker/`](ejercicios/catalogo-docker) · [`retos/`](retos) · [soluciones](soluciones)

## Cómo vamos a trabajar

- **Por parejas, con un solo ordenador.** Una persona escribe y la otra dicta, revisa y busca en la chuleta. **Cambiad de papel cada vez que terminéis una parte.**
- **Primero pensad, después escribid.** Antes de ejecutar un comando, decid en voz alta qué esperáis que pase.
- **Leed los errores enteros.** Casi siempre dicen qué falla y en qué línea. Los comprobadores, además, dan una pista para cada fallo.
- **Trabajad en archivos y en la terminal**, no en un notebook.
- Si os atascáis, preguntad. Pero antes, contad qué habéis probado.

En los bloques de comandos, los que empiezan por `$` son para **bash/zsh** (macOS, Linux y WSL) y los que empiezan por `>` son para **PowerShell** (Windows). No copies el `$` ni el `>`.

---

## 1. Prepara el material

### 1.1 Trae el material nuevo y abre Docker Desktop

```bash
$ cd ~/proyectos/master/laboratorio-mbd-2026
$ git pull
```

Abre **Docker Desktop** ya, para que esté arrancado cuando lo necesites. Y descarga la imagen base mientras trabajas en la primera práctica, para no esperar después:

```bash
$ docker pull python:3.13-slim
```

### 1.2 Tu carpeta del proyecto

Todo el taller se hace en **una sola carpeta**: `~/proyectos/master/catalogo-datasets`.

- **Si ya la tienes**, sigue trabajando en ella.
- **Si no la tienes**, cópiala del repositorio:

```bash
$ cd ~/proyectos/master
$ cp -r laboratorio-mbd-2026/sesiones/POO_en_Python/ejercicios/catalogo catalogo-datasets
```

```powershell
> cd ~\proyectos\master
> cp -r laboratorio-mbd-2026\sesiones\POO_en_Python\ejercicios\catalogo catalogo-datasets
```

Después, copia **dentro** de ella los archivos nuevos de la segunda práctica, y aparte, los retos:

```bash
$ cp laboratorio-mbd-2026/sesiones/Taller_Python_Docker/ejercicios/catalogo-docker/* catalogo-datasets/
$ cp -r laboratorio-mbd-2026/sesiones/Taller_Python_Docker/retos retos
$ cd catalogo-datasets
$ ls
$ code .
```

```powershell
> cp laboratorio-mbd-2026\sesiones\Taller_Python_Docker\ejercicios\catalogo-docker\* catalogo-datasets\
> cp -r laboratorio-mbd-2026\sesiones\Taller_Python_Docker\retos retos
> cd catalogo-datasets
> ls
> code .
```

**Punto de control 1:** en `catalogo-datasets` tienes `catalogo.py`, `comprobar.py`, `datos/`, `informe.py`, `requirements.txt` y `comprobar_docker.py`.

---

## 2. Práctica 1 · Termina el catálogo

Completa `catalogo.py`. **Empieza leyendo `ENUNCIADO.md`**, que está en la misma carpeta: explica el diseño de las tres clases, cómo son los datos y, para cada tarea, qué hacer, con un ejemplo de uso y su resultado. En `catalogo.py`, cada tarea está marcada con `TODO` y su número, del 1 al 16.

> **Si copiaste la carpeta hace días**, puede que no tengas `ENUNCIADO.md`. Tráelo sin tocar tu trabajo:
>
> ```bash
> $ cp ~/proyectos/master/laboratorio-mbd-2026/sesiones/POO_en_Python/ejercicios/catalogo/ENUNCIADO.md ~/proyectos/master/catalogo-datasets/
> ```
>
> Si todavía no habías empezado, copia también el `catalogo.py` nuevo, que trae todos los métodos ya declarados.

Las cinco partes:

| Parte | Qué haces |
|---|---|
| A | El `Enum` `Formato` y la *dataclass* inmutable `Dataset`, con validación y la propiedad `es_grande` |
| B | `Dataset.desde_dict()` y `a_dict()`, para convertir desde y hacia JSON |
| C | La clase `Catalogo` y la excepción `DatasetDuplicado`, con los métodos especiales |
| D | Las consultas: `buscar()`, `por_formato()`, `mas_recientes()` y `resumen()` |
| E | `Catalogo.desde_json()`, que descarta las fichas con errores, y `guardar_json()` |

Después de cada parte, ejecuta el comprobador desde la terminal integrada de VS Code:

```bash
$ python3 comprobar.py
```

En Windows, `python comprobar.py`. Si ya la tenías terminada, ejecuta el comprobador igualmente para confirmarlo y pasa a la práctica 2.

**Punto de control 2:** `comprobar.py` muestra `26 de 26 comprobaciones correctas`.

---

## 3. Práctica 2 · El catálogo en un contenedor

**Objetivo:** que cualquier persona con Docker pueda generar el informe de tu catálogo **sin instalar Python ni ninguna librería**. Al terminar, un `docker run` dejará en tu carpeta `salida/` un archivo `informe.json` generado **dentro de un contenedor**.

Los archivos nuevos son:

| Archivo | Qué es |
|---|---|
| `informe.py` | Usa tu clase `Catalogo` para mostrar un resumen en la terminal y guardarlo en `salida/informe.json`. **No lo modifiques** |
| `requirements.txt` | Su dependencia: la librería `rich`, que dibuja tablas en la terminal |
| `comprobar_docker.py` | Comprueba la práctica parte a parte. Ejecútalo con `python3 comprobar_docker.py` |

Lee `informe.py` antes de empezar: qué archivos lee, dónde escribe y qué **variables de entorno** usa.

Esta vez **no hay pasos**: cada parte dice **qué** tiene que cumplirse, y el **cómo** lo decidís vosotros. Tenéis los comandos en la chuleta.

### Parte A · Funciona en tu ordenador

Antes de meter un programa en un contenedor, tiene que funcionar fuera.

- Hay un **entorno virtual** `.venv` dentro de `catalogo-datasets`.
- Las dependencias de `requirements.txt` están instaladas **en ese entorno**, no en el Python del sistema.
- `informe.py` se ejecuta con el entorno activado, muestra la tabla y crea `salida/informe.json`.

`informe.py` necesita la variable de entorno `AUTOR`. Para dársela solo a un comando:

```bash
$ AUTOR="Tu nombre" python informe.py
```

```powershell
> $env:AUTOR = "Tu nombre"; python informe.py
```

### Parte B · El `Dockerfile` y el `.dockerignore`

Escribe un `Dockerfile` en `catalogo-datasets` que:

- Parta de la imagen oficial de **Python 3.13** en su versión reducida (`slim`).
- Trabaje en la carpeta `/app`.
- Instale las dependencias de `requirements.txt` **antes** de copiar el código, para aprovechar la caché.
- Copie **solo el código** que hace falta para generar el informe. Pista: `informe.py` importa algo más.
- Ejecute `informe.py` al arrancar.

Y un `.dockerignore` (con el punto delante) para que **nunca** acaben en la imagen ni tu entorno virtual, ni los datos, ni las salidas.

### Parte C · La imagen

- Construye la imagen con el nombre y la etiqueta **`catalogo:1.0`**.
- Dentro de la imagen tiene que estar tu código, pero no `.venv`, ni `datos`, ni `salida`. El comprobador lo mira por dentro.

### Parte D · La ejecución

Ejecuta un contenedor de `catalogo:1.0` que:

- Se **borre solo** al terminar.
- Lleve tu nombre en la variable `AUTOR` y busque `aire` con la variable `BUSCAR`.
- Lea tu carpeta `datos` del ordenador, **montada en solo lectura**: el contenedor no debe poder modificar tus datos. Piensa en **qué ruta** del contenedor busca `informe.py` la carpeta `datos`.
- Deje el informe en tu carpeta `salida` del ordenador.

**Punto de control 3:** `comprobar_docker.py` muestra todas las comprobaciones correctas y `salida/informe.json` dice `"en_docker": true`.

### Retos extra

- Muestra solo los 3 datasets más recientes con la variable `TOP`. El comprobador lo reconoce.
- Cambia el valor de `UMBRAL_GRANDE` en `catalogo.py`, reconstruye la imagen y fíjate en qué pasos salen como `CACHED`. ¿Por qué no se reinstala `rich`?
- Usa la misma imagen para ejecutar `catalogo.py` en lugar de `informe.py`, sin cambiar el `Dockerfile`.
- Construye una versión `catalogo:1.1` y lista las dos con `docker image ls catalogo`.

---

## 4. Retos de depuración

En la carpeta `retos` que copiaste en el apartado 1.2 hay cuatro programas que **no funcionan**: un `Dockerfile` que no construye, una web que no responde, un script que no encuentra sus datos y una clase con tres fallos. Las instrucciones están en su [`README.md`](retos/README.md).

---

## Problemas frecuentes

| Problema | Solución |
|---|---|
| `Cannot connect to the Docker daemon` / `error during connect` | Docker Desktop no está arrancado. Ábrelo y espera a que diga que está en marcha |
| En PowerShell, `Activate.ps1 cannot be loaded because running scripts is disabled` | Ejecuta una vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y vuelve a activar el entorno |
| `ModuleNotFoundError: No module named 'rich'` al ejecutar en tu ordenador | El entorno virtual no está activado, o instalaste las dependencias con otro Python. Activa `.venv` y repite el `pip install` |
| `ERROR: falta la variable de entorno AUTOR` | Las variables de tu terminal **no** entran en el contenedor: hay que pasarlas al ejecutar |
| `docker: invalid reference format` | Revisa las comillas del `-v` y, en PowerShell, usa `${PWD}` en lugar de `$(pwd)` |
| Cambias el código y el contenedor sigue haciendo lo de antes | La imagen tiene una **copia** del código: vuelve a construirla |
| `comprobar_docker.py` dice que el informe no se generó en un contenedor, pero `docker run` funcionó | El informe se escribió dentro del contenedor y se borró con él. ¿Qué carpeta no has montado? |

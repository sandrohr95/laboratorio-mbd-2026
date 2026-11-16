# Soluciones · Taller práctico de Python y Docker

> Consulta las soluciones **después** de haberlo intentado. Si tu solución es distinta pero los comprobadores dan todo correcto, también es válida.

| Archivo | Qué es |
|---|---|
| [`catalogo.py`](catalogo.py) | Solución de la práctica 1. Con ella, `comprobar.py` da 26 de 26 |
| [`Dockerfile`](Dockerfile) | Solución de la parte B de la práctica 2 |
| [`dockerignore`](dockerignore) | Solución de la parte B de la práctica 2. Aquí se llama `dockerignore` para que se vea; en tu carpeta tiene que llamarse `.dockerignore`, con el punto delante |

Con el `Dockerfile` y el `.dockerignore` de esta carpeta, `comprobar_docker.py` da todas las comprobaciones correctas.

---

## Práctica 1 · Catálogo de datasets

La solución completa está en [`catalogo.py`](catalogo.py). Para probarla sin perder tu trabajo, cópiala con otro nombre a tu carpeta y compárala con la tuya en VS Code (clic derecho sobre los dos archivos → *Comparar seleccionados*).

---

## Práctica 2 · El catálogo en un contenedor

### Parte A · En tu ordenador

```bash
$ cd ~/proyectos/master/catalogo-datasets
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install -r requirements.txt
(.venv) $ AUTOR="Ana" python informe.py
```

```powershell
> cd ~\proyectos\master\catalogo-datasets
> python -m venv .venv
> .venv\Scripts\Activate.ps1
(.venv) > pip install -r requirements.txt
(.venv) > $env:AUTOR = "Ana"; python informe.py
```

Sin `AUTOR`, `informe.py` termina con un error que lo explica: las variables de entorno también se usan fuera de Docker.

> **¿Y un archivo `.env`?** Python no lo lee por sí solo: `os.environ` solo tiene las variables que ya existen cuando arranca el programa. En bash o zsh puedes cargarlo con `set -a; source .env; set +a`, y en Docker, con `docker run --env-file .env ...` (en ese caso, escribe los valores **sin comillas**: `AUTOR=Ana`). Si usas un `.env`, añádelo también al `.dockerignore`.

### Parte B · `Dockerfile` y `.dockerignore`

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Primero las dependencias: esta capa se reutiliza mientras requirements.txt no cambie
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Después el código, que es lo que más cambia. Los datos NO se copian: se montan con -v
COPY catalogo.py informe.py ./

CMD ["python", "informe.py"]
```

```text
.venv/
__pycache__/
*.pyc
salida/
datos/
.git/
```

### Partes C y D · Construir y ejecutar

```bash
$ docker build -t catalogo:1.0 .
$ docker run --rm -e AUTOR="Ana" -e BUSCAR=aire \
    -v "$(pwd)/datos:/app/datos:ro" -v "$(pwd)/salida:/app/salida" catalogo:1.0
```

```powershell
> docker build -t catalogo:1.0 .
> docker run --rm -e AUTOR="Ana" -e BUSCAR=aire `
    -v "${PWD}/datos:/app/datos:ro" -v "${PWD}/salida:/app/salida" catalogo:1.0
```

- `--rm` borra el contenedor al terminar.
- `-e` pasa variables de entorno al contenedor.
- `datos` se monta en `/app/datos` porque `informe.py` busca `datos/datasets.json` de forma relativa a la carpeta de trabajo, que es `/app`. El `:ro` lo monta en solo lectura.
- `salida` también se monta: si no, el informe se escribe dentro del contenedor y desaparece con él.

### Errores frecuentes y qué enseñan

| Error | Causa | Qué enseña |
|---|---|---|
| `ERROR: falta la variable de entorno AUTOR` | No se pasa `-e AUTOR=...` | Las variables de entorno de tu ordenador **no** entran en el contenedor |
| `ERROR: no encuentro /app/datos/datasets.json` | No se monta `datos`, o se monta en otra ruta (`/datos`) | La ruta de dentro del `-v` es la carpeta de trabajo más `datos` |
| El comprobador dice que el informe no se generó en un contenedor, aunque `docker run` funcionó | No se monta `salida` | Lo que no se monta, se pierde al borrar el contenedor |
| La imagen contiene `.venv`, `datos` o `salida` | `COPY . .` sin `.dockerignore` | El contexto de `docker build` es la carpeta entera |
| `docker: invalid reference format` | En PowerShell, `$(pwd)` en lugar de `${PWD}`, o rutas con espacios sin comillas | Pon siempre comillas alrededor del `-v` |
| `ModuleNotFoundError: No module named 'catalogo'` en el contenedor | Solo se copia `informe.py` | `informe.py` importa `catalogo.py`: hay que copiar los dos |

### Retos extra

- **Solo 3 datasets recientes:** añade `-e TOP=3` al `docker run`.
- **Caché de capas:** al cambiar `UMBRAL_GRANDE` y reconstruir, el paso `pip install` sale `CACHED`, porque `requirements.txt` no ha cambiado y esa capa está antes de copiar el código.
- **Otro comando con la misma imagen:** lo que escribas después del nombre de la imagen sustituye al `CMD`:

  ```bash
  $ docker run --rm -v "$(pwd)/datos:/app/datos:ro" catalogo:1.0 python catalogo.py
  ```

- **Varias versiones:** `docker build -t catalogo:1.1 .` y después `docker image ls catalogo`.

---

## Retos de depuración

### Reto 1 · No construye

Dos fallos, uno detrás de otro:

1. `RUN pip install requirements.txt`: sin `-r`, pip busca un **paquete** llamado `requirements.txt`. Error: `No matching distribution found for requirements.txt`.
2. `CMD ["python", "main.py"]`: el archivo se llama `saludo.py`. Error al arrancar: `can't open file '/app/main.py'`.

Mejora extra: `COPY . .` antes de `pip install` invalida la caché de las dependencias con cualquier cambio en el código. Solución completa:

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY saludo.py .
CMD ["python", "saludo.py"]
```

### Reto 2 · La web no responde

El servidor escucha en `127.0.0.1`, que **dentro del contenedor** es el propio contenedor. Las conexiones que llegan por `-p` vienen de fuera y no las acepta: `curl` responde *Empty reply from server*, pero desde dentro, con `docker exec`, sí funciona. El arreglo es escuchar en todas las interfaces:

```python
HTTPServer(("0.0.0.0", 8000), Saludo)
```

Te pasará igual con cualquier servidor dentro de un contenedor: Flask, FastAPI, Jupyter, Streamlit...

### Reto 3 · No encuentra los datos

Con `WORKDIR /app`, la ruta relativa `datos/ventas.csv` es `/app/datos/ventas.csv`, pero la carpeta se montó en `/datos`. Se arregla sin tocar el código ni el `Dockerfile`:

```bash
$ docker run --rm -v "$(pwd)/datos:/app/datos:ro" reto-ventas
```

Resultado: café 4, tostada 2, té 1, zumo 1.

### Reto 4 · Las estaciones comparten bicis

Tres fallos, que aparecen en este orden:

1. `bicis = []` es un **atributo de clase**, así que todas las estaciones comparten la misma lista. Hay que crearla en `__init__`: `self.bicis = []`.
2. `len(self.bicis) > self.capacidad` deja aparcar una bici de más. Debe ser `>=`.
3. `__repr__` hace `print(...)` en lugar de `return ...`: devuelve `None`, y Python lanza `TypeError: __repr__ returned non-string`.

# Chuleta · Docker I

## Las piezas

```text
Dockerfile  --docker build-->  Imagen  --docker run-->  Contenedor
 (receta)                   (plantilla)              (imagen en marcha)
                               ^   |
                   docker pull |   | docker push
                               |   v
                     Registro (Docker Hub, GHCR...)
```

| Máquina virtual | Contenedor |
|---|---|
| Virtualiza el hardware: cada una lleva su SO completo | Comparte el núcleo del anfitrión: es un proceso aislado |
| Gigabytes, arranca en minutos | Megabytes, arranca en segundos |

## Comprobar la instalación

```bash
docker version                 # debe mostrar Client y Server
docker run hello-world
docker login                   # evita el límite de descargas anónimas
```

## Ejecutar contenedores

```bash
docker run [opciones] imagen[:etiqueta] [orden]
```

| Qué quiero | Comando |
|---|---|
| Entrar en un contenedor de usar y tirar | `docker run -it --rm python:3.13-slim` |
| Una terminal dentro de una imagen | `docker run -it --rm python:3.13-slim bash` |
| Ejecutar una sola orden | `docker run --rm python:3.13-slim python -c "print(1+1)"` |
| Un servicio en segundo plano con nombre | `docker run -d --name web nginx:alpine` |
| Publicar un puerto (anfitrión:contenedor) | `docker run -d -p 8080:80 nginx:alpine` |
| Pasar una variable de entorno | `docker run -e AUTOR="Ana" imagen` |
| Montar la carpeta actual en `/app` | `docker run -v "$(pwd):/app" -w /app imagen` |
| Montarla en solo lectura | `-v "$(pwd)/datos:/app/datos:ro"` |

En PowerShell, `$(pwd)` se escribe `${PWD}`.

## Gestionar contenedores

| Qué hago | Comando |
|---|---|
| Ver los que están en marcha / todos | `docker ps` · `docker ps -a` |
| Ver sus logs / seguirlos en directo | `docker logs web` · `docker logs -f web` |
| Abrir una terminal en uno en marcha | `docker exec -it web sh` (o `bash`) |
| Ejecutar una orden en uno en marcha | `docker exec bd psql -U postgres -c "SELECT 1;"` |
| Parar / arrancar / reiniciar | `docker stop web` · `docker start web` · `docker restart web` |
| Borrar (parado) / forzar | `docker rm web` · `docker rm -f web` |
| Pausar / reanudar | `docker pause web` · `docker unpause web` |
| Parada inmediata | `docker kill web` |
| Ver detalles (puertos, montajes, variables) | `docker inspect web` |
| Un solo campo de los detalles | `docker inspect -f '{{.State.Status}}' web` |
| Consumo de CPU y memoria | `docker stats` · `docker stats --no-stream` |
| Procesos del contenedor | `docker top web` |
| Copiar archivos (contenedor ⇄ ordenador) | `docker cp web:/ruta/archivo .` · `docker cp archivo web:/ruta/` |
| Borrar todos los parados | `docker container prune` |
| Limitar recursos al arrancar | `docker run --memory 256m --cpus 0.5 ...` |
| Reiniciar solo si falla o al encender | `docker run --restart unless-stopped ...` |
| Filtrar el listado | `docker ps -a --filter status=exited` |

**Códigos de salida** (`Exited (n)` en `docker ps -a`): `0` bien · `1` error de la aplicación · `130` Ctrl+C · `137` matado (`kill` o sin memoria).

```text
          run              stop              rm
imagen ------> en marcha ------> parado ------> borrado
                   ^                |
                   +----- start ----+
```

## Imágenes

| Qué hago | Comando |
|---|---|
| Buscar en Docker Hub | `docker search postgres` (mejor en hub.docker.com) |
| Listar | `docker images` · `docker images python` |
| Descargar sin ejecutar | `docker pull postgres:17-alpine` |
| Ver sus capas | `docker history imagen` |
| Ver su configuración | `docker image inspect -f '{{json .Config.Cmd}}' imagen` |
| Para qué procesador es | `docker image inspect -f '{{.Os}}/{{.Architecture}}' imagen` |
| Forzar otro procesador | `docker run --platform linux/amd64 ...` |
| Ponerle otro nombre | `docker tag imagen tu_usuario/imagen:1.0` |
| Subirla a Docker Hub | `docker login` y `docker push tu_usuario/imagen:1.0` |
| Borrar | `docker rmi python:3.12-slim` |
| Construir desde la carpeta actual | `docker build -t nombre:etiqueta .` |

**Nombre completo:** `registro/usuario/repositorio:etiqueta`. `python:3.13-slim` = `docker.io/library/python:3.13-slim`.

Fija siempre la etiqueta (`python:3.13-slim`, no `python`): `latest` cambia sin avisar. `slim` y `alpine` son variantes ligeras.

## Dockerfile

```dockerfile
# Imagen de partida
FROM python:3.13-slim
WORKDIR /app
# Primero lo que menos cambia: las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Después tu código
COPY . .
ENV TOP=3
EXPOSE 5000
CMD ["python", "analisis.py"]
```

`.dockerignore` (junto al Dockerfile): lo que **no** entra en el contexto.

```text
__pycache__/
.venv/
.env
.git/
```

Los comentarios (`#`) solo valen al principio de una línea, nunca detrás de una instrucción.

| Instrucción | Para qué | Cuándo |
|---|---|---|
| `FROM` | Imagen base | Construir |
| `WORKDIR` | Carpeta de trabajo (la crea si no existe) | Construir |
| `COPY` | Copiar archivos del contexto a la imagen | Construir |
| `RUN` | Ejecutar órdenes (instalar paquetes…) | Construir |
| `ENV` | Variables de entorno | Construir y ejecutar |
| `EXPOSE` | Documenta el puerto (no lo publica: eso es `-p`) | Informativo |
| `CMD` | Orden por defecto; lo que escribes tras la imagen en `docker run` la **sustituye** | Ejecutar |
| `ENTRYPOINT` | Programa que siempre se ejecuta; lo que escribes tras la imagen se **añade** como argumentos | Ejecutar |

`CMD` y `ENTRYPOINT`, siempre en forma JSON: `["python", "app.py"]`. Una aplicación web en un contenedor debe escuchar en `0.0.0.0`, no en `127.0.0.1`.

**Caché:** cada instrucción es una capa. Docker reconstruye desde la primera que cambia hasta el final. Pon primero lo que menos cambia.

## Imágenes útiles

| Imagen | Para qué | Ejemplo |
|---|---|---|
| `python:3.13-slim` | Python | `docker run -it --rm python:3.13-slim` |
| `nginx:alpine` | Servidor web | `docker run -d -p 8080:80 nginx:alpine` |
| `postgres:17-alpine` | Base de datos PostgreSQL | `docker run -d -e POSTGRES_PASSWORD=master -p 5432:5432 postgres:17-alpine` |
| `alpine` | Linux mínimo para probar órdenes | `docker run --rm alpine cat /etc/os-release` |
| `redis:alpine` | Base de datos clave-valor | `docker run -d --name cache redis:alpine` |
| `quay.io/jupyter/scipy-notebook` | JupyterLab con NumPy, pandas, scikit-learn | `docker run -it --rm -p 8888:8888 quay.io/jupyter/scipy-notebook` |

## Limpieza

```bash
docker system df               # cuánto ocupa todo
docker container prune         # borra los contenedores parados
docker image prune             # borra las imágenes sin nombre
docker image prune -a          # borra todas las que no usa ningún contenedor
docker system prune            # limpieza general (pregunta antes)
```

## Docker Desktop: recursos

**Settings → Resources:** CPU, memoria y swap para **todos** los contenedores juntos. En Windows con WSL2, en `C:\Users\tu_usuario\.wslconfig` (`memory=4GB`, `processors=2`) y después `wsl --shutdown`.

# Chuleta · Docker I

## Las piezas

```
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
| Ver detalles (IP, montajes, variables) | `docker inspect web` |
| Consumo de CPU y memoria | `docker stats` |

```
          run              stop              rm
imagen ------> en marcha ------> parado ------> borrado
                   ^                |
                   +----- start ----+
```

## Imágenes

| Qué hago | Comando |
|---|---|
| Listar | `docker images` |
| Descargar sin ejecutar | `docker pull postgres:17-alpine` |
| Borrar | `docker rmi python:3.12-slim` |
| Ver sus capas | `docker history imagen` |
| Construir desde la carpeta actual | `docker build -t nombre:etiqueta .` |

Fija siempre la etiqueta (`python:3.13-slim`, no `python`): `latest` cambia sin avisar. `slim` y `alpine` son variantes ligeras.

## Dockerfile

```dockerfile
FROM python:3.13-slim                                # imagen de partida
WORKDIR /app                                         # carpeta de trabajo
COPY requirements.txt .                              # 1.º lo que menos cambia
RUN pip install --no-cache-dir -r requirements.txt   # se ejecuta al construir
COPY . .                                             # 2.º tu código
ENV TOP=3                                            # variable con valor por defecto
CMD ["python", "analisis.py"]                        # se ejecuta al arrancar
```

| Instrucción | Para qué | Cuándo |
|---|---|---|
| `FROM` | Imagen base | Construir |
| `WORKDIR` | Carpeta de trabajo (la crea si no existe) | Construir |
| `COPY` | Copiar archivos del contexto a la imagen | Construir |
| `RUN` | Ejecutar órdenes (instalar paquetes…) | Construir |
| `ENV` | Variables de entorno | Construir y ejecutar |
| `CMD` | Orden por defecto del contenedor | Ejecutar |

**Caché:** cada instrucción es una capa. Docker reconstruye desde la primera que cambia hasta el final. Pon primero lo que menos cambia.

## Imágenes útiles

| Imagen | Para qué | Ejemplo |
|---|---|---|
| `python:3.13-slim` | Python | `docker run -it --rm python:3.13-slim` |
| `nginx:alpine` | Servidor web | `docker run -d -p 8080:80 nginx:alpine` |
| `postgres:17-alpine` | Base de datos PostgreSQL | `docker run -d -e POSTGRES_PASSWORD=master postgres:17-alpine` |
| `alpine` | Linux mínimo para probar órdenes | `docker run --rm alpine cat /etc/os-release` |

## Limpieza

```bash
docker system df               # cuánto ocupa todo
docker container prune         # borra los contenedores parados
docker image prune             # borra las imágenes sin nombre
docker system prune            # limpieza general (pregunta antes)
```

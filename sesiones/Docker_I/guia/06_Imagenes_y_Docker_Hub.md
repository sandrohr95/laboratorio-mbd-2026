# 6 · Imágenes y Docker Hub

Anterior: [5 · Gestión de contenedores](05_Gestion_contenedores.md) · [Índice](../GUIA.md) · Siguiente: [7 · Dockerfile y docker build](07_Dockerfile.md)

Hasta ahora las imágenes se descargaban solas al hacer `docker run`. En este capítulo aprendes a gestionarlas: buscarlas, descargarlas, ver qué hay dentro, etiquetarlas, subirlas a Docker Hub y borrarlas.

---

## 6.1 Buscar imágenes

La forma más cómoda es la web de [Docker Hub](https://hub.docker.com). Busca, por ejemplo, *postgres* y abre la imagen oficial. En su página encontrarás:

- **Overview:** cómo se usa, qué variables de entorno acepta, qué puertos expone y dónde guarda los datos.
- **Tags:** todas las etiquetas disponibles, con su tamaño y para qué procesadores existe cada una.
- La insignia **Docker Official Image**, que indica que es la imagen oficial.

También se puede buscar desde la terminal, aunque con menos información:

```bash
$ docker search postgres --limit 5
```

La columna `OFFICIAL` marca con `[OK]` la imagen oficial.

> **Antes de usar una imagen de la comunidad**, mira cuántas descargas tiene, cuándo se actualizó por última vez y si su Dockerfile es público. Una imagen es código que ejecutas en tu ordenador.

---

## 6.2 Descargar y listar imágenes

```bash
$ docker pull python:3.13-slim          # descarga sin ejecutar
$ docker pull python:3.12-slim
$ docker images                          # o docker image ls
```

```text
IMAGE              ID             DISK USAGE   CONTENT SIZE   EXTRA
nginx:alpine       a3554c0d0b48       94.1MB         26.2MB   U
python:3.12-slim   5e9b0c1a7f3d        198MB         44.9MB
python:3.13-slim   d98cc29d3266        204MB         45.5MB
```

| Columna | Qué significa |
|---|---|
| `IMAGE` | Nombre y etiqueta |
| `ID` | Identificador de la imagen (los primeros caracteres de su huella) |
| `DISK USAGE` | Lo que ocupa en tu disco, descomprimida |
| `CONTENT SIZE` | Lo que se descarga, comprimida |
| `EXTRA` | Una `U` indica que algún contenedor la está usando (*in use*) |

Con versiones de Docker anteriores a la 29, las columnas son `REPOSITORY`, `TAG`, `IMAGE ID`, `CREATED` y `SIZE`, pero la información es la misma.

Al descargar la segunda imagen de Python es posible que algunas capas aparezcan como *Already exists*: las dos comparten capas, y Docker no vuelve a descargarlas.

Filtrar el listado:

```bash
$ docker images python                  # solo las de un repositorio
$ docker images --format "{{.Repository}}:{{.Tag}}  {{.Size}}"
```

---

## 6.3 Qué hay dentro de una imagen

### Sus capas: `docker history`

```bash
$ docker history python:3.13-slim
$ docker history nginx:alpine
```

Cada fila es una capa, de la más reciente (arriba) a la más antigua (abajo), con la instrucción que la creó y su tamaño. Las de `0B` solo cambian metadatos, como `CMD` o `ENV`.

### Su configuración: `docker image inspect`

```bash
$ docker image inspect python:3.13-slim
$ docker image inspect -f '{{.Os}}/{{.Architecture}}' python:3.13-slim
$ docker image inspect -f '{{json .Config.Env}}' python:3.13-slim
$ docker image inspect -f '{{json .Config.Cmd}}' python:3.13-slim
```

Así sabes, sin ejecutarla, con qué orden arranca, qué variables trae y para qué procesador es.

### Procesadores distintos: amd64 y arm64

Las imágenes se compilan para un tipo de procesador concreto. Los dos más habituales son **amd64** (Intel y AMD, la mayoría de portátiles con Windows y los servidores) y **arm64** (Mac con Apple Silicon, Raspberry Pi y cada vez más servidores en la nube).

Las imágenes oficiales son **multiplataforma**: el mismo nombre sirve para los dos procesadores, y Docker descarga automáticamente la variante del tuyo. Compruébalo: en un Mac M1 el comando anterior dice `linux/arm64`, y en un portátil con Intel, `linux/amd64`.

Si una imagen solo existe para amd64 y tienes un Mac con Apple Silicon, verás el error *no matching manifest for linux/arm64*. Se puede forzar la otra plataforma, que funcionará con emulación (más lenta):

```bash
$ docker run --rm --platform linux/amd64 alpine uname -m      # x86_64, emulado
```

---

## 6.4 Etiquetas y digests

Una etiqueta es solo un **nombre que apunta a una imagen**, como una rama en Git: puede cambiar. Mañana, `python:3.13-slim` puede apuntar a una versión con un parche de seguridad nuevo. Por eso conviene saber qué tipos de etiqueta hay:

| Etiqueta | Ejemplo | Estabilidad |
|---|---|---|
| `latest` | `python:latest` | Ninguna: hoy 3.14, mañana 3.15 |
| Versión mayor | `python:3`, `postgres:17` | Cambia dentro de esa versión |
| Versión menor | `python:3.13-slim` | Solo recibe parches. **La recomendada** |
| Versión exacta | `python:3.13.17-slim` | Casi fija |

Para una reproducibilidad total se usa el **digest**, la huella SHA-256 del contenido, que nunca cambia:

```bash
$ docker images --digests python
$ docker pull python@sha256:<el digest que veas>
```

### Poner tus propias etiquetas: `docker tag`

`docker tag` crea un nombre nuevo para una imagen que ya tienes. No copia nada: las dos etiquetas apuntan al mismo ID.

```bash
$ docker tag python:3.13-slim mi-python:base
$ docker images                        # mi-python:base tiene el mismo IMAGE ID
```

---

## 6.5 Subir una imagen a Docker Hub

Para subir una imagen a tu cuenta, su nombre tiene que empezar por **tu usuario de Docker Hub**. Prueba con una imagen pequeña:

```bash
$ docker login
$ docker pull alpine
$ docker tag alpine tu_usuario/mi-alpine:1.0
$ docker push tu_usuario/mi-alpine:1.0
```

(Sustituye `tu_usuario` por tu nombre de usuario real). Entra en <https://hub.docker.com> y verás el repositorio `mi-alpine` en tu cuenta. Por defecto es **público**: cualquiera puede descargarlo con `docker pull tu_usuario/mi-alpine:1.0`. Las cuentas gratuitas permiten también un repositorio privado.

Fíjate en que el `push` dice *Mounted from library/alpine* o *Layer already exists*: Docker Hub ya tiene esas capas y no hace falta volver a subirlas.

> **Nunca subas a un repositorio público una imagen con contraseñas, claves o datos personales dentro.** Todo lo que copias en una imagen viaja con ella, y las capas se pueden inspeccionar.

En el capítulo 7 construirás tu propia imagen, y en la práctica final podrás subirla.

---

## 6.6 Borrar imágenes y liberar espacio

```bash
$ docker rmi python:3.12-slim          # o docker image rm
$ docker rmi mi-python:base            # borra solo la etiqueta si hay otras apuntando al mismo ID
$ docker image prune                   # borra las imágenes «colgadas» (sin nombre, restos de builds)
$ docker image prune -a                # borra TODAS las imágenes que no use ningún contenedor
$ docker system df                     # cuánto ocupan imágenes, contenedores, volúmenes y caché
$ docker system prune                  # limpieza general: contenedores parados, redes, imágenes colgadas y caché
```

No se puede borrar una imagen que esté usando un contenedor, aunque esté parado: primero hay que borrar el contenedor (o usar `docker rmi -f`).

Las imágenes ocupan mucho disco. Haz `docker system df` de vez en cuando, y `docker system prune` cuando ocupen demasiado.

---

## 6.7 Exportar e importar sin registro (opcional)

Si necesitas llevar una imagen a un ordenador sin conexión, puedes guardarla en un archivo:

```bash
$ docker save -o alpine.tar alpine:latest       # imagen → archivo
$ docker load -i alpine.tar                     # archivo → imagen
```

---

## Práctica · Retos con imágenes

1. Descarga `python:3.13-slim`, `python:3.13-alpine` y `python:3.13`. Ordénalas por tamaño. ¿Cuánto más ocupa la completa que la `slim`?
2. ¿Con qué orden arranca por defecto la imagen `nginx:alpine`? ¿Y `postgres:17-alpine`? Averígualo **sin ejecutarlas**.
3. ¿Cuántas capas tiene `python:3.13-slim`? ¿Cuál es la más grande?
4. ¿Para qué procesador es tu `python:3.13-slim`? ¿Para cuál sería el de tu compañero o compañera de al lado?
5. Etiqueta `alpine` como `tu_usuario/mi-alpine:1.0` y súbela a tu cuenta de Docker Hub. Pide a alguien que la descargue.
6. Borra las imágenes de los retos que ya no vayas a usar y comprueba cuánto espacio has liberado con `docker system df`.

**Punto de control 6:** sabes explicar qué es una etiqueta, por qué conviene fijar la versión y qué hace falta para subir una imagen a Docker Hub.

## Para saber más

- [Referencia de comandos de imágenes](https://docs.docker.com/reference/cli/docker/image/)
- [Repositorios de Docker Hub](https://docs.docker.com/docker-hub/repos/)
- [Imágenes multiplataforma](https://docs.docker.com/build/building/multi-platform/)

---

Anterior: [5 · Gestión de contenedores](05_Gestion_contenedores.md) · [Índice](../GUIA.md) · Siguiente: [7 · Dockerfile y docker build](07_Dockerfile.md)

# 4 · Ejecutar contenedores

Anterior: [3 · Conceptos básicos](03_Conceptos.md) · [Índice](../GUIA.md) · Siguiente: [5 · Gestión de contenedores](05_Gestion_contenedores.md)

Toca practicar. En este capítulo ejecutas contenedores a partir de imágenes que ya existen en Docker Hub: un Python que no tienes instalado, un Linux mínimo, un servidor web y una base de datos. Por el camino aprendes las opciones más usadas de `docker run`.

---

## 4.1 Qué ha pasado con `hello-world`

Vuelve a ejecutar la prueba de la instalación y lee la salida con calma:

```bash
$ docker run hello-world
```

```text
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
Digest: sha256:...
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

Paso a paso:

1. El **cliente** `docker` pide al **Engine** que ejecute la imagen `hello-world`.
2. El Engine busca la imagen en tu ordenador y no la encuentra: *Unable to find image locally*. Fíjate en que ha añadido la etiqueta `latest`, porque no indicaste ninguna.
3. La **descarga** de Docker Hub (*Pulling from library/hello-world*; `library` indica que es oficial).
4. **Crea un contenedor** a partir de la imagen.
5. **Lo arranca.** El programa que contiene escribe el mensaje y termina.
6. Como el programa ha terminado, el contenedor **se detiene**. No se borra: sigue existiendo, parado.

Ejecútalo otra vez: ahora no descarga nada, porque la imagen ya está en tu ordenador. Y cada ejecución crea un contenedor **nuevo**. Compruébalo:

```bash
$ docker ps -a
```

Verás un contenedor `hello-world` por cada vez que lo has ejecutado, todos con estado *Exited (0)*. El `0` es el código de salida del programa: terminó sin errores.

---

## 4.2 Anatomía de `docker run`

```text
docker run  [opciones]   imagen[:etiqueta]   [orden y argumentos]
docker run  -it --rm     python:3.13-slim    python -c "print(1)"
```

- **Opciones:** cómo quieres ejecutarlo. Van **antes** de la imagen.
- **Imagen:** qué ejecutar.
- **Orden:** opcional. Si la escribes, sustituye a la orden por defecto de la imagen. Todo lo que va **después** de la imagen se pasa al contenedor, no a Docker.

Las opciones que más vas a usar:

| Opción | Qué hace |
|---|---|
| `-i` y `-t` (juntas, `-it`) | Modo interactivo: conecta tu teclado y tu terminal con el contenedor |
| `--rm` | Borra el contenedor automáticamente cuando termina |
| `-d` | Lo ejecuta en segundo plano (*detached*) y te devuelve la terminal |
| `--name nombre` | Le pone un nombre. Si no, Docker inventa uno, como `happy_turing` |
| `-p 8080:80` | Publica un puerto: **anfitrión:contenedor** |
| `-e CLAVE=valor` | Define una variable de entorno dentro del contenedor |
| `-v origen:destino` | Monta una carpeta de tu ordenador dentro del contenedor (capítulo 8) |
| `-w /carpeta` | Carpeta de trabajo dentro del contenedor |

---

## 4.3 Contenedores interactivos: un Python que no tienes

Compara tu Python con el de un contenedor:

```bash
$ python3 --version                        # en Windows: python --version
$ docker run -it --rm python:3.13-slim
```

Se abre el intérprete de Python 3.13, tengas la versión que tengas en tu ordenador. Explora un poco:

```python
>>> import sys, platform
>>> sys.version
>>> platform.system(), platform.machine()   # ('Linux', ...): estás dentro de Linux
>>> exit()
```

Al salir del intérprete termina el proceso principal, el contenedor se detiene y, gracias a `--rm`, se borra. Prueba ahora otras versiones sin instalar nada:

```bash
$ docker run --rm python:3.12-slim python --version
$ docker run --rm python:3.14-slim python --version
```

Aquí no hace falta `-it`, porque no vas a escribir nada: el contenedor ejecuta la orden, muestra el resultado y termina.

### Una terminal dentro de un contenedor

En lugar de Python, puedes pedirle una terminal `bash`:

```bash
$ docker run -it --rm python:3.13-slim bash
```

Ahora estás «dentro». Mira a tu alrededor:

```bash
root@3f2a9c1b7d4e:/# cat /etc/os-release      # ¿qué Linux hay en la imagen?
root@3f2a9c1b7d4e:/# whoami                   # eres root, pero solo dentro del contenedor
root@3f2a9c1b7d4e:/# hostname                 # el nombre de la máquina es el ID del contenedor
root@3f2a9c1b7d4e:/# ls /
root@3f2a9c1b7d4e:/# exit
```

Una prueba de los *namespaces*: tu ordenador tiene cientos de procesos en marcha, pero un contenedor solo ve los suyos. La imagen `slim` no trae la orden `ps`, así que pruébalo con Alpine:

```bash
$ docker run --rm alpine ps aux
```

Solo aparece un proceso, el propio `ps`, y es el número 1.

### Lo que pasa dentro, se queda dentro

```bash
$ docker run -it --rm python:3.13-slim bash
root@...:/# echo "hola" > /tmp/nota.txt
root@...:/# cat /tmp/nota.txt
root@...:/# exit
$ docker run -it --rm python:3.13-slim bash
root@...:/# cat /tmp/nota.txt                 # No such file or directory
root@...:/# exit
```

El archivo ha desaparecido. Cada `docker run` crea un contenedor **nuevo** a partir de la imagen, que no ha cambiado. El archivo vivía en la capa de escritura del primer contenedor, y esa capa se borró con él.

### Un Linux de pocos megas

[`alpine`](https://hub.docker.com/_/alpine) es una distribución Linux minúscula, muy usada como base de imágenes:

```bash
$ docker run --rm alpine cat /etc/os-release
$ docker run --rm alpine ls /bin
$ docker run -it --rm alpine sh               # Alpine trae sh, no bash
```

---

## 4.4 Contenedores en segundo plano: un servidor web

Los servidores (web, bases de datos) no terminan: se quedan esperando peticiones. Para no bloquear la terminal, se ejecutan en segundo plano con `-d`.

```bash
$ docker run -d --name web -p 8080:80 nginx:alpine
```

La terminal te devuelve el **ID** del contenedor, una cadena larga como `3f2a9c1b7d4e…`, y queda libre. Comprueba que está en marcha:

```bash
$ docker ps
```

```text
CONTAINER ID   IMAGE          COMMAND                  STATUS         PORTS                  NAMES
3f2a9c1b7d4e   nginx:alpine   "/docker-entrypoint.…"   Up 5 seconds   0.0.0.0:8080->80/tcp   web
```

Abre <http://localhost:8080> en el navegador: es la página de bienvenida de nginx, servida desde el contenedor.

### Publicar puertos con `-p`

![Publicación de puertos](../img/puertos.svg)

Cada contenedor tiene su propia red aislada. nginx escucha en el puerto 80 **del contenedor**, y desde tu ordenador no se llega a él… salvo que lo **publiques**. `-p 8080:80` conecta el puerto 8080 de tu ordenador con el 80 del contenedor. La regla para recordarlo: **fuera:dentro**.

Algunas consecuencias:

- Puedes publicar el mismo puerto interno en puertos externos distintos: `-p 8081:80`, `-p 8082:80`… y tener varios nginx a la vez.
- No puedes usar **dos veces el mismo puerto externo**: el segundo contenedor fallará con *port is already allocated*.
- Si no pones `-p`, el servicio funciona, pero solo es accesible desde dentro de la red de Docker.

Haz la prueba: arranca un segundo nginx en otro puerto y abre los dos en el navegador.

```bash
$ docker run -d --name web2 -p 8081:80 nginx:alpine
```

Cuando termines, bórralos (el capítulo 5 explica estos comandos en detalle):

```bash
$ docker rm -f web web2
```

---

## 4.5 Variables de entorno: una base de datos en un minuto

Muchas imágenes se configuran con **variables de entorno**, que se pasan con `-e`. Cada imagen documenta las suyas en su página de Docker Hub. Abre la de [`postgres`](https://hub.docker.com/_/postgres) y busca la sección *Environment Variables*: `POSTGRES_PASSWORD` es obligatoria.

```bash
$ docker run -d --name bd -e POSTGRES_PASSWORD=master postgres:17-alpine
$ docker logs bd
```

Espera a ver en los logs *database system is ready to accept connections*. Ahora abre la consola de PostgreSQL **dentro del contenedor**:

```bash
$ docker exec -it bd psql -U postgres
```

```sql
postgres=# CREATE TABLE ciudades (nombre text, habitantes int);
postgres=# INSERT INTO ciudades VALUES ('Málaga', 592000), ('Sevilla', 684000);
postgres=# SELECT * FROM ciudades;
postgres=# \q
```

Acabas de usar PostgreSQL sin instalarlo. `docker exec` ejecuta una orden dentro de un contenedor que ya está en marcha; lo verás con más detalle en el capítulo 5.

Ahora comprueba qué pasa con los datos si borras el contenedor y creas otro igual:

```bash
$ docker rm -f bd
$ docker run -d --name bd -e POSTGRES_PASSWORD=master postgres:17-alpine
$ docker exec -it bd psql -U postgres -c "SELECT * FROM ciudades;"
```

*ERROR: relation "ciudades" does not exist*. **Los datos vivían en la capa de escritura del contenedor y se fueron con él.** Para que una base de datos guarde sus datos hacen falta **volúmenes**, que veremos más adelante en el curso. Por ahora, bórralo:

```bash
$ docker rm -f bd
```

### Conectarte desde tu ordenador

Hasta ahora has entrado en la base de datos **desde dentro** del contenedor, con `docker exec`. Pero si quieres usarla desde un programa de tu ordenador (un script de Python, DBeaver, la extensión de PostgreSQL de VS Code…), te pasará lo mismo que con nginx: Postgres escucha en el puerto 5432 **del contenedor**, y sin `-p` no se llega a él desde fuera. Créalo publicando el puerto:

```bash
$ docker run -d --name bd -e POSTGRES_PASSWORD=master -p 5432:5432 postgres:17-alpine
```

Ahora cualquier cliente de tu ordenador puede conectarse con estos datos:

| Dato | Valor |
|------|-------|
| Servidor | `localhost` |
| Puerto | `5432` (el de la izquierda de `-p`) |
| Usuario | `postgres` |
| Contraseña | `master` (la de `POSTGRES_PASSWORD`) |
| Base de datos | `postgres` |

Por ejemplo, desde Python, con tu entorno virtual activado:

```bash
$ pip install "psycopg[binary]"
```

```python
import psycopg

with psycopg.connect("postgresql://postgres:master@localhost:5432/postgres") as con:
    print(con.execute("SELECT version();").fetchone()[0])
```

Fíjate en dos diferencias con `docker exec`:

- Desde fuera **sí se pide la contraseña**. Dentro del contenedor, la imagen oficial confía en las conexiones locales y `psql` entra sin ella.
- En `psql -U postgres`, la opción `-U` es de `psql` e indica el **usuario de la base de datos**. No tiene nada que ver con Docker: todo lo que escribes después del nombre del contenedor se le pasa tal cual al programa.

Si ya tienes PostgreSQL instalado en tu ordenador, el puerto 5432 estará ocupado (*port is already allocated*) o, peor, te conectarás al Postgres de tu ordenador sin darte cuenta. La solución es la misma que con los dos nginx: cambia el puerto de **fuera** y deja el de dentro.

```bash
$ docker run -d --name bd -e POSTGRES_PASSWORD=master -p 5433:5432 postgres:17-alpine
```

Y en la conexión usa `localhost:5433`. Cuando termines, bórralo con `docker rm -f bd`.

> Usa contraseñas sencillas como `master` **solo en tu ordenador y para practicar**. Nunca en un servidor accesible desde internet.

---

## 4.6 Elegir la imagen: etiquetas y variantes

En la página de cada imagen oficial, la sección *Supported tags* lista todas las etiquetas. Para `python`, por ejemplo:

| Etiqueta | Qué es | Tamaño aproximado |
|---|---|---|
| `python:3.13` | Debian completo con herramientas de compilación | ~1 GB |
| `python:3.13-slim` | Debian recortado. **La opción recomendada** para casi todo | ~200 MB |
| `python:3.13-alpine` | Sobre Alpine. Muy pequeña, pero algunas librerías científicas dan problemas al instalarse | ~60 MB |
| `python:latest` | La última versión publicada. **Cambia sin avisar** | ~1 GB |

Dos reglas prácticas:

1. **Fija siempre la versión** (`python:3.13-slim`, `postgres:17-alpine`). Con `latest`, el mismo comando puede darte otra versión dentro de unos meses y romper tu proyecto.
2. Para Python, empieza por **`slim`**. Para servicios como nginx o Redis, `alpine` suele ser perfecta.

---

## 4.7 Opcional: Jupyter en un contenedor

Si tienes buena conexión (la imagen pesa más de 1 GB), prueba un entorno de ciencia de datos completo sin instalar nada:

```bash
$ docker run -it --rm -p 8888:8888 quay.io/jupyter/scipy-notebook
```

En la salida aparece una dirección como `http://127.0.0.1:8888/lab?token=...`. Ábrela en el navegador: tienes JupyterLab con NumPy, pandas, Matplotlib y scikit-learn. Ojo: lo que guardes ahí se pierde al parar el contenedor, porque hemos usado `--rm` y no hemos montado ninguna carpeta. Para pararlo, pulsa `Ctrl+C` en la terminal.

---

## Práctica · Retos con imágenes de Docker Hub

Resuélvelos con lo que has visto. Cada uno se resuelve con uno o dos comandos.

1. Comprueba la versión de Python de la imagen `python:3.12-slim` en una sola orden y sin que quede ningún contenedor.
2. ¿Qué versión de Alpine trae la imagen `alpine`? ¿Y la imagen `nginx:alpine`?
3. Arranca dos servidores nginx, `web1` y `web2`, en los puertos 8081 y 8082. Comprueba que los dos responden.
4. Intenta arrancar un tercer nginx en el puerto 8081. ¿Qué error da y por qué?
5. Busca en Docker Hub la imagen oficial de **Redis**. Arráncala en segundo plano con el nombre `cache`, abre `redis-cli` dentro con `docker exec`, guarda una clave (`SET saludo hola`) y léela (`GET saludo`).
6. Ejecuta `docker run --rm -e NOMBRE=Ana alpine sh -c 'echo "Hola, $NOMBRE"'`. ¿Qué hace `-e`? ¿Por qué hay comillas simples por fuera?

**Punto de control 4:** sabes explicar qué hacen `-it`, `--rm`, `-d`, `--name`, `-p` y `-e`, y has abierto nginx en el navegador.

## Para saber más

- [Referencia de `docker run`](https://docs.docker.com/reference/cli/docker/container/run/)
- [Publicar puertos](https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/)
- [Variables de entorno en contenedores](https://docs.docker.com/get-started/docker-concepts/running-containers/overriding-container-defaults/)

---

Anterior: [3 · Conceptos básicos](03_Conceptos.md) · [Índice](../GUIA.md) · Siguiente: [5 · Gestión de contenedores](05_Gestion_contenedores.md)

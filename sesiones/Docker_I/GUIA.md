# Docker I · Primeros contenedores

> **Guía de laboratorio.** Síguela durante la clase a la vez que las diapositivas. Cada bloque termina con un **punto de control**: si no lo superas, avisa antes de seguir.

**Material:** [diapositivas](https://sandrohr95.github.io/laboratorio-mbd-2026/slides/Docker_I.html) · [chuleta](CHEATSHEET.md) · [`ejemplos/`](ejemplos/) · [`ejercicios/bicis-docker/`](ejercicios/bicis-docker/)

**Qué vas a hacer:** entender qué problema resuelve Docker y en qué se diferencia de una máquina virtual; instalarlo; arrancar, inspeccionar y borrar contenedores de Python, nginx y PostgreSQL; escribir tus propios Dockerfiles; y empaquetar un análisis de datos para que funcione igual en cualquier ordenador.

En los bloques de comandos, los que empiezan por `$` son para **bash/zsh** (macOS, Linux y WSL) y los que empiezan por `>` son para **PowerShell** (Windows). No copies el `$` ni el `>`. Cuando un comando es igual en los dos, solo aparece con `$`.

Algunos comandos son largos y se parten en varias líneas. En bash/zsh, cada línea partida termina en `\`; en PowerShell, en `` ` `` (acento grave). También puedes escribirlos en una sola línea.

---

## Antes de empezar · Actualiza el material

Trae el material nuevo del repositorio del curso y copia la carpeta de la sesión a tu zona de trabajo, para no tocar el clon:

```bash
$ cd ~/proyectos/master/laboratorio-mbd-2026
$ git pull
$ mkdir -p ~/proyectos/master/docker-lab
$ cp -r sesiones/Docker_I/ejemplos sesiones/Docker_I/ejercicios ~/proyectos/master/docker-lab/
$ cd ~/proyectos/master/docker-lab
```

```powershell
> cd ~\proyectos\master\laboratorio-mbd-2026
> git pull
> mkdir ~\proyectos\master\docker-lab
> cp -r sesiones\Docker_I\ejemplos, sesiones\Docker_I\ejercicios ~\proyectos\master\docker-lab\
> cd ~\proyectos\master\docker-lab
```

Abre la carpeta en VS Code (`code .`) e instala la extensión **Container Tools** (o **Docker**) de Microsoft: resalta los Dockerfiles y muestra tus imágenes y contenedores en la barra lateral.

---

## Bloque 1 · El problema y la idea

### 1.1 «En mi máquina funciona»

Tu análisis funciona en tu portátil, pero al pasárselo a otra persona falla. Las causas casi siempre son las mismas:

- **Otra versión de Python** (3.11 frente a 3.13) o de una librería (`pandas` 1.x frente a 2.x).
- **Otro sistema operativo**: rutas con `\` o `/`, librerías del sistema que en Windows no existen.
- **Servicios que faltan**: el script necesita una base de datos PostgreSQL que solo está instalada en tu ordenador.
- **Pasos que nadie apuntó**: «ah, antes tienes que instalar esto y poner esta variable».

Un entorno virtual (`venv`) resuelve solo una parte: aísla los **paquetes de Python**, pero no la versión de Python ni el sistema operativo ni los servicios. Docker va un paso más allá y empaqueta **todo el entorno**: sistema base, versión de Python, librerías, tu código y la orden para arrancarlo.

### 1.2 Máquina virtual frente a contenedor

```
        MÁQUINAS VIRTUALES                       CONTENEDORES
  +-------------+ +-------------+         +-------------+ +-------------+
  |    App A    | |    App B    |         |    App A    | |    App B    |
  |  Librerías  | |  Librerías  |         |  Librerías  | |  Librerías  |
  | SO invitado | | SO invitado |         +-------------+ +-------------+
  +-------------+ +-------------+         |        Docker Engine        |
  |         Hipervisor          |         +-----------------------------+
  +-----------------------------+         | SO anfitrión (núcleo Linux) |
  |        SO anfitrión         |         +-----------------------------+
  +-----------------------------+         |          Hardware           |
  |          Hardware           |         +-----------------------------+
  +-----------------------------+
```

| | Máquina virtual | Contenedor |
|---|---|---|
| Qué virtualiza | El **hardware**: cada VM lleva su propio sistema operativo completo | El **sistema operativo**: todos comparten el núcleo del anfitrión |
| Tamaño | Gigabytes | Megabytes |
| Arranque | Minutos | Segundos o menos |
| Aislamiento | Muy fuerte | Fuerte, pero comparten núcleo |
| Ejemplos | VirtualBox, VMware, Hyper-V, Parallels | Docker, Podman |

Un contenedor es, en el fondo, un **proceso normal** del sistema al que el núcleo de Linux le pone unas «anteojeras»: solo ve sus propios archivos, procesos y red (*namespaces*) y solo puede gastar la memoria y la CPU que se le permitan (*cgroups*). Por eso arranca tan rápido: no hay que encender ningún sistema operativo.

Las máquinas virtuales no desaparecen: siguen siendo la opción cuando necesitas otro sistema operativo completo (por ejemplo, Windows dentro de un Mac) o un aislamiento máximo. Y en la nube, tus contenedores suelen ejecutarse dentro de máquinas virtuales.

### 1.3 Las piezas de Docker

- **Imagen:** una plantilla de solo lectura con todo lo necesario para ejecutar algo (sistema base, Python, librerías, código). Se construye por **capas**, como una pila de transparencias.
- **Contenedor:** una imagen **en marcha**. De una misma imagen puedes arrancar muchos contenedores, cada uno con su propia capa de escritura. Si borras el contenedor, lo que escribió dentro se pierde.
- **Registro:** un almacén de imágenes. El público por defecto es [Docker Hub](https://hub.docker.com); hay otros, como GitHub Container Registry.
- **Dockerfile:** la receta, en texto, para construir una imagen.
- **Docker Engine:** el servicio (*daemon*) que construye imágenes y ejecuta contenedores. Tú le hablas con el **cliente** `docker` desde la terminal.
- **Docker Desktop:** la aplicación para macOS y Windows. Los contenedores necesitan un núcleo Linux, así que Docker Desktop arranca una **pequeña máquina virtual Linux** (en Windows, mediante WSL2) con Docker Engine dentro, y añade una interfaz gráfica.

Una analogía de cocina: el **Dockerfile** es la receta, la **imagen** es el plato congelado y envasado, el **contenedor** es una ración calentada y servida, y el **registro** es el supermercado donde están los platos congelados de todo el mundo.

Hay alternativas compatibles con los mismos comandos e imágenes: **Podman** (sin *daemon*), y en macOS **OrbStack** y **Colima**.

---

## Bloque 2 · Instalación

### 2.1 Instala Docker

**Windows 10/11.** Necesitas la virtualización activada en la BIOS (en el Administrador de tareas, pestaña *Rendimiento* → *CPU*, debe decir *Virtualización: habilitada*) y WSL2:

```powershell
> wsl --install            # en PowerShell como administrador; reinicia si lo pide
> wsl --status             # debe decir "Versión predeterminada: 2"
```

Después descarga **Docker Desktop for Windows** de <https://docs.docker.com/desktop/setup/install/windows-install/>, instálalo dejando marcada la opción *Use WSL 2*, reinicia si lo pide y ábrelo.

**macOS.** Descarga **Docker Desktop for Mac** de <https://docs.docker.com/desktop/setup/install/mac-install/>. Elige la versión de tu procesador: *Apple Silicon* (M1, M2, M3…) o *Intel* (menú Apple → *Acerca de este Mac*). Arrastra Docker a Aplicaciones y ábrelo.

**Linux (Ubuntu).** Instala Docker Engine con el script oficial y añade tu usuario al grupo `docker` para no tener que usar `sudo`:

```bash
$ curl -fsSL https://get.docker.com | sh
$ sudo usermod -aG docker $USER
```

Cierra la sesión y vuelve a entrar para que el cambio de grupo tenga efecto.

Docker Desktop es gratuito para uso personal, educativo y empresas pequeñas. La primera vez te pedirá aceptar las condiciones; puedes saltarte el registro.

### 2.2 Comprueba la instalación

Con Docker Desktop abierto (en macOS y Windows tiene que estar **en marcha**, con la ballena en la barra de menús o en la bandeja del sistema):

```bash
$ docker version
$ docker run hello-world
```

`docker version` debe mostrar dos bloques, **Client** y **Server**. Si solo aparece *Client* y un error *Cannot connect to the Docker daemon*, Docker Desktop no está arrancado.

### 2.3 Qué ha pasado con `hello-world`

```
  docker run hello-world
      |
      v
  1. El cliente (docker) pide al Engine que ejecute la imagen hello-world
  2. El Engine no la tiene en local  ->  "Unable to find image 'hello-world:latest' locally"
  3. La descarga de Docker Hub        ->  "Pulling from library/hello-world"
  4. Crea un contenedor a partir de la imagen
  5. Lo arranca: el programa escribe el mensaje que ves y termina
  6. El contenedor se detiene (pero sigue existiendo, parado)
```

Vuelve a ejecutar `docker run hello-world`: ahora no descarga nada, porque la imagen ya está en tu ordenador.

### 2.4 Inicia sesión en Docker Hub

Docker Hub limita las descargas anónimas por dirección IP, y en el aula todos salís a internet por la misma. Crea una cuenta gratuita en <https://hub.docker.com> y conéctate:

```bash
$ docker login
```

### 2.5 Un paseo por Docker Desktop

Abre Docker Desktop y localiza:

- **Containers:** los contenedores, en marcha o parados. Desde aquí puedes ver sus logs, abrir una terminal dentro, pararlos y borrarlos.
- **Images:** las imágenes descargadas o construidas, con su tamaño.
- **Volumes:** los datos persistentes (los veremos más adelante).
- **Settings → Resources:** la memoria y la CPU que puede usar la máquina virtual de Docker.

Todo lo que hagas en Docker Desktop se puede hacer con la terminal. En esta guía usaremos la terminal, y Docker Desktop para mirar.

**Punto de control 2:** `docker version` muestra *Client* y *Server*, y `docker run hello-world` muestra *Hello from Docker!*

---

## Bloque 3 · El ciclo de vida de un contenedor

### 3.1 Anatomía de `docker run`

```
docker run  [opciones]  imagen[:etiqueta]  [orden]
            -it --rm     python:3.13-slim   python
```

| Opción | Qué hace |
|---|---|
| `-it` | Modo interactivo: conecta tu teclado y tu terminal con el contenedor |
| `-d` | En segundo plano (*detached*): te devuelve la terminal |
| `--rm` | Borra el contenedor automáticamente al terminar |
| `--name nombre` | Le da un nombre (si no, Docker inventa uno, como `happy_turing`) |
| `-p 8080:80` | Publica un puerto: **anfitrión:contenedor** |
| `-e CLAVE=valor` | Define una variable de entorno dentro del contenedor |
| `-v origen:destino` | Monta una carpeta (lo veremos en el bloque 4) |

La **etiqueta** (*tag*) indica la versión de la imagen: `python:3.13-slim`, `postgres:17-alpine`. Si no la pones, Docker usa `latest`, que puede cambiar de un día para otro: en proyectos reales, fija siempre la etiqueta. Las variantes `slim` y `alpine` son versiones reducidas, mucho más ligeras.

### 3.2 Un Python que no está instalado en tu ordenador

```bash
$ python3 --version                          # en Windows: python --version
$ docker run -it --rm python:3.13-slim
```

Se abre el REPL de Python 3.13, aunque en tu ordenador tengas otra versión. Prueba:

```python
>>> import sys, platform
>>> sys.version
>>> platform.system(), platform.machine()     # ('Linux', ...): estás dentro de Linux
>>> exit()
```

También puedes ejecutar una sola orden en lugar del REPL, o abrir una terminal `bash` dentro del contenedor:

```bash
$ docker run --rm python:3.13-slim python -c "print(2 ** 100)"
$ docker run -it --rm python:3.13-slim bash
```

Dentro de `bash`, mira alrededor con `ls /`, `cat /etc/os-release` y `whoami`. Crea un archivo con `touch /tmp/hola.txt` y sal con `exit`. Vuelve a entrar con el mismo comando: el archivo **ya no está**, porque cada `docker run` crea un contenedor nuevo desde la imagen, que no cambia.

### 3.3 Un servidor web en segundo plano

```bash
$ docker run -d --name web -p 8080:80 nginx:alpine
$ docker ps
```

Abre <http://localhost:8080> en el navegador: es la página de bienvenida de nginx, servida desde el contenedor. El `-p 8080:80` conecta el puerto 8080 de tu ordenador con el puerto 80 del contenedor.

Ahora gestiona el contenedor:

```bash
$ docker logs web                 # lo que ha escrito el servidor (recarga el navegador y repite)
$ docker logs -f web              # sigue los logs en directo; sal con Ctrl+C
$ docker exec -it web sh          # abre una terminal DENTRO del contenedor en marcha
```

Dentro del contenedor, mira la página que sirve nginx y sal:

```bash
/ # cat /usr/share/nginx/html/index.html
/ # exit
```

Y el ciclo de vida completo:

```bash
$ docker stop web                 # lo para (la página ya no carga)
$ docker ps                       # no aparece...
$ docker ps -a                    # ...pero sigue existiendo, parado
$ docker start web                # lo vuelve a arrancar
$ docker rm -f web                # lo para y lo borra
```

```
           docker run                docker stop             docker rm
  imagen  ------------>  en marcha  ------------>  parado  ----------->  (borrado)
                            ^                        |
                            +------ docker start ----+
```

> `docker run` = `docker pull` (si hace falta) + `docker create` + `docker start`. Cada `docker run` crea un contenedor **nuevo**: para volver a arrancar uno que ya existe, usa `docker start`.

### 3.4 Una base de datos en un minuto

Instalar PostgreSQL a mano lleva un rato. Con Docker:

```bash
$ docker run -d --name bd -e POSTGRES_PASSWORD=master postgres:17-alpine
$ docker logs bd                  # espera a ver "database system is ready to accept connections"
$ docker exec -it bd psql -U postgres
```

Ya estás en la consola de PostgreSQL. Prueba:

```sql
postgres=# CREATE TABLE ciudades (nombre text, habitantes int);
postgres=# INSERT INTO ciudades VALUES ('Málaga', 592000), ('Sevilla', 684000);
postgres=# SELECT * FROM ciudades;
postgres=# \q
```

La variable `POSTGRES_PASSWORD` es obligatoria para esta imagen: cada imagen documenta las suyas en su página de Docker Hub. Busca *postgres* en <https://hub.docker.com> y localiza la sección *Environment Variables*.

Ahora borra el contenedor y crea otro igual:

```bash
$ docker rm -f bd
$ docker run -d --name bd -e POSTGRES_PASSWORD=master postgres:17-alpine
$ docker exec -it bd psql -U postgres -c "SELECT * FROM ciudades;"
```

Error: *relation "ciudades" does not exist*. **Los datos vivían dentro del contenedor y se fueron con él.** Para guardarlos hacen falta volúmenes, que veremos más adelante. Bórralo: `docker rm -f bd`.

### 3.5 Imágenes

```bash
$ docker images                    # las imágenes que tienes y cuánto ocupan
$ docker pull python:3.12-slim     # descargar sin ejecutar
$ docker rmi python:3.12-slim      # borrar una imagen
```

Fíjate en la columna *SIZE*: `nginx:alpine` ocupa decenas de megas; una máquina virtual con Ubuntu, varios gigas.

### 3.6 Práctica · Mini retos

Resuélvelos con lo que has visto. La solución de cada uno es uno o dos comandos.

1. Ejecuta `python:3.12-slim` y comprueba que la versión es 3.12, en una sola orden y sin que quede ningún contenedor.
2. Arranca **dos** servidores nginx a la vez, llamados `web1` y `web2`, en los puertos 8081 y 8082. Comprueba que los dos responden en el navegador.
3. ¿Cuántos contenedores tienes, contando los parados? ¿Cuál es el más antiguo? (Pista: los de `hello-world` siguen ahí).
4. Ejecuta `alpine` (un Linux mínimo, de unos pocos megas) con la orden `cat /etc/os-release`. ¿Qué versión de Alpine es?
5. Borra `web1`, `web2` y todos los contenedores parados.

**Punto de control 3:** sabes explicar la diferencia entre `docker run` y `docker start`, y `docker ps -a` no muestra ningún contenedor de los retos.

---

## Bloque 4 · Tu primer Dockerfile

### 4.1 La receta

Hasta ahora has usado imágenes que hizo otra persona. Ahora vas a construir la tuya. Entra en la carpeta del ejemplo:

```bash
$ cd ~/proyectos/master/docker-lab/ejemplos/fizzbuzz
$ code fizzbuzz.py
```

Es un FizzBuzz que lee cuántos números mostrar de la variable de entorno `N`. Crea con VS Code, en esa misma carpeta, un archivo llamado exactamente **`Dockerfile`** (sin extensión) con este contenido:

```dockerfile
# Imagen de partida: Python 3.13 sobre Debian, versión reducida
FROM python:3.13-slim

# Carpeta de trabajo dentro de la imagen (la crea si no existe)
WORKDIR /app

# Copia el script de tu ordenador a /app, dentro de la imagen
COPY fizzbuzz.py .

# Orden que se ejecuta al arrancar un contenedor
CMD ["python", "fizzbuzz.py"]
```

| Instrucción | Qué hace | Cuándo se ejecuta |
|---|---|---|
| `FROM` | Imagen de partida. Siempre la primera | Al construir |
| `WORKDIR` | Carpeta de trabajo para lo que viene después | Al construir |
| `COPY origen destino` | Copia archivos de tu ordenador a la imagen | Al construir |
| `RUN orden` | Ejecuta una orden, por ejemplo instalar paquetes | Al construir |
| `ENV CLAVE=valor` | Variable de entorno con valor por defecto | Al construir |
| `CMD [...]` | Orden por defecto al arrancar el contenedor | Al **ejecutar** |

### 4.2 Construye y ejecuta

```bash
$ docker build -t fizzbuzz .
$ docker images fizzbuzz
$ docker run --rm fizzbuzz
$ docker run --rm -e N=30 fizzbuzz
```

`-t fizzbuzz` le pone nombre a la imagen y el **punto final** indica dónde están el Dockerfile y los archivos que se pueden copiar (el **contexto**). Sin el punto, falla.

Fíjate en la primera línea de la salida: `Python 3.13`, aunque en tu ordenador tengas otra versión. Y la orden de `CMD` se puede sustituir al ejecutar:

```bash
$ docker run --rm fizzbuzz python --version
```

### 4.3 Las capas y la caché

Cada instrucción del Dockerfile crea una **capa**. Vuelve a construir sin cambiar nada:

```bash
$ docker build -t fizzbuzz .
```

Es instantáneo: todas las capas salen de la caché (`CACHED`). Ahora cambia algo en `fizzbuzz.py` (por ejemplo, el mensaje de la primera línea) y vuelve a construir. Las capas anteriores a `COPY` se reutilizan y solo se rehacen la de `COPY` y las siguientes. **Docker reconstruye desde la primera capa que cambia hasta el final.**

Por eso, cuando hay dependencias, el orden importa:

```dockerfile
# Mal: cualquier cambio en el código obliga a reinstalar todas las dependencias
COPY . .
RUN pip install -r requirements.txt

# Bien: las dependencias solo se reinstalan si cambia requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

Pon **primero lo que menos cambia** (sistema, dependencias) y **al final lo que más cambia** (tu código).

### 4.4 Trabajar con tus archivos: *bind mounts*

Con `-v carpeta_del_ordenador:carpeta_del_contenedor` el contenedor ve una carpeta de tu ordenador **en directo**: lo que cambias en un lado aparece en el otro. Se llama *bind mount*.

Sirve tu propia web con nginx sin construir ninguna imagen:

```bash
$ cd ~/proyectos/master/docker-lab/ejemplos/web
$ docker run -d --name miweb -p 8080:80 -v "$(pwd):/usr/share/nginx/html:ro" nginx:alpine
```

```powershell
> cd ~\proyectos\master\docker-lab\ejemplos\web
> docker run -d --name miweb -p 8080:80 -v "${PWD}:/usr/share/nginx/html:ro" nginx:alpine
```

Abre <http://localhost:8080>. Cambia el texto de `index.html` en VS Code, guarda y recarga el navegador: el cambio aparece sin reiniciar nada. El `:ro` (*read only*) impide que el contenedor modifique tus archivos. Cuando acabes: `docker rm -f miweb`.

Lo mismo funciona con Python: ejecuta tu código local en un Python 3.13 **sin construir imagen**.

```bash
$ cd ~/proyectos/master/docker-lab/ejemplos/fizzbuzz
$ docker run --rm -v "$(pwd):/app" -w /app python:3.13-slim python fizzbuzz.py
```

```powershell
> cd ~\proyectos\master\docker-lab\ejemplos\fizzbuzz
> docker run --rm -v "${PWD}:/app" -w /app python:3.13-slim python fizzbuzz.py
```

(`-w` fija la carpeta de trabajo, como `WORKDIR`).

**Cuándo usar cada cosa:** `COPY` en el Dockerfile para **distribuir** (la imagen lleva el código dentro y funciona en cualquier sitio); `-v` para **desarrollar** (editas en tu ordenador y el contenedor lo ve al momento) y para **entregar o recoger datos**.

**Punto de control 4:** `docker run --rm -e N=5 fizzbuzz` muestra el FizzBuzz hasta 5 con Python 3.13, y has visto tu `index.html` modificado en el navegador.

---

## Bloque 5 · Práctica · Dockeriza el análisis de bicis

Vas a empaquetar un análisis de datos del servicio de bicicletas de Málaga (datos simulados) para que cualquiera pueda ejecutarlo con un solo comando, sin instalar Python ni librerías.

```bash
$ cd ~/proyectos/master/docker-lab/ejercicios/bicis-docker
```

```
bicis-docker/
├── analisis.py          el análisis (no hace falta tocarlo)
├── requirements.txt     sus dependencias (tabulate)
├── datos/               viajes.csv y estaciones.json
└── comprobar.py         comprueba tu solución
```

Lee `analisis.py`: lee `datos/`, escribe `salida/resumen.json`, necesita la librería `tabulate` y la variable de entorno `AUTOR`, y acepta otra opcional, `TOP`.

### Parte A · El Dockerfile

Escribe un `Dockerfile` en `bicis-docker/` que:

1. Parta de `python:3.13-slim`.
2. Trabaje en `/app`.
3. Instale las dependencias de `requirements.txt` **aprovechando la caché** (apartado 4.3).
4. Copie `analisis.py`, pero **no** la carpeta `datos/`: los datos se entregan al ejecutar, no viajan dentro de la imagen.
5. Ejecute `python analisis.py` al arrancar.

### Parte B · La imagen

Construye la imagen con el nombre y la etiqueta `bicis-analisis:1.0`.

### Parte C · La ejecución

Ejecuta un contenedor de esa imagen que se borre al terminar y que:

- monte `datos/` en `/app/datos` en **solo lectura**;
- monte `salida/` en `/app/salida`, para que el resumen aparezca en tu ordenador;
- reciba tu nombre en la variable `AUTOR`.

Si lo has hecho bien, verás una tabla con las estaciones con más viajes y tendrás `salida/resumen.json` en tu carpeta. Ábrelo: el campo `python` dice `3.13` y `en_docker` dice `true`.

Comprueba tu solución desde `bicis-docker`, en tu ordenador (no dentro del contenedor):

```bash
$ python3 comprobar.py           # en Windows: python comprobar.py
```

**Reto extra:** vuelve a ejecutarlo mostrando las 5 estaciones con más viajes, sin cambiar el código ni reconstruir la imagen. Después cambia algo de `analisis.py` (por ejemplo, el texto del primer `print`), reconstruye y fíjate en qué capas salen de la caché.

**Punto de control 5:** `comprobar.py` termina con *Ejercicio completado*.

---

## Limpieza

Las imágenes ocupan disco. Para ver cuánto y limpiar lo que no se usa:

```bash
$ docker system df                # espacio usado por imágenes, contenedores y volúmenes
$ docker container prune          # borra los contenedores parados
$ docker image prune              # borra las imágenes sin nombre (restos de builds)
$ docker system prune             # todo lo anterior y más; pregunta antes de borrar
```

Cuando no estés usando Docker, cierra Docker Desktop: su máquina virtual consume memoria aunque no tengas contenedores en marcha.

---

## Checklist

- [ ] Sé explicar qué diferencia hay entre una máquina virtual y un contenedor.
- [ ] Distingo imagen, contenedor, registro y Dockerfile.
- [ ] Tengo Docker funcionando y he iniciado sesión en Docker Hub.
- [ ] Arranco contenedores interactivos (`-it`), en segundo plano (`-d`) y de usar y tirar (`--rm`).
- [ ] Publico puertos con `-p` y paso variables con `-e`.
- [ ] Uso `ps`, `logs`, `exec`, `stop`, `start` y `rm`.
- [ ] Escribo un Dockerfile con `FROM`, `WORKDIR`, `COPY`, `RUN` y `CMD`, y lo construyo con `docker build -t`.
- [ ] Ordeno el Dockerfile para aprovechar la caché.
- [ ] Monto carpetas de mi ordenador con `-v`.
- [ ] `comprobar.py` del ejercicio de bicis termina con *Ejercicio completado*.

---

## Problemas frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| `Cannot connect to the Docker daemon` / `error during connect` | Docker Desktop no está arrancado | Ábrelo y espera a que la ballena deje de moverse |
| Windows: *WSL 2 installation is incomplete* o *Virtualization support not detected* | Falta WSL2 o la virtualización está desactivada en la BIOS | `wsl --install` y reiniciar. Si sigue, activar *Intel VT-x* o *AMD-V/SVM* en la BIOS |
| Linux: `permission denied ... docker.sock` | Tu usuario no está en el grupo `docker` | `sudo usermod -aG docker $USER` y cerrar sesión |
| `toomanyrequests: You have reached your pull rate limit` | Límite de descargas anónimas de Docker Hub | `docker login` con tu cuenta |
| `Bind for 0.0.0.0:8080 failed: port is already allocated` | Otro contenedor (o programa) usa ese puerto | `docker ps` para ver cuál; bórralo o usa otro puerto, como `-p 8081:80` |
| `Conflict. The container name "/web" is already in use` | Ya existe un contenedor con ese nombre, quizá parado | `docker rm -f web` o `docker start web` |
| `docker build` dice *requires 1 argument* | Falta el punto final | `docker build -t nombre .` |
| `failed to read dockerfile` | El archivo se llama `Dockerfile.txt` o está en otra carpeta | Renómbralo a `Dockerfile` (VS Code muestra la extensión real) y ejecuta el build en su carpeta |
| `COPY failed: file not found` | La ruta del `COPY` no existe dentro del contexto | Las rutas son relativas a la carpeta del build; comprueba el nombre con `ls` |
| El contenedor termina al instante con `docker run -d python:3.13-slim` | El contenedor vive lo que dura su orden, y el REPL sin terminal termina enseguida | Usa `-it` para trabajar dentro, o ejecuta una orden concreta |
| `-v` no monta nada o da error de ruta en Windows | Sintaxis de bash en PowerShell | En PowerShell usa `"${PWD}:/app"`; en bash, `"$(pwd):/app"` |
| `ERROR: no encuentro la carpeta /app/datos` en el ejercicio | Falta el `-v` de los datos o la ruta de origen está mal | Ejecuta el `docker run` desde la carpeta `bicis-docker` |
| Mac con Apple Silicon: *no matching manifest for linux/arm64* | Esa imagen solo existe para procesadores Intel | Añade `--platform linux/amd64` (irá más lento) o busca una imagen multiplataforma |

---

## Para practicar en casa (opcional)

- **Play with Docker** (<https://labs.play-with-docker.com>): un laboratorio de Docker en el navegador, sin instalar nada.
- Busca en Docker Hub la imagen oficial de **Redis**, arráncala y conéctate con `docker exec -it <nombre> redis-cli` para guardar y leer una clave (`SET saludo hola`, `GET saludo`).
- Escribe un Dockerfile para cualquiera de tus scripts de Python que use alguna librería externa.
- Mira el historial de capas de tu imagen: `docker history bicis-analisis:1.0`.

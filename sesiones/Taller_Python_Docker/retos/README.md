# Retos: encuentra el fallo

Cada carpeta tiene algo que **no funciona**. Tu trabajo es reproducir el problema, leer el error con calma, encontrar la causa y arreglarlo. Antes de tocar nada, **di en voz alta qué crees que pasa**.

Trabaja en una copia, fuera del repositorio del curso:

```bash
$ cp -r ~/proyectos/master/laboratorio-mbd-2026/sesiones/Taller_Python_Docker/retos ~/proyectos/master/retos
$ cd ~/proyectos/master/retos
```

En PowerShell, cambia `$(pwd)` por `${PWD}` en los comandos de `docker run`.

---

## Reto 1 · No construye

Un script que saluda y muestra una tabla. Su autor dice que "en su ordenador funcionaba".

```bash
$ cd reto1-no-construye
$ docker build -t reto-saludo .
$ docker run --rm -e NOMBRE=Ana reto-saludo
```

**Síntoma:** `docker build` falla. Y cuando consigas que construya, el contenedor tampoco arranca.

**Está resuelto cuando:** el contenedor imprime `Hola, Ana` y una tabla con Docker y Python.

**Mejora extra:** el `Dockerfile` construye, pero desaprovecha la caché. ¿Por qué? Cambia una letra de `saludo.py`, vuelve a construir y fíjate en qué pasos se repiten.

---

## Reto 2 · La web no responde

Un servidor web mínimo hecho solo con la biblioteca estándar de Python.

```bash
$ cd reto2-web-muda
$ docker build -t reto-web .
$ docker run --rm --name web -p 8000:8000 reto-web
```

Abre <http://localhost:8000> en el navegador.

**Síntoma:** el contenedor está en marcha y dice `Escuchando en el puerto 8000...`, el puerto está publicado con `-p`... pero el navegador no recibe respuesta.

**Pistas, de menos a más:**
1. Desde otra terminal, entra en el contenedor: `docker exec -it web python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000').read())"`. ¿Funciona desde dentro?
2. Si desde dentro funciona y desde fuera no, el problema no está en el código de la página, sino en **dónde escucha** el servidor.

**Está resuelto cuando:** el navegador muestra «Hola desde el contenedor». Para pararlo: `Ctrl+C` o `docker stop web`.

---

## Reto 3 · No encuentra los datos

Un script que cuenta las ventas de cada producto. Los datos **no** van dentro de la imagen: se montan al ejecutar.

```bash
$ cd reto3-sin-datos
$ docker build -t reto-ventas .
$ docker run --rm -v "$(pwd)/datos:/datos" reto-ventas
```

**Síntoma:** `FileNotFoundError: ... 'datos/ventas.csv'`, aunque la carpeta `datos` está montada.

**Pista:** el script busca `datos/ventas.csv`, una ruta **relativa**. ¿Relativa a qué carpeta del contenedor? Mira el `Dockerfile`.

**Está resuelto cuando:** aparece la lista de productos, con el café en primer lugar. Arréglalo **sin cambiar** `contar.py` ni el `Dockerfile`. Si además montas los datos en solo lectura, mejor.

---

## Reto 4 · Las estaciones comparten bicis

Una clase `Estacion` y un script que la prueba. No hace falta Docker.

```bash
$ cd reto4-estaciones
$ python3 probar.py
```

**Síntoma:** `probar.py` falla. Hay **tres** fallos distintos en `estaciones.py`: cuando arregles uno, aparecerá el siguiente.

**Está resuelto cuando:** `probar.py` imprime `Correcto`. **No modifiques** `probar.py`.

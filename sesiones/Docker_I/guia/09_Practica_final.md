# 9 · Práctica final: dockeriza el análisis de bicis

Anterior: [8 · Trabajar con tus archivos](08_Bind_mounts.md) · [Índice](../GUIA.md)

Vas a juntar todo lo anterior: empaquetar un análisis de datos del servicio de bicicletas de Málaga (datos simulados) en una imagen, para que cualquiera pueda ejecutarlo con un solo comando, sin instalar Python ni librerías.

```bash
$ cd ~/proyectos/master/docker-lab/ejercicios/bicis-docker
$ code .
```

```text
bicis-docker/
├── analisis.py          el análisis (no hace falta tocarlo)
├── requirements.txt     sus dependencias (tabulate)
├── datos/               viajes.csv y estaciones.json
└── comprobar.py         comprueba tu solución
```

Lee `analisis.py` antes de empezar. Fíjate en cuatro cosas:

- lee los datos de la carpeta `datos/`;
- escribe el resultado en `salida/resumen.json`;
- necesita la librería `tabulate`;
- necesita la variable de entorno `AUTOR` y acepta otra opcional, `TOP`.

---

## Parte A · El Dockerfile

Escribe un `Dockerfile` en `bicis-docker/` que:

1. Parta de `python:3.13-slim`.
2. Trabaje en `/app`.
3. Instale las dependencias de `requirements.txt` **aprovechando la caché** ([capítulo 7.3](07_Dockerfile.md#73-las-capas-y-la-caché)).
4. Copie `analisis.py`, pero **no** la carpeta `datos/`: los datos se entregan al ejecutar, no viajan dentro de la imagen.
5. Ejecute `python analisis.py` al arrancar.

## Parte B · La imagen

Construye la imagen con el nombre y la etiqueta `bicis-analisis:1.0`. Comprueba con `docker history` cuántas capas tiene y cuánto ocupa la de las dependencias.

## Parte C · La ejecución

Ejecuta un contenedor de esa imagen que se borre al terminar y que:

- monte `datos/` en `/app/datos` en **solo lectura**;
- monte `salida/` en `/app/salida`, para que el resumen aparezca en tu ordenador;
- reciba tu nombre en la variable `AUTOR`.

Si lo has hecho bien, verás una tabla con las estaciones con más viajes y tendrás `salida/resumen.json` en tu carpeta. Ábrelo: el campo `python` dice `3.13` y `en_docker` dice `true`.

## Comprueba tu solución

Desde `bicis-docker`, en tu ordenador (no dentro del contenedor):

```bash
$ python3 comprobar.py           # en Windows: python comprobar.py
```

Te dirá qué comprobaciones pasan y te dará pistas para las que no. El objetivo es llegar a *Ejercicio completado*.

---

## Retos extra

1. Vuelve a ejecutarlo mostrando las **5** estaciones con más viajes, sin cambiar el código ni reconstruir la imagen.
2. Cambia algo de `analisis.py` (por ejemplo, el texto del primer `print`), reconstruye como `bicis-analisis:1.1` y fíjate en qué capas salen de la caché.
3. Añade un `.dockerignore` que excluya `datos/`, `salida/` y `__pycache__/`. Comprueba con `docker build` que el contexto que se envía es más pequeño.
4. Sube tu imagen a Docker Hub como `tu_usuario/bicis-analisis:1.0`. Pide a alguien que descargue tu imagen y la ejecute con **sus** datos.
5. Haz que la imagen muestre las 5 estaciones por defecto, sin pasar `-e TOP=5`, pero que siga siendo posible cambiarlo al ejecutar.

**Punto de control 9:** `comprobar.py` termina con *Ejercicio completado*.

---

## Checklist de todo lo aprendido

- [ ] Sé explicar qué diferencia hay entre una máquina virtual y un contenedor.
- [ ] Distingo imagen, contenedor, Dockerfile y registro, y sé cómo se relacionan.
- [ ] Tengo Docker funcionando y he iniciado sesión en Docker Hub.
- [ ] Sé ajustar cuánta memoria y CPU puede usar Docker.
- [ ] Ejecuto contenedores interactivos (`-it`), en segundo plano (`-d`) y de usar y tirar (`--rm`).
- [ ] Publico puertos con `-p` y paso variables con `-e`.
- [ ] Gestiono contenedores con `ps`, `logs`, `exec`, `stop`, `start`, `rm`, `inspect` y `stats`.
- [ ] Busco, descargo, inspecciono, etiqueto, subo y borro imágenes.
- [ ] Escribo Dockerfiles con `FROM`, `WORKDIR`, `COPY`, `RUN`, `ENV`, `EXPOSE` y `CMD`, y los construyo con `docker build -t`.
- [ ] Ordeno el Dockerfile para aprovechar la caché y uso `.dockerignore`.
- [ ] Monto carpetas de mi ordenador con `-v`, también en solo lectura.
- [ ] Limpio lo que no uso con `docker system prune`.

## Para practicar en casa

- **Play with Docker** (<https://labs.play-with-docker.com>): un laboratorio de Docker en el navegador, sin instalar nada. Necesita una cuenta de Docker Hub.
- **Docker Get Started** (<https://docs.docker.com/get-started/>): la guía oficial, con ejercicios.
- Dockeriza alguno de tus notebooks convertido en script (`jupyter nbconvert --to script`).

---

Anterior: [8 · Trabajar con tus archivos](08_Bind_mounts.md) · [Índice](../GUIA.md)

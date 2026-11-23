# Solución · Detective de Git

Antes de leer la solución, inténtalo tú. Si te atascas en una pregunta, mira solo la idea de esa pregunta y vuelve a probar con la terminal.

Todos los comandos se ejecutan dentro de la carpeta `detective/proyecto`. Los *hash* que aparecen aquí son los mismos que verás tú, porque el repositorio del detective es idéntico para todo el mundo.

Esta es la historia completa del proyecto (`git log --oneline --graph --all`):

```
* 08921ba Añade la función moda
* c87f02a Limpia archivos de datos
| * 36f3eb8 Documenta la fórmula de la media      ← rama feature/percentiles
| * d1be749 Añade la función percentil
|/
* d3bc38a Refactoriza el cálculo de la media
*   272ce95 Fusiona la rama feature/graficos
|\
| * a48c4af Añade gráficos de barras en la terminal
* | cfbf9d1 Documenta el uso en el README
|/
* bd367a8 Añade un script de ejemplo
* 20f2ff4 Añade la función mediana
* f3d8106 Añade datos de ventas de ejemplo
* 97a9f79 Añade la función media
* 4af4cbd Crea el proyecto con un README
```

---

## Parte A · Investiga la historia

`respuestas.txt` completo:

```
1: 11
2: Grace Hopper
3: cuaderno
4: 2026-09-24
5: percentil
```

### 1. ¿Cuántos commits tiene la rama `main`?

**Idea:** contar los commits que forman la historia de `main`.

```bash
git log --oneline main        # y cuenta las líneas
git rev-list --count main     # o deja que Git las cuente
```

**Respuesta: `11`.**

Cuentan el commit de la rama `feature/graficos`, porque se fusionó en `main`, y el propio commit de fusión. **No** cuentan los dos commits de `feature/percentiles`, porque esa rama todavía no se ha fusionado. Con `git log --oneline --graph --all` se ve qué commits son de cada rama.

### 2. ¿Quién escribió la función `mediana`?

**Idea:** buscar el commit que **añadió** el texto `def mediana` y mirar su autor.

```bash
git log -S "def mediana" --format="%an  %s"
```

También sirve `git blame estadisticas.py`, que muestra al lado de cada línea quién la escribió.

**Respuesta: `Grace Hopper`.**

`-S` busca en el **código**: encuentra los commits que añadieron o quitaron ese texto. Para buscar en los **mensajes** de commit se usa `--grep`.

### 3. ¿Qué palabra hay detrás de `clave:` en el archivo borrado?

**Idea:** el archivo ya no está en tu carpeta, pero **sigue en la historia**. Basta con mirarlo en un commit en el que todavía existía.

```bash
git log --oneline -- datos/ventas.csv
# c87f02a Limpia archivos de datos           ← aquí se borró
# f3d8106 Añade datos de ventas de ejemplo   ← aquí se creó

git show c87f02a^:datos/ventas.csv | head -1
# clave: cuaderno
```

`c87f02a^` significa "el commit anterior a `c87f02a`", es decir, el último en el que el archivo existía. También vale `f3d8106`.

**Respuesta: `cuaderno`.**

Borrar un archivo no lo hace desaparecer de Git: todo lo que estuvo en un commit se puede recuperar.

### 4. ¿Qué día se introdujo el error en `media`?

**Idea:** primero, encontrar el error leyendo el código. Después, buscar qué commit lo metió.

```bash
cat estadisticas.py
```

La media divide entre `len(numeros) - 1`, cuando debería dividir entre `len(numeros)`. Ahora busca el commit que añadió ese texto:

```bash
git log -S "len(numeros) - 1" --format="%ad %an %s" --date=short
# 2026-09-24 Alan Turing Refactoriza el cálculo de la media
```

**Respuesta: `2026-09-24`.**

Si en lugar de `-S` usas `git log -p --date=short -- estadisticas.py`, verás el diff de cada commit y tendrás que buscar tú el cambio (en el paginador, escribe `/len(numeros) - 1` y pulsa Intro). El commit que buscas es este:

```diff
-    return total / len(numeros)
+    return total / (len(numeros) - 1)
```

Fíjate en el mensaje: "Refactoriza" debería significar que el código hace lo mismo con otra forma, y sin embargo cambió el resultado. No te fíes solo de los mensajes: comprueba el código.

### 5. ¿Qué función añade la rama sin fusionar?

**Idea:** ver qué ramas hay y qué tiene esa rama que `main` no tiene.

```bash
git branch -a                                  # feature/graficos, feature/percentiles y main
git log --oneline main..feature/percentiles    # sus 2 commits
git diff main...feature/percentiles            # el código nuevo
```

`feature/graficos` ya está fusionada: `git log --oneline main..feature/graficos` no muestra nada. La pendiente es `feature/percentiles`. `main..feature/percentiles` se lee "lo que está en `feature/percentiles` y no en `main`". En el diff aparece un archivo nuevo, `percentiles.py`, con `def percentil(numeros, p)`.

**Respuesta: `percentil`.**

---

## Parte B · Arregla el proyecto

Asegúrate de estar en `main` (`git switch main`) y con `git status` limpio.

### 1. Corrige el error de `media()`

En `estadisticas.py`, cambia esta línea:

```python
    return total / (len(numeros) - 1)
```

por esta:

```python
    return total / len(numeros)
```

Guarda y haz el commit:

```bash
git add estadisticas.py
git commit -m "Corrige la división en la función media"
```

### 2. Recupera `datos/ventas.csv`

Trae el archivo desde el último commit en el que existía y guárdalo en un commit nuevo:

```bash
git restore --source c87f02a^ -- datos/ventas.csv
git add datos/ventas.csv
git commit -m "Recupera los datos de ventas"
```

### 3. Fusiona la rama pendiente y resuelve el conflicto

```bash
git merge feature/percentiles
# CONFLICT (content): Merge conflict in estadisticas.py
```

Las dos ramas cambiaron la misma línea: tú corregiste la división y la otra rama añadió un comentario a la línea antigua. Git no sabe con cuál quedarse y marca la zona en `estadisticas.py`:

```python
<<<<<<< HEAD
    return total / len(numeros)
=======
    return total / (len(numeros) - 1)  # media = suma / número de elementos
>>>>>>> feature/percentiles
```

- Entre `<<<<<<< HEAD` y `=======` está tu versión (`main`).
- Entre `=======` y `>>>>>>>` está la versión de la otra rama.

Deja **tu corrección y su comentario** en una sola línea, y borra las tres líneas de marcas:

```python
    return total / len(numeros)  # media = suma / número de elementos
```

Termina la fusión:

```bash
git add estadisticas.py
git commit              # acepta el mensaje de fusión que propone Git
git status              # nothing to commit, working tree clean
```

Si en algún momento te lías, `git merge --abort` deja todo como estaba antes del `git merge`.

La historia queda así (los *hash* de tus commits serán distintos):

```
*   Merge branch 'feature/percentiles'
|\
| * 36f3eb8 Documenta la fórmula de la media
| * d1be749 Añade la función percentil
* | Recupera los datos de ventas
* | Corrige la división en la función media
* | 08921ba Añade la función moda
```

### Comprobación

Desde la carpeta `detective` (no desde `proyecto`):

```bash
cd ..
python3 comprobar.py     # en Windows: python comprobar.py
```

Debe terminar con *Caso resuelto*.

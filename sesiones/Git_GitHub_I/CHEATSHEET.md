# Chuleta · Git y GitHub

## Configuración (una vez por ordenador)

```bash
git config --global user.name "Nombre Apellido"
git config --global user.email "tu_correo@ejemplo.com"
git config --global init.defaultBranch main
git config --global core.editor "code --wait"
git config --global pull.rebase false
git config --global --list                # ver la configuración
```

## Las tres zonas

```
Directorio de trabajo  --git add-->  Área de preparación  --git commit-->  Repositorio  --git push-->  GitHub
                       <--------------------------------- git pull ---------------------------------
```

## Empezar

| Qué hago | Comando |
|---|---|
| Convertir una carpeta en repositorio | `git init` |
| Descargar un repositorio remoto | `git clone <url>` |
| Ver el estado (lo uso todo el rato) | `git status` |

## Guardar cambios

| Qué hago | Comando |
|---|---|
| Preparar un archivo / todo | `git add archivo` · `git add .` |
| Guardar la foto | `git commit -m "Mensaje en imperativo"` |
| Preparar y guardar lo ya seguido | `git commit -am "Mensaje"` |
| Ver lo cambiado sin preparar / preparado | `git diff` · `git diff --staged` |
| Sacar del área de preparación | `git restore --staged archivo` |
| Descartar cambios de un archivo (sin papelera) | `git restore archivo` |
| Cambiar el mensaje del último commit (antes de subirlo) | `git commit --amend -m "Nuevo mensaje"` |

## Leer la historia

| Qué quiero saber | Comando |
|---|---|
| Historia resumida | `git log --oneline` |
| Historia con ramas | `git log --oneline --graph --all` |
| Qué cambió en un commit | `git show <hash>` |
| Diferencias entre dos commits | `git diff <hash1> <hash2>` |
| Historia de un archivo | `git log --oneline -- ruta` |
| Commits que añadieron o quitaron un texto | `git log -S "texto"` |
| Quién escribió cada línea | `git blame archivo` |
| Un archivo tal como era en un commit | `git show <hash>:ruta` |
| Recuperar un archivo de un commit | `git restore --source <hash> -- ruta` |

`<hash>^` es el commit anterior a `<hash>`. Con los 7 primeros caracteres del *hash* basta.

## Ramas

| Qué hago | Comando |
|---|---|
| Ver las ramas (`*` = actual) | `git branch` · `git branch -a` |
| Crear una rama y cambiar a ella | `git switch -c nombre` |
| Cambiar de rama | `git switch nombre` |
| Fusionar una rama en la actual | `git merge nombre` |
| Cancelar una fusión con conflictos | `git merge --abort` |
| Borrar una rama ya fusionada / sin fusionar | `git branch -d nombre` · `git branch -D nombre` |
| Volver de un commit suelto (*detached HEAD*) | `git switch main` |

## Resolver un conflicto

```
<<<<<<< HEAD
tu versión (la de la rama actual)
=======
la versión de la rama que fusionas
>>>>>>> otra-rama
```

1. Deja el texto como quieras que quede y **borra las tres líneas de marcas** (en VS Code: *Aceptar cambio actual / entrante / ambos*).
2. `git add archivo`
3. Comprueba que el código funciona (un archivo con marcas no se puede ejecutar)
4. `git commit`

## Remoto (GitHub)

| Qué hago | Comando |
|---|---|
| Crear el repositorio en GitHub y subirlo | `gh repo create nombre --private --source . --remote origin --push` |
| Conectar con un repositorio vacío ya creado | `git remote add origin <url>` |
| Ver los remotos | `git remote -v` |
| Primera subida de una rama | `git push -u origin main` |
| Subir / traer | `git push` · `git pull` |
| Ver si hay novedades sin tocar tus archivos | `git fetch` y después `git status` |
| Abrir el repositorio en el navegador | `gh repo view --web` |

## Flujo de cada día

```bash
git pull
# ...trabajar...
git status
git add <archivos>
git commit -m "Mensaje claro"
git push
```

## `.gitignore` básico para Python

```gitignore
.venv/
__pycache__/
.ipynb_checkpoints/
salida/
.DS_Store
Thumbs.db
.env
```

Antes de cada commit, `git status`: es la forma de no subir por error un secreto o un archivo enorme.

## Buenos mensajes de commit

- En imperativo: *Añade*, *Corrige*, *Elimina*, *Refactoriza*.
- Una línea corta (unos 50 caracteres) que diga **qué** cambia.
- Un cambio lógico por commit.

## VS Code

| Acción | Dónde |
|---|---|
| Panel de Git | Control de código fuente: `⌃⇧G` (macOS) · `Ctrl+Shift+G` |
| Preparar un archivo | **+** junto al archivo |
| Commit | Mensaje arriba y **Confirmar** |
| `pull` + `push` | **Sincronizar cambios** |
| Cambiar o crear rama | Nombre de la rama, abajo a la izquierda |

## Más allá de lo básico

| Qué hago | Comando |
|---|---|
| Marcar una versión y subir la etiqueta | `git tag -a v1.0 -m "Mensaje"` · `git push origin v1.0` |
| Crear una *release* en GitHub | `gh release create v1.0 --notes "Mensaje"` |
| Subir una rama y abrir un *pull request* | `git push -u origin rama` · `gh pr create --fill` |
| Guardar cambios a medias y recuperarlos | `git stash` · `git stash list` · `git stash pop` |
| Rehacer el último commit (no subido) | `git commit --amend` |
| Reordenar o unir los últimos commits (no subidos) | `git rebase -i HEAD~3` |
| Deshacer un commit ya subido | `git revert <hash>` |
| Buscar el commit que introdujo un error | `git bisect start <malo> <bueno>` · `git bisect run <prueba>` · `git bisect reset` |
| Ver todos los movimientos de `HEAD` | `git reflog` |
| Volver a un punto anterior (descarta cambios sin commit) | `git reset --hard HEAD@{1}` |

Nunca reescribas (`--amend`, `rebase`, `reset`) commits que ya has subido.

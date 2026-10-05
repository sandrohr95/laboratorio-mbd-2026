# Chuleta · Terminal y VS Code

## Navegar y gestionar archivos

| Qué hago | bash / zsh (macOS, Linux, WSL) | PowerShell (Windows) |
|---|---|---|
| ¿Dónde estoy? | `pwd` | `pwd` |
| Listar (incluidos los ocultos) | `ls -la` | `ls -Force` |
| Entrar en una carpeta / subir / ir a *home* | `cd carpeta` · `cd ..` · `cd ~` | `cd carpeta` · `cd ..` · `cd ~` |
| Volver a la carpeta anterior | `cd -` | `cd -` |
| Crear carpetas (con intermedias) | `mkdir -p a/b/c` | `mkdir a\b\c` |
| Crear un archivo vacío | `touch f.txt` | `ni f.txt` |
| Copiar (una carpeta entera: `-r`) | `cp origen destino` · `cp -r dir1 dir2` | `cp origen destino` · `cp -r dir1 dir2` |
| Mover o renombrar | `mv viejo nuevo` | `mv viejo nuevo` |
| Borrar un archivo / una carpeta | `rm f.txt` · `rm -r carpeta` | `rm f.txt` · `rm -r carpeta` |
| Abrir la carpeta en el explorador | `open .` (macOS) · `explorer.exe .` (WSL) | `ii .` |
| Abrir la carpeta en VS Code | `code .` | `code .` |

**La terminal no tiene papelera.** Antes de un `rm -r`, comprueba dónde estás con `pwd` y `ls`.

## Leer y buscar

| Qué hago | bash / zsh | PowerShell |
|---|---|---|
| Ver un archivo | `cat f.txt` | `cat f.txt` |
| Verlo página a página (`q` para salir) | `less f.txt` | `more f.txt` |
| Primeras / últimas N líneas | `head -n 20 f` · `tail -n 20 f` | `gc f -Head 20` · `gc f -Tail 20` |
| Seguir un log en directo | `tail -f app.log` | `gc app.log -Wait` |
| Buscar archivos por nombre | `find . -name "*.csv"` | `ls -Recurse -Filter *.csv` |
| Buscar texto en archivos | `grep -rn "texto" .` | `Select-String -Pattern "texto" -Path *.txt` |
| Contar líneas | `wc -l f.txt` | `(gc f.txt).Count` |
| ¿Qué ejecutable se usa? | `which python3` · `which -a python3` | `Get-Command python` · `where.exe python` |

## Redirecciones y tuberías

| Símbolo | Qué hace | Ejemplo |
|---|---|---|
| `>` | Guarda la salida en un archivo (lo **sobrescribe**) | `ls > lista.txt` |
| `>>` | La **añade** al final del archivo | `echo "más" >> lista.txt` |
| `\|` | Pasa la salida de un comando como entrada al siguiente | `grep ERROR app.log \| wc -l` |
| `&&` | Ejecuta el segundo comando solo si el primero ha ido bien | `mkdir s01 && cd s01` |

## Variables de entorno

| Qué hago | bash / zsh | PowerShell |
|---|---|---|
| Ver una variable | `echo $HOME` | `echo $env:USERPROFILE` |
| Ver el `PATH` | `echo $PATH` | `$env:PATH -split ";"` |
| Definirla para esta sesión | `export MI_VAR=valor` | `$env:MI_VAR = "valor"` |
| Definirla para siempre | añádela a `~/.zshrc` o `~/.bashrc` | Configuración → *Variables de entorno* |

## Atajos de la terminal

| Atajo | Qué hace |
|---|---|
| `Tab` | Autocompleta (dos veces: muestra las opciones) |
| `↑` / `↓` | Recorre el historial |
| `Ctrl+R` | Busca en el historial |
| `Ctrl+C` | Interrumpe el comando en curso |
| `Ctrl+L` | Limpia la pantalla |
| `Ctrl+A` / `Ctrl+E` | Va al principio o al final de la línea (bash/zsh) |

## Ayuda

- `comando --help`: resumen de opciones.
- `man comando`: manual completo (macOS y Linux). `q` para salir.
- `Get-Help comando`: ayuda en PowerShell.
- <https://explainshell.com>: pega un comando y te explica cada parte.

## Gestores de paquetes

| Qué hago | winget (Windows) | Homebrew (macOS) | apt (Ubuntu/WSL) |
|---|---|---|---|
| Buscar | `winget search x` | `brew search x` | `apt search x` |
| Instalar | `winget install x` | `brew install x` | `sudo apt install x` |
| Actualizar todo | `winget upgrade --all` | `brew upgrade` | `sudo apt update && sudo apt upgrade` |
| Desinstalar | `winget uninstall x` | `brew uninstall x` | `sudo apt remove x` |

## VS Code

| Atajo (macOS) | Windows / Linux | Qué hace |
|---|---|---|
| `⇧⌘P` | `Ctrl+Shift+P` | **Paleta de comandos**: todo está aquí |
| `⌘P` | `Ctrl+P` | Abrir un archivo por su nombre |
| ``⌃` `` | ``Ctrl+` `` | Mostrar u ocultar la terminal integrada |
| `⌘B` | `Ctrl+B` | Mostrar u ocultar la barra lateral |
| `F5` | `F5` | Ejecutar con el depurador |
| `F10` / `F11` | `F10` / `F11` | Depurador: siguiente línea / entrar en la función |
| `⌘/` | `Ctrl+/` | Comentar o descomentar |
| `⌥` + clic | `Alt` + clic | Varios cursores |
| `⌥↑` / `⌥↓` | `Alt+↑` / `Alt+↓` | Mover la línea arriba o abajo |
| `⌘D` | `Ctrl+D` | Seleccionar la siguiente aparición |

**Extensiones del curso:** Python · Jupyter · Ruff · WSL (Windows) · y más adelante Container Tools (Docker) y GitLens.

## Python

| Qué hago | macOS / Linux | Windows |
|---|---|---|
| Versión | `python3 --version` | `python --version` · `py --version` |
| Ejecutar un script | `python3 script.py` | `python script.py` |
| Abrir el REPL / salir | `python3` · `exit()` | `python` · `exit()` |
| Elegir versión (lanzador) | – | `py -3.13 script.py` |

## Sintaxis básica de Python

| Qué | Ejemplo |
|---|---|
| Variable y tipo | `x = 42` · `type(x)` · `isinstance(x, int)` |
| Conversión | `int("42")` · `float("3.5")` · `str(10)` |
| División · entera · resto · potencia | `7 / 2` · `7 // 2` · `7 % 2` · `2 ** 10` |
| Comparación y lógica | `==` `!=` `<` `>=` · `and` `or` `not` · `0 < x < 10` |
| Índices y *slicing* | `s[0]` · `s[-1]` · `s[1:4]` · `s[::-1]` · `len(s)` |
| Métodos de cadena | `s.strip()` · `s.lower()` · `s.split(",")` · `"-".join(lista)` |
| f-string | `f"{nombre} tiene {saldo:.2f} €"` |
| Leer del teclado | `texto = input("Pregunta: ")` (siempre devuelve `str`) |

```python
if nota >= 9:                         # condicional
    print("Sobresaliente")
elif nota >= 5:
    print("Aprobado")
else:
    print("Suspenso")

for i in range(5):                    # 0, 1, 2, 3, 4
    print(i)

for i, ciudad in enumerate(ciudades): # posición y elemento
    print(i, ciudad)

while cuenta > 0:                     # mientras se cumpla
    cuenta -= 1

def saludar(nombre, saludo="Hola"):   # función con valor por defecto
    """Devuelve un saludo."""
    return f"{saludo}, {nombre}"
```

## Notebooks en VS Code

| Atajo o acción | Qué hace |
|---|---|
| `Shift+Intro` | Ejecuta la celda y pasa a la siguiente |
| `Ctrl+Intro` | Ejecuta la celda y se queda en ella |
| `A` / `B` (fuera de la celda) | Inserta una celda encima / debajo |
| `M` / `Y` | Convierte la celda en texto (Markdown) / en código |
| `L` | Muestra los números de línea |
| Seleccionar kernel (arriba a la derecha) | Elige el Python que ejecuta el notebook |
| Reiniciar (barra superior) | Borra todas las variables: vuelve a ejecutar desde arriba |


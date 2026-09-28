# Sistema operativo, terminal e IDEs

> **Guía de laboratorio.** Síguela durante la clase a la vez que las diapositivas. Cada bloque termina con un **punto de control**: si no lo superas, avisa antes de seguir.

**Material:** [diapositivas](https://sandrohr95.github.io/laboratorio-mbd-2026/slides/SO_Terminal_IDEs.html) · [chuleta](CHEATSHEET.md) · [`ejercicios/tesoro.zip`](ejercicios/tesoro.zip)

**Qué necesitas:** tu portátil con permisos de administrador, conexión a internet y una cuenta de GitHub.

En los bloques de comandos, los que empiezan por `$` son para **bash/zsh** (macOS, Linux y WSL) y los que empiezan por `>` son para **PowerShell** (Windows). No copies el `$` ni el `>`.

---

## Bloque 1 · El sistema operativo

### 1.1 Abre una terminal

| Sistema | Cómo |
|---|---|
| Windows | Instala **Windows Terminal** si no lo tienes (`winget install Microsoft.WindowsTerminal`) y ábrelo. Por defecto usa PowerShell |
| macOS | `⌘ + espacio` → escribe *Terminal* → Intro. Usa `zsh` |
| Linux | `Ctrl + Alt + T`. Suele usar `bash` |

### 1.2 ¿Dónde estoy y qué hay aquí?

```bash
$ pwd          # ruta de la carpeta actual
$ ls           # su contenido
$ cd ~         # vuelve a tu carpeta personal
```

Apunta tres rutas: la de tu carpeta personal, la de tu Escritorio y la de Descargas. ¿Cuáles son absolutas? ¿Cómo llegarías a Descargas con una ruta **relativa** desde tu carpeta personal?

### 1.3 Variables de entorno y `PATH`

```bash
$ echo $HOME
$ echo $PATH
```

```powershell
> echo $env:USERPROFILE
> $env:PATH -split ";"
```

Cada carpeta del `PATH` es un sitio donde el shell busca los programas. Averigua dónde está el comando `ls` (o `Get-ChildItem`):

```bash
$ which ls
```

```powershell
> Get-Command ls
```

### 1.4 (Solo Windows) Instala WSL2

WSL2 te da un Linux real dentro de Windows y es lo que usa Docker Desktop por debajo. Abre PowerShell **como administrador**:

```powershell
> wsl --install
```

Reinicia cuando te lo pida. Al volver se abrirá Ubuntu y te pedirá un usuario y una contraseña de Linux. No tienen que coincidir con los de Windows y **no se ve nada mientras escribes la contraseña**: es normal.

> Si el proceso se alarga, déjalo en segundo plano y sigue con el bloque 2 en PowerShell.

**Punto de control 1:** sabes decir en qué carpeta estás y has visto el contenido de tu `PATH`.

---

## Bloque 2 · La terminal

### 2.1 Crea tu carpeta de trabajo del máster

Trabajaremos siempre en una **ruta corta, sin espacios ni tildes y fuera de OneDrive o iCloud**:

```bash
$ mkdir -p ~/proyectos/master
$ cd ~/proyectos/master
$ pwd
```

```powershell
> mkdir ~\proyectos\master
> cd ~\proyectos\master
> pwd
```

> En WSL, trabaja dentro de Linux (`/home/tu_usuario/proyectos/master`) y no en `/mnt/c/...`: es mucho más rápido.

### 2.2 Practica los comandos básicos

Prueba cada comando y observa qué ocurre. Los tienes todos en la [chuleta](CHEATSHEET.md).

```bash
$ echo "hola terminal" > saludo.txt     # crea un archivo con texto
$ echo "segunda línea" >> saludo.txt    # añade una línea
$ cat saludo.txt
$ cp saludo.txt copia.txt
$ mv copia.txt renombrado.txt
$ ls -la
$ rm renombrado.txt
$ history | tail -n 5                  # tus últimos 5 comandos
```

Trucos: `Tab` autocompleta, `↑` recupera el comando anterior, `Ctrl+C` corta lo que se está ejecutando y `Ctrl+R` busca en el historial.

### 2.3 Un gestor de paquetes

Comprueba que tienes un gestor de paquetes y úsalo para instalar `git`, que usaremos durante todo el curso:

| Sistema | Comando |
|---|---|
| Windows | `winget install Git.Git` |
| macOS | Instala Homebrew desde <https://brew.sh> y luego `brew install git` |
| Ubuntu / WSL | `sudo apt update && sudo apt install git` |

```bash
$ git --version
```

### 2.4 Práctica · Búsqueda del tesoro

1. Descarga [`ejercicios/tesoro.zip`](ejercicios/tesoro.zip) y muévelo a `~/proyectos/master` **con la terminal**:
   ```bash
   $ mv ~/Downloads/tesoro.zip ~/proyectos/master/     # o ~/Descargas
   ```
   ```powershell
   > mv ~\Downloads\tesoro.zip ~\proyectos\master\
   ```
2. Descomprímelo y entra:
   ```bash
   $ unzip tesoro.zip && cd tesoro       # en Ubuntu/WSL: sudo apt install unzip
   ```
   ```powershell
   > Expand-Archive tesoro.zip -DestinationPath . ; cd tesoro
   ```
3. Lee `LEEME.txt` y sigue las pistas. **Solo puedes usar la terminal.**
4. Al final tendrás la respuesta guardada en `entrega/respuesta.txt`. La comprobarás con Python en el bloque 4.

> En Windows, PowerShell muestra los archivos que empiezan por punto sin necesidad de `-Force`. En macOS y Linux están ocultos.

**Punto de control 2:** tienes `entrega/respuesta.txt` con 5 partes separadas por guiones y has borrado la carpeta `trampa`.

---

## Bloque 3 · IDEs y editores

Este bloque es sobre todo de exposición. Mientras tanto:

1. Si eres estudiante, solicita **GitHub Education** (<https://education.github.com>) con tu correo `@uma.es`. Te da GitHub Copilot y otras herramientas gratis. La aprobación puede tardar unos días.
2. Solicita la **licencia educativa de JetBrains** (<https://www.jetbrains.com/academy/student-pack/>) para IntelliJ IDEA, PyCharm y DataGrip.
3. Comprueba que puedes abrir [Google Colab](https://colab.research.google.com) con tu cuenta de Google. Es el **plan B** si algo falla en tu portátil.

**Normas para usar asistentes de IA en el laboratorio:**
- Úsalos para aprender, no para dejar de aprender.
- Si no sabes explicar el código que entregas, no es tuyo.
- Nunca pegues contraseñas, claves de API ni datos personales.
- Comprueba siempre lo que te respondan.

**Punto de control 3:** has solicitado GitHub Education y la licencia de JetBrains.

---

## Bloque 4 · Python y VS Code

### 4.1 Instala Python 3.13

| Sistema | Comando |
|---|---|
| Windows | `winget install Python.Python.3.13` |
| macOS | `brew install python@3.13` |
| Ubuntu / WSL | `sudo apt install python3 python3-venv python3-pip` |

Si en Windows usas el instalador de <https://python.org>, marca **Add python.exe to PATH** en la primera pantalla.

**Cierra la terminal y ábrela de nuevo** (así se recarga el `PATH`) y comprueba:

```bash
$ python3 --version        # macOS / Linux
```

```powershell
> python --version         # Windows (también vale: py --version)
```

<details>
<summary>Problemas frecuentes</summary>

- **Windows abre la Microsoft Store al escribir `python`:** Configuración → Aplicaciones → Configuración avanzada de aplicaciones → *Alias de ejecución de aplicaciones*. Desactiva `python.exe` y `python3.exe`.
- **`python: command not found` en macOS o Linux:** usa `python3`. Si quieres, crea un alias: `echo 'alias python=python3' >> ~/.zshrc` (o `~/.bashrc`).
- **Aparece una versión antigua:** mira qué ejecutable se está usando con `which -a python3` o `where.exe python`. El orden del `PATH` decide cuál gana.
- **En Ubuntu, `apt` instala una versión distinta de la 3.13:** para esta práctica vale igual. Si necesitas exactamente la 3.13, instala `uv` (<https://docs.astral.sh/uv/>) y ejecuta `uv python install 3.13`.

</details>

Entra en el intérprete interactivo (REPL) y sal de él:

```python
>>> print("Hola, máster")
>>> 2 ** 10
>>> exit()
```

### 4.2 Instala y configura VS Code

1. Instálalo desde <https://code.visualstudio.com>, o con `winget install Microsoft.VisualStudioCode` / `brew install --cask visual-studio-code`.
2. Activa el comando `code` en la terminal. En macOS: paleta (`⇧⌘P`) → *Shell Command: Install 'code' command in PATH*. En Windows y Linux se activa solo.
3. Instala estas extensiones desde la vista de extensiones (`⇧⌘X` / `Ctrl+Shift+X`):
   - **Python** (incluye Pylance y el depurador)
   - **Jupyter**
   - **Ruff**
   - **WSL** (solo Windows)
4. Abre la configuración en JSON (paleta → *Preferences: Open User Settings (JSON)*) y añade:
   ```json
   {
     "editor.formatOnSave": true,
     "files.autoSave": "afterDelay",
     "[python]": {
       "editor.defaultFormatter": "charliermarsh.ruff"
     }
   }
   ```

### 4.3 Primer script y depurador

```bash
$ cd ~/proyectos/master
$ mkdir primer-script && cd primer-script
$ code .
```

En VS Code, crea `hola.py`:

```python
import platform
import sys

nombre = input("¿Cómo te llamas? ")
print(f"Hola, {nombre}")
print(f"Python {sys.version.split()[0]}")
print(f"en {platform.system()}")
```

1. Selecciona el intérprete: paleta → *Python: Select Interpreter* → Python 3.13.
2. Ejecútalo con el botón de ejecutar (arriba a la derecha).
3. Ejecútalo desde la terminal integrada (`` Ctrl+` ``): `python hola.py`.
4. Pon un *breakpoint* en la línea del primer `print` (clic a la izquierda del número de línea) y pulsa `F5`. Mira el valor de `nombre` en el panel *Variables*.

### 4.4 Práctica final · Comprueba el tesoro

```bash
$ cd ~/proyectos/master/tesoro
$ code .
$ python comprobar.py
```

Abre `comprobar.py` y lee qué hace, aunque todavía no entiendas cada línea. Si no dice que la respuesta es correcta, revísala o pon un *breakpoint* para ver qué está leyendo.

**Punto de control 4 (checklist de salida):**

- [ ] `python --version` (o `python3 --version`) muestra 3.13.x
- [ ] `code .` abre VS Code desde la terminal
- [ ] `git --version` responde
- [ ] `python comprobar.py` confirma que la respuesta es correcta
- [ ] (Windows) `wsl` abre Ubuntu

---

## Para practicar en casa (opcional)

- Juega a **OverTheWire: Bandit** (<https://overthewire.org/wargames/bandit/>), niveles 0–10: más búsquedas del tesoro en un servidor Linux real.
- Personaliza tu *prompt* con **Starship** (<https://starship.rs>).
- Recorre el tutorial interactivo de VS Code: paleta → *Help: Welcome* → *Walkthroughs*.

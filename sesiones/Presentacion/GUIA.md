# Guía de instalación · Visual Studio Code, Git y GitHub

Esta guía deja tu ordenador listo para trabajar en el laboratorio. Vas a instalar tres cosas:

| Herramienta | Qué es |
|---|---|
| **Visual Studio Code** | El editor de código que usaremos en clase |
| **Git** | El programa que guarda el historial de tu código en tu ordenador |
| **GitHub** | La web donde se alojan los repositorios de Git para compartirlos y colaborar |

Sigue las partes **en este orden**. En Windows es importante instalar VS Code antes que Git, porque el instalador de Git lo detecta y lo configura como editor.

En los bloques de comandos, los que empiezan por `$` son para la terminal de **macOS y Linux** (bash o zsh) y los que empiezan por `>` son para **PowerShell** en Windows. No copies el `$` ni el `>`.

---

## Parte 1 · Visual Studio Code

### ¿Qué es?

Visual Studio Code (VS Code) es un editor de código gratuito y multiplataforma de Microsoft. Por sí solo es ligero, y con **extensiones** se convierte en un entorno completo para Python, notebooks de Jupyter, Docker, Git y casi cualquier lenguaje.

> No lo confundas con **Visual Studio**, que es otro producto de Microsoft: un IDE pesado, pensado sobre todo para C# y .NET en Windows. En este curso usamos **Visual Studio Code**.

### Instalación

**Windows**

Opción A, desde la terminal (PowerShell):

```powershell
> winget install -e --id Microsoft.VisualStudioCode
```

Opción B, con el instalador: descarga el *User Installer* de <https://code.visualstudio.com/download>. En la pantalla *Seleccionar tareas adicionales* marca:
- **Agregar a PATH** (viene marcado; no lo quites).
- **Agregar la acción "Abrir con Code"** al menú contextual de archivos y de carpetas.

**macOS**

Opción A, con Homebrew:

```bash
$ brew install --cask visual-studio-code
```

Opción B: descarga el `.zip` para macOS (*Universal*) de <https://code.visualstudio.com/download>, descomprímelo y **arrastra Visual Studio Code a la carpeta Aplicaciones**. Si lo ejecutas desde Descargas, dará problemas al actualizarse.

Después, activa el comando `code` en la terminal: abre VS Code, pulsa `⇧⌘P`, escribe *shell command* y elige **Shell Command: Install 'code' command in PATH**.

**Linux (Ubuntu / Debian)**

Descarga el paquete `.deb` de <https://code.visualstudio.com/download> e instálalo:

```bash
$ sudo apt install ./code_*.deb
```

El paquete añade el repositorio de Microsoft, así que VS Code se actualizará con el resto del sistema (`sudo apt upgrade`). En Fedora usa el `.rpm`. También está disponible como Snap: `sudo snap install code --classic`.

### Comprobación

Cierra la terminal, ábrela de nuevo y ejecuta:

```bash
$ code --version
$ code .
```

El segundo comando abre VS Code en la carpeta actual. Si funciona, la instalación está completa.

### Configuración básica

1. **Extensiones.** Abre la vista de extensiones (`⇧⌘X` en macOS, `Ctrl+Shift+X` en Windows y Linux) e instala:
   - **Python** (de Microsoft; incluye Pylance y el depurador)
   - **Jupyter** (de Microsoft)
   - **WSL** (de Microsoft; solo en Windows)
   - **Spanish Language Pack** (opcional, si prefieres la interfaz en español)
2. **Guardado automático.** Menú *Archivo* → marca **Guardado automático**.
3. **Terminal integrada.** Ábrela con ``Ctrl+` `` (también en macOS). Es la misma terminal de tu sistema, abierta en la carpeta del proyecto.
4. **Paleta de comandos.** `⇧⌘P` o `Ctrl+Shift+P`. Desde aquí puedes llegar a cualquier opción de VS Code escribiendo su nombre.

---

## Parte 2 · Git

### ¿Qué es Git y para qué sirve?

Git es un **sistema de control de versiones**: un programa que guarda la historia completa de los archivos de un proyecto. Cada vez que decides que tu trabajo está en un punto que merece la pena guardar, haces un **commit**: una "foto" de todos los archivos en ese momento, con un mensaje que explica qué ha cambiado.

Sin control de versiones acabamos con carpetas como esta:

```
analisis.py
analisis_v2.py
analisis_v2_bueno.py
analisis_FINAL.py
analisis_FINAL_ahora_si.py
```

Con Git hay un solo `analisis.py` y un historial con todas sus versiones. Eso permite:

- **Volver atrás** a cualquier versión anterior si algo deja de funcionar.
- **Saber qué cambió, cuándo, quién lo hizo y por qué.**
- **Probar ideas en ramas** (*branches*): copias paralelas del proyecto que se pueden descartar o integrar después.
- **Trabajar en equipo**: varias personas modifican el mismo proyecto a la vez y Git combina los cambios.
- **Tener una copia de seguridad** en un servidor remoto, como GitHub.

Git es el estándar de la industria: lo usan prácticamente todas las empresas de software y de datos, y lo usarás en las prácticas en empresa y en el TFM.

### Git y GitHub no son lo mismo

| | Git | GitHub |
|---|---|---|
| Qué es | Un programa | Una plataforma web |
| Dónde funciona | En tu ordenador, incluso sin internet | En internet |
| Para qué | Guardar el historial de un proyecto | Alojar repositorios de Git, compartirlos y colaborar |
| Alternativas | – | GitLab, Bitbucket, Gitea |

### Vocabulario mínimo

| Término | Significado |
|---|---|
| **Repositorio** (*repo*) | Carpeta de un proyecto cuyo historial gestiona Git |
| **Commit** | Versión guardada del proyecto, con un mensaje descriptivo |
| **Rama** (*branch*) | Línea de desarrollo independiente. La principal se llama `main` |
| **Remoto** (*remote*) | Copia del repositorio en un servidor (por ejemplo, en GitHub) |
| **clone** | Descargar un repositorio remoto a tu ordenador |
| **push** | Subir tus commits al remoto |
| **pull** | Traer a tu ordenador los commits nuevos del remoto |

El flujo básico de trabajo es este:

```
tu carpeta  --git add-->  preparados  --git commit-->  historial local  --git push-->  GitHub
tu carpeta  <------------------------------ git pull --------------------------------  GitHub
```

No hace falta memorizarlo ahora: a lo largo del curso trabajaremos Git con detalle.

### Instalación

**Windows**

Opción A, desde PowerShell:

```powershell
> winget install -e --id Git.Git
```

Opción B, con el instalador de <https://git-scm.com/download/win>. Acepta las opciones por defecto **salvo estas dos**:
- *Choosing the default editor used by Git*: elige **Use Visual Studio Code as Git's default editor**.
- *Adjusting the name of the initial branch in new repositories*: elige **Override the default branch name** y escribe `main`.

El instalador incluye **Git Bash** (una terminal tipo Linux) y **Git Credential Manager**, que gestiona el inicio de sesión en GitHub.

**macOS**

macOS incluye Git con las herramientas de línea de comandos de Apple. Si al escribir `git` en la terminal te propone instalarlas, acepta. También puedes instalarlas tú:

```bash
$ xcode-select --install
```

Para tener una versión más reciente, instálalo con Homebrew:

```bash
$ brew install git
```

**Linux**

```bash
$ sudo apt update && sudo apt install git     # Ubuntu / Debian
$ sudo dnf install git                        # Fedora
```

### Comprobación

Cierra la terminal, ábrela de nuevo y ejecuta:

```bash
$ git --version
```

Debe mostrar algo como `git version 2.5x.x`.

### Configuración inicial

Git firma cada commit con tu nombre y tu correo. Configúralos **una sola vez** por ordenador. Estos comandos son iguales en todos los sistemas:

```bash
$ git config --global user.name "Nombre Apellido"
$ git config --global user.email "tu_correo@ejemplo.com"
$ git config --global init.defaultBranch main
$ git config --global core.editor "code --wait"
```

- Usa **el mismo correo que en tu cuenta de GitHub**; así tus commits aparecerán asociados a tu perfil. Si no quieres que tu correo sea público, GitHub te da uno privado en *Settings → Emails* (del tipo `12345678+usuario@users.noreply.github.com`).
- `init.defaultBranch main` hace que la rama principal se llame `main`, igual que en GitHub.
- `core.editor` hace que Git abra VS Code cuando necesite que escribas un mensaje largo.

Configura también los saltos de línea, que Windows guarda de forma distinta a macOS y Linux:

```powershell
> git config --global core.autocrlf true        # Windows
```

```bash
$ git config --global core.autocrlf input       # macOS y Linux
```

Comprueba la configuración:

```bash
$ git config --global --list
```

---

## Parte 3 · GitHub

### Crea tu cuenta

1. Entra en <https://github.com/signup> y crea una cuenta.
   - Elige un **nombre de usuario profesional** (por ejemplo, `nombreapellido`): aparecerá en tu CV y en tus proyectos.
   - Puedes registrarte con tu correo personal y añadir después el de la UMA en *Settings → Emails*.
2. Activa la **verificación en dos pasos** (*Settings → Password and authentication*). GitHub la exige para contribuir a repositorios. Usa una app de autenticación (Google Authenticator, Microsoft Authenticator, 1Password…) y **guarda los códigos de recuperación**.
3. Si eres estudiante, solicita **GitHub Education** en <https://education.github.com/pack> con tu correo `@uma.es`. Es gratuito y da acceso, entre otras cosas, a GitHub Copilot.

### Conecta Git con GitHub

GitHub **no acepta tu contraseña** para las operaciones de Git (`clone`, `push`…). Hay que autorizar a tu ordenador por otra vía. Elige **una** de estas dos opciones; si no sabes cuál, usa la A.

#### Opción A (recomendada) · HTTPS con GitHub CLI

GitHub CLI (`gh`) es la herramienta oficial de GitHub para la terminal. Inicia sesión en el navegador y configura Git para que no vuelva a pedirte nada.

1. Instálala:

   | Sistema | Comando |
   |---|---|
   | Windows | `winget install -e --id GitHub.cli` |
   | macOS | `brew install gh` |
   | Ubuntu / Debian | `sudo apt install gh` (o sigue <https://cli.github.com>) |

2. Cierra la terminal, ábrela de nuevo e inicia sesión:

   ```bash
   $ gh auth login
   ```

   Responde a las preguntas así:
   - *Where do you use GitHub?* → **GitHub.com**
   - *What is your preferred protocol for Git operations?* → **HTTPS**
   - *Authenticate Git with your GitHub credentials?* → **Yes**
   - *How would you like to authenticate GitHub CLI?* → **Login with a web browser**

3. La terminal mostrará un código de un solo uso. Pulsa Intro, se abrirá el navegador: pega el código y autoriza.

4. Comprueba que todo ha ido bien:

   ```bash
   $ gh auth status
   ```

> En Windows, **Git Credential Manager** (incluido en Git) también funciona sin GitHub CLI: la primera vez que hagas `git push` se abrirá el navegador para que inicies sesión.

#### Opción B · Claves SSH

Una clave SSH es un par de archivos: una clave **privada**, que nunca sale de tu ordenador, y una **pública**, que subes a GitHub. Así GitHub reconoce a tu ordenador sin contraseña.

1. Genera la clave (pulsa Intro para aceptar la ruta por defecto; puedes ponerle una frase de contraseña o dejarla vacía):

   ```bash
   $ ssh-keygen -t ed25519 -C "tu_correo@ejemplo.com"
   ```

2. Copia la clave **pública** al portapapeles:

   ```bash
   $ pbcopy < ~/.ssh/id_ed25519.pub                  # macOS
   $ cat ~/.ssh/id_ed25519.pub                       # Linux: selecciónala y cópiala
   ```

   ```powershell
   > Get-Content ~\.ssh\id_ed25519.pub | Set-Clipboard
   ```

3. En GitHub: *Settings → SSH and GPG keys → New SSH key*. Ponle un nombre (por ejemplo, *Portátil*), pega la clave y guarda.

4. Comprueba la conexión (la primera vez te pedirá confirmar la huella del servidor; escribe `yes`):

   ```bash
   $ ssh -T git@github.com
   ```

   Debe responder `Hi usuario! You've successfully authenticated...`.

5. Con SSH, clona los repositorios con la dirección que empieza por `git@github.com:` en lugar de `https://`.

> **Nunca compartas ni subas a ningún sitio el archivo `id_ed25519` (sin `.pub`).** Es tu clave privada.

### Prueba final

Vamos a comprobar que todo funciona de principio a fin.

1. En GitHub, pulsa **+ → New repository**. Llámalo `prueba-git`, márcalo como **Private**, activa **Add a README file** y pulsa *Create repository*.
2. En la página del repositorio, pulsa **Code** y copia la dirección (HTTPS o SSH, según la opción que hayas elegido).
3. En tu terminal:

   ```bash
   $ mkdir -p ~/proyectos && cd ~/proyectos
   $ git clone https://github.com/TU_USUARIO/prueba-git.git
   $ cd prueba-git
   $ code .
   ```

4. En VS Code, edita `README.md`: añade una línea con tu nombre y guarda.
5. Vuelve a la terminal:

   ```bash
   $ git status                              # README.md aparece como modificado
   $ git add README.md
   $ git commit -m "Añade mi nombre al README"
   $ git push
   ```

6. Recarga la página del repositorio en GitHub: tu cambio debe aparecer.

Si el `push` funciona sin pedirte la contraseña, Git, GitHub y VS Code están bien configurados. Puedes borrar el repositorio de prueba desde *Settings → Danger Zone → Delete this repository*.

> VS Code también puede hacer todo esto sin terminal, desde el panel **Control de código fuente** (el icono de ramas de la barra lateral). Conviene saber hacerlo con comandos para entender qué ocurre por debajo.

---

## Problemas frecuentes

| Problema | Solución |
|---|---|
| `code`, `git` o `gh` "no se reconoce" / "command not found" justo después de instalar | Cierra **todas** las terminales (y VS Code) y ábrelas de nuevo para que se recargue el `PATH` |
| macOS: `code: command not found` | En VS Code: `⇧⌘P` → **Shell Command: Install 'code' command in PATH** |
| macOS: VS Code no se actualiza o pide permisos cada vez | Muévelo a la carpeta **Aplicaciones** |
| `git push` pide usuario y contraseña, y la contraseña no funciona | GitHub no acepta contraseñas. Ejecuta `gh auth login` (opción A) o configura SSH (opción B) |
| `Permission denied (publickey)` | La clave SSH no está añadida a GitHub o estás usando otra. Revisa el paso 3 de la opción B y prueba `ssh -T git@github.com` |
| `Author identity unknown` al hacer commit | Falta configurar `user.name` y `user.email` (ver *Configuración inicial*) |
| Los commits no aparecen asociados a tu perfil de GitHub | El `user.email` de Git no coincide con ningún correo de tu cuenta. Añádelo en *Settings → Emails* o cambia el de Git |
| Al hacer commit se abre un editor raro en la terminal (Vim) | Escribe `:q!` y pulsa Intro para salir. Después configura `git config --global core.editor "code --wait"` |
| `fatal: not a git repository` | No estás dentro de la carpeta del repositorio. Usa `cd` para entrar en ella |

---

## Checklist

- [ ] `code --version` muestra la versión de VS Code
- [ ] `code .` abre VS Code en la carpeta actual
- [ ] Extensiones Python y Jupyter instaladas (y WSL en Windows)
- [ ] `git --version` muestra la versión de Git
- [ ] `git config --global --list` muestra tu nombre y tu correo
- [ ] Tienes cuenta de GitHub con verificación en dos pasos
- [ ] `gh auth status` (opción A) o `ssh -T git@github.com` (opción B) confirma la conexión
- [ ] Has hecho `clone`, `commit` y `push` en el repositorio `prueba-git`

## Enlaces

- Visual Studio Code: <https://code.visualstudio.com/docs>
- Git: <https://git-scm.com/book/es/v2> (libro oficial *Pro Git*, en español)
- GitHub CLI: <https://cli.github.com/manual>
- Claves SSH en GitHub: <https://docs.github.com/es/authentication/connecting-to-github-with-ssh>

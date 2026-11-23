"""Comprueba la práctica «El catálogo bajo control de versiones».

Ejecútalo desde tu carpeta catalogo-datasets:
    python3 comprobar_git.py        (en Windows: python comprobar_git.py)

Puedes ejecutarlo tantas veces como quieras: después de cada bloque de la guía,
las comprobaciones de ese bloque deberían pasar a [OK]. No modifica nada de tu
repositorio: solo lo consulta (y hace un git fetch para mirar GitHub).
"""
import re
import subprocess
import sys
from pathlib import Path

MENSAJES_VAGOS = {"cambios", "cambio", "update", "updates", "asdf", "wip", "fix", "arreglos",
                  "arreglos varios", "commit", "prueba", "pruebas", "test", "ya funciona", "final", "."}
NO_DEBEN_ESTAR = {  # ruta de ejemplo → cómo se llama en la pista
    ".venv/pyvenv.cfg": ".venv/",
    "__pycache__/catalogo.cpython-313.pyc": "__pycache__/",
    "salida/informe.json": "salida/",
    ".env": ".env",
}

aciertos = 0
total = 0


def comprobar(descripcion: str, ok: bool, pista: str = "") -> bool:
    global aciertos, total
    total += 1
    aciertos += ok
    print(f"  [{'OK' if ok else '  '}] {descripcion}")
    if not ok and pista:
        print(f"         Pista: {pista}")
    return ok


def git(*args: str, timeout: int = 30) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(["git", *args], capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout)
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(args, 1, "", "timeout")


def salida(*args: str) -> str:
    return git(*args).stdout.strip()


if not Path("catalogo.py").is_file():
    raise SystemExit("\nEjecuta comprobar_git.py desde tu carpeta catalogo-datasets, junto a catalogo.py.")

# ------------------------------------------------------------------ Bloque 2
print("\nBloque 2 · Tu repositorio")
raiz = salida("rev-parse", "--show-toplevel")
es_repo = bool(raiz) and Path(raiz).resolve() == Path.cwd().resolve()
pista = "ejecuta git init dentro de catalogo-datasets"
if raiz and not es_repo:
    pista = (f"estás dentro de otro repositorio ({raiz}). Tu carpeta catalogo-datasets "
             "no debe estar dentro de laboratorio-mbd-2026 ni de otro repositorio")
comprobar("catalogo-datasets es un repositorio de Git", es_repo, pista)
if not es_repo:
    print(f"\n{aciertos} de {total} comprobaciones correctas. Sin repositorio no se puede comprobar nada más.")
    sys.exit()

hay_commits = git("rev-parse", "--verify", "-q", "HEAD").returncode == 0
rama = salida("branch", "--show-current")
comprobar("Estás en la rama main", rama == "main",
          f"estás en '{rama}'. Vuelve con: git switch main" if rama
          else "configura la rama por defecto con: git config --global init.defaultBranch main")

n_commits = int(salida("rev-list", "--count", "HEAD") or 0) if hay_commits else 0
comprobar("Hay al menos 3 commits", n_commits >= 3,
          f"tienes {n_commits}. Guarda el proyecto en varios commits, uno por cada cambio lógico")

autores = set(salida("log", "--format=%an <%ae>").splitlines()) if hay_commits else set()
sin_identidad = [a for a in autores if "(none)" in a or a.startswith("<") or ".local>" in a]
comprobar("Tus commits llevan tu nombre y tu correo", hay_commits and not sin_identidad,
          "configura git config --global user.name y user.email (los commits ya hechos se quedan así)")

asuntos = salida("log", "--no-merges", "--format=%s").splitlines() if hay_commits else []
vagos = [s for s in asuntos if s.strip().lower().rstrip("!.") in MENSAJES_VAGOS or len(s.split()) < 2]
comprobar("Los mensajes de commit explican el cambio", hay_commits and not vagos,
          f"poco claros: {', '.join(repr(v) for v in vagos[:3])}. Usa frases como "
          "'Añade el catálogo de datasets'. Se corrigen los nuevos; los antiguos se pueden quedar")

pendiente = salida("status", "--porcelain")
comprobar("No hay cambios sin guardar (git status limpio)", hay_commits and not pendiente,
          "revisa git status: haz commit de lo que falte, o añádelo al .gitignore si no debe guardarse")

# ------------------------------------------------------------------ .gitignore
print("\nBloque 2 · Qué se guarda y qué no")
seguidos = set(salida("ls-files").splitlines())
comprobar("El .gitignore está guardado en el repositorio", ".gitignore" in seguidos,
          "créalo (con el punto delante) y haz commit de él")
imprescindibles = ["README.md", "catalogo.py", "comprobar.py", "datos/datasets.json"]
faltan = [f for f in imprescindibles if f not in seguidos]
comprobar("README.md, el código y los datos están en el repositorio", not faltan,
          f"faltan: {', '.join(faltan)}")
docker = [f for f in ("informe.py", "requirements.txt", "Dockerfile", ".dockerignore") if Path(f).is_file()]
faltan_docker = [f for f in docker if f not in seguidos]
comprobar("Los archivos de Docker que tienes también están en el repositorio", not faltan_docker,
          f"faltan: {', '.join(faltan_docker)}. ¿Los has metido en el .gitignore por error?")

no_ignorados = [nombre for ruta, nombre in NO_DEBEN_ESTAR.items()
                if git("check-ignore", "-q", "--no-index", ruta).returncode != 0]
comprobar("El .gitignore excluye .venv/, __pycache__/, salida/ y .env", not no_ignorados,
          f"añade al .gitignore: {', '.join(no_ignorados)}")

historia = set(salida("log", "--all", "--format=", "--name-only").splitlines())
colados = set()
for ruta in historia:
    partes = ruta.split("/")
    for nombre in NO_DEBEN_ESTAR.values():
        if (nombre.endswith("/") and nombre[:-1] in partes[:-1]) or partes[-1] == nombre:
            colados.add(nombre)
colados = sorted(colados)
comprobar("Nunca se ha guardado en un commit ningún archivo que no debía", not colados,
          f"en tu historia aparece {', '.join(colados)}. Quitarlo ahora no lo borra de los commits "
          "anteriores: pregunta al profesor cómo arreglarlo")

# ------------------------------------------------------------------ Bloque 4
print("\nBloque 4 · Ramas y conflictos")
fusiones = int(salida("rev-list", "--merges", "--count", "HEAD") or 0) if hay_commits else 0
comprobar("La historia tiene al menos un commit de fusión", fusiones >= 1,
          "provoca y resuelve el conflicto del apartado 4.3: crea un commit de fusión")
marcas = git("grep", "-n", "-E", r"^(<<<<<<<|>>>>>>>)( |$)").stdout.strip() if hay_commits else ""
comprobar("Ningún archivo guardado tiene marcas de conflicto", not marcas,
          f"quedan marcas en {marcas.splitlines()[0].rsplit(':', 2)[0] if marcas else ''}: "
          "bórralas, deja el texto bueno y haz un commit nuevo")
umbrales = re.findall(r"^UMBRAL_GRANDE\s*=\s*([\d_]+)\s*$",
                      Path("catalogo.py").read_text(encoding="utf-8"), flags=re.M)
comprobar("catalogo.py tiene una sola línea UMBRAL_GRANDE = 100_000",
          umbrales == ["100_000"] or umbrales == ["100000"],
          f"en catalogo.py hay {len(umbrales)} línea(s) UMBRAL_GRANDE con {umbrales}. "
          "Debe quedar una sola, con 100_000")
importa = subprocess.run([sys.executable, "-c", "import catalogo"], capture_output=True, text=True)
comprobar("catalogo.py se puede importar sin errores", importa.returncode == 0,
          (importa.stderr.strip().splitlines() or [""])[-1])

# ------------------------------------------------------------------ Bloque 5
print("\nBloque 5 · GitHub")
url = salida("config", "--get", "remote.origin.url")
comprobar("El remoto origin apunta a GitHub", "github.com" in url,
          f"origin es '{url}'" if url else "crea el repositorio en GitHub con gh repo create (apartado 5.1)")
seguimiento = salida("rev-parse", "--abbrev-ref", "main@{upstream}")
comprobar("Tu rama main está enlazada con origin/main", seguimiento == "origin/main",
          "súbela con: git push -u origin main")
sin_red = git("fetch", "-q", "origin", timeout=20).returncode != 0 if url else True
delante, detras = (salida("rev-list", "--left-right", "--count", "main...origin/main").split() + ["?", "?"])[:2]
nota = " (sin conexión: comparo con lo último que sabe tu repositorio)" if url and sin_red else ""
comprobar(f"Tu main y la de GitHub están igual{nota}", (delante, detras) == ("0", "0"),
          f"tienes {delante} commit(s) sin subir y te faltan {detras} por traer: "
          "git pull y después git push" if delante != "?" else "primero sube tu rama main a GitHub")
desde_web = "GitHub" in salida("log", "--format=%cn", "main") if hay_commits else False
comprobar("Has traído a tu ordenador un cambio hecho en la web de GitHub", desde_web,
          "edita el README en GitHub, haz commit allí y tráelo con git pull (apartado 5.2)")

# ------------------------------------------------------------------ Extras
etiqueta = git("rev-parse", "-q", "--verify", "refs/tags/v1.0").returncode == 0
if etiqueta:
    subida = bool(url) and bool(git("ls-remote", "--tags", "origin", "v1.0", timeout=20).stdout.strip())
    print(f"  [++] Reto extra: tienes la etiqueta v1.0{' y está en GitHub' if subida else ' (falta subirla: git push origin v1.0)'}")
if hay_commits and re.search(r"^Merge pull request #\d+", salida("log", "--merges", "--format=%s", "main"), re.M):
    print("  [++] Reto extra: has fusionado un pull request")

print(f"\n{aciertos} de {total} comprobaciones correctas.")
if aciertos == total:
    print("Tu catálogo está bajo control de versiones y en GitHub.")

import os

from tabulate import tabulate

nombre = os.environ.get("NOMBRE", "mundo")
print(f"Hola, {nombre}\n")
print(tabulate([["Docker", "contenedores"], ["Python", "lenguaje"]], headers=["Herramienta", "Qué es"]))

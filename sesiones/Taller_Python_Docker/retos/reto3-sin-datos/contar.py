"""Cuenta las ventas de cada producto a partir de datos/ventas.csv."""
import csv
from collections import Counter

with open("datos/ventas.csv", encoding="utf-8", newline="") as f:
    ventas = Counter(fila["producto"] for fila in csv.DictReader(f))

for producto, n in ventas.most_common():
    print(f"{producto:<12}{n:>4}")

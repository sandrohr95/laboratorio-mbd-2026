"""Prueba la clase Estacion. Ejecútalo con: python3 probar.py"""
from estaciones import Estacion

soho = Estacion("Soho", capacidad=2)
muelle = Estacion("Muelle Uno", capacidad=3)

soho.aparcar("B-01")
assert len(muelle.bicis) == 0, "Muelle Uno tiene bicis que se aparcaron en Soho"

soho.aparcar("B-02")
assert soho.libres == 0
try:
    soho.aparcar("B-03")
    raise AssertionError("Se ha aparcado una tercera bici en una estación de capacidad 2")
except ValueError:
    pass

assert repr(muelle) == "Estacion('Muelle Uno', 3)"
print([soho, muelle])
print("Correcto")

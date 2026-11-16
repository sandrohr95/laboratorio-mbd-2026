"""Estaciones de bicicletas con capacidad limitada."""


class Estacion:
    bicis = []

    def __init__(self, nombre, capacidad):
        self.nombre = nombre
        self.capacidad = capacidad

    def aparcar(self, bici):
        if len(self.bicis) > self.capacidad:
            raise ValueError(f"{self.nombre} está llena")
        self.bicis.append(bici)

    @property
    def libres(self):
        return self.capacidad - len(self.bicis)

    def __repr__(self):
        print(f"Estacion({self.nombre!r}, {self.capacidad})")

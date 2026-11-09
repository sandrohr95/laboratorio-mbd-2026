# Chuleta · Programación orientada a objetos en Python

## De Java a Python

| Java | Python |
|---|---|
| `public class Bicicleta { }` | `class Bicicleta:` |
| `public Bicicleta(String id) { this.id = id; }` | `def __init__(self, id): self.id = id` |
| `this` | `self`, que se escribe como **primer parámetro** de cada método |
| `new Bicicleta("B-01")` | `Bicicleta("B-01")` |
| `private int km;` | `self._km` (por convención: "no lo toques desde fuera") |
| `getKm()` / `setKm()` | Acceso directo `b.km` y, si hace falta validar, `@property` |
| `static` | Atributo de clase · `@classmethod` · `@staticmethod` |
| `toString()` | `__str__` (para usuarios) y `__repr__` (para programadores) |
| `equals()` / `compareTo()` | `__eq__` / `__lt__` |
| `extends Padre` | `class Hija(Padre):` |
| `super(id)` / `super.metodo()` | `super().__init__(id)` / `super().metodo()` |
| `@Override` | No hace falta: basta con definir un método con el mismo nombre |
| `interface` / `abstract class` | `class X(ABC)` con `@abstractmethod`, o `Protocol` |
| `enum` | `class X(Enum)` / `class X(StrEnum)` |
| `record` | `@dataclass(frozen=True)` |
| `null` | `None` |

## Una clase completa

```python
class Estacion:
    TARIFA = 0.05                        # atributo de clase (compartido)

    def __init__(self, nombre, capacidad):
        self.nombre = nombre             # atributos de instancia
        self.capacidad = capacidad
        self._bicis = []                 # las listas, SIEMPRE en __init__

    def aparcar(self, bici):             # método normal
        if len(self._bicis) >= self.capacidad:
            raise ValueError("Estación llena")
        self._bicis.append(bici)

    @property
    def libres(self):                    # se usa sin paréntesis: e.libres
        return self.capacidad - len(self._bicis)

    @classmethod
    def desde_dict(cls, d):              # constructor alternativo
        return cls(d["nombre"], int(d["capacidad"]))

    @staticmethod
    def es_nombre_valido(nombre):        # función normal dentro de la clase
        return bool(nombre.strip())

    def __repr__(self):
        return f"Estacion({self.nombre!r}, {self.capacidad})"

    def __len__(self):
        return len(self._bicis)
```

## Propiedad con validación

```python
class Temperatura:
    def __init__(self, celsius):
        self.celsius = celsius           # pasa por el setter

    @property
    def celsius(self):
        return self._celsius             # el valor se guarda con otro nombre

    @celsius.setter
    def celsius(self, valor):
        if valor < -273.15:
            raise ValueError("Por debajo del cero absoluto")
        self._celsius = valor
```

## Métodos especiales

| Método | Se activa con |
|---|---|
| `__init__(self, ...)` | `Clase(...)` |
| `__repr__(self)` / `__str__(self)` | La consola y las listas / `print(x)`, `str(x)`, `f"{x}"` |
| `__eq__(self, otro)` | `x == y` (devuelve `NotImplemented` si `otro` no es de tu clase) |
| `__lt__(self, otro)` | `x < y`, `sorted`, `min`, `max` |
| `__add__(self, otro)` | `x + y` |
| `__len__(self)` | `len(x)` |
| `__iter__(self)` | `for e in x` (devuelve `iter(...)`) |
| `__contains__(self, e)` | `e in x` |
| `__getitem__(self, clave)` | `x[clave]` |
| `__hash__(self)` | Usar `x` como clave de un diccionario o en un conjunto |

## Herencia, abstractas y *duck typing*

```python
from abc import ABC, abstractmethod

class Vehiculo(ABC):                     # no se puede instanciar
    def __init__(self, id):
        self.id = id

    @abstractmethod
    def tarifa(self, minutos): ...

class Bicicleta(Vehiculo):
    def tarifa(self, minutos):
        return minutos * 0.05

class BicicletaElectrica(Bicicleta):
    def __init__(self, id, bateria=100):
        super().__init__(id)             # inicializa la parte del padre
        self.bateria = bateria

    def tarifa(self, minutos):           # sobrescribe
        return super().tarifa(minutos) + 0.50

isinstance(e, Bicicleta)                 # ¿es de esa clase o de una hija?
issubclass(BicicletaElectrica, Vehiculo)
```

- **Herencia** = "es un". **Composición** = "tiene un" (un atributo que guarda otros objetos). Ante la duda, composición.
- ***Duck typing***: no importa la clase de un objeto, sino que tenga los métodos que necesitas.

## *Dataclasses*

```python
from dataclasses import dataclass, field

@dataclass(frozen=True, order=True)      # inmutable y ordenable
class Viaje:
    minutos: float                       # order=True compara en este orden
    origen: str
    destino: str
    etiquetas: list[str] = field(default_factory=list)   # nunca "= []"

    def __post_init__(self):             # validar después del __init__ generado
        if self.minutos <= 0:
            raise ValueError("Duración no válida")
```

| Opción | Qué hace |
|---|---|
| (por defecto) | Genera `__init__`, `__repr__` y `__eq__` |
| `frozen=True` | No se pueden cambiar los campos (`FrozenInstanceError`). Se puede meter en un `set` |
| `order=True` | Genera `<`, `<=`, `>`, `>=` |
| `field(default_factory=list)` | Valor por defecto modificable, uno nuevo para cada objeto |
| `dataclasses.asdict(x)` | Convierte el objeto en un diccionario |

Los campos con valor por defecto van **al final**.

## Enumeraciones

```python
from enum import Enum, StrEnum

class Nivel(Enum):
    AMARILLO = 1
    ROJO = 3

class Formato(StrEnum):                  # sus miembros también son str
    CSV = "csv"
    JSON = "json"

Nivel.ROJO.name, Nivel.ROJO.value        # ('ROJO', 3)
Formato("csv") is Formato.CSV            # desde un valor leído de un fichero
list(Formato)                            # todos los miembros
Formato("pdf")                           # ValueError
```

## Anotaciones de tipo

| Anotación | Significa |
|---|---|
| `x: int` · `def f(a: str) -> bool:` | Variable / parámetro y valor de retorno |
| `list[int]` · `dict[str, float]` · `set[str]` | Colecciones con el tipo de sus elementos |
| `tuple[float, float]` · `tuple[str, ...]` | Tupla de 2 floats · tupla de cualquier longitud |
| `str \| None` | Cadena o `None` |
| `class Tarificable(Protocol):` | "Cualquier objeto que tenga estos métodos" |

Python **no** las comprueba al ejecutar. Para comprobarlas:

```bash
$ pip install mypy
$ mypy mi_modulo.py
```

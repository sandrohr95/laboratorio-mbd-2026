"""FizzBuzz: múltiplos de 3 → Fizz, de 5 → Buzz, de ambos → FizzBuzz."""
import os
import platform

n = int(os.environ.get("N", "15"))
print(f"FizzBuzz hasta {n} · Python {platform.python_version()}")
for i in range(1, n + 1):
    if i % 15 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)

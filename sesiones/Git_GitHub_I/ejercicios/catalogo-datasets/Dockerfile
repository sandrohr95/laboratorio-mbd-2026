# Imagen de Docker del informe del catálogo
FROM python:3.13-slim

WORKDIR /app

# Primero las dependencias: esta capa se reutiliza mientras requirements.txt no cambie
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Después el código, que es lo que más cambia. Los datos NO se copian: se montan con -v
COPY catalogo.py informe.py ./

CMD ["python", "informe.py"]

# Basis-Image mit Python
FROM python:3.9-slim

# Installiere notwendige Systempakete (z. B. Git)
RUN apt-get update && apt-get install -y git && apt-get clean

# Setze das Arbeitsverzeichnis
WORKDIR /app

# Kopiere das Startskript in den Container
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Installiere Streamlit (falls nicht in requirements.txt vorhanden)
RUN pip install streamlit

# Führt das Startskript aus, wenn der Container gestartet wird
CMD ["/app/start.sh"]

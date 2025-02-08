# Base-Image
FROM python:3.9

# Setze das Arbeitsverzeichnis
WORKDIR /app

# Kopiere start.sh ins Image
COPY start.sh /app/start.sh

# Mache die Datei ausführbar
RUN chmod +x /app/start.sh

# Öffne den Port für Streamlit
EXPOSE 8501

# Setze das Startkommando
CMD ["/app/start.sh"]

#!/bin/bash

# Setze die URL deines GitHub-Repos und den Branch
REPO_URL="https://github.com/V4Cmeister/MCI_IoT_Monitor3D.git"
BRANCH="main"

# Klone das Repo, wenn es nicht existiert, oder ziehe die neuesten Änderungen
if [ ! -d "MCI_IoT_Monitor3D" ]; then
    echo "Klone das Repository..."
    git clone -b $BRANCH $REPO_URL
else
    echo "Aktualisiere das Repository..."
    cd MCI_IoT_Monitor3D
    git reset --hard  # Setzt Änderungen zurück, falls vorhanden
    git pull origin $BRANCH
    cd ..
fi

# Wechsle ins Repo-Verzeichnis
cd MCI_IoT_Monitor3D

# Prüfe und installiere Abhängigkeiten, falls requirements.txt geändert wurde
if [ -f "requirements.txt" ]; then
    echo "Installiere Abhängigkeiten aus requirements.txt..."
    pip install -r requirements.txt
fi

# Führe die Python-Dateien aus
echo "Starte DataCollector.py..."
python DataCollector.py &

echo "Starte Streamlit Login.py..."
streamlit run Login.py

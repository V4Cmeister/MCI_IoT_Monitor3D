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
cd /app/MCI_IoT_Monitor3D
export PYTHONPATH="$PYTHONPATH:/app/MCI_IoT_Monitor3D"

# Prüfe und installiere Abhängigkeiten, falls requirements.txt geändert wurde
pip install --upgrade pip
pip install -r requirements.txt

# Führe die Python-Dateien aus
echo "Starte DataCollector.py..."
python /app/MCI_IoT_Monitor3D/DataCollector.py &

sleep 2

echo "Starte Streamlit Login.py..."
streamlit run /app/MCI_IoT_Monitor3D/Login.py

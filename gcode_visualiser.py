import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import tkinter as tk
from tkinter import filedialog

def parse_gcode(filepath):
    """Parst die G-Code Datei und extrahiert X, Y, Z-Koordinaten."""
    x, y, z = [], [], []
    current_z = 0  # Falls Z nicht in jedem Befehl enthalten ist

    with open(filepath, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith(("G0", "G1")):  # Nur Bewegungsbefehle
                parts = line.split()
                x_val = next((float(p[1:]) for p in parts if p.startswith("X")), None)
                y_val = next((float(p[1:]) for p in parts if p.startswith("Y")), None)
                z_val = next((float(p[1:]) for p in parts if p.startswith("Z")), None)

                if z_val is not None:
                    current_z = z_val
                if x_val is not None and y_val is not None:
                    x.append(x_val)
                    y.append(y_val)
                    z.append(current_z)

    return np.array(x), np.array(y), np.array(z)

# Datei auswählen
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(title="Wähle eine G-Code Datei", filetypes=[("G-Code Dateien", "*.gcode *.nc")])

if not file_path:
    print("Keine Datei ausgewählt. Beende das Programm.")
    exit()

# G-Code verarbeiten
x, y, z = parse_gcode(file_path)

# Liniensegmente für die 3D-Darstellung erstellen
points = np.array([x, y, z]).T.reshape(-1, 1, 3)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# Farbcodierung basierend auf Höhe
norm = plt.Normalize(z.min(), z.max())
colors = plt.cm.jet(norm(z[:-1]))  # "jet" für hohen Kontrast

# 3D-Plot erstellen
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Linien mit Farbübergängen zeichnen
line_collection = Line3DCollection(segments, colors=colors, linewidth=2)
ax.add_collection(line_collection)

# Achsenbeschriftungen und Titel
ax.set_xlabel("X-Achse")
ax.set_ylabel("Y-Achse")
ax.set_zlabel("Z-Achse")
ax.set_title("G-Code 3D-Druckpfad mit Layer-Farben")

# Achsen anpassen, um das gesamte Druckbett darzustellen
ax.set_xlim(0, 235)
ax.set_ylim(0, 235)
ax.set_zlim(z.min(), z.max())

# Isometrische Ansicht von rechts oben
ax.view_init(elev=30, azim=-45)

plt.show()

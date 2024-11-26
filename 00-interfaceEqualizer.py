import tkinter as tk
from tkinter import filedialog, ttk

# Créer la fenêtre principale
root = tk.Tk()
root.title("Slider Simple")
root.geometry("400x600")

# Fonction pour mettre à jour la valeur affichée du slider
def update_value(value):
    print(f"Valeur : {slider.get()}")
    label.config(text=f"Valeur: {int(float(value))}")

# Fonction pour afficher la valeur du slider
def affichageSlider():
    print(f"Valeur du slider: {slider.get()}")

# Fonction pour sélectionner uniquement des .wav
def ouvertureWAV():
    file_path = filedialog.askopenfilename(filetypes=[("Fichiers WAV", "*.wav")])
    print("Fichier sélectionné :", file_path)

# Bouton pour ouvrir un fichier WAV
ttk.Button(root, text="Sélectionner un fichier WAV", command=ouvertureWAV).pack(pady=10)

# Label pour afficher la valeur du slider
label = ttk.Label(root, text="Valeur: 50")
label.pack(pady=10)

# Slider vertical
slider = ttk.Scale(
    root,
    from_=0,
    to=100,
    orient='vertical',
    length=300,
    command=update_value
)
slider.set(50)
slider.pack(pady=20)

# Bouton pour afficher la valeur du slider
button = ttk.Button(root, text="Afficher la valeur", command=affichageSlider)
button.pack(pady=20)

# Lancer l'application
root.mainloop()

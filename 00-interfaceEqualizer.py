import tkinter as tk
from tkinter import ttk

# Créer la fenetre principale
root = tk.Tk()
root.title("Sliders Simples")
root.geometry("800x600")  # Ajuster la taille de la fenêtre

# Fonction pour mettre à jour la valeur affichée du slider
def update_value(value, label):
    print(f"Valeur : {slider.get()}")
    label.config(text=f"Valeur: {int(float(value))}")

def affichageSlider(value):
    print(f"Valeur du slider: {slider.get()}")

# Créer un label pour afficher la valeur du slider
def create_slider_frame(root, row, col):
    frame = ttk.Frame(root)
    frame.grid(row=row, column=col, padx=20, pady=20)

    label = ttk.Label(frame, text="Valeur: 50")
    label.pack(pady=10)

    slider = ttk.Scale(
        frame,
        from_=0,
        to=100,
        orient='vertical',
        length=300,
        command=lambda value, label=label: update_value(value, label)
    )
    slider.set(50)
    slider.pack(pady=20)

    return slider, label

# Créer les sliders côte à côte dans un layout grid
sliders = []
labels = []

for i in range(4):
    slider, label = create_slider_frame(root, row=0, col=i)
    sliders.append(slider)
    labels.append(label)

# Créer un bouton pour afficher la valeur
button = ttk.Button(root, text="Afficher la valeur", command=affichageSlider)
button.grid(row=1, column=0, columnspan=4, pady=20)

# Lancement
root.mainloop()

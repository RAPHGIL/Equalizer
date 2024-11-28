import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Variables globales pour l'audio
frequence = None
audio_data = None
audio_data_filtered = None

# Création d'un dictionnaire pour les filtres
filtres = [
    {"a0": 0.2183, "a1": -0.2183, "b1": 1.7505, "b2": -0.7661, "gain": 1.0},
    {"a0": 0.194, "a1": -0.194, "b1": 1.5568, "b2": -0.6813, "gain": 1.0},
    {"a0": 0.1989, "a1": -0.1989, "b1": -1.2747, "b2": -0.5578, "gain": 1.0},
    {"a0": 0.1249, "a1": -0.1249, "b1": 1.0023, "b2": -0.4386, "gain": 1.0},
    {"a0": 0.0972, "a1": -0.00972, "b1": 0.7800, "b2": -0.3414, "gain": 1.0}
]

# Fonctions pour appliquer les filtres
def apply_filter(signal, a0, a1, b1, b2, gain=1.0):
    output = np.zeros_like(signal)
    output[0] = a0 * signal[0]
    output[1] = a0 * signal[1] + a1 * signal[0] + b1 * output[0]
    output[2:] = a0 * signal[2:] + a1 * signal[1:-1] + b1 * output[1:-1] + b2 * output[:-2]
    return output * gain

def apply_all_filters(signal, filters):
    return [apply_filter(signal, **filtres[i]) for i, f in enumerate(filters)]

# Classe principale de l'interface
class AudioEqualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Égaliseur Audio")
        self.root.geometry("600x500")

        # Initialisation des widgets
        self.sliders = []
        self.labels = []
        self.create_widgets()

    def create_widgets(self):
        """Créer les sliders et boutons pour l'interface"""
        # Cadre des sliders
        sliders_frame = ttk.Frame(self.root)
        sliders_frame.pack(pady=30)

        # Création des sliders et labels
        for i in range(5):
            frame = ttk.Frame(sliders_frame)
            frame.pack(side=tk.LEFT, padx=10)

            label = ttk.Label(frame, text=f"Filtre {i+1}: 50.0")
            label.pack()

            slider = ttk.Scale(frame, from_=100, to=0, orient="vertical", length=300, command=self.update_equalizer)
            slider.set(50)  # Valeur initiale
            slider.pack()

            self.sliders.append(slider)
            self.labels.append(label)

        # Cadre des boutons
        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack(pady=20)

        # Bouton pour charger un fichier audio
        load_button = ttk.Button(buttons_frame, text="Charger Audio", command=self.load_audio)
        load_button.pack(side=tk.LEFT, padx=5)

        # Bouton pour enregistrer l'audio filtré
        save_button = ttk.Button(buttons_frame, text="Enregistrer Audio Filtré", command=self.save_filtered_audio)
        save_button.pack(side=tk.LEFT, padx=5)

        # Bouton pour générer le graphique
        graph_button = ttk.Button(buttons_frame, text="Générer le Graphe", command=self.generate_and_save_graph)
        graph_button.pack(side=tk.LEFT, padx=5)

        # Label pour le statut
        self.status_label = ttk.Label(self.root, text="Prêt")
        self.status_label.pack(pady=10)

        # Cadre pour afficher les graphes
        self.graph_frame = ttk.Frame(self.root)
        self.graph_frame.pack(pady=20)

    def load_audio(self):
        """Charger un fichier audio WAV"""
        global frequence, audio_data
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers WAV", "*.wav")])
        if file_path:
            frequence, audio_data = wavfile.read(file_path)
            if len(audio_data.shape) > 1:
                audio_data = audio_data[:, 0]  # Si l'audio est stéréo, je ne garde que le premier canal
            self.status_label.config(text="Fichier audio chargé")
            self.update_equalizer()  # Mettre à jour les filtres et afficher les graphes

    def update_equalizer(self, event=None):
        """Mettre à jour les paramètres de l'égaliseur"""
        global audio_data_filtered
        # Appliquer les filtres en fonction des valeurs des sliders
        for i, slider in enumerate(self.sliders):
            filtres[i]["gain"] = slider.get() / 50  # Normalisation à [0, 2]
            self.labels[i].config(text=f"Filtre {i+1}: {slider.get():.1f}")

        if audio_data is not None:
            # Appliquer les filtres et combiner les signaux filtrés
            filtered_signals = apply_all_filters(audio_data, filtres)
            audio_data_filtered = np.sum(filtered_signals, axis=0)
            self.status_label.config(text="Audio filtré")

    def save_filtered_audio(self):
        """Enregistrer le fichier audio filtré"""
        global audio_data_filtered
        if audio_data_filtered is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("Fichiers WAV", "*.wav")])
            if file_path:
                # Normalisation et enregistrement du fichier
                normalized_data = np.int16(audio_data_filtered / np.max(np.abs(audio_data_filtered)) * 32767)
                wavfile.write(file_path, frequence, normalized_data)
                self.status_label.config(text="Audio filtré enregistré")

    def generate_and_save_graph(self):
        """Générer et enregistrer le graphique du signal original et filtré"""
        if audio_data is not None:
            # Créer une nouvelle figure pour le graphique
            fig, axs = plt.subplots(2, 1, figsize=(8, 6))

            # Graphique du signal original
            axs[0].plot(audio_data[:1000], label="Signal Original")
            axs[0].set_title("Signal Original")
            axs[0].set_xlabel("Échantillons")
            axs[0].set_ylabel("Amplitude")
            axs[0].legend()

            # Graphique du signal filtré
            if audio_data_filtered is not None:
                axs[1].plot(audio_data_filtered[:1000], label="Signal Filtré", color='r')
                axs[1].set_title("Signal Filtré")
                axs[1].set_xlabel("Échantillons")
                axs[1].set_ylabel("Amplitude")
                axs[1].legend()

            # Enregistrer le graphique en tant que fichier PNG
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Fichiers PNG", "*.png")])
            if file_path:
                fig.savefig(file_path)  # Sauvegarde en PNG
                self.status_label.config(text="Graphique enregistré")

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = AudioEqualizerApp(root)
    root.mainloop()

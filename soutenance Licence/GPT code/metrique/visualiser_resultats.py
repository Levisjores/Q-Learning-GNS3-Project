"""import tkinter as tk
from tkinter import ttk
import csv

FICHIER_CSV = "metriques_fusionnees.csv"

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📊 Visualisation des Métriques Réseau")
        self.geometry("1000x500")
        self.resizable(True, True)

        self.method_filter = tk.StringVar()
        self.method_filter.set("Tous")

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(filter_frame, text="Méthode :").pack(side=tk.LEFT)
        method_menu = ttk.Combobox(filter_frame, textvariable=self.method_filter, values=["Tous", "SSH", "SNMP", "Wireshark", "Scapy"], state="readonly")
        method_menu.pack(side=tk.LEFT, padx=5)
        method_menu.bind("<<ComboboxSelected>>", lambda e: self.load_data())

        self.tree = ttk.Treeview(self, columns=("Date", "Routeur", "Méthode", "Input", "Output", "Input errors", "Autres"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_by(c, False))
            self.tree.column(col, width=120, anchor="w")
        self.tree.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            with open(FICHIER_CSV, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if self.method_filter.get() == "Tous" or row["Méthode"] == self.method_filter.get():
                        self.tree.insert("", "end", values=(
                            row["Date"], row["Routeur"], row["Méthode"],
                            row["Input"], row["Output"], row["Input errors"], row["Autres"]
                        ))
        except FileNotFoundError:
            print("Fichier CSV introuvable. Lance initialiser_csv.py d'abord.")

    def sort_by(self, col, descending):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        data.sort(reverse=descending)
        for index, (val, child) in enumerate(data):
            self.tree.move(child, '', index)
        self.tree.heading(col, command=lambda: self.sort_by(col, not descending))

if __name__ == "__main__":
    app = Application()
    app.mainloop()
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Button, Label, filedialog, messagebox
from tkinter.ttk import Treeview
from openpyxl import Workbook

# Nom du fichier CSV fusionné
CSV_FUSIONNE = 'metriques_fusionnees.csv'

# ✅ 1. Créer le fichier s'il n'existe pas
def initialiser_fichier_csv():
    if not os.path.exists(CSV_FUSIONNE):
        colonnes = ["timestamp", "lien", "latence", "perte", "congestion", "bande_passante", "sauts", "goulot"]
        df = pd.DataFrame(columns=colonnes)
        df.to_csv(CSV_FUSIONNE, index=False)
        print("Fichier initialisé :", CSV_FUSIONNE)

# ✅ 2. Exporter vers Excel
def exporter_excel():
    try:
        df = pd.read_csv(CSV_FUSIONNE)
        chemin = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Fichiers Excel", "*.xlsx")])
        if chemin:
            df.to_excel(chemin, index=False)
            messagebox.showinfo("Exportation", "Données exportées avec succès vers Excel.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d’exporter : {e}")

# ✅ 3. Affichage des graphes matplotlib
def afficher_graphes():
    try:
        df = pd.read_csv(CSV_FUSIONNE)
        if df.empty:
            messagebox.showwarning("Aucune donnée", "Le fichier est vide.")
            return

        for metrique in ["latence", "perte", "congestion", "bande_passante", "sauts", "goulot"]:
            plt.figure()
            for lien in df["lien"].unique():
                valeurs = df[df["lien"] == lien][metrique]
                timestamps = df[df["lien"] == lien]["timestamp"]
                plt.plot(timestamps, valeurs, label=f"Lien {lien}")
            plt.title(f"Évolution de la métrique : {metrique}")
            plt.xlabel("Timestamp")
            plt.ylabel(metrique.capitalize())
            plt.legend()
            plt.grid(True)
        plt.show()

    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d’afficher les graphes : {e}")

# ✅ 4. Affichage des données dans un tableau
def afficher_donnees(tree):
    try:
        df = pd.read_csv(CSV_FUSIONNE)
        tree.delete(*tree.get_children())  # Nettoyage
        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de lire le fichier CSV : {e}")

# ✅ 5. Lancement de l’interface
def lancer_interface():
    initialiser_fichier_csv()

    root = Tk()
    root.title("Visualisation des métriques réseau")

    label = Label(root, text="Métriques collectées :")
    label.pack(pady=5)

    columns = ["timestamp", "lien", "latence", "perte", "congestion", "bande_passante", "sauts", "goulot"]
    tree = Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(padx=10, pady=5)

    afficher_donnees(tree)

    # Boutons
    refresh_button = Button(root, text="🔄 Rafraîchir", command=lambda: afficher_donnees(tree))
    refresh_button.pack(pady=5)

    graph_button = Button(root, text="📊 Afficher les graphes", command=afficher_graphes)
    graph_button.pack(pady=5)

    export_button = Button(root, text="📤 Exporter vers Excel", command=exporter_excel)
    export_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    lancer_interface()

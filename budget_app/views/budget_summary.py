import tkinter as tk
from tkinter import ttk
import sqlite3
from utils.db import create_connection

class BudgetSummary(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Résumé du Budget par Catégorie", font=("Helvetica", 16, "bold"))
        self.label.pack(pady=20)

        # Création du Treeview
        self.tree = ttk.Treeview(self, columns=("category", "total_budget", "total_spent", "remaining"), show="headings")
        self.tree.pack(fill="both", expand=True)

        # Définition des colonnes
        self.tree.heading("category", text="Catégorie")
        self.tree.heading("total_budget", text="Budget Total")
        self.tree.heading("total_spent", text="Dépensé Total")
        self.tree.heading("remaining", text="Restant")

        # Définir les largeurs de colonnes
        self.tree.column("category", width=150, anchor='center')
        self.tree.column("total_budget", width=100, anchor='center')
        self.tree.column("total_spent", width=100, anchor='center')
        self.tree.column("remaining", width=100, anchor='center')

        self.load_summary()

        # Ajout d'un bouton pour revenir au tableau de bord
        self.back_button = tk.Button(self, text="Retour au Tableau de Bord", 
                                     command=lambda: self.controller.show_frame("Dashboard"))
        self.back_button.pack(pady=5)

    def load_summary(self):
        conn = create_connection("budget.db")
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute('''
                    SELECT category, SUM(amount) as total_spent
                    FROM transactions
                    GROUP BY category
                ''')
                rows = c.fetchall()
                for row in rows:
                    # Supposez que vous avez une méthode pour obtenir le budget total par catégorie
                    total_budget = 1000  # Valeur d'exemple
                    total_spent = row[1]
                    remaining = total_budget - total_spent
                    self.tree.insert("", "end", values=(row[0], total_budget, total_spent, remaining))
            except sqlite3.Error as e:
                print(e)
            finally:
                conn.close()
        else:
            print("Error! Cannot create the database connection.")

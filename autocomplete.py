import tkinter as tk
import json
from analyse_input import analyze_and_highlight

# Charger les mots-clés depuis commandes.json
def load_keywords():
    with open("commandes.json", "r") as file:
        data = json.load(file)
    keywords = list(data["commands"].keys()) + list(data["conditionals"].keys()) + list(data["loops"].keys())
    return keywords

# Fonction d'autocomplétion
class Autocomplete:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.suggestion_box = None
        self.keywords = load_keywords()
        self.suppress_analysis = False  # Flag pour éviter une analyse immédiate
        self.current_suggestion = None  # Pour suivre la suggestion insérée

        # Bind pour l'autocomplétion
        self.text_widget.bind("<KeyRelease>", self.on_key_release)

    def on_key_release(self, event):
        if self.suppress_analysis:
            return  # Empêche l'analyse temporairement lors de l'insertion d'une suggestion

        self.close_suggestions()
        self.current_suggestion = None

        # Récupérer le mot en cours
        current_line = self.text_widget.get("insert linestart", "insert")
        last_word = current_line.split()[-1] if current_line.split() else ""

        # Trouver les suggestions possibles
        suggestions = [kw for kw in self.keywords if kw.startswith(last_word)]

        if suggestions and last_word:
            self.show_suggestions(suggestions)

        # Relancer l'analyse après saisie normale
        analyze_and_highlight(self.text_widget)

    def show_suggestions(self, suggestions):
        # Positionner la boîte de suggestions
        x, y, _, _ = self.text_widget.bbox("insert")
        x_offset, y_offset = x + 20, y + 25

        self.suggestion_box = tk.Toplevel()
        self.suggestion_box.wm_overrideredirect(True)
        self.suggestion_box.geometry(f"+{self.text_widget.winfo_rootx() + x_offset}+{self.text_widget.winfo_rooty() + y_offset}")

        listbox = tk.Listbox(self.suggestion_box, bg="white", fg="black", selectbackground="gray", highlightthickness=0)
        for suggestion in suggestions:
            listbox.insert(tk.END, suggestion)
        listbox.pack()

        listbox.bind("<<ListboxSelect>>", lambda e: self.insert_suggestion(listbox))

    def insert_suggestion(self, listbox):
        # Insérer proprement la suggestion sans déclencher l'analyse immédiate
        self.suppress_analysis = True
        selected = listbox.get(listbox.curselection())
        self.current_suggestion = selected

        # Effacer proprement le mot en cours d'écriture
        self.text_widget.delete("insert-1c wordstart", "insert")
        self.text_widget.insert("insert", selected + " ")

        self.close_suggestions()
        self.suppress_analysis = False  # Réactiver l'analyse

        # Relancer l'analyse après modification
        analyze_and_highlight(self.text_widget)

    def close_suggestions(self):
        if self.suggestion_box:
            self.suggestion_box.destroy()
            self.suggestion_box = None
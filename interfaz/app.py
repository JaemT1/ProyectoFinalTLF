import tkinter as tk
from tkinter import messagebox, ttk
import re
from automatas.dfa import DFA
from automatas.graficador import graficar_automata
from utils.validador_regex import validar_regex

class RegexApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Validador de Expresiones Regulares y DFAs/NFAs de Cadenas")
        self.root.geometry("600x400")

        self.label_regex = ttk.Label(root, text="Expresión Regular:")
        self.label_regex.pack(pady=5)

        self.entry_regex = ttk.Entry(root, width=50)
        self.entry_regex.pack(pady=5)

        self.label_cadenas = ttk.Label(root, text="Cadenas a Validar (una por línea):")
        self.label_cadenas.pack(pady=5)

        self.text_cadenas = tk.Text(root, height=8, width=50)
        self.text_cadenas.pack(pady=5)

        self.button_validar = ttk.Button(root, text="Validar y Generar NFA Optimizado", command=self.validar_cadenas)
        self.button_validar.pack(pady=10)

        self.label_resultados = ttk.Label(root, text="Resultados:")
        self.label_resultados.pack(pady=5)

        self.text_resultados = tk.Text(root, height=10, width=50)
        self.text_resultados.pack(pady=5)

    def validar_cadenas(self):
        regex = self.entry_regex.get()
        cadenas = self.text_cadenas.get("1.0", tk.END).strip().split("\n")
        self.text_resultados.delete("1.0", tk.END)

        if not validar_regex(regex):
            messagebox.showerror("Error", "Expresión regular inválida.")
            return

        cadenas_validas = [cadena for cadena in cadenas if re.fullmatch(regex, cadena)]
        for cadena in cadenas:
            resultado = f"{cadena} -> {'Aceptada' if cadena in cadenas_validas else 'Rechazada'}\n"
            self.text_resultados.insert(tk.END, resultado)

        if cadenas_validas:
            automata = DFA()
            automata.construir_desde_cadenas_validas(cadenas_validas)
            graficar_automata(automata, titulo="NFA_Optimizado", carpeta="imagenes")
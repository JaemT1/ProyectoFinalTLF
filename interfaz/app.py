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
        self.root.geometry("600x500")
        self.root.resizable(False, False)  # Deshabilita el redimensionamiento

        # Crear un fondo con gradiente
        self.canvas = tk.Canvas(root, width=600, height=500)
        self.canvas.pack(fill="both", expand=True)
        self.draw_gradient(self.canvas, "#1C1C1C", "#4B0082")  # Morado oscuro a negro

        # Configurar estilo de los Labels (fuente Helvetica, blanco)
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Candara", 12), background="#1e0730", foreground="white")

        # Widgets (centrados y con estilo solicitado)
        self.label_regex = ttk.Label(root, text="Expresión Regular:")
        self.label_regex.place(x=80, y=20)

        self.entry_regex = ttk.Entry(root, width=50, font=("Candara", 12), background="#333333", foreground="black")
        self.entry_regex.place(x=80, y=50)

        self.label_cadenas = ttk.Label(root, text="Cadenas a Validar (una por línea):")
        self.label_cadenas.place(x=80, y=90)

        self.text_cadenas = tk.Text(root, height=8, width=50, font=("Candara", 12), background="white",
                                    foreground="black", relief="flat", insertbackground="white")
        self.text_cadenas.place(x=80, y=120)

        self.button_validar = tk.Button(root, text="Validar y Generar NFA Optimizado", font=("Candara", 12),
                                        bg="#333333", fg="white", relief="flat", command=self.validar_cadenas)
        self.button_validar.place(x=180, y=280)

        self.label_resultados = ttk.Label(root, text="Resultados:")
        self.label_resultados.place(x=80, y=330)

        self.text_resultados = tk.Text(root, height=5, width=50, font=("Candara", 12), background="white",
                                       foreground="black", relief="flat", insertbackground="white")
        self.text_resultados.place(x=80, y=360)

        # Aplicar hover al botón
        self.apply_hover_effect(self.button_validar)

    def draw_gradient(self, canvas, color1, color2):
        """Dibuja un gradiente de color en el canvas."""
        steps = 300
        for i in range(steps):
            r1, g1, b1 = self.hex_to_rgb(color1)
            r2, g2, b2 = self.hex_to_rgb(color2)
            r = int(r1 + (r2 - r1) * i / steps)
            g = int(g1 + (g2 - g1) * i / steps)
            b = int(b1 + (b2 - b1) * i / steps)
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_rectangle(0, i * 4, 800, (i + 1) * 4, outline="", fill=color)

    @staticmethod
    def hex_to_rgb(hex_color):
        """Convierte un color hexadecimal a un tuple RGB."""
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


    def apply_hover_effect(self, button):
        """Aplica efecto de hover para un botón."""

        def on_enter(event):
            button.configure(bg="#444444", fg="white")  # Fondo gris oscuro, texto blanco

        def on_leave(event):
            button.configure(bg="#333333", fg="white")  # Fondo negro, texto blanco

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)


        """
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
        """


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
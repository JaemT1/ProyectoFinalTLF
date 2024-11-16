import os
import tkinter as tk
from tkinter import messagebox, ttk
import re
from graphviz import Digraph

class DFA:
    def __init__(self, cadena):
        self.states = []  # Lista de estados en el DFA
        self.transitions = {}  # Diccionario de transiciones {(estado, simbolo): estado_destino}
        self.initial_state = 0  # El estado inicial siempre será 0
        self.accept_state = len(cadena)  # El estado final es igual a la longitud de la cadena

        # Construir el DFA basado en la cadena
        self.build_dfa(cadena)

    def build_dfa(self, cadena):
        """Construye el DFA que acepta exactamente la cadena dada."""
        current_state = 0
        for i, char in enumerate(cadena):
            next_state = current_state + 1
            self.transitions[(current_state, char)] = next_state
            self.states.append(current_state)
            current_state = next_state
        self.states.append(current_state)  # Agregar el estado final

    def get_transitions(self):
        """Retorna las transiciones para el grafo."""
        return [(from_state, char, to_state) for (from_state, char), to_state in self.transitions.items()]


# Función para graficar el DFA de una cadena y abrirla con el visualizador de imágenes de Windows
def graficar_dfa(dfa, cadena):
    dot = Digraph(format="png")

    # Crear los nodos en Graphviz
    for state in dfa.states:
        if state == dfa.accept_state:
            dot.node(str(state), shape="doublecircle", style="filled", color="lightgreen")
        else:
            dot.node(str(state), shape="circle", style="filled", color="lightblue")

    # Añadir transiciones
    for (from_state, char, to_state) in dfa.get_transitions():
        dot.edge(str(from_state), str(to_state), label=char)

    # Guardar la imagen
    dfa_path = "dfa_image"
    dot.render(dfa_path, format="png", cleanup=True)

    # Abrir la imagen con el visualizador de imágenes predeterminado de Windows
    try:
        os.startfile(dfa_path + ".png")  # Solo funciona en Windows
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir la imagen del DFA: {e}")

    return dfa_path  # Retornamos la ruta en caso de que sea necesario usarla más adelante


# Configuración de la interfaz gráfica
class RegexApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Validador de Expresiones Regulares y DFAs de Cadenas")
        self.root.geometry("600x400")

        self.label_regex = ttk.Label(root, text="Expresión Regular:")
        self.label_regex.pack(pady=5)

        self.entry_regex = ttk.Entry(root, width=50)
        self.entry_regex.pack(pady=5)

        self.label_cadenas = ttk.Label(root, text="Cadenas a Validar (una por línea):")
        self.label_cadenas.pack(pady=5)

        self.text_cadenas = tk.Text(root, height=8, width=50)
        self.text_cadenas.pack(pady=5)

        self.button_validar = ttk.Button(root, text="Validar y Generar DFAs", command=self.validar_cadenas)
        self.button_validar.pack(pady=10)

        self.label_resultados = ttk.Label(root, text="Resultados:")
        self.label_resultados.pack(pady=5)

        self.text_resultados = tk.Text(root, height=10, width=50)
        self.text_resultados.pack(pady=5)

    def validar_cadenas(self):
        # Obtener la expresión regular ingresada
        regex = self.entry_regex.get()
        cadenas = self.text_cadenas.get("1.0", tk.END).strip().split("\n")
        self.text_resultados.delete("1.0", tk.END)

        # Intentar compilar la expresión regular para verificar que sea válida
        try:
            patron = re.compile(regex)
        except re.error as e:
            messagebox.showerror("Error", f"Expresión regular inválida: {e}")
            return

        # Validar cada cadena y generar el DFA si es aceptada
        for cadena in cadenas:
            if patron.fullmatch(cadena):
                resultado = f"{cadena} -> Aceptada\n"
                self.text_resultados.insert(tk.END, resultado)

                # Crear y graficar el DFA específico para esta cadena
                dfa = DFA(cadena)
                graficar_dfa(dfa, cadena)
            else:
                resultado = f"{cadena} -> Rechazada\n"
                self.text_resultados.insert(tk.END, resultado)


# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = RegexApp(root)
    root.mainloop()

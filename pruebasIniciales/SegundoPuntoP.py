import os
import tkinter as tk
from tkinter import messagebox, ttk
import re
from graphviz import Digraph


class DFA:
    def __init__(self):
        self.states = []
        self.transitions = {}
        self.initial_state = "q0"
        self.accept_states = []
        self.alphabet = []

    def construir_desde_cadenas_validas(self, cadenas_validas):
        """
        Construye un NFA optimizado que acepte varias cadenas válidas.
        Si varias cadenas comparten un prefijo, utiliza un único conjunto de nodos para ese prefijo.
        """
        if not cadenas_validas:
            raise ValueError("No se proporcionaron cadenas válidas para construir el NFA.")

        self.states = ["q0"]
        self.initial_state = "q0"
        self.accept_states = []
        self.transitions = {}
        estado_count = 1

        for cadena in cadenas_validas:
            estado_actual = "q0"

            for simbolo in cadena:
                # Verificar si ya existe una transición para el símbolo actual
                if (estado_actual, simbolo) not in self.transitions:
                    # Si no existe, crear un nuevo estado
                    estado_siguiente = f"q{estado_count}"
                    self.states.append(estado_siguiente)
                    self.transitions[(estado_actual, simbolo)] = {estado_siguiente}
                    estado_count += 1
                else:
                    # Si ya existe una transición, seguimos al estado existente
                    estado_siguiente = list(self.transitions[(estado_actual, simbolo)])[0]

                # Avanzar al siguiente estado
                estado_actual = estado_siguiente

            # Marcar el último estado como de aceptación
            if estado_actual not in self.accept_states:
                self.accept_states.append(estado_actual)

        # Asegurarse de que el alfabeto contenga todos los símbolos de las cadenas
        for cadena in cadenas_validas:
            for simbolo in cadena:
                if simbolo not in self.alphabet:
                    self.alphabet.append(simbolo)

        return self

    def get_transitions(self):
        """Retorna las transiciones para el grafo."""
        return [(from_state, char, to_state) for (from_state, char), to_state_set in self.transitions.items() for
                to_state in to_state_set]


# Función para graficar el NFA o DFA y abrirlo en el visualizador de imágenes de Windows
def graficar_automata(automata, titulo="automata"):
    dot = Digraph(format="png")

    # Crear los nodos en Graphviz
    for state in automata.states:
        if state in automata.accept_states:
            dot.node(state, shape="doublecircle", style="filled", color="lightgreen")
        else:
            dot.node(state, shape="circle", style="filled", color="lightblue")

    # Añadir transiciones
    for (from_state, char, to_state) in automata.get_transitions():
        dot.edge(from_state, to_state, label=char)

    # Guardar la imagen
    automata_path = f"{titulo}_image"
    dot.render(automata_path, format="png", cleanup=True)

    # Abrir la imagen con el visualizador de imágenes predeterminado de Windows
    try:
        os.startfile(automata_path + ".png")  # Solo funciona en Windows
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir la imagen del autómata: {e}")

    return automata_path  # Retornamos la ruta en caso de que sea necesario usarla más adelante


# Configuración de la interfaz gráfica
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

        # Validar cada cadena y agregar las cadenas válidas
        cadenas_validas = []
        for cadena in cadenas:
            if patron.fullmatch(cadena):
                resultado = f"{cadena} -> Aceptada\n"
                cadenas_validas.append(cadena)
            else:
                resultado = f"{cadena} -> Rechazada\n"
            self.text_resultados.insert(tk.END, resultado)

        # Construir y graficar el NFA optimizado para las cadenas válidas
        if cadenas_validas:
            automata = DFA()
            automata.construir_desde_cadenas_validas(cadenas_validas)
            graficar_automata(automata, titulo="NFA_Optimizado")


# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = RegexApp(root)
    root.mainloop()

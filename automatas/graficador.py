from graphviz import Digraph
from tkinter import messagebox
import os

def graficar_automata(automata, titulo="automata", carpeta="imagenes"):
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

    # Crear carpeta si no existe
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    # Guardar la imagen en la carpeta especificada
    automata_path = os.path.join(carpeta, f"{titulo}_image")
    dot.render(automata_path, format="png", cleanup=True)

    # Abrir la imagen con el visualizador de imágenes predeterminado de Windows
    try:
        os.startfile(automata_path + ".png")  # Solo funciona en Windows
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir la imagen del autómata: {e}")

    return automata_path
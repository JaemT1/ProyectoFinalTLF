import tkinter as tk
from tkinter import messagebox, ttk
import re
import matplotlib.pyplot as plt
import networkx as nx

# Función para convertir la expresión regular a un autómata
def regex_to_automata(expresion_regular):
    automata = {
        "expresion": expresion_regular,
        "estados": ["q0", "q1", "q2"],  # Ejemplo de estados
        "transiciones": [],
        "estado_inicial": "q0",
        "estado_final": "q2"
    }
    
    # Obtener transiciones a partir de la expresión regular
    if expresion_regular == r"[a-zA-Z]+$":
        automata["transiciones"].append(("q0", "[a-zA-Z]", "q1"))  # Transición de q0 a q1 por letras
        automata["transiciones"].append(("q1", "[a-zA-Z]", "q1"))  # q1 puede aceptar múltiples letras
        automata["transiciones"].append(("q1", "$", "q2"))         # q1 a q2 por el final de la cadena
        automata["transiciones"].append(("q0", "$", "q2"))         # Transición directa a q2 por el símbolo de dólar
    else:
        automata["transiciones"].append(("q0", expresion_regular, "q1"))
        automata["transiciones"].append(("q1", "$", "q2"))

    return automata

# Función para validar una cadena usando un autómata simulado
def validar_con_automata(cadena, automata):
    patron = re.compile(automata["expresion"])
    return bool(patron.fullmatch(cadena))

# Función para mostrar el autómata en el área de resultados
def mostrar_automata(automata):
    representacion = f"Autómata para la expresión regular:\n"
    representacion += f"Expresión: {automata['expresion']}\n"
    representacion += f"Estado inicial: {automata['estado_inicial']}\n"
    representacion += f"Estado final: {automata['estado_final']}\n"
    representacion += "Estados:\n"
    for estado in automata["estados"]:
        representacion += f"  {estado}\n"
    representacion += "Transiciones:\n"
    for origen, simbolo, destino in automata["transiciones"]:
        representacion += f"  {origen} --[{simbolo}]--> {destino}\n"
    
    return representacion

# Función para crear y mostrar el gráfico del autómata
def mostrar_grafico_automata(automata):
    G = nx.DiGraph()  # Creamos un grafo dirigido
    
    # Añadimos los estados
    for estado in automata["estados"]:
        G.add_node(estado)
    
    # Añadimos las transiciones como aristas
    for origen, simbolo, destino in automata["transiciones"]:
        G.add_edge(origen, destino, label=simbolo)
    
    # Dibujar el autómata
    pos = nx.spring_layout(G)  # Posicionamiento automático
    edge_labels = nx.get_edge_attributes(G, 'label')
    
    plt.figure(figsize=(6, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=12, font_weight='bold', arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    
    plt.title("Autómata generado")
    plt.show()

# Función para manejar la validación de cadenas
def validar_cadenas():
    # Obtener la expresión regular ingresada por el usuario
    expresion_regular = entry_regex.get()

    # Modificar la expresión regular para aceptar espacios (si no lo hace ya)
    if r"\s" not in expresion_regular:
        expresion_regular = expresion_regular.replace("[", "[\\s")

    # Obtener las cadenas ingresadas, separarlas por saltos de línea
    cadenas = text_cadenas.get("1.0", tk.END).strip().split("\n")

    # Limpiar el área de resultados
    text_resultados.delete("1.0", tk.END)

    # Intentar compilar la expresión regular
    try:
        # Analizar la expresión regular y convertirla en un autómata
        automata = regex_to_automata(expresion_regular)
        # Mostrar el autómata en el área de resultados
        automata_representation = mostrar_automata(automata)
        text_resultados.insert(tk.END, automata_representation + "\n")
    except re.error as e:
        messagebox.showerror("Error", f"Expresión regular inválida: {e}")
        return

    # Validar cada cadena y mostrar el resultado
    for cadena in cadenas:
        if validar_con_automata(cadena, automata):
            resultado = f"'{cadena}' -> Aceptada por el autómata\n"
        else:
            resultado = f"'{cadena}' -> Rechazada por el autómata\n"
        text_resultados.insert(tk.END, resultado)

# Función para mostrar el gráfico del autómata en un modal
def mostrar_modal_automata():
    # Obtener la expresión regular ingresada por el usuario
    expresion_regular = entry_regex.get()
    
    # Analizar la expresión regular y convertirla en un autómata
    automata = regex_to_automata(expresion_regular)
    
    # Mostrar el gráfico del autómata
    mostrar_grafico_automata(automata)

# Crear la ventana principal
root = tk.Tk()
root.title("Proyecto Final TLF")  # Título de la ventana
root.geometry("600x600")  # Aumentar altura para espacio adicional
root.configure(bg="#2c3e50")
root.resizable(False, False)

# Estilo personalizado
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 12), background="#2c3e50", foreground="white")
style.configure("TEntry", font=("Helvetica", 12))
style.configure("TFrame", background="#34495e")

# Frame principal
frame_principal = ttk.Frame(root, padding=20, style="TFrame")
frame_principal.pack(fill="both", expand=True)

# Añadir un título en la parte superior
label_titulo = ttk.Label(frame_principal, text="Validador de Expresiones Regulares", style="TLabel", font=("Helvetica", 16, "bold"))
label_titulo.pack(pady=10)

# Frame para la entrada de expresión regular
frame_regex = ttk.Frame(frame_principal, style="TFrame")
frame_regex.pack(pady=10, fill="x")

label_regex = ttk.Label(frame_regex, text="Expresión Regular:", style="TLabel")
label_regex.pack(side="left", padx=10)

entry_regex = ttk.Entry(frame_regex, width=55)  # Ajustado para que coincida con el resto
entry_regex.pack(side="left", padx=10)

# Frame para las cadenas de texto
frame_cadenas = ttk.Frame(frame_principal, style="TFrame")
frame_cadenas.pack(pady=10, fill="x")

label_cadenas = ttk.Label(frame_cadenas, text="Cadenas a Validar (una por línea):", style="TLabel")
label_cadenas.pack(anchor="nw", padx=10)  # Alineado arriba a la izquierda

text_cadenas = tk.Text(frame_cadenas, height=8, width=55, font=("Helvetica", 12))  # Misma anchura que el Entry
text_cadenas.pack(pady=5, padx=10)  # Añadido padding para alineación

# Botón para validar las cadenas
button_validar = ttk.Button(frame_principal, text="Validar Cadenas", command=validar_cadenas)
button_validar.pack(pady=15)

# Botón para mostrar el gráfico del autómata
button_grafico = ttk.Button(frame_principal, text="Mostrar Autómata Gráfico", command=mostrar_modal_automata)
button_grafico.pack(pady=5)

# Frame para los resultados
frame_resultados = ttk.Frame(frame_principal, style="TFrame")
frame_resultados.pack(pady=10, fill="x")

label_resultados = ttk.Label(frame_resultados, text="Resultados:", style="TLabel")
label_resultados.pack(anchor="nw", padx=10)

text_resultados = tk.Text(frame_resultados, height=10, width=55, font=("Helvetica", 12), state='normal')
text_resultados.pack(pady=5, padx=10)

# Ejecutar el bucle principal de la ventana
root.mainloop()

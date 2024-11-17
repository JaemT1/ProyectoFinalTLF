import tkinter as tk
from tkinter import messagebox, ttk
import re

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
        patron = re.compile(expresion_regular)
    except re.error as e:
        messagebox.showerror("Error", f"Expresión regular inválida: {e}")
        return

    # Validar cada cadena y mostrar el resultado
    for cadena in cadenas:
        if patron.fullmatch(cadena):
            resultado = f"'{cadena}' -> Aceptada\n"
        else:
            resultado = f"'{cadena}' -> Rechazada\n"
        text_resultados.insert(tk.END, resultado)


# Crear la ventana principal
root = tk.Tk()
root.title("Proyecto Final TLF - Validador de Expresiones Regulares")  # Título de la ventana
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

# Agrupamos el label y el campo de texto en el mismo frame para alinearlos correctamente
label_cadenas = ttk.Label(frame_cadenas, text="Cadenas a Validar (una por línea):", style="TLabel")
label_cadenas.pack(anchor="nw", padx=10)  # Alineado arriba a la izquierda

text_cadenas = tk.Text(frame_cadenas, height=8, width=55, font=("Helvetica", 12))  # Misma anchura que el Entry
text_cadenas.pack(pady=5, padx=10)  # Añadido padding para alineación

# Botón para validar las cadenas
button_validar = ttk.Button(frame_principal, text="Validar Cadenas", command=validar_cadenas)
button_validar.pack(pady=15)

# Frame para los resultados
frame_resultados = ttk.Frame(frame_principal, style="TFrame")
frame_resultados.pack(pady=10, fill="x")

# Agrupamos el label y el campo de texto en el mismo frame para alinearlos correctamente
label_resultados = ttk.Label(frame_resultados, text="Resultados:", style="TLabel")
label_resultados.pack(anchor="nw", padx=10)  # Alineado arriba a la izquierda

text_resultados = tk.Text(frame_resultados, height=10, width=55, font=("Helvetica", 12), state='normal')  # Misma anchura que el resto
text_resultados.pack(pady=5, padx=10)  # Añadido padding para alineación

# Ejecutar el bucle principal de la ventana
root.mainloop()

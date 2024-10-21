import tkinter as tk
from tkinter import messagebox
import re


# Función para validar las cadenas usando la expresión regular
def validar_cadenas():
    # Obtener la expresión regular ingresada por el usuario
    expresion_regular = entry_regex.get()

    # Modificar la expresión regular para aceptar espacios (si no lo hace ya)
    if r"\s" not in expresion_regular:
        # Agregar soporte de espacios dentro de las clases de caracteres
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
root.title("Validador de Expresiones Regulares con Espacios")

# Etiqueta y campo de entrada para la expresión regular
label_regex = tk.Label(root, text="Expresión Regular:")
label_regex.pack(pady=5)
entry_regex = tk.Entry(root, width=50)
entry_regex.pack(pady=5)

# Etiqueta y área de texto para las cadenas
label_cadenas = tk.Label(root, text="Cadenas a Validar (una por línea):")
label_cadenas.pack(pady=5)
text_cadenas = tk.Text(root, height=10, width=50)
text_cadenas.pack(pady=5)

# Botón para iniciar la validación
button_validar = tk.Button(root, text="Validar Cadenas", command=validar_cadenas)
button_validar.pack(pady=10)

# Área de texto para mostrar los resultados
label_resultados = tk.Label(root, text="Resultados:")
label_resultados.pack(pady=5)
text_resultados = tk.Text(root, height=10, width=50, state='normal')
text_resultados.pack(pady=5)

# Ejecutar el bucle principal de la ventana
root.mainloop()

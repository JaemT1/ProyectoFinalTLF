import tkinter as tk
from interfaz.app import RegexApp

if __name__ == "__main__":
    root = tk.Tk()
    app = RegexApp(root)
    root.mainloop()
import importlib
import tkinter as tk
from tkinter import messagebox

COLOR_FONDO = "#f4f6fb"
COLOR_TITULO = "#1f3a5f"
MODULOS = [
    ("Nivel 3 · Lenguajes regulares", "Autómata finito determinista", "nivel3_afd"),
    ("Nivel 2 · Lenguajes libres de contexto", "Autómata de pila", "nivel2_pila"),
    (
        "Nivel 1 · Lenguajes dependientes del contexto",
        "Autómata linealmente acotado",
        "nivel1_lba",
    ),
    (
        "Nivel 0 · Lenguajes recursivamente enumerables",
        "Máquina de Turing",
        "nivel0_turing",
    ),
]


def abrir_modulo(root, nombre_modulo):
    modulo = importlib.import_module(nombre_modulo)
    if not hasattr(modulo, "abrir"):
        messagebox.showinfo(
            "En construcción",
            "Este módulo aún no está implementado.",
            parent=root,
        )
        return

    modulo.abrir(root)


def main():
    root = tk.Tk()
    root.title("Simulador de la Jerarquía de Chomsky")
    root.geometry("640x480")
    root.configure(bg=COLOR_FONDO)
    root.resizable(False, False)
    encabezado = tk.Frame(root, bg=COLOR_TITULO)
    encabezado.pack(fill="x")  # ocupa todo el ancho
    tk.Label(
        encabezado,
        text="Simulador de la Jerarquía de Chomsky",
        font=("Segoe UI", 18, "bold"),
        bg=COLOR_TITULO,
        fg="white",
    ).pack(pady=(18, 2))
    tk.Label(
        encabezado,
        text="Autómatas, Gramáticas y Lenguajes · Elige un nivel para simular",
        font=("Segoe UI", 10),
        bg=COLOR_TITULO,
        fg="#c9d6ea",
    ).pack(pady=(0, 16))
    cuerpo = tk.Frame(root, bg=COLOR_FONDO)
    cuerpo.pack(fill="both", expand=True, padx=30, pady=20)
    for titulo, modelo, modulo in MODULOS:
        tk.Button(
            cuerpo,
            text=f"{titulo}\n{modelo}",  # el texto del botón (dos líneas)
            font=("Segoe UI", 11),
            bg="white",
            fg=COLOR_TITULO,
            activebackground="#dce6f7",
            relief="groove",
            bd=2,
            cursor="hand2",
            command=lambda m=modulo: abrir_modulo(root, m),
        ).pack(fill="x", pady=7, ipady=8)

    root.mainloop()


if __name__ == "__main__":
    main()

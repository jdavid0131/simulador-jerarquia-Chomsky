"""Panel principal del Simulador de la Jerarquía de Chomsky.

Cada nivel vive en su propio archivo y expone una función `abrir(root)`
que crea su ventana. Si un módulo todavía no la tiene, se avisa al usuario.
"""
# importlib permite cargar un archivo .py usando su nombre escrito como texto.
import importlib
# tkinter: la librería de ventanas. "as tk" le pone el apodo "tk".
import tkinter as tk
# messagebox: para mostrar ventanitas de aviso.
from tkinter import messagebox

# Colores del panel, en formato hexadecimal (#rrggbb).
COLOR_FONDO = "#f4f6fb"
COLOR_TITULO = "#1f3a5f"

# Lista de módulos. Cada elemento tiene 3 datos:
# (título del nivel, modelo computacional, nombre del archivo SIN el .py)
MODULOS = [
    ("Nivel 3 · Lenguajes regulares", "Autómata finito determinista", "nivel3_afd"),
    ("Nivel 2 · Lenguajes libres de contexto", "Autómata de pila", "nivel2_pila"),
    ("Nivel 1 · Lenguajes dependientes del contexto", "Autómata linealmente acotado", "nivel1_lba"),
    ("Nivel 0 · Lenguajes recursivamente enumerables", "Máquina de Turing", "nivel0_turing"),
]


# Se ejecuta al pulsar un botón. Recibe la ventana principal (root)
# y el nombre del archivo del nivel, por ejemplo "nivel3_afd".
def abrir_modulo(root, nombre_modulo):
    # Carga ese archivo. Es como escribir "import nivel3_afd",
    # pero eligiendo el nombre con una variable.
    modulo = importlib.import_module(nombre_modulo)

    # hasattr pregunta: ¿ese archivo tiene algo llamado "abrir"?
    # Si NO, avisa "En construcción" y termina (return).
    if not hasattr(modulo, "abrir"):
        messagebox.showinfo(
            "En construcción",
            "Este módulo aún no está implementado.",
            parent=root,
        )
        return

    # Si SÍ lo tiene, lo ejecuta pasándole la ventana principal.
    modulo.abrir(root)


# Arma y muestra el panel principal.
def main():
    # Crea la ventana principal y configura su título, tamaño y color.
    root = tk.Tk()
    root.title("Simulador de la Jerarquía de Chomsky")
    root.geometry("640x480")
    root.configure(bg=COLOR_FONDO)
    root.resizable(False, False)   # no se puede cambiar el tamaño

    # Franja azul de arriba (el encabezado), con dos textos.
    encabezado = tk.Frame(root, bg=COLOR_TITULO)
    encabezado.pack(fill="x")      # ocupa todo el ancho
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

    # Zona donde van los botones.
    cuerpo = tk.Frame(root, bg=COLOR_FONDO)
    cuerpo.pack(fill="both", expand=True, padx=30, pady=20)

    # Crea un botón por cada módulo de la lista MODULOS.
    # En cada vuelta: titulo, modelo y modulo toman los 3 datos de un elemento.
    for titulo, modelo, modulo in MODULOS:
        tk.Button(
            cuerpo,
            text=f"{titulo}\n{modelo}",     # el texto del botón (dos líneas)
            font=("Segoe UI", 11),
            bg="white",
            fg=COLOR_TITULO,
            activebackground="#dce6f7",
            relief="groove",
            bd=2,
            cursor="hand2",
            # Lo que pasa al pulsar: abrir_modulo con el archivo de ESTE botón.
            # "m=modulo" guarda el valor de esta vuelta; sin eso, todos los
            # botones abrirían el último módulo de la lista.
            command=lambda m=modulo: abrir_modulo(root, m),
        ).pack(fill="x", pady=7, ipady=8)

    # Deja la ventana abierta, esperando clics, hasta que se cierre.
    root.mainloop()


# Esto es verdadero solo cuando ejecutas ESTE archivo directamente
# (python main.py). Entonces arranca el programa.
if __name__ == "__main__":
    main()
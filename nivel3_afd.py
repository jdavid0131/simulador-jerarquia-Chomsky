import tkinter as tk
from tkinter import ttk, messagebox

# ===== CAPA 1: DATOS =====

AUTOMATAS = {
    "Cadenas binarias que terminan en 01": {
        "descripcion": "L = { w ∈ {0,1}* : w termina en 01 }",
        "alfabeto": ["0", "1"],
        "estados": ["q0", "q1", "q2"],
        "inicial": "q0",
        "finales": {"q2"},
        "transiciones": {
            ("q0", "0"): "q1",
            ("q0", "1"): "q0",
            ("q1", "0"): "q1",
            ("q1", "1"): "q2",
            ("q2", "0"): "q1",
            ("q2", "1"): "q0",
        },
        "ejemplos": ["", "01", "001", "1101", "10", "0110"],
    },
    "cantidad par de unos": {
        "descripcion": "L={w ∈ {0,1}* : w tiene una cantidad par de 1 }",
        "alfabeto": ["0", "1"],
        "estados": ["q0", "q1"],
        "inicial": "q0",
        "finales": {"q0"},
        "transiciones": {
            ("q0", "0"): "q0",
            ("q0", "1"): "q1",
            ("q1", "0"): "q1",
            ("q1", "1"): "q0",
        },
        "ejemplos": ["", "11", "1010", "0110", "1", "0111"],
    },
    # tercer automata
    "Contiene la subcadena ab": {
        "descripcion": "L = { w ∈ {a,b}* : w contiene la subcadena ab }",
        "alfabeto": ["a", "b"],
        "estados": ["s0", "s1", "s2"],
        "inicial": "s0",
        "finales": {"s2"},
        "transiciones": {
            ("s0", "a"): "s1",
            ("s0", "b"): "s0",
            ("s1", "a"): "s1",
            ("s1", "b"): "s2",
            ("s2", "a"): "s2",
            ("s2", "b"): "s2",
        },
        "ejemplos": ["ab", "aab", "bbab", "ba", "bbb", "aaa"],
    },
}


# ===== CAPA 2: LÓGICA =====
def acepta(afd, cadena):
    estado = afd["inicial"]
    for simbolo in cadena:
        estado = afd["transiciones"].get((estado, simbolo))
        if estado is None:
            return False
    return estado in afd["finales"]


# ===== CAPA 3: INTERFAZ =====
ESTADOS_POR_FILA = 6
COLOR_ACTUAL = "#ffe082"
COLOR_ACEPTA = "#a5d6a7"
COLOR_RECHAZA = "#ef9a9a"


class VentanaAFD(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Nivel 3 · Autómata Finito Determinista")
        self.minsize(720, 640)

        self.afd = None
        self.cadena = ""
        self.pos = 0
        self.actual = None
        self.terminado = False
        self.aceptada = False
        self.etiquetas_estados = {}

        self._construir()
        self._cargar_automata()

    def _construir(self):
        marco = ttk.Frame(self, padding=10)
        marco.pack(fill="both", expand=True)
        fila = ttk.Frame(marco)
        fila.pack(fill="x")
        ttk.Label(fila, text="Lenguaje:").pack(side="left")
        self.combo_afd = ttk.Combobox(
            fila, values=list(AUTOMATAS), state="readonly", width=40
        )
        self.combo_afd.current(0)
        self.combo_afd.pack(side="left", padx=8)
        self.combo_afd.bind("<<ComboboxSelected>>", lambda e: self._cargar_automata())
        self.lbl_desc = ttk.Label(marco, font=("Segoe UI", 11, "bold"))
        self.lbl_desc.pack(anchor="w", pady=(8, 6))
        ttk.Label(marco, text="Estados del autómata").pack(anchor="w")
        self.marco_estados = tk.Frame(marco)
        self.marco_estados.pack(fill="x", pady=(2, 10))

        fila2 = ttk.Frame(marco)
        fila2.pack(fill="x")
        ttk.Label(fila2, text="Cadena:").pack(side="left")
        self.entrada = ttk.Entry(fila2, width=22, font=("Consolas", 12))
        self.entrada.pack(side="left", padx=8)
        ttk.Button(fila2, text="Cargar", command=self._cargar_cadena).pack(side="left")
        ttk.Label(fila2, text="   Ejemplos:").pack(side="left")
        self.combo_ej = ttk.Combobox(fila2, state="readonly", width=18)
        self.combo_ej.pack(side="left", padx=6)
        self.combo_ej.bind("<<ComboboxSelected>>", lambda e: self._elegir_ejemplo())

        self.lbl_cadena = tk.Label(marco, font=("Consolas", 20, "bold"))
        self.lbl_cadena.pack(pady=(14, 4))
        self.lbl_actual = tk.Label(marco, font=("Segoe UI", 16, "bold"), fg="#1f3a5f")
        self.lbl_actual.pack()
        self.lbl_paso = tk.Label(marco, font=("Segoe UI", 11))
        self.lbl_paso.pack(pady=4)

        fila3 = ttk.Frame(marco)
        fila3.pack(pady=10)
        ttk.Button(fila3, text="Siguiente paso", command=self.paso).pack(
            side="left", padx=5
        )
        ttk.Button(fila3, text="Reiniciar", command=self._cargar_cadena).pack(
            side="left", padx=5
        )

        self.lbl_resultado = tk.Label(marco, font=("Segoe UI", 12, "bold"))
        self.lbl_resultado.pack()
        ttk.Label(marco, text="Tabla de transiciones δ   (→ inicial · * final)").pack(
            anchor="w", pady=(10, 2)
        )
        self.tabla = ttk.Treeview(marco, show="headings", height=5)
        self.tabla.tag_configure("actual", background=COLOR_ACTUAL)
        self.tabla.tag_configure("acepta", background=COLOR_ACEPTA)
        self.tabla.tag_configure("rechaza", background=COLOR_RECHAZA)
        self.tabla.pack(fill="x")

    # ---------------------------------------------------------- Cargar lenguaje
    def _cargar_automata(self):
        self.afd = AUTOMATAS[self.combo_afd.get()]
        self.lbl_desc.config(text=self.afd["descripcion"])
        self._crear_etiquetas_estados()
        self._crear_tabla()
        self.combo_ej["values"] = [
            f"{c or 'ε'}  →  {'acepta' if acepta(self.afd, c) else 'rechaza'}"
            for c in self.afd["ejemplos"]
        ]
        self.combo_ej.set("")
        self.entrada.delete(0, tk.END)
        self.cadena = ""
        self._reiniciar()

    def _crear_etiquetas_estados(self):
        for w in self.marco_estados.winfo_children():  # borra las casillas anteriores
            w.destroy()
        self.etiquetas_estados = {}
        for i, nombre in enumerate(self.afd["estados"]):
            notas = []
            if nombre == self.afd["inicial"]:
                notas.append("inicial")
            if nombre in self.afd["finales"]:
                notas.append("final")
            etiqueta = tk.Label(
                self.marco_estados,
                text=f"{nombre}\n{' y '.join(notas) or ' '}",
                width=11,
                height=2,
                relief="solid",
                bg="white",
                font=("Segoe UI", 11, "bold"),
                bd=4 if nombre in self.afd["finales"] else 1,  # borde grueso = final
            )
            etiqueta.grid(
                row=i // ESTADOS_POR_FILA, column=i % ESTADOS_POR_FILA, padx=3, pady=3
            )
            self.etiquetas_estados[nombre] = etiqueta

    def _crear_tabla(self):
        simbolos = self.afd["alfabeto"]
        # Columnas: "estado" + una por símbolo (se llaman c0, c1... y su título es el símbolo).
        columnas = ["estado"] + [f"c{i}" for i in range(len(simbolos))]
        self.tabla.delete(*self.tabla.get_children())  # borra las filas anteriores
        self.tabla["columns"] = columnas
        self.tabla.heading("estado", text="δ")
        self.tabla.column("estado", width=90, anchor="center")
        for i, simbolo in enumerate(simbolos):
            self.tabla.heading(f"c{i}", text=simbolo)
            self.tabla.column(f"c{i}", width=70, anchor="center")
        for e in self.afd["estados"]:
            marca = ("→" if e == self.afd["inicial"] else "") + (
                "*" if e in self.afd["finales"] else ""
            )
            destinos = [self.afd["transiciones"].get((e, s), "—") for s in simbolos]
            self.tabla.insert("", "end", iid=e, values=[f"{marca}{e}"] + destinos)

    def _elegir_ejemplo(self):
        cadena = self.combo_ej.get().split("  →  ")[0]
        self.entrada.delete(0, tk.END)
        self.entrada.insert(0, "" if cadena == "ε" else cadena)
        self._cargar_cadena()

    def _cargar_cadena(self):
        texto = self.entrada.get().strip()
        for simbolo in texto:
            if simbolo not in self.afd["alfabeto"]:
                messagebox.showwarning(
                    "Cadena inválida",
                    f"Solo se permiten los símbolos: {' '.join(self.afd['alfabeto'])}",
                    parent=self,
                )
                return False
        self.cadena = texto
        self._reiniciar()
        return True

    def _reiniciar(self):
        self.pos = 0
        self.actual = self.afd["inicial"]
        self.terminado = False
        self.aceptada = False
        self.lbl_paso.config(text="")
        self._refrescar()

    # simulacion
    def paso(self):
        if self.pos == 0 and not self.terminado:
            if not self._cargar_cadena():
                return
        if self.terminado:
            return

        if self.pos < len(self.cadena):
            simbolo = self.cadena[self.pos]
            anterior = self.actual
            self.actual = self.afd["transiciones"][(anterior, simbolo)]  # nuevo estado
            self.pos += 1
            self.lbl_paso.config(
                text=f"Leí '{simbolo}':   {anterior}  →  {self.actual}"
            )

        if self.pos == len(self.cadena):
            self.terminado = True
            self.aceptada = self.actual in self.afd["finales"]
        self._refrescar()

    # pantalla
    def _refrescar(self):
        if self.terminado:
            color = COLOR_ACEPTA if self.aceptada else COLOR_RECHAZA
        else:
            color = COLOR_ACTUAL
        for nombre, etiqueta in self.etiquetas_estados.items():
            etiqueta.config(bg=color if nombre == self.actual else "white")
        self.lbl_actual.config(text=f"Estado actual: {self.actual}")
        etiqueta_tabla = (
            ("acepta" if self.aceptada else "rechaza") if self.terminado else "actual"
        )
        for nombre in self.afd["estados"]:
            self.tabla.item(
                nombre, tags=(etiqueta_tabla,) if nombre == self.actual else ()
            )
        if not self.cadena:
            self.lbl_cadena.config(text="ε  (cadena vacía)")
        else:
            texto = ""
            for i, simbolo in enumerate(self.cadena):
                if i == self.pos and not self.terminado:
                    texto += f"[{simbolo}]"
                else:
                    texto += f" {simbolo} "
            self.lbl_cadena.config(text=texto)
        if not self.terminado:
            self.lbl_resultado.config(text="")
        elif self.aceptada:
            self.lbl_resultado.config(
                text=f"Cadena ACEPTADA: terminó en {self.actual}, que es final",
                fg="#1b7f3b",
            )
        else:
            self.lbl_resultado.config(
                text=f"Cadena RECHAZADA: terminó en {self.actual}, que no es final",
                fg="#c62828",
            )


# main.py busca esta función y la llama al pulsar el botón del Nivel 3.
def abrir(root):
    VentanaAFD(root)

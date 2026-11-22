import tkinter as tk
from tkinter import ttk, messagebox

# capa de datos
# transiciones:  (estado, entrada, tope)  ->  (estado nuevo, acción, elemento)
PILAS = {
    "aⁿbⁿ": {
        "descripcion": "L = { aⁿbⁿ : n ≥ 0 }     cada b saca una a",
        "alfabeto": ["a", "b"],
        "inicial": "q0",
        "finales": {"q0", "q2"},
        "transiciones": {
            ("q0", "a", "ε"): ("q1", "in", "a"),
            ("q1", "a", "a"): ("q1", "in", "a"),
            ("q1", "b", "a"): ("q2", "out", "a"),
            ("q2", "b", "a"): ("q2", "out", "a"),
        },
        "ejemplos": ["", "ab", "aabb", "aaabbb", "aab", "abb", "ba"],
    },
    "aⁿb²ⁿ": {
        "descripcion": "L = { aⁿb²ⁿ : n ≥ 0 } ",
        "alfabeto": ["a", "b"],
        "inicial": "q0",
        "finales": {"q0", "q3"},
        "transiciones": {
            ("q0", "a", "ε"): ("q1", "in", "a"),
            ("q1", "a", "a"): ("q1", "in", "a"),
            ("q1", "b", "a"): ("q2", "ε", "ε"),
            ("q2", "b", "a"): ("q3", "out", "a"),
            ("q3", "b", "a"): ("q2", "ε", "ε"),
        },
        "ejemplos": ["", "abb", "aabbbb", "aaabbbbbb", "aabb", "abbb", "ab"],
    },
    "a³ⁿb⁴ⁿ": {
        "descripcion": "L = { a³ⁿb⁴ⁿ : n ≥ 0 }     cada 3 a apilan una a, cada 4 b la sacan",
        "alfabeto": ["a", "b"],
        "inicial": "q0",
        "finales": {"q0", "b4"},
        "transiciones": {
            ("q0", "a", "*"): ("q1", "ε", "ε"),
            ("q1", "a", "*"): ("q2", "ε", "ε"),
            ("q2", "a", "*"): ("q3", "in", "a"),
            ("q3", "a", "*"): ("q1", "ε", "ε"),
            ("q3", "b", "a"): ("b1", "ε", "ε"),
            ("b1", "b", "a"): ("b2", "ε", "ε"),
            ("b2", "b", "a"): ("b3", "ε", "ε"),
            ("b3", "b", "a"): ("b4", "out", "a"),
            ("b4", "b", "a"): ("b1", "ε", "ε"),
        },
        "ejemplos": [
            "",
            "aaabbbb",
            "aaaaaabbbbbbbb",
            "aaabbb",
            "aaaabbbb",
            "aaabbbbb",
            "aaaaaabbbb",
        ],
    },
}


# ===== CAPA 2: LÓGICA =====
def siguiente(pda, estado, simbolo, pila):
    tope = pila[-1] if pila else "ε"
    trans = pda["transiciones"]
    t = trans.get((estado, simbolo, tope)) or trans.get((estado, simbolo, "*"))
    if t and t[1] == "out" and not pila:
        return None
    return t


def acepta(pda, cadena):
    estado, pila = pda["inicial"], []
    for simbolo in cadena:
        t = siguiente(pda, estado, simbolo, pila)
        if t is None:
            return False
        estado, accion, elemento = t
        if accion == "in":
            pila.append(elemento)
        elif accion == "out":
            pila.pop()
    return estado in pda["finales"] and not pila


# capa interfaz
LARGO_MAX = 30


class VentanaPila(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Nivel 2 · Autómata de Pila")
        self.minsize(820, 560)
        self.pda = None
        self.cadena = ""
        self.pos = 0
        self.estado = None
        self.pila = []
        self.terminado = False
        fila = ttk.Frame(self, padding=10)
        fila.pack(fill="x")
        ttk.Label(fila, text="Lenguaje:").pack(side="left")
        self.combo = ttk.Combobox(fila, values=list(PILAS), state="readonly", width=12)
        self.combo.current(0)
        self.combo.pack(side="left", padx=8)
        self.combo.bind("<<ComboboxSelected>>", lambda e: self._cargar_lenguaje())
        self.lbl_desc = ttk.Label(fila, font=("Segoe UI", 11, "bold"))
        self.lbl_desc.pack(side="left", padx=10)

        self.canvas = tk.Canvas(
            self, width=240, height=380, bg="white", highlightthickness=1
        )
        self.canvas.pack(side="right", padx=10, pady=10)

        izq = ttk.Frame(self, padding=10)
        izq.pack(side="left", fill="both", expand=True)

        fila2 = ttk.Frame(izq)
        fila2.pack(fill="x")
        ttk.Label(fila2, text="Cadena:").pack(side="left")
        self.entrada = ttk.Entry(fila2, width=20, font=("Consolas", 12))
        self.entrada.pack(side="left", padx=8)
        ttk.Button(fila2, text="Cargar", command=self._cargar_cadena).pack(side="left")
        ttk.Label(fila2, text="Ejemplos:").pack(side="left", padx=(10, 0))
        self.combo_ej = ttk.Combobox(fila2, state="readonly", width=20)
        self.combo_ej.pack(side="left", padx=8)
        self.combo_ej.bind("<<ComboboxSelected>>", lambda e: self._elegir_ejemplo())

        self.lbl_cadena = tk.Label(izq, font=("Consolas", 20, "bold"))
        self.lbl_cadena.pack(pady=(14, 4))
        self.lbl_estado = tk.Label(izq, font=("Segoe UI", 14, "bold"), fg="#1f3a5f")
        self.lbl_estado.pack()
        self.lbl_paso = tk.Label(izq, font=("Segoe UI", 11))
        self.lbl_paso.pack(pady=4)

        fila3 = ttk.Frame(izq)
        fila3.pack(pady=8)
        ttk.Button(fila3, text="Siguiente paso", command=self.paso).pack(
            side="left", padx=5
        )
        ttk.Button(fila3, text="Reiniciar", command=self._cargar_cadena).pack(
            side="left", padx=5
        )

        self.lbl_resultado = tk.Label(
            izq, font=("Segoe UI", 12, "bold"), wraplength=480, justify="left"
        )
        self.lbl_resultado.pack(anchor="w", pady=6)

        ttk.Label(
            izq,
            text="Transiciones  (estado → entrada | tope, acción, elemento → estado nuevo)",
        ).pack(anchor="w", pady=(10, 2))
        self.lbl_tabla = tk.Label(
            izq, font=("Consolas", 10), justify="left", anchor="w"
        )
        self.lbl_tabla.pack(anchor="w")

        self._cargar_lenguaje()

    # cargar
    def _cargar_lenguaje(self):
        self.pda = PILAS[self.combo.get()]
        self.lbl_desc.config(text=self.pda["descripcion"])
        lineas = [
            f"{e} → {s} | {t}, {a}, {el} → {n}"
            for (e, s, t), (n, a, el) in self.pda["transiciones"].items()
        ]
        self.lbl_tabla.config(text="\n".join(lineas))
        self.combo_ej["values"] = [
            f"{c or 'ε'}  →  {'acepta' if acepta(self.pda, c) else 'rechaza'}"
            for c in self.pda["ejemplos"]
        ]
        self.entrada.delete(0, tk.END)
        self.entrada.insert(0, self.pda["ejemplos"][2])
        self._cargar_cadena()

    def _elegir_ejemplo(self):
        cadena = self.combo_ej.get().split("  →  ")[0]
        self.entrada.delete(0, tk.END)
        self.entrada.insert(0, "" if cadena == "ε" else cadena)
        self._cargar_cadena()

    def _cargar_cadena(self):
        texto = self.entrada.get().strip()
        if any(s not in self.pda["alfabeto"] for s in texto) or len(texto) > LARGO_MAX:
            messagebox.showwarning(
                "Cadena inválida",
                f"Usa solo estos símbolos: {' '.join(self.pda['alfabeto'])}  (máximo {LARGO_MAX})",
                parent=self,
            )
            return False
        self.cadena = texto
        self.pos = 0
        self.estado = self.pda["inicial"]
        self.pila = []
        self.terminado = False
        self.lbl_paso.config(text="")
        self.lbl_resultado.config(text="")
        self._dibujar()
        return True

    def paso(self):
        if self.terminado:
            return
        if self.pos < len(self.cadena):
            simbolo = self.cadena[self.pos]
            t = siguiente(self.pda, self.estado, simbolo, self.pila)
            if t is None:
                self._terminar(
                    False, f"no hay transición desde {self.estado} leyendo '{simbolo}'."
                )
                return
            anterior = self.estado
            self.estado, accion, elemento = t
            if accion == "in":
                self.pila.append(elemento)
            elif accion == "out":
                self.pila.pop()
            self.pos += 1
            texto = {"in": f"apila {elemento}", "out": f"desapila {elemento}"}.get(
                accion, "la pila no cambia"
            )
            self.lbl_paso.config(
                text=f"Leí '{simbolo}':   {anterior} → {self.estado}   ({texto})"
            )
            self._dibujar()
        if self.pos == len(self.cadena):
            ok = self.estado in self.pda["finales"] and not self.pila
            motivo = f"terminó en {self.estado} y la pila " + (
                "quedó vacía."
                if not self.pila
                else f"no está vacía ({len(self.pila)} elemento(s)."
            )
            self._terminar(ok, motivo)

    def _terminar(self, ok, motivo):
        self.terminado = True
        self.lbl_resultado.config(
            text=("Cadena ACEPTADA: " if ok else "Cadena RECHAZADA: ") + motivo,
            fg="#1b7f3b" if ok else "#c62828",
        )

    # dibujo
    def _dibujar(self):
        # La cadena, con el símbolo que sigue entre corchetes.
        if not self.cadena:
            self.lbl_cadena.config(text="ε  (cadena vacía)")
        else:
            self.lbl_cadena.config(
                text="".join(
                    f"[{s}]" if i == self.pos else f" {s} "
                    for i, s in enumerate(self.cadena)
                )
            )
        tope = self.pila[-1] if self.pila else "pila vacía"
        self.lbl_estado.config(text=f"Estado: {self.estado}Tope: {tope}")

        c = self.canvas
        c.delete("all")
        c.create_line(
            50, 40, 50, 350, 190, 350, 190, 40, width=4, fill="#1f3a5f"
        )  # las paredes
        c.create_text(120, 365, text="fondo de la pila", fill="#607d8b")
        alto = min(
            30, 300 // max(len(self.pila), 1)
        )  # si la pila crece, los bloques se achican
        for i, elemento in enumerate(self.pila):
            y = 350 - (i + 1) * alto
            c.create_rectangle(54, y, 186, y + alto, fill="#90caf9", outline="#1f3a5f")
            c.create_text(
                120, y + alto / 2, text=elemento, font=("Consolas", 14, "bold")
            )
        if not self.pila:
            c.create_text(
                120,
                320,
                text="pila vacía",
                fill="#90a4ae",
                font=("Segoe UI", 11, "italic"),
            )


# main.py busca esta función y la llama al pulsar el botón del Nivel 2.
def abrir(root):
    VentanaPila(root)

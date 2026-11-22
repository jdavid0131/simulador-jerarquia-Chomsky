import tkinter as tk
from tkinter import ttk, messagebox

INI, FIN = "$", "$"  # delimitadores de frontera (borde izquierdo y derecho)
LARGO_MAX = 20
ANCHO_CASILLA = 34  # tamaño de cada casilla de la cinta (píxeles)
ANCHO_CINTA = (
    ANCHO_CASILLA * (LARGO_MAX + 2) + 40
)
INICIAL, ACEPTA = "Inicio", "Fin"
TRANS = {
    ("Inicio", "a"): ("Derecha", "A", "R"),  
    ("Derecha", "b"): ("BuscarC", "B", "R"),
    ("Derecha", "C"): (
        "Verificar",
        "C",
        "R",
    ), 
    ("Derecha", FIN): (ACEPTA, FIN, "S"),  
    ("BuscarC", "c"): ("SegundaC", "C", "R"),  
    ("SegundaC", "c"): ("Volver", "C", "L"),  
    ("Volver", INI): ("Derecha", INI, "R"),  
    ("Verificar", "C"): ("Verificar", "C", "R"),  
    ("Verificar", FIN): (ACEPTA, FIN, "S"), 
}
for simbolo in "AB":  
    TRANS[("Derecha", simbolo)] = ("Derecha", simbolo, "R")
for simbolo in "bC":  
    TRANS[("BuscarC", simbolo)] = ("BuscarC", simbolo, "R")
for simbolo in "bcABC":  
    TRANS[("Volver", simbolo)] = ("Volver", simbolo, "L")

EJEMPLOS = [
    "a",
    "abcc",
    "abbcccc",
    "abbbcccccc",
    "",
    "abbccc",
    "abbccccc",
    "abc",
    "acbc",
]


#capa logica
def crear_cinta(cadena):
    return [INI] + list(cadena) + [FIN]

def dar_paso(estado, cinta, pos):
    regla = TRANS.get((estado, cinta[pos]))
    if regla is None:
        return None
    nuevo, escribe, mov = regla
    cinta = list(cinta)
    cinta[pos] = escribe  # reescribe la casilla actual
    pos += {"R": 1, "L": -1, "S": 0}[mov]  # mueve el cabezal
    if not 0 <= pos < len(cinta):
        return None  # no puede salir de la cinta
    return nuevo, cinta, pos

def acepta(cadena):
    estado, cinta, pos = INICIAL, crear_cinta(cadena), 1
    for _ in range(5000):
        if estado == ACEPTA:
            return True
        paso = dar_paso(estado, cinta, pos)
        if paso is None:
            return False
        estado, cinta, pos = paso
    return False


#capa interfaz
class VentanaLBA(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Nivel 1 · Autómata Linealmente Acotado")
        self.minsize(820, 640)
        self.fila_usada = None
        self._construir()
        self.entrada.insert(0, "abbcccc")
        self._cargar()

    def _construir(self):
        marco = ttk.Frame(self, padding=12)
        marco.pack(fill="both", expand=True)
        ttk.Label(
            marco,
            text="L = { a bⁿ c²ⁿ : n ≥ 0 }   (ejemplo del profesor)",
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", pady=(0, 8))
        fila = ttk.Frame(marco)
        fila.pack(fill="x")
        ttk.Label(fila, text="Cadena:").pack(side="left")
        self.entrada = ttk.Entry(fila, width=22, font=("Consolas", 12))
        self.entrada.pack(side="left", padx=6)
        ttk.Button(fila, text="Cargar", command=self._cargar).pack(side="left")
        ttk.Label(fila, text="   Ejemplos:").pack(side="left")
        self.combo = ttk.Combobox(
            fila,
            state="readonly",
            width=24,
            values=[
                f"{c or 'ε'}   →   {'acepta' if acepta(c) else 'rechaza'}"
                for c in EJEMPLOS
            ],
        )
        self.combo.pack(side="left", padx=6)
        self.combo.bind("<<ComboboxSelected>>", lambda e: self._elegir())
        self.cinta_ui = tk.Canvas(
            marco, width=ANCHO_CINTA, height=105, highlightthickness=0
        )
        self.cinta_ui.pack(pady=(10, 4))
        ttk.Label(
            marco,
            text=f"{INI} y {FIN} son los delimitadores: el cabezal (▼) va a izquierda y "
            "derecha.",
            font=("Segoe UI", 9, "italic"),
        ).pack()

        self.lbl_estado = tk.Label(marco, font=("Segoe UI", 14, "bold"), fg="#1f3a5f")
        self.lbl_estado.pack(pady=(10, 2))
        self.lbl_msg = tk.Label(marco, font=("Segoe UI", 10), wraplength=780, height=2)
        self.lbl_msg.pack()
        botones = ttk.Frame(marco)
        botones.pack(pady=6)
        ttk.Button(botones, text="Siguiente paso", command=self.paso).pack(
            side="left", padx=4
        )
        ttk.Button(botones, text="Reiniciar", command=self._cargar).pack(
            side="left", padx=4
        )
        self.lbl_res = tk.Label(marco, font=("Segoe UI", 12, "bold"))
        self.lbl_res.pack(pady=4)

        # Tabla de transiciones
        ttk.Label(
            marco,
            text="Tabla de transiciones δ:  (estado, lee) → (estado nuevo, escribe, mueve)",
        ).pack(anchor="w")
        self.tabla = ttk.Treeview(
            marco, columns=("e", "l", "n", "w", "m"), show="headings", height=7
        )
        for col, titulo in zip(
            "elnwm", ["Estado", "Lee", "Estado nuevo", "Escribe", "Mueve"]
        ):
            self.tabla.heading(col, text=titulo)
            self.tabla.column(col, width=100, anchor="center")
        self.tabla.tag_configure("usada", background="#ffe082")
        self.tabla.pack(fill="x")
        for (e, leido), (n, w, m) in TRANS.items():
            self.tabla.insert(
                "",
                "end",
                iid=f"{e}|{leido}",
                values=(
                    e,
                    leido,
                    n,
                    w,
                    {"R": "→ derecha", "L": "← izquierda", "S": "● se queda"}[m],
                ),
            )

    def _elegir(self):
        texto = self.combo.get().split("   →")[0]
        self.entrada.delete(0, tk.END)
        self.entrada.insert(0, "" if texto == "ε" else texto)
        self._cargar()

    # Validar cadena
    def _cargar(self):
        texto = self.entrada.get().strip()
        if any(s not in "abc" for s in texto) or len(texto) > LARGO_MAX:
            messagebox.showwarning(
                "Cadena inválida",
                f"Usa solo a, b, c (máximo {LARGO_MAX}).",
                parent=self,
            )
            return
        self.cinta, self.pos, self.estado, self.pasos = (
            crear_cinta(texto),
            1,
            INICIAL,
            0,
        )
        self.terminado, self.aceptada, self.fila_usada = False, False, None
        self.msg = "Pulsa «Siguiente paso» para empezar."
        self._refrescar()

    def paso(self):
        if self.terminado:
            return
        leido = self.cinta[self.pos]
        resultado = dar_paso(self.estado, self.cinta, self.pos)
        if resultado is None:
            self.terminado, self.aceptada, self.fila_usada = True, False, None
            self.msg = f"En {self.estado} leyendo '{leido}' no hay transición: se bloquea y rechaza."
        else:
            nuevo, escribe, mov = TRANS[(self.estado, leido)]
            lado = {"R": "derecha", "L": "izquierda", "S": "se queda"}[mov]
            marca = f"marcar {escribe}" if escribe != leido else "sin marcar"
            self.msg = f"{self.estado}:  leer {leido} → {marca} → {lado}      (siguiente estado: {nuevo})"
            self.fila_usada = f"{self.estado}|{leido}"
            self.estado, self.cinta, self.pos = resultado
            self.pasos += 1
            if self.estado == ACEPTA:
                self.terminado, self.aceptada = True, True
        self._refrescar()

    # Redibuja la cinta
    def _refrescar(self):
        c = self.cinta_ui
        c.delete("all")
        x0 = (
            ANCHO_CINTA - len(self.cinta) * ANCHO_CASILLA
        ) / 2 
        for i, simbolo in enumerate(self.cinta):
            x = x0 + i * ANCHO_CASILLA
            fondo = (
                "#ffe082"
                if i == self.pos
                else (
                    "#cfd8dc"
                    if simbolo in (INI, FIN)
                    else "#bbdefb" if simbolo in "ABC" else "white"
                )
            )
            c.create_rectangle(
                x, 40, x + ANCHO_CASILLA, 76, fill=fondo, outline="#1f3a5f", width=2
            )
            c.create_text(
                x + ANCHO_CASILLA / 2, 58, text=simbolo, font=("Consolas", 15, "bold")
            )
            c.create_text(
                x + ANCHO_CASILLA / 2,
                90,
                text=str(i),
                font=("Segoe UI", 8),
                fill="#78909c",
            )
            if i == self.pos:
                cx = x + ANCHO_CASILLA / 2
                c.create_polygon(
                    cx - 9, 12, cx + 9, 12, cx, 32, fill="#c62828", outline=""
                )
        xf = x0 + len(self.cinta) * ANCHO_CASILLA
        c.create_line(x0, 34, x0, 82, width=6, fill="#1f3a5f")
        c.create_line(xf, 34, xf, 82, width=6, fill="#1f3a5f")
        self.lbl_estado.config(
            text=f"Estado actual: {self.estado} Pasos: {self.pasos}"
        )
        self.lbl_msg.config(text=self.msg)
        self.lbl_res.config(
            text=(
                ("Cadena ACEPTADA" if self.aceptada else "Cadena RECHAZADA")
                if self.terminado
                else ""
            ),
            fg="#2e7d32" if self.aceptada else "#c62828",
        )
        for iid in self.tabla.get_children():
            self.tabla.item(iid, tags=())
        if self.fila_usada:
            self.tabla.item(self.fila_usada, tags=("usada",))


def abrir(root):
    VentanaLBA(root)

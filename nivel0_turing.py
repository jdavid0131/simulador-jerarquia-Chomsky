import tkinter as tk
from tkinter import ttk, messagebox

BLANCO = "_"
MAX_PASOS = 5000
CELDAS = 15
ANCHO = 44
ANCHO_CINTA = CELDAS * ANCHO + 80
MOV = {"L": -1, "R": 1}
LADO = {"L": "izquierda", "R": "derecha"}

# capa de datos
MAQUINAS = {
    "Aceptar aⁿbⁿ": {
        "tipo": "acepta",
        "descripcion": "L = { aⁿbⁿ : n ≥ 0 }",
        "entrada": ["a", "b"],
        "cinta": ["a", "b", "X", "Y", BLANCO],
        "delta": {
            ("q0", "a"): ("q1", "X", "R"),  
            ("q0", "Y"): ("q3", "Y", "R"),  
            ("q0", BLANCO): ("qf", BLANCO, "R"), 
            ("q1", "a"): ("q1", "a", "R"),
            ("q1", "Y"): ("q1", "Y", "R"),
            ("q1", "b"): ("q2", "Y", "L"), 
            ("q2", "a"): ("q2", "a", "L"),
            ("q2", "Y"): ("q2", "Y", "L"),
            ("q2", "X"): ("q0", "X", "R"),  
            ("q3", "Y"): ("q3", "Y", "R"),
            ("q3", BLANCO): ("qf", BLANCO, "R"), 
        },
        "ejemplos": ["", "ab", "aabb", "aaabbb", "aab", "abb", "ba", "abab"],
    },
    "Suma (x + y)": {
        "tipo": "funcion",
        "descripcion": "f(x, y) = x + y",
        "codificar": True,
        "entrada": ["1", "+"],
        "cinta": ["1", "+", BLANCO],
        "delta": {
            ("q0", "1"): ("q0", "1", "R"),
            ("q0", "+"): ("q1", "1", "R"),
            ("q1", "1"): ("q1", "1", "R"),
            ("q1", BLANCO): ("q2", BLANCO, "L"), 
            ("q2", "1"): ("qf", BLANCO, "L"), 
        },
        "ejemplos": ["0+1", "1+1", "2+1", "2+3", "3+2", "4+0", "1+1+1"],
        "salida": lambda s: f"{s or 'ε'}  (= {len(s)})",
    },
    "Incremento binario": {
        "tipo": "funcion",
        "descripcion": "f(n) = n + 1 con n en binario. Va al final y suma 1 llevando el acarreo a la izquierda.",
        "entrada": ["0", "1"],
        "cinta": ["0", "1", BLANCO],
        "delta": {
            ("q0", "0"): ("q0", "0", "R"),
            ("q0", "1"): ("q0", "1", "R"),
            ("q0", BLANCO): ("q1", BLANCO, "L"),  
            ("q1", "1"): ("q1", "0", "L"), 
            ("q1", "0"): ("qf", "1", "R"), 
            ("q1", BLANCO): (
                "qf",
                "1",
                "R",
            ),  
        },
        "ejemplos": ["1011", "111", "0", "100", "1"],
        "salida": lambda s: f"{s}  (= {int(s, 2)})" if s else "ε",
    },
}


#capa logica
def codificar(maq, texto):
    if not maq.get("codificar"):
        return texto
    partes, numero = [], ""
    for s in texto + " ": 
        if s.isdigit():
            numero += s
        else:
            if numero:
                partes.append("1" * int(numero))
                numero = ""
            if s != " ":
                partes.append(s)
    return "".join(partes)

def contenido(cinta):
    if not cinta:
        return ""
    return "".join(
        cinta.get(i, BLANCO) for i in range(min(cinta), max(cinta) + 1)
    ).strip(BLANCO)

def dar_paso(maq, estado, cinta, cab):
    regla = maq["delta"].get((estado, cinta.get(cab, BLANCO)))
    if regla is None:
        return None
    nuevo, escribe, mov = regla
    cinta = dict(cinta)
    if escribe == BLANCO:
        cinta.pop(cab, None)  # escribir blanco = borrar
    else:
        cinta[cab] = escribe
    return nuevo, cinta, cab + MOV[mov]

def ejecutar(maq, cadena):
    estado, cinta, cab = "q0", dict(enumerate(codificar(maq, cadena))), 0
    for _ in range(MAX_PASOS):
        if estado == "qf":
            return "fin", contenido(cinta)
        paso = dar_paso(maq, estado, cinta, cab)
        if paso is None:
            return "bloqueada", contenido(cinta)
        estado, cinta, cab = paso
    return "limite", contenido(cinta)

def veredicto(maq, cadena):
    fin, texto = ejecutar(maq, cadena)
    if maq["tipo"] == "acepta":
        return "acepta" if fin == "fin" else "rechaza"
    return maq["salida"](texto) if fin == "fin" else "entrada inválida"


#capa interfaz
class VentanaTuring(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Nivel 0 · Máquina de Turing")
        self.minsize(820, 720)
        self.fila_usada = None
        self._construir()
        self._cargar_maquina()

    def _construir(self):
        marco = ttk.Frame(self, padding=12)
        marco.pack(fill="both", expand=True)

        fila = ttk.Frame(marco)
        fila.pack(fill="x")
        ttk.Label(fila, text="Máquina:").pack(side="left")
        self.combo = ttk.Combobox(
            fila, values=list(MAQUINAS), state="readonly", width=22
        )
        self.combo.current(0)
        self.combo.pack(side="left", padx=8)
        self.combo.bind("<<ComboboxSelected>>", lambda e: self._cargar_maquina())
        self.lbl_desc = ttk.Label(marco, font=("Segoe UI", 10, "bold"), wraplength=780)
        self.lbl_desc.pack(anchor="w", pady=(8, 2))
        self.lbl_alfabeto = ttk.Label(marco, font=("Segoe UI", 10))
        self.lbl_alfabeto.pack(anchor="w", pady=(0, 8))

        fila2 = ttk.Frame(marco)
        fila2.pack(fill="x")
        ttk.Label(fila2, text="Entrada:").pack(side="left")
        self.entrada = ttk.Entry(fila2, width=22, font=("Consolas", 12))
        self.entrada.pack(side="left", padx=6)
        ttk.Button(fila2, text="Cargar", command=self._cargar).pack(side="left")
        ttk.Label(fila2, text="   Ejemplos:").pack(side="left")
        self.combo_ej = ttk.Combobox(fila2, state="readonly", width=30)
        self.combo_ej.pack(side="left", padx=6)
        self.combo_ej.bind("<<ComboboxSelected>>", lambda e: self._elegir())

        # La cinta se dibuja en un lienzo: 15 casillas, con el cabezal siempre en la del centro.
        self.cinta_ui = tk.Canvas(
            marco, width=ANCHO_CINTA, height=105, highlightthickness=0
        )
        self.cinta_ui.pack(pady=(10, 4))
        ttk.Label(
            marco,
            text="La cinta es infinita: lo que no se ve es blanco. El número bajo cada casilla es su posición.",
            font=("Segoe UI", 9, "italic"),
        ).pack()

        self.lbl_estado = tk.Label(marco, font=("Segoe UI", 14, "bold"), fg="#1f3a5f")
        self.lbl_estado.pack(pady=(8, 2))
        self.lbl_msg = tk.Label(marco, font=("Segoe UI", 10), wraplength=780, height=2)
        self.lbl_msg.pack()
        botones = ttk.Frame(marco)
        botones.pack(pady=4)
        ttk.Button(botones, text="Siguiente paso", command=self.paso).pack(
            side="left", padx=4
        )
        ttk.Button(botones, text="Reiniciar", command=self._cargar).pack(
            side="left", padx=4
        )
        self.lbl_res = tk.Label(marco, font=("Segoe UI", 12, "bold"), wraplength=780)
        self.lbl_res.pack(pady=4)

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

    # Carga la máquina elegida.
    def _cargar_maquina(self):
        self.maq = MAQUINAS[self.combo.get()]
        self.lbl_desc.config(text=self.maq["descripcion"])
        self.lbl_alfabeto.config(
            text=f"Alfabeto de entrada: {{{', '.join(self.maq['entrada'])}}}      "
            f"Alfabeto de la cinta: {{{', '.join(self.maq['cinta'])}}}"
        )
        self.combo_ej.config(
            values=[
                f"{c or 'ε'}   →   {veredicto(self.maq, c)}"
                for c in self.maq["ejemplos"]
            ]
        )
        self.combo_ej.set("")
        self.tabla.delete(*self.tabla.get_children())
        for (e, leido), (n, w, m) in self.maq["delta"].items():
            self.tabla.insert(
                "",
                "end",
                iid=f"{e}|{leido}",
                values=(e, leido, n, w, "→ derecha" if m == "R" else "← izquierda"),
            )
        self.entrada.delete(0, tk.END)
        self.entrada.insert(
            0, self.maq["ejemplos"][2] if len(self.maq["ejemplos"]) > 2 else ""
        )
        self._cargar()

    def _elegir(self):
        texto = self.combo_ej.get().split("   →")[0]
        self.entrada.delete(0, tk.END)
        self.entrada.insert(0, "" if texto == "ε" else texto)
        self._cargar()

    def _cargar(self):
        texto = self.entrada.get().strip()
        en_cinta = codificar(self.maq, texto)  # lo que realmente se escribe en la cinta
        permitidos = (
            list("0123456789+") if self.maq.get("codificar") else self.maq["entrada"]
        )
        if any(s not in self.maq["entrada"] for s in en_cinta) or len(en_cinta) > 25:
            messagebox.showwarning(
                "Entrada inválida",
                "Usa solo: "
                + " ".join(permitidos)
                + "  (la cinta admite máximo 25 símbolos).",
                parent=self,
            )
            return
        self.cinta, self.cab, self.estado, self.pasos = (
            dict(enumerate(en_cinta)),
            0,
            "q0",
            0,
        )
        self.terminado, self.fila_usada = False, None
        self.msg, self.res, self.ok = "Pulsa Siguiente paso para empezar.", "", True
        if en_cinta != texto:
            self.msg = (
                f"Entrada {texto} escrita en unario en la cinta: {en_cinta}.  "
                + self.msg
            )
        self._refrescar()

    def paso(self):
        if self.terminado:
            return
        leido = self.cinta.get(self.cab, BLANCO)
        resultado = dar_paso(self.maq, self.estado, self.cinta, self.cab)
        if resultado is None:
            self.terminado, self.fila_usada, self.ok = True, None, False
            self.msg = f"En {self.estado} leyendo '{leido}' no hay transición: la máquina se bloquea."
            self.res = (
                "RECHAZADA" if self.maq["tipo"] == "acepta" else "ENTRADA INVÁLIDA"
            )
        else:
            nuevo, escribe, mov = self.maq["delta"][(self.estado, leido)]
            accion = f"escribir {escribe}" if escribe != leido else "sin cambio"
            self.msg = (
                f"{self.estado}:  leer {leido} → {accion} → {LADO[mov]}      "
                f"(siguiente estado: {nuevo})"
            )
            self.fila_usada = f"{self.estado}|{leido}"
            self.estado, self.cinta, self.cab = resultado
            self.pasos += 1
            if self.estado == "qf":
                self.terminado = True
                if self.maq["tipo"] == "acepta":
                    self.res = "ACEPTADA"
                else:
                    self.res = "Resultado en la cinta: " + self.maq["salida"](
                        contenido(self.cinta)
                    )
            elif self.pasos >= MAX_PASOS:
                self.terminado, self.ok, self.res = (
                    True,
                    False,
                    "Se superó el máximo de pasos.",
                )
        self._refrescar()

    # Redibuja la cinta (ventana de 15 casillas alrededor del cabezal), estado y resultado.
    def _refrescar(self):
        c = self.cinta_ui
        c.delete("all")
        mitad = CELDAS // 2
        for k in range(CELDAS):
            pos = self.cab - mitad + k  # posición real de esta casilla en la cinta
            simbolo = self.cinta.get(pos, BLANCO)
            x = 40 + k * ANCHO
            fondo = (
                "#ffe082" if k == mitad else "#bbdefb" if simbolo in "XY" else "white"
            )
            c.create_rectangle(
                x, 40, x + ANCHO, 78, fill=fondo, outline="#1f3a5f", width=2
            )
            c.create_text(
                x + ANCHO / 2,
                59,
                text=simbolo,
                font=("Consolas", 16, "bold"),
                fill="#90a4ae" if simbolo == BLANCO else "black",
            )
            c.create_text(
                x + ANCHO / 2, 92, text=str(pos), font=("Segoe UI", 8), fill="#78909c"
            )
        cx = (
            40 + mitad * ANCHO + ANCHO / 2
        )  # el cabezal: triángulo rojo en la casilla central
        c.create_polygon(cx - 10, 12, cx + 10, 12, cx, 34, fill="#c62828", outline="")
        c.create_text(
            18, 59, text="…", font=("Segoe UI", 20)
        )  # la cinta sigue a ambos lados
        c.create_text(ANCHO_CINTA - 18, 59, text="…", font=("Segoe UI", 20))
        self.lbl_estado.config(
            text=f"Estado activo: {self.estado}     ·     Cabezal: {self.cab}     ·     Pasos: {self.pasos}"
        )
        self.lbl_msg.config(text=self.msg)
        self.lbl_res.config(text=self.res, fg="#2e7d32" if self.ok else "#c62828")
        for iid in self.tabla.get_children():
            self.tabla.item(iid, tags=())
        if self.fila_usada:
            self.tabla.item(self.fila_usada, tags=("usada",))


def abrir(root):
    VentanaTuring(root)

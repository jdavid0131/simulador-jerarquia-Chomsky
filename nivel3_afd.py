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
            ("q0", "0"): "q1", ("q0", "1"): "q0",
            ("q1", "0"): "q1", ("q1", "1"): "q2",
            ("q2", "0"): "q1", ("q2", "1"): "q0",
        },
        "ejemplos": ["", "01", "001", "1101", "10", "0110"],
        #ejemplos de cadenas que saldran en la interfaz
    
    },
    "cantidad par de unos":{
        "descripcion": "L={w ∈ {0,1}* : w tiene una cantidad par de 1 }",
        "alfabeto":["0","1"],
        "estados":["q0","q1"],
        "inicial":"q0",
        "finales":{"q0"},
        "transiciones":{
             ("q0", "0"): "q0", ("q0", "1"): "q1",
            ("q1", "0"): "q1", ("q1", "1"): "q0"
        },
        "ejemplos": ["", "11", "1010", "0110", "1", "0111"],

    },
    #tercer automata
    "Contiene la subcadena ab": {
        "descripcion": "L = { w ∈ {a,b}* : w contiene la subcadena ab }",
        "alfabeto": ["a", "b"],
        # s0 = todavía no vi una 'a' que me sirva,
        # s1 = acabo de ver una 'a' (si viene una 'b', completo "ab"),
        # s2 = ya encontré "ab" (final).
        "estados": ["s0", "s1", "s2"],
        "inicial": "s0",
        "finales": {"s2"},
        "transiciones": {
            ("s0", "a"): "s1", ("s0", "b"): "s0",
            ("s1", "a"): "s1", ("s1", "b"): "s2",
            # Una vez que encontré "ab", ya no importa lo que venga: me quedo en s2.
            ("s2", "a"): "s2", ("s2", "b"): "s2",
        },
        "ejemplos": ["ab", "aab", "bbab", "ba", "bbb", "aaa"],
    },

}
#capa de logica
def acepta (afd,cadena):
    estado = afd["inicial"]
    for simbolo in cadena:
        estado= afd["transiciones"].get((estado,simbolo))
        if estado is None:
            return False
    return estado in afd["finales"]
#capa de interfaz
class VentanaAFD(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("nivel3- Automata Finito Determinista")
        self.minsize(720,600)
        ttk.Label(self, text="Aquí irá el simulador del Nivel 3").pack(padx=20, pady=20)
def abrir(root):
        VentanaAFD(root)


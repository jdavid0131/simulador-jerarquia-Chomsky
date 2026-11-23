# simulador-jerarquia-Chomsky
simulador interactivo de la jerarquia de chomky

# Simulador de la Jerarquía de Chomsky

Aplicación de escritorio con interfaz gráfica (Python + tkinter) que permite **simular paso a paso** los cuatro modelos computacionales de la jerarquía de Chomsky: autómata finito, autómata de pila, autómata linealmente acotado y máquina de Turing.

Proyecto tercero · Autómatas, Gramáticas y Lenguajes · Periodo 2026-II
Autor: [Juan David Rodriguez]

---

## 1. Requisitos

Requisito: Python
Detalle: 3.8 o superior (probado con Python 3.14)
Requisito:tkinter
Detalle: Viene incluido con Python en Windows y macOS
Requisito :Librerias Externas
Detalle: Ninguna. No hay que instalar nada con pip 

En Linux, si tkinter no esta instalado:

sudo apt install python3-tk

Para comprobar que tkinter funciona, ejecuta 'python -m tkinter': debe abrirse una ventana pequeña de prueba.

## 2. Instalación y ejecución

1. Clona el repositorio (o descárgalo como ZIP desde GitHub con Code -> Download ZIP  y descomprímelo)

   git clone https://github.com/jdavid0131/simulador-jerarquia-Chomsky.git
   cd simulador-jerarquia-Chomsky

2. Ejecuta el programa desde esa carpeta:

   python main.py

   En Windows, si python no se reconoce, usa 'py main.py'. En macOS y Linux suele ser 'python3 main.py'.

3. Se abre el panel principal con un botón por nivel.

## 3. Estructura del proyecto

Archivo: main.py
Contenido: Panel principal: abre la ventana de cada nivel

Archivo:nivel3_afd.py
Contenido: Nivel 3 · Autómata finito determinista (lenguajes regulares)

Archivo: nivel2_pila.py
Contenido: Nivel 2 · Autómata de pila (lenguajes libres de contexto)

Archivo: nivel1_lba.py
Contenido: Nivel 1 · Autómata linealmente acotado (lenguajes sensibles al contexto)

Archivo: nivel0_turing.py
Contenido: Nivel 0 · Máquina de Turing (lenguajes recursivamente enumerables)

Archivo: docs/DOCUMENTACION.md
Contenido: Documento que explica la implementación y los conceptos aplicados


## 4. Cómo se usa

Todos los niveles funcionan igual:

1. Pulsa el botón del nivel en el panel principal. Se abre su ventana.
2. Elige el lenguaje (o la máquina) en el menú desplegable.
3. Escribe una cadena en el cuadro de texto y pulsa 'Cargar', o elige una del menú 'Ejemplos'. El menú indica de antemano si la cadena se acepta o se rechaza. Para probar la cadena vacía (ε) deja el cuadro vacío o elige 'ε' en los ejemplos.
4. Pulsa 'Siguiente paso' para avanzar. Pulsa 'Reiniciar' para volver al principio con la misma cadena.
5. Al terminar aparece el resultado: 'ACEPTADA' (verde) o 'RECHAZADA' (rojo), con el motivo.

Si escribes un símbolo que no pertenece al alfabeto, un aviso indica cuáles se permiten.

## 5. Qué muestra cada nivel y ejemplos de prueba

Los mismos ejemplos están incluidos en el menú **Ejemplos** de cada ventana.

### Nivel 3 · Autómata finito determinista

Muestra los estados del autómata (el actual se ilumina; borde grueso = estado final), la cadena leída símbolo a símbolo y la tabla de transiciones δ.

Lenguaje: Cadenas binarias que terminan en 01
Cadenas que se aceptan: 01, 001, 1101
Cadenas que se rechazan: ε, 10, 0110

Lenguaje: Cantidad par de unos
Cadenas que se aceptan: ε, 11, 1010, 0110
Cadenas que se rechazan: 1, 0111

Lenguaje: Contiene la subcadena ab
Cadenas que se aceptan: ab, aab, bbab
Cadenas que se rechazan: ba, bbb, aaa

### Nivel 2 · Autómata de pila

Muestra la pila dibujada : cada símbolo apilado es un bloque, y la pila cambia con cada paso (se agrega o se quita un bloque). También muestra el estado actual, el tope y la tabla de transiciones en la notación 'entrada | tope, acción, elemento'.

Una cadena se acepta si, al terminar, el autómata está en un estado final y la pila está vacía.

Lenguaje: aⁿbⁿ
Cadenas que se aceptan: ε, ab, aabb, aaabbb
Cadenas que se rechazan: aab, abb, ba

Lenguaje: aⁿb²ⁿ
Cadenas que se aceptan: ε, abb, aabbbb, aaabbbbbb
Cadenas que se rechazan: aabb, abbb, ab

Lenguaje: a³ⁿb⁴ⁿ
Cadenas que se aceptan: ε, aaabbbb, aaaaaabbbbbbbb
Cadenas que se rechazan: aaabbb, aaaabbbb, aaabbbbb, aaaaaabbbb

### Nivel 1 · Autómata linealmente acotado

Muestra la cinta acotada con sus delimitadores de frontera '$' (izquierdo)y '$$'(deecho), el cabezal (triángulo rojo) moviéndose de izquierda a derecha, los símbolos ya marcados ('A', 'B', 'C', en azul) y la tabla de transiciones con la regla usada resaltada.

Lenguaje: **L = { a bⁿ c²ⁿ : n ≥ 0 }
Cadenas que se aceptan: ε, aaabbbb, aaaaaabbbbbbbb
Cadenas que se rechazan: aaabbb, aaaabbbb, aaabbbbb, aaaaaabbbb

La cadena admite máximo 20 símbolos y solo las letras 'a', 'b', 'c'.

### Nivel 0 · Máquina de Turing

Muestra la cinta extendible (una ventana de 15 casillas alrededor del cabezal, con la posición de cada casilla), el alfabeto de entrada y de la cinta, el cabezal y el estado activo '_' es el símbolo blanco.

Maquina: Aceptar aⁿbⁿ
Tipo: Acepta o rechaza
Ejemplos de entrada:ε, ab, aabb, aaabbb → acepta · aab, abb, ba, abab -> rechaza

Maquina:Suma (x + y)
Tipo:Calcula una función
Ejemplos de entrada:0+1 → 1 · 1+1 → 2 · 2+3 → 5 · 3+2 → 5 · 4+0 ->4

Maquina:Incremento binario
Tipo:Calcula una función
Ejemplo de entrada:1011 → 1100 · 111 → 1000 · 0 → 1 · 100 → 101 · 1 ->10

En la suma los números se escriben en decimal y la ventana los pasa a unario en la cinta (por ejemplo, '2+3' queda como '11+111'). La entrada '1+1+1' se rechaza porque la máquina solo suma dos números. La cinta admite máximo 25 símbolos.

## 6. Documentación

La explicación de la implementación y de los conceptos aplicados está en (docs/DOCUMENTACION.md).

## 7. Solución de problemas

Problema: ModuleNotFoundError: No module named 'tkinter'
Solucion:Instala tkinter (en Linux: sudo apt install python3-tk)

Problema:ModuleNotFoundError: No module named 'nivel2_pila'
Solucion:Ejecuta python main.py desde la carpeta del proyecto, donde están todos los archivos .py

Problema:python no se reconoce (Windows)
Solucion:Prueba con py main.py


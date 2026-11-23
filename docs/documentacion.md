# Simulador de la Jerarquía de Chomsky: implementación y conceptos aplicados

**Autor:** [juan David Rodriguez Contreras]
**Curso:** Autómatas, Gramáticas y Lenguajes · Periodo 2026-II
**Lenguaje de programación:** Python 3 con la librería gráfica tkinter

---

## 1. Objetivo

Diseñar e implementar una aplicación con interfaz gráfica que permita visualizar y simular el comportamiento de los modelos computacionales de los cuatro niveles de la jerarquía de Chomsky. Para cada nivel, el usuario escribe una cadena (o elige un ejemplo) y la recorre paso a paso, viendo cómo cambian el estado y la memoria del modelo hasta llegar a aceptar o rechazar.

## 2. Conceptos aplicados: la jerarquía de Chomsky

La jerarquía clasifica los lenguajes formales según la complejidad de sus reglas y según qué tanta memoria necesita la máquina que los reconoce. Cada tipo incluye al anterior: Tipo 3 ⊂ Tipo 2 ⊂ Tipo 1 ⊂ Tipo 0.

Tipo:3
Lenguaje:Regulares
Modelo: Automata Finito Determinista(AFD)
Memoria: Solo el estado(finita)
Ejemplo: Cadenas que terminan en 01

Tipo:3
Lenguaje:Regulares
Modelo: Automata Finito Determinista(AFD)
Memoria: Solo el estado(finita)
Ejemplo: Cadenas que terminan en 01

Tipo 2: Libres de contexto
Modelo: Automata de Pila
Memoria: Una pila(LIFO)
Ejemplo: aⁿbⁿ, aⁿb²ⁿ, a³ⁿb⁴ⁿ

Tipo 1: Sensibles al contexto
Modelo: Automata Linealmente Acotado(LBA)
Memoria: Cinta de tamaño de la entrada
Ejemplo: a bⁿ c²ⁿ

La idea que une los cuatro niveles es que más memoria permite reconocer lenguajes más difíciles. Por ejemplo, aⁿbⁿ no es regular porque exige recordar cuántas `a` llegaron y n no tiene límite, mientras que los estados de un AFD son finitos. La pila resuelve esa necesidad de contar.

## 3. Arquitectura del proyecto

```
main.py ──► nivel3_afd.py      (AFD)
        ├─► nivel2_pila.py     (autómata de pila)
        ├─► nivel1_lba.py      (LBA)
        └─► nivel0_turing.py   (máquina de Turing)
```

### 3.1 Panel principal (`main.py`)

Muestra un botón por nivel a partir de la lista `MODULOS`, donde cada elemento tiene el título del nivel, el modelo y el nombre del archivo. Al pulsar un botón, la función 'abrir_modulo' carga ese archivo con 'importlib.import_module' y llama a su función 'abrir(root)'. Si el archivo no tiene esa función lanza una excepcion.De esta manera permite que cada nivel sea independiente

### 3.2 Organización en tres capas

Cada archivo de nivel está dividido en tres partes:

Capa: Datos
Que contiene:El modelo escrito con estructuras de datos como (diccionarios y listas)
Ejemplo: El AFD como diccionario de transiciones.

Capa: Logica
Que contiene: Funciones que simulan el modelo, sin la parte grafica.
Ejemplo: acepta,siguiente

Capa: interfaz:
Que contiene: Las vistas graficas(clase que hereda de tk.TopLevel)
Ejemplo: VentanaPila

Separar la lógica de la interfaz permite probar el modelo sin abrir la ventana, y hace que las vistas  solo se ocupe de mostrar  como salida lo que la lógica calcula.

### 3.3 Funcionamiento común de las vistas

Todas las ventanas comparten el mismo esquema de uso:

- Un menú para elegir el lenguaje o la máquina.
- Un cuadro de texto para la cadena, un botón 'Cargar' y un menú de 'Ejemplos' que indica si cada cadena se acepta o se rechaza.
- El botón 'Siguiente paso', que ejecuta exactamente una transición, y el botón 'Reiniciar'.
- Un mensaje que describe lo que hizo el último paso y un resultado final en verde (aceptada) o rojo (rechazada).

## 4. Nivel 3: autómata finito determinista (`nivel3_afd.py`)

### 4.1 Concepto

Un AFD es una máquina con un número finito de estados que lee la cadena de izquierda a derecha, un símbolo a la vez, y cambia de estado según una función de transición. Formalmente M = (Q, Σ, δ, q₀, F). Acepta si, al terminar la cadena, está en un estado de F.

### 4.2 Representación

Cada lenguaje es un diccionario con su descripción, alfabeto, estados, estado inicial, estados finales, transiciones y ejemplos. La función δ se guarda como un diccionario donde la clave es '(estado, símbolo)' y el valor es el estado siguiente:

("q1", "1"): "q2"      # estando en q1 y leyendo 1, pasa a q2

Los lenguajes incluidos son: cadenas binarias que terminan en '01', cantidad par de unos y cadenas que contienen la subcadena 'ab'.

### 4.3 Algoritmo

La función 'acepta(afd, cadena)' parte del estado inicial y, para cada símbolo, busca la transición correspondiente. Si no existe, rechaza. Al final devuelve si el estado alcanzado es final. Los tres autómatas están completos (tienen transición para cada estado y símbolo), por lo que nunca se bloquean.

### 4.4 Interfaz

- Cada estado se dibuja como una casilla. El 'estado actual' se ilumina en amarillo y, al terminar, en verde (acepta) o rojo (rechaza). Los 'estados finales' tienen el borde grueso.
- La cadena se muestra con el símbolo que se va a leer entre corchetes.
- La 'tabla de transiciones δ' marca el estado inicial con '>' y los finales con '*', y resalta la fila del estado actual.

## 5. Nivel 2: autómata de pila (`nivel2_pila.py`)

### 5.1 Concepto

Un autómata de pila agrega al AFD una 'pila', que es una memoria de tipo LIFO (el último que entra es el primero que sale). Gracias a ella puede contar y comparar cantidades sin límite, y así reconoce los lenguajes libres de contexto.

### 5.2 Representación

Se usa la notación de las clases: en cada transición se indica entrada | tope, acción, elemento.
("q1", "b", "a"): ("q2", "out", "a") # estando en q1, leyendo b y con una a en el tope: desapila la a y pasa a q2

Campo: tope
Valores: un símbolo de la pila, ε si la pila está vacía, o * si el tope no importa
Accion:	in apila, out desapila, ε no toca la pila
Elemento: el símbolo que se apila o desapila

La pila es una lista de Python: 'append' apila y 'pop' desapila.

### 5.3 Algoritmo

- 'siguiente(pda, estado, símbolo, pila)' toma el tope de la pila y busca la transición con ese tope. Si no la encuentra, prueba con el comodín '*'. Si tampoco existe (o si intenta desapilar una pila vacía), devuelve 'None' y la cadena se rechaza. Esto cumple el papel del 'estado trampa': lo que no tiene transición, se rechaza.
- 'Criterio de aceptación:' al terminar la cadena, el autómata debe estar en un estado final 'y' la pila debe estar vacía.

### 5.4 Lenguajes

Lenguaje:aⁿbⁿ
Como funciona:Cada 'a' apila una marca y cada 'b' saca una. Los estados q1 y q2 evitan que lleguen 'a' después de empezar las 'b'

### 5.5 Interfaz

La pila se dibuja  con sus paredes y un bloque por cada elemento, con la etiqueta 'tope' en el último. En cada paso la pila se redibuja, así se visualiza cómo crece y se reduce. Si la pila se hace grande, los bloques se achican para que quepan. También se muestran el estado actual, el tope, el texto de la acción realizada (por ejemplo 'apila a') y la tabla de transiciones.

## 6. Nivel 1: autómata linealmente acotado (`nivel1_lba.py`)

### 6.1 Concepto

Un LBA es una máquina de Turing cuya cinta 'no puede crecer': solo puede usar las casillas ocupadas por la entrada, limitadas por dos delimitadores de frontera. El cabezal se mueve en ambos sentidos y puede 'reescribir' los símbolos. Reconoce los lenguajes sensibles al contexto, como aⁿbⁿcⁿ, que una pila no puede reconocer porque habría que comparar tres cantidades a la vez.

### 6.2 Representación

La cinta es una lista de Python que empieza y termina con el delimitador '$' y '$$': la cadena 'abcc' queda como '$ a b c c $$'. El cabezal comienza en la primera casilla de la cadena.

Las transiciones se guardan en el diccionario 'TRANS', con clave '(estado, símbolo leído)' y valor '(estado nuevo, símbolo que escribe, movimiento)', donde el movimiento es 'R' (derecha), 'L' (izquierda) o 'S' (se queda).

("Derecha", "b"): ("BuscarC", "B", "R")   # marca la b como B y sigue a la derecha

### 6.3 Lenguaje y algoritmo

El lenguaje es 'L = { a bⁿ c²ⁿ : n ≥ 0 }', el ejemplo visto en clase. El LBA verifica que haya el doble de 'c' que de 'b' 'marcando' símbolos con letras mayúsculas ('A', 'B', 'C'), para recordar cuáles ya se emparejaron:

1. Inicio: marca la 'a' como 'A'.
2. Derecha: avanza saltando las marcas 'A' y 'B' hasta encontrar una 'b' sin marcar y la marca como 'B'.
3. Buscar C: avanza saltando las 'b' y las 'C' hasta encontrar una 'c' sin marcar y la marca como 'C'.
4. Segunda C: exige otra 'c' y la marca. Si no hay, se bloquea.
5. Volver: regresa hacia la izquierda hasta el delimitador '$' y repite desde el paso 2.
6. Verificar: cuando no quedan 'b' sin marcar, comprueba que lo que queda sea solo 'C` hasta el delimitador derecho. Si es así, el estado es 'Fin' y acepta.

El caso n = 0 (la cadena 'a') se acepta directamente: después de marcar la 'a', el estado Derecha llega al delimitador '$' sin encontrar ninguna 'b'.

Si en algún momento no hay transición, o el cabezal intentaría salir de la cinta, la cadena se rechaza.

### 6.4 Interfaz

La cinta se dibuja casilla por casilla: los delimitadores en gris, los símbolos marcados en azul y la casilla actual en amarillo, con el cabezal como un triángulo rojo encima. Debajo de cada casilla se muestra su posición. En la tabla de transiciones se resalta la regla usada en el último paso, y el mensaje describe la acción, por ejemplo leer b > marcar B > derecha.

## 7. Nivel 0: máquina de Turing (`nivel0_turing.py`)

### 7.1 Concepto

La máquina de Turing es el modelo más general: tiene una cinta infinita en ambos sentidos, un cabezal que lee y escribe, y puede ir a izquierda y derecha sin restricciones. Sirve para reconocer lenguajes recursivamente enumerables y también para 'calcular funciones'.

### 7.2 Representación

- La cinta es un diccionario '{posición: símbolo}' Como solo guarda las casillas escritas, es 'extendible' a ambos lados: las posiciones pueden ser negativas y cualquier casilla ausente vale blanco ('_').
-La función δ es un diccionario '(estado, símbolo leído) > (estado nuevo, símbolo que escribe, movimiento)'.
- El estado inicial es 'q0' y el estado de parada es 'qf'.

### 7.3 Algoritmo

- dar_paso' ejecuta una transición: copia la cinta, escribe el símbolo (escribir un blanco borra la casilla) y mueve el cabezal una posición.
- 'ejecutar' repite pasos hasta llegar a 'qf', bloquearse (no hay transición) o superar el límite de 5000 pasos, para evitar ciclos infinitos.
- 'veredicto' convierte el resultado en acepta» o rechaza, o en el valor calculado si la máquina es de tipo función.

### 7.4 Máquinas incluidas

Maquina:Aceptar aⁿbⁿ
Como Funciona: Cambia una a por X, busca la primera b sin marcar y la cambia por Y, regresa a la X y repite. Cuando no quedan a, verifica que solo queden Y

Maquina: Suma (x + y)
Como Funciona: Los números se escriben en unario (el número n es n unos). La máquina cambia el + por un 1 y borra el último 1, de modo que la cinta queda con x + y unos. La ventana convierte el texto decimal a unario antes de cargar la cinta.

Maquina: Incremento binario
Como Funciona:Va hasta el final del número y suma 1 llevando el acarreo hacia la izquierda: cada 1 pasa a 0 hasta encontrar un 0 (que pasa a 1) o un blanco.


### 7.5 Interfaz

La cinta se muestra como una ventana de 15 casillas con el 'cabezal' siempre en la casilla central, y la posición de cada casilla debajo. Se muestran el 'alfabeto de entrada' y el 'alfabeto de la cinta', el 'estado activo', la posición del cabezal y el número de pasos. La tabla de transiciones resalta la regla usada.

## 8. Decisiones de diseño

-Modelos como datos: cada autómata es un diccionario, no código escrito a mano. Para agregar un lenguaje basta con añadir una entrada, sin tocar la lógica ni la interfaz.
-Lo que no tiene transición, se rechaza. No se dibujan estados trampa: el rechazo ocurre cuando no hay regla aplicable.
- Un paso a la vez. Cada clic ejecuta exactamente una transición, para poder explicar el funcionamiento.
- Ejemplos en la interfaz. Cada ventana trae cadenas de prueba, con y sin aceptación, y el resultado esperado.

## 9. Pruebas

Los ejemplos incluidos en cada menú se ejecutan con la lógica de cada nivel y su resultado coincide con la definición del lenguaje. Entre ellos hay cadenas que deben aceptarse, cadenas que deben rechazarse y casos límite como la cadena vacía.

## 10. Limitaciones y mejoras posibles

- Las cadenas tienen un largo máximo (30 símbolos en el Nivel 2, 20 en el Nivel 1 y 25 en el Nivel 0) para que el dibujo quepa en la ventana.
- Los autómatas son deterministas y están definidos en el código; no se pueden dibujar ni editar desde la interfaz.
- Mejoras posibles: modo de ejecución automática, animación del movimiento de los bloques de la pila, y cargar autómatas desde un archivo.

## 11. Herramientas utilizadas

Durante el desarrollo se usó un asistente de inteligencia artificial  como apoyo para estudiar los conceptos y consultar elementos del lenguaje . Los autómatas parten de los ejemplos vistos en clase.

## 12. Referencias

- Material y ejemplos del curso Autómatas, Gramáticas y Lenguajes.
- Documentación de Python y de tkinter: <https://docs.python.org/3/library/tkinter.html>
-aut . (s/f). Ugr.es. Recuperado el 22 de noviembre de 2026, de https://ccia.ugr.es/~rosa/tutormc/teoria/aut_pilas.html
-Pagina nueva 1. (s/f). Edu.ar. Recuperado el 22 de noviembre de 2026, de https://www.profesores.frc.utn.edu.ar/sistemas/ssl/marciszack/ghd/T-M-AFD.htm
-Representation of Turing Machine in automata theory. (s/f). Tutorialspoint.com. Recuperado el 22 de noviembre de 2026, de https://www.tutorialspoint.com/automata_theory/representation_of_turing_machine.htm
-Python lists. (s/f). W3Schools. Recuperado el 22 de noviembre de 2026, de https://www.w3schools.com/python/python_lists.asp
-Python dictionaries. (s/f). W3Schools. Recuperado el 22 de noviembre de 2026, de https://www.w3schools.com/python/python_dictionaries.asp

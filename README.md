# MusicBox, versión 5.0

Sistema de recomendaciones musicales. Trabajo Práctico Integrador de Estructuras de Datos.

| Versión | Contenido | Trabajos prácticos |
|---------|-----------|--------------------|
| 1.0 | Objetos, clases y análisis de complejidad | TP1, TP2 |
| 2.0 | Árbol binario de búsqueda y AVL | TP3, TP4 |
| 3.0 | Árbol general (n-ario) de categorías integrado a la terminal | TP5 |
| 4.0 | Heap binaria de recomendaciones, calificación persistente y ranking Top-N | TP6 |
| 5.0 | Grafo de canciones relacionadas, consultas y camino más corto (BFS) | TP7 |

# Descripción

MusicBox permite cargar un catálogo de canciones, listarlas, buscarlas por
título o artista, filtrarlas por género, calificarlas, ver un ranking dinámico
de favoritas y explorar qué canciones están relacionadas entre sí, todo desde
la terminal. Es un proyecto que fue incorporando árboles, heaps y grafos en
sucesivas entregas.

# Estructura del repositorio

    musicbox/
    ├── main.py              # clases del dominio + árboles (BST / AVL / general) + heap + grafo + interfaz de terminal
    ├── datos/
    │   └── canciones.json   # catálogo de canciones (guarda puntajes)
    └── README.md

# Requisitos

- Python 3.8 o superior (no requiere instalar librerías externas).

# Cómo ejecutar

1. Cloná o descargá este repositorio.
2. Parate en la carpeta musicbox/ (la que contiene main.py).
3. Ejecutá:

    python3 main.py

4. Vas a ver el menú principal:

    --------------------------------------------------
                        MusicBox
    --------------------------------------------------
    1.  Lista de Temas
    2.  Buscar canciones por titulo
    3.  Buscar canciones por artista
    4.  Explorar por genero o categorias
    5.  Ver mi Top de favoritas
    6.  Ver canciones relacionadas
    7.  Calificar cancion
    8.  Buscar titulo exacto con arbol
    9.  Recorrer arbol binario
    10. Experimento de complejidad
    11. Comparar BST común vs. AVL
    12. Comparar Heap vs. ordenamiento
    13. Explorar relaciones entre canciones (grafo)
    0.  Salir

# Funcionalidades actuales

1. Lista de Temas: muestra el catálogo completo, sin filtrar.
2. Buscar por título: búsqueda parcial, devuelve todas las coincidencias.
3. Buscar por artista: muestra todos los temas de un artista o banda.
4. Explorar por género o categorías: submenú con dos opciones: (1) listar canciones de un género y (2) mostrar el árbol general de categorías.
5. Ver mi Top de favoritas: usa la heap para mostrar el ranking de las canciones más calificadas con las tres primeras posiciones destacadas.
6. Ver canciones relacionadas: pide un título y muestra las canciones relacionadas según el grafo (comparten artista o género). Si el título no existe, sugiere títulos parecidos.
7. Calificar canción: asignás un puntaje del 1 al 10. El puntaje se guarda en canciones.json y persiste entre sesiones.
8. Buscar título exacto con árbol: búsqueda exacta en el AVL.
9. Recorrer árbol binario: inorder, preorder o postorder.
10. Experimento de complejidad: compara búsqueda secuencial vs AVL con distintos tamaños de entrada.
11. Comparar BST común vs. AVL: experimento de desbalance con títulos insertados en orden alfabético.
12. Comparar Heap vs. ordenamiento: mide el tiempo de obtener el Top-N con heap versus ordenar todo el catálogo.
13. Explorar relaciones entre canciones (grafo): submenú con cinco consultas: (1) mostrar todas las relaciones, (2) buscar canciones relacionadas, (3) camino más corto entre dos canciones, (4) canciones más conectadas y (5) estadísticas del grafo.

# Modelo de clases

- Artista: nombre y país.
- Genero: nombre del género musical.
- Album: título, año y el Artista al que pertenece.
- Cancion: título, Artista, Album, Genero, duración en segundos y puntaje personal. Incluye el método calificar() y el setter mi_puntaje.
- NodoArbol: nodo del árbol binario (BST / AVL) que almacena una Cancion con referencias a izquierda y derecha.
- NodoGeneral: nodo del árbol general (n-ario) con nombre y lista de hijos. Se usa para la jerarquía de categorías del TP5.
- HeapRecomendaciones: heap binaria máxima implementada manualmente. Almacena pares (prioridad, cancion) y garantiza que el elemento de mayor prioridad siempre está en la raíz.
- GrafoCanciones: grafo no dirigido y no pesado de canciones, representado con lista de adyacencia. Se usa para las relaciones del TP7.

# Búsqueda por título: dos estrategias

- buscar_por_titulo: recorrido secuencial, coincidencia parcial (autocompletar).
- buscar_en_arbol: árbol AVL ordenado por título, coincidencia exacta, O(log n) promedio.

# Análisis de complejidad

| Estrategia                | Mejor caso | Promedio   | Peor caso |
|---------------------------|------------|------------|-----------|
| Secuencial                | Ω(1)       | Θ(n)       | O(n)      |
| Árbol (BST no balanceado) | Ω(1)       | Θ(log n)   | O(n)      |
| Árbol AVL                 | Ω(1)       | Θ(log n)   | O(log n)  |

La secuencial siempre recorre el catálogo completo cuando busca por coincidencia exacta, es decir Θ(n). El AVL descarta mitades en cada paso, es decir Θ(log n) promedio, y al ser balanceado garantiza O(log n) también en el peor caso.

# Experimento y resultados (TP2/TP3)

Se corre con la opción 10. Genera catálogos de prueba y mide el tiempo de cada estrategia.

| N elementos | Secuencial  | AVL       |
|-------------|-------------|-----------|
| 100         | 0.0084 ms   | 0.0054 ms |
| 1.000       | 0.0649 ms   | 0.0058 ms |
| 10.000      | 0.7615 ms   | 0.0102 ms |

A mayor cantidad de elementos el AVL es notablemente más rápido; la secuencial crece linealmente con N, el árbol prácticamente no.

# Conclusión técnica

El árbol conviene cuando el catálogo es grande y se busca seguido: tarda un poco más en armarse, pero después cada búsqueda es mucho más rápida. La secuencial no se puede eliminar porque es la única que permite autocompletar (coincidencia parcial). Si el catálogo es chico o cambia todo el tiempo, el árbol no aporta ventaja real.

# TP4: El árbol también puede enfermarse

## Objetivo

Investigar qué ocurre cuando un BST pierde el equilibrio, implementar un AVL que lo evite y comparar ambos en casos de desbalance.

## Implementación

- BST común (insertar_bst): inserta sin reequilibrar.
- AVL (insertar_arbol): calcula el factor de equilibrio tras cada inserción y aplica la rotación correspondiente:
  - Izquierda-izquierda: rotación simple a la derecha.
  - Derecha-derecha: rotación simple a la izquierda.
  - Izquierda-derecha: rotación doble (izquierda luego derecha).
  - Derecha-izquierda: rotación doble (derecha luego izquierda).

## Experimento de desbalance (opción 11)

Los títulos se insertaron en orden alfabético, que es el peor caso para un BST común.

| Canciones | Altura BST | Altura AVL | Comparaciones BST | Comparaciones AVL |
|-----------|------------|------------|-------------------|-------------------|
| 100       | 100        | 7          | 100               | 7                 |
| 500       | 500        | 9          | 500               | 9                 |
| 900       | 900        | 10         | 900               | 10                |

Para 900 canciones la altura del AVL fue 10, lo esperado según la teoría (log₂(900) ≈ 9,8).

## Resultados

El BST común se desbalanceó por completo: su altura coincidió con la cantidad de canciones y la búsqueda necesitó 900 comparaciones. El AVL mantuvo altura logarítmica y necesitó solo 10 comparaciones para las mismas 900 canciones.

En conclusión, el equilibrio es fundamental para conservar la eficiencia de las búsquedas. El AVL evita que el árbol se degrade hasta comportarse como una lista enlazada. El BST común sigue siendo útil cuando los datos llegan en orden aleatorio o el catálogo es pequeño, ya que no tiene el costo extra de las rotaciones.

## Limitaciones

- Solo se probó inserción en orden ascendente (peor caso). Con inserción aleatoria el BST queda mucho menos desbalanceado.
- El factor de equilibrio se recalcula recorriendo los subárboles en cada inserción. Una mejora posible es guardar la altura en cada nodo para calcularlo en O(1). Por eso la opción 10 (que inserta hasta 10.000 elementos) tarda varios segundos (unos 15 en la prueba realizada).
- Los títulos duplicados no se insertan.

# TP5: Árboles generales (n-arios)

## Objetivo

Representar una jerarquía natural del dominio con un árbol general (cada nodo puede tener cualquier cantidad de hijos) e integrarla a la terminal.

## Jerarquía implementada

    Música
    ├── Rock
    │   ├── Rock nacional
    │   └── Hard rock
    ├── Pop
    │   ├── Pop latino
    │   └── K-pop
    └── Electrónica
        ├── Techno
        └── House

Son 10 categorías en 3 niveles.

## Implementación

- NodoGeneral: nodo con nombre y lista hijos de cualquier tamaño.
- crear_arbol_categorias: arma la jerarquía.
- mostrar_categorias: imprime el árbol indentado (recorrido en preorden con sangría). Se usa desde la opción 4, subopción 2.
- buscar_categoria: búsqueda en profundidad por nombre en cualquier nivel, sin distinguir mayúsculas.

## Complejidad

Con n categorías, la búsqueda y el recorrido son O(n): en el peor caso visitan cada nodo una vez.

## Limitaciones

- La jerarquía está escrita en el código y no está vinculada a los géneros del catálogo: varios géneros reales (por ejemplo Cuarteto o Thrash Metal) no figuran en el árbol.
- buscar_categoria está implementada pero el menú todavía no la usa; la opción 4, subopción 2 solo muestra el árbol.

# TP6: Sistema de recomendaciones mediante Heap Binaria

## Objetivo

Implementar un ranking dinámico de canciones favoritas usando una heap binaria máxima, integrada al sistema real de calificaciones.

## Implementación

La clase HeapRecomendaciones implementa manualmente las operaciones básicas:

- insertar(prioridad, cancion): agrega al final y sube hasta restaurar la propiedad del Max-Heap, con costo O(log n).
- _subir(indice): compara el nodo con su padre y los intercambia mientras el hijo tenga mayor prioridad.
- extraer_maximo(): extrae la raíz (el de mayor prioridad), pone el último elemento en la raíz y baja, con costo O(log n).
- _bajar(indice): compara el nodo con sus dos hijos y lo intercambia con el mayor mientras sea necesario.

La función de prioridad es calcular_prioridad(cancion), que devuelve el mi_puntaje asignado por el usuario (escala 1-10).

## Función obtener_top_N

obtener_top_n(canciones, n=5) inserta todas las canciones calificadas en la heap y extrae las n de mayor prioridad. Se ejecuta desde la opción 5 del menú y muestra el resultado con medallas.

Ejemplo de salida real (el catálogo ya traía Chau con 10 y se calificaron otras cuatro canciones desde la opción 7):

    ===== TOP 5 DE CANCIONES FAVORITAS =====
    1. Chau - Puntaje: 10/10
    2. Bohemian Rhapsody - Puntaje: 9/10
    3. One - Puntaje: 8/10
    4. Nothing Else Matters - Puntaje: 8/10
    5. Get Lucky - Puntaje: 7/10

## Calificación persistente

Al calificar una canción (opción 7), el puntaje se guarda en canciones.json mediante guardar_puntajes(). La próxima vez que se ejecute el programa, cargar_canciones() recupera los puntajes con dato.get(mi_puntaje, 0), por lo que el ranking persiste entre sesiones.

## Comparación Heap vs. Ordenamiento (opción 12)

| Estrategia | Complejidad |
|------------|-------------|
| Heap Top-N | O(n log n) construcción + O(k log n) extracciones |
| Ordenar todo | O(n log n) |

El heap es especialmente útil cuando la colección es grande y se necesita un Top-N pequeño: no hace falta ordenar todo el dataset, solo extraer los k mejores. En conjuntos pequeños, ordenar todo puede ser igual de eficiente o incluso más rápido en la práctica, ya que sorted() de Python está altamente optimizado. Con el catálogo de 151 canciones los dos tiempos son del mismo orden (alrededor de 0,017 ms contra 0,016 ms).

## Justificación de la elección

Se eligió el heap porque permite insertar en O(log n) y extraer el máximo en O(log n). Para obtener los primeros k resultados el costo es O(k log n), una vez construido el heap. Ordenar todo el conjunto requiere O(n log n) independientemente de cuántos resultados se necesiten.

Nota: en la implementación actual el heap se vuelve a construir en cada consulta, por eso el costo total de una consulta es O(n log n + k log n). La ventaja asintótica sobre ordenar aparece si el heap se mantiene armado entre consultas (cada calificación nueva cuesta O(log n)) o si se construye con heapify en O(n).

# TP7: Grafos, conectá las cosas

## Objetivo

Convertir las relaciones del dominio en una red: representar qué canciones están relacionadas entre sí, consultarlas e integrarlo al sistema.

## Modelo del grafo

| Elemento | Decisión | Justificación |
|----------|----------|---------------|
| Vértice | Una canción, identificada por su título | La canción es la unidad que el usuario busca, califica y recibe como recomendación. En el catálogo los 151 títulos son únicos, así que hay 151 vértices. |
| Arista | Dos canciones están conectadas si comparten artista o género | Son relaciones que ya existen en los datos del catálogo y no requieren información extra. Si te gusta una canción, es razonable recomendar otra del mismo artista o del mismo género. |
| Dirección | No dirigido | Comparten artista o género es una relación simétrica: si A se relaciona con B, B se relaciona con A. |
| Peso | No pesado | La relación es binaria (comparten o no comparten). No se mide cuánto se parecen. |

Ejemplo con datos reales (igual que el esquema del enunciado):

    A Este Lado del Camino ---- Nothing Else Matters ---- One
     (No Te Va Gustar, Rock)     (Metallica, Rock)          (Metallica, Thrash Metal)
              mismo género: Rock         mismo artista: Metallica

## Representación: lista de adyacencia

Se implementó como un diccionario que asocia cada título con el conjunto (set) de títulos de sus canciones relacionadas.

Justificación según la densidad del grafo (medida sobre el catálogo real, opción 13, subopción 5):

| Dato | Valor |
|------|-------|
| Vértices (V) | 151 |
| Aristas (E) | 1541 |
| Aristas posibles (V·(V−1)/2) | 11.325 |
| Densidad (E / posibles) | 0,136 (13,6 %) |
| Grado promedio / máximo | 20,4 / 53 |
| Entradas en la lista de adyacencia (2·E) | 3.082 |
| Celdas de una matriz de adyacencia (V²) | 22.801 |

- Con una densidad de 0,136 el grafo es ralo: la lista guarda unas 7,4 veces menos entradas que las celdas de una matriz.
- Recorrer los vecinos de una canción cuesta O(grado) en la lista, contra O(V) de recorrer una fila completa de la matriz.
- Preguntar si dos canciones están conectadas es O(1) con set, igual que en la matriz.
- Agregar una canción nueva solo agrega una clave; en una matriz habría que redimensionarla.
- La matriz convendría si el grafo fuera denso (densidad cercana a 1) o si hiciera falta consultar muchas aristas en bloque. No es el caso.

## Operaciones y complejidad

Sea V la cantidad de canciones, E la cantidad de relaciones y k la cantidad de vecinos de una canción.

| Operación | Complejidad |
|-----------|-------------|
| construir_grafo (compara todos los pares) | O(V²), unos 2 ms con 151 canciones |
| agregar_cancion / conectar | O(1) promedio |
| buscar_relacionadas | O(V + k log k): ubicar el título + ordenar los k vecinos |
| camino_mas_corto (BFS) | O(V + E log V): recorrido en anchura con vecinos ordenados para que el resultado sea siempre el mismo |
| mas_conectadas | O(V log V) |
| estadisticas | O(V) |

## Ejemplos de consultas

Salidas reales del programa con el catálogo del proyecto.

Canciones relacionadas (opción 6, o 13 subopción 2)

    Canciones relacionadas con Get Lucky (1):
    - One More Time

Canción sin relaciones (es la única de su artista y su género)

    Esta canción no tiene relaciones.
(por ejemplo, Billie Jean)

Título que no existe: el programa sugiere (escribiendo nothing else)

    La canción no existe en el grafo.
    ¿Quisiste decir alguna de estas?
      - Nothing Else Matters

Camino más corto entre dos canciones (opción 13 subopción 3, BFS)

    Camino más corto (2 saltos):
    A Este Lado del Camino -> Nothing Else Matters -> One

Dos canciones sin camino (opción 13 subopción 3, entre One y Smells Like Teen Spirit)

    No hay camino entre esas dos canciones.

Canciones más conectadas (opción 13 subopción 4)

    ===== CANCIONES MAS CONECTADAS =====
    1. Nothing Else Matters - 53 relaciones
    2. A Este Lado del Camino - 44 relaciones
    3. Al Fin Estamos Solos - 44 relaciones
    4. Another One Bites the Dust - 44 relaciones
    5. Bohemian Rhapsody - 44 relaciones
(en los empates se ordena alfabéticamente)

Estadísticas del grafo (opción 13, subopción 5)

    ===== ESTADISTICAS DEL GRAFO =====
    Vertices (canciones): 151
    Aristas (relaciones): 1541
    Densidad: 0.136
    Grado promedio: 20.4
    Grado maximo: 53
    Entradas en la lista de adyacencia: 3082 (una matriz usaria 22801 celdas)
    Canciones sin relaciones: 5
      - Billie Jean
      - Losing My Religion
      - Smells Like Teen Spirit
      - Superstition
      - Take Five

## Integración en la terminal

- Opción 6 (Ver canciones relacionadas): consulta directa de las relaciones de una canción.
- Opción 13 (Explorar relaciones entre canciones): submenú con todas las consultas del grafo.
- El grafo se construye una sola vez al iniciar el programa, junto con el AVL, y muestra por pantalla Grafo de canciones: 151 vertices, 1541 aristas. No hace falta reconstruirlo al calificar una canción porque las aristas dependen del artista y del género, no del puntaje.

## Forma del grafo con este catálogo

El grafo tiene 15 componentes conexas (grupos de canciones que se alcanzan entre sí):

- 1 componente grande de 54 canciones: todo el Rock, unido con las canciones de Metallica de otros géneros (Thrash Metal, Heavy Metal, Hard Rock).
- 9 componentes de entre 2 y 20 canciones, cada una de un mismo artista o género (por ejemplo Cuarteto, Cumbia Villera, Dubstep o Daft Punk).
- 5 canciones aisladas, únicas de su artista y género.

La distancia máxima entre dos canciones conectadas es de 2 saltos. Como consecuencia, entre canciones de componentes distintas la consulta de camino más corto responde que no hay camino.

## Limitaciones

- La relación es binaria: no distingue si dos canciones comparten artista, género o ambos, ni mide qué tan relacionadas están. Una mejora posible es un grafo pesado (por ejemplo, un peso mayor por compartir artista que por compartir género).
- El grafo es muy fragmentado (15 componentes). Se podría conectar más sumando otra relación, como la década o el país.
- El vértice se identifica por el título: dos canciones con el mismo título se fusionarían en un solo vértice. En este catálogo los 151 títulos son únicos.
- Los títulos se buscan por coincidencia exacta (sin distinguir mayúsculas); si no hay coincidencia, el programa sugiere títulos que contienen el texto.

# Estado del proyecto

| TP | Contenido | Estado |
|----|-----------|--------|
| TP1 | Objetos y clases | Completo |
| TP2 | Análisis de complejidad, búsqueda secuencial vs árbol | Completo |
| TP3 | Árbol binario de búsqueda (BST), recorridos | Completo |
| TP4 | AVL, rotaciones, comparación contra BST desbalanceado | Completo |
| TP5 | Árbol general (n-ario) de categorías musicales | Completo |
| TP6 | Heap binaria, ranking Top-N, calificación persistente | Completo |
| TP7 | Grafo de canciones relacionadas, consultas y camino más corto | Completo |

Versión actual: 5.0.

Proxima entrega Tp8

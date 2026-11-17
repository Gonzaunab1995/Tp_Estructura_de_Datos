# MusicBox, versión 6.0

Sistema de recomendaciones musicales. Trabajo Práctico Integrador de Estructuras de Datos.

| Versión | Contenido | Trabajos prácticos |
|---------|-----------|--------------------|
| 1.0 | Objetos, clases y análisis de complejidad | TP1, TP2 |
| 2.0 | Árbol binario de búsqueda y AVL | TP3, TP4 |
| 3.0 | Árbol general (n-ario) de categorías integrado a la terminal | TP5 |
| 4.0 | Heap binaria de recomendaciones, calificación persistente y ranking Top-N | TP6 |
| 5.0 | Grafo de canciones relacionadas, consultas y camino más corto (BFS) | TP7 |
| 6.0 | Recorridos del grafo: BFS y DFS, con dos casos de uso y análisis de complejidad | TP8 |

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
13. Explorar relaciones entre canciones (grafo): submenú con nueve consultas: (1) mostrar todas las relaciones, (2) buscar canciones relacionadas, (3) camino más corto entre dos canciones, (4) canciones más conectadas, (5) estadísticas del grafo, (6) canciones por distancia con BFS, (7) exploración en profundidad con DFS, (8) grupos de canciones conectadas con DFS y (9) comparación entre BFS y DFS.

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

# TP8: Recorridos, explorá la red

## Objetivo

Usar recorridos de grafos para responder preguntas reales sobre el catálogo. Se implementan BFS (búsqueda en anchura) y DFS (búsqueda en profundidad) sobre el mismo grafo del TP7, sin cambiar su representación.

## Qué hace cada algoritmo

- BFS visita primero las canciones más cercanas al origen: primero las que están a 1 salto, después las de 2 saltos, y así sucesivamente. Usa una cola (primero en entrar, primero en salir).
- DFS toma una conexión y profundiza todo lo posible antes de retroceder y probar otra. Usa una pila (último en entrar, primero en salir).

En los dos casos se guarda un conjunto de visitados para no recorrer dos veces la misma canción. Los vecinos se visitan en orden alfabético, para que el resultado sea siempre el mismo.

## Casos de uso

| Algoritmo | Pregunta que responde | Dónde se usa |
|-----------|-----------------------|--------------|
| BFS | Qué canciones hay a 1, 2, 3... saltos de una canción dada, y cuál es el camino más corto entre dos canciones | Opción 13, subopciones 6 y 3 |
| DFS | Qué canciones se alcanzan desde una canción explorando en profundidad, y cuántos grupos de canciones conectadas tiene el catálogo | Opción 13, subopciones 7 y 8 |

Por qué BFS en el primer caso: la distancia entre dos canciones es la cantidad de aristas del camino, y BFS descubre cada canción por primera vez con la menor cantidad posible de saltos. Una recomendación a 1 salto es más cercana que una a 2 saltos, y BFS entrega esa información ordenada por niveles.

Por qué DFS en el segundo caso: para saber qué canciones se alcanzan desde una dada alcanza con visitar cada una una vez, y la pila lo resuelve recorriendo hasta el fondo antes de retroceder. Aplicado a todo el catálogo, repetir DFS desde cada canción todavía no visitada separa los grupos de canciones conectadas (componentes conexas). Para solo alcanzar canciones BFS también serviría; DFS es la opción natural cuando importa el recorrido completo de un grupo y no la distancia.

## Implementación

Los tres métodos están en la clase GrafoCanciones:

| Método | Qué devuelve |
|--------|--------------|
| bfs(origen) | Lista de pares (canción, distancia) en el orden en que BFS las visita |
| dfs(origen) | Lista de pares (canción, profundidad) en el orden en que DFS las visita |
| componentes() | Lista de grupos de canciones conectadas, del más grande al más chico, armada llamando a dfs desde cada canción no visitada |

| Estructura | Función |
|------------|---------|
| Lista con índice (cola de BFS) | Canciones pendientes. El índice evita hacer pop(0), que cuesta O(n) |
| Diccionario de distancias | Marca las canciones ya descubiertas y guarda su distancia al origen |
| Lista (pila de DFS) | Pares (canción, profundidad) pendientes, se extrae siempre el último |
| Conjunto de visitados (DFS) | Evita repetir canciones |

En la terminal se muestran con mostrar_niveles (opción 6), mostrar_exploracion (opción 7), mostrar_grupos (opción 8) y comparar_recorridos (opción 9) del submenú 13. Si el título no existe, se sugieren títulos parecidos, igual que en el resto del grafo. Si la canción no tiene relaciones, se informa.

## Ejemplos de ejecución

BFS desde A Este Lado del Camino (salida abreviada: de las 44 canciones a 1 salto solo se muestran las primeras tres):

    Canciones por distancia desde A Este Lado del Camino (BFS):

    A 1 salto (44):
    - Al Fin Estamos Solos
    - Another One Bites the Dust
    - Bohemian Rhapsody

    A 2 saltos (9):
    - Battery
    - Enter Sandman
    - Fade to Black
    - For Whom the Bell Tolls
    - Master of Puppets
    - One
    - Sad But True
    - Seek and Destroy
    - Whiskey in the Jar

Las 9 canciones a 2 saltos son las de Metallica que no son Rock: se llega a ellas a través de Nothing Else Matters, que es Rock y de Metallica a la vez.

DFS desde Get Lucky, un grupo chico de 2 canciones:

    Exploración en profundidad desde Get Lucky (DFS), 1 canción alcanzada:
    - Get Lucky (profundidad 0)
    - One More Time (profundidad 1)

Grupos de canciones conectadas (DFS), primeras líneas:

    Grupos de canciones conectadas (DFS): 15
    1. 54 canciones (por ejemplo: A Este Lado del Camino, Al Fin Estamos Solos, Another One Bites the Dust)
    2. 20 canciones (por ejemplo: Ando Rajao, Chica Sexy, Como Olvidarte)
    3. 10 canciones (por ejemplo: Amerika, Deutschland, Du Hast)

Canción sin relaciones:

    Esta canción no tiene relaciones.

Comparación desde A Este Lado del Camino:

    Comparación de recorridos desde A Este Lado del Camino:
    Canciones alcanzadas por BFS: 53
    Canciones alcanzadas por DFS: 53
    Distancia máxima en BFS: 2
    Profundidad máxima en DFS: 44
    Primeras visitadas por BFS: Al Fin Estamos Solos, Another One Bites the Dust, Bohemian Rhapsody, Buenos Dias Mundo Cruel, Cara de Rusa
    Primeras visitadas por DFS: Al Fin Estamos Solos, Another One Bites the Dust, Bohemian Rhapsody, Buenos Dias Mundo Cruel, Cara de Rusa

Resultado importante: los dos algoritmos alcanzan exactamente las mismas 53 canciones (se verificó para los 151 vértices), pero con una forma distinta. BFS ve el grupo en 2 niveles; DFS lo recorre como una cadena de profundidad 44, porque dentro de un grupo de canciones que comparten género cada canción está conectada con todas las demás y DFS siempre pasa a la primera que todavía no visitó.

Las primeras cinco visitadas coinciden porque dentro de un grupo completo el orden alfabético es el mismo para los dos. Se separan en la canción número 26: BFS sigue con la siguiente canción a 1 salto (Persiana americana), mientras que DFS, al pasar por Nothing Else Matters, se mete enseguida en las canciones de Metallica (Battery) antes de terminar el grupo de Rock.

## Diferencias entre BFS y DFS

| Aspecto | BFS | DFS |
|---------|-----|-----|
| Estructura | Cola | Pila |
| Orden de visita | Por niveles, de lo más cercano a lo más lejano | Hasta el fondo de una rama y después retrocede |
| Camino más corto en aristas | Sí, garantizado | No |
| Memoria | Guarda el nivel actual: en el peor caso O(V) | Guarda la rama actual y los vecinos pendientes: en el peor caso O(E) |
| Uso típico | Distancias, recomendaciones por cercanía, camino mínimo | Exploración completa, componentes conexas, detectar ciclos |
| En MusicBox | Opciones 13.6 y 13.3 | Opciones 13.7 y 13.8 |

## Análisis de complejidad

Sea V la cantidad de canciones y E la cantidad de relaciones. El grafo usa lista de adyacencia.

| Algoritmo | Teórica | En esta implementación | Por qué |
|-----------|---------|------------------------|---------|
| BFS | O(V + E) | O(V + E log V) | Cada canción entra una vez a la cola y se recorre la lista de vecinos de cada una una sola vez. El log V extra viene de ordenar los vecinos con sorted para que el resultado sea siempre el mismo |
| DFS | O(V + E) | O(V + E log V) | Cada canción se visita una vez y cada arista se mira dos veces, una por cada extremo. También ordena los vecinos |
| componentes | O(V + E) | O(V + E log V) | Cada llamada a dfs trabaja solo sobre su grupo, así que entre todas visitan cada canción y cada arista una vez |

- Con matriz de adyacencia ambos pasarían a O(V²), porque para cada canción habría que revisar las V columnas. Por eso la lista de adyacencia es la representación correcta para este grafo ralo (densidad 0,136).
- En DFS la pila puede guardar la misma canción varias veces, una por cada vecino que la apiló antes de visitarla. Por eso en el peor caso crece hasta O(E) y no O(V). Se evita repetir el trabajo con el chequeo de visitados al extraer.
- Medición con las 151 canciones, desde A Este Lado del Camino (54 canciones alcanzadas): BFS tarda unos 0,10 ms, DFS unos 0,16 ms y componentes unos 0,33 ms. DFS es algo más lento porque apila vecinos que después descarta por ya estar visitados.

## Cuándo conviene cada uno

- BFS cuando importa la cercanía: camino con menos saltos, recomendaciones por distancia, o cualquier pregunta del tipo cuál es lo más cercano.
- DFS cuando importa recorrer todo un grupo: separar componentes conexas, explorar a fondo, o problemas que necesitan retroceder (ciclos, orden de dependencias).
- Si solo hay que saber si una canción es alcanzable desde otra, ambos sirven y cuestan lo mismo.

## Limitaciones

- DFS está implementado de forma iterativa con pila propia, no recursiva, así que no depende del límite de recursión de Python. A cambio, el orden de visita es el de una pila, que puede diferir del de una versión recursiva.
- Como los grupos de canciones son casi completos (todas se conectan con todas), DFS arma cadenas largas y la profundidad no refleja distancia real. Para medir cercanía hay que usar BFS.
- camino_mas_corto (TP7) y bfs repiten parte de la lógica. camino_mas_corto corta apenas encuentra el destino y bfs recorre todo lo alcanzable.
- Los resultados dependen de la relación elegida (artista o género). Con otra relación o un grafo pesado, BFS dejaría de dar el camino de menor costo y habría que usar Dijkstra.

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
| TP8 | Recorridos del grafo: BFS y DFS, casos de uso y análisis de complejidad | Completo |

Versión actual: 6.0.

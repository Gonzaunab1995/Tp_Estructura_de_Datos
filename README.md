# MusicBox — versión 4.0

Sistema de recomendaciones musicales — Trabajo Práctico Integrador de Estructuras de Datos.

| Versión | Contenido | Trabajos prácticos |
|---------|-----------|--------------------|
| 1.0 | Objetos, clases y análisis de complejidad | TP1, TP2 |
| 2.0 | Árbol binario de búsqueda y AVL | TP3, TP4 |
| 3.0 | Árbol general (n-ario) de categorías integrado a la terminal | TP5 |
| 4.0 | Heap binaria de recomendaciones, calificación persistente y ranking Top-N | TP6 |

# Descripción

MusicBox permite cargar un catálogo de canciones, listarlas, buscarlas por
título o artista, filtrarlas por género, calificarlas y ver un ranking dinámico
de favoritas, todo desde la terminal. Es un proyecto que va incorporando
árboles, heaps y grafos en sucesivas entregas.

# Estructura del repositorio

```
musicbox/
├── main.py              # clases del dominio + árboles (BST / AVL / general) + heap + interfaz de terminal
├── datos/
│   └── canciones.json   # catálogo de canciones (guarda puntajes)
└── README.md
```

# Requisitos

- Python 3.8 o superior (no requiere instalar librerías externas).

# Cómo ejecutar

1. Cloná o descargá este repositorio.
2. Parate en la carpeta `musicbox/` (la que contiene `main.py`).
3. Ejecutá:

```
python3 main.py
```

4. Vas a ver el menú principal:

```
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
0.  Salir
```

# Funcionalidades actuales

1. **Lista de Temas**: muestra el catálogo completo, sin filtrar.
2. **Buscar por título**: búsqueda parcial, devuelve todas las coincidencias.
3. **Buscar por artista**: muestra todos los temas de un artista o banda.
4. **Explorar por género o categorías**: submenú con dos opciones: (1) listar canciones de un género y (2) explorar el árbol general de categorías.
5. **Ver mi Top de favoritas**: usa la heap para mostrar el ranking de las canciones más calificadas con medallas .
6. **Ver canciones relacionadas**: pendiente.
7. **Calificar canción**: asignás un puntaje del 1 al 10. El puntaje se guarda en `canciones.json` y persiste entre sesiones.
8. **Buscar título exacto con árbol**: búsqueda exacta en el AVL.
9. **Recorrer árbol binario**: inorder, preorder o postorder.
10. **Experimento de complejidad**: compara búsqueda secuencial vs AVL con distintos tamaños de entrada.
11. **Comparar BST común vs. AVL**: experimento de desbalance con títulos insertados en orden alfabético.
12. **Comparar Heap vs. ordenamiento**: mide el tiempo de obtener el Top-N con heap versus ordenar todo el catálogo.

# Modelo de clases

- `Artista`: nombre y país.
- `Genero`: nombre del género musical.
- `Album`: título, año y el `Artista` al que pertenece.
- `Cancion`: título, `Artista`, `Album`, `Genero`, duración en segundos y puntaje personal. Incluye el método `calificar()` y el setter `mi_puntaje`.
- `NodoArbol`: nodo del árbol binario (BST / AVL) que almacena una `Cancion` con referencias a izquierda y derecha.
- `NodoGeneral`: nodo del árbol general (n-ario) con nombre y lista de hijos. Se usa para la jerarquía de categorías del TP5.
- `HeapRecomendaciones`: heap binaria máxima implementada manualmente. Almacena pares `(prioridad, cancion)` y garantiza que el elemento de mayor prioridad siempre está en la raíz.

# Búsqueda por título: dos estrategias

- `buscar_por_titulo`: recorrido secuencial, coincidencia parcial (autocompletar).
- `buscar_en_arbol`: árbol AVL ordenado por título, coincidencia exacta, O(log n) promedio.

# Análisis de complejidad

| Estrategia                | Mejor caso | Promedio   | Peor caso |
|---------------------------|------------|------------|-----------|
| Secuencial                | Ω(1)       | Θ(n)       | O(n)      |
| Árbol (BST no balanceado) | Ω(1)       | Θ(log n)   | O(n)      |
| Árbol AVL                 | Ω(1)       | Θ(log n)   | O(log n)  |

La secuencial siempre recorre el catálogo completo cuando busca por coincidencia exacta → Θ(n). El AVL descarta mitades en cada paso → Θ(log n) promedio, y al ser balanceado garantiza O(log n) también en el peor caso.

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

- **BST común** (`insertar_bst`): inserta sin reequilibrar.
- **AVL** (`insertar_arbol`): calcula el factor de equilibrio tras cada inserción y aplica la rotación correspondiente:
  - **Izquierda-izquierda:** rotación simple a la derecha.
  - **Derecha-derecha:** rotación simple a la izquierda.
  - **Izquierda-derecha:** rotación doble (izquierda luego derecha).
  - **Derecha-izquierda:** rotación doble (derecha luego izquierda).

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
- El factor de equilibrio se recalcula recorriendo los subárboles. Una mejora posible es guardar la altura en cada nodo para calcularlo en O(1).
- Los títulos duplicados no se insertan.

# TP5: Árboles generales (n-arios)

## Objetivo

Representar una jerarquía natural del dominio con un árbol general (cada nodo puede tener cualquier cantidad de hijos) e integrarla a la terminal.

## Jerarquía elegida

```
Música
├── Rock
│   ├── Alternative Rock
│   ├── Funk Rock
│   ├── Grunge
│   └── Hard Rock
├── Metal
│   ├── Heavy Metal
│   ├── Thrash Metal
│   ├── Nu Metal
│   └── Industrial Metal
├── Pop
│   └── Pop Latino
├── Música popular argentina
│   ├── Folclore
│   ├── Chacarera
│   ├── Cuarteto
│   └── Cumbia Villera
├── Electrónica
│   ├── Dubstep
│   └── House
└── Jazz y Funk
    ├── Jazz
    └── Funk
```

## Complejidad

Con `n` categorías, la búsqueda y todos los recorridos son O(n): en el peor caso visitan cada nodo una vez.

# TP6: Sistema de recomendaciones mediante Heap Binaria

## Objetivo

Implementar un ranking dinámico de canciones favoritas usando una heap binaria máxima, integrada al sistema real de calificaciones.

## Implementación

La clase `HeapRecomendaciones` implementa manualmente las operaciones básicas:

- `insertar(prioridad, cancion)`: agrega al final y sube hasta restaurar la propiedad del Max-Heap → O(log n).
- `_subir(indice)`: compara el nodo con su padre y los intercambia mientras el hijo tenga mayor prioridad.
- `extraer_maximo()`: extrae la raíz (el de mayor prioridad), pone el último elemento en la raíz y baja → O(log n).
- `_bajar(indice)`: compara el nodo con sus dos hijos y lo intercambia con el mayor mientras sea necesario.

La función de prioridad es `calcular_prioridad(cancion)`, que devuelve el `mi_puntaje` asignado por el usuario (escala 1-10).

## Función obtener_top_N

`obtener_top_n(canciones, n=5)` inserta todas las canciones calificadas en la heap y extrae las `n` de mayor prioridad. Se ejecuta desde la opción 5 del menú y muestra el resultado con medallas:

```
===== TOP 5 DE CANCIONES FAVORITAS =====
 Bohemian Rhapsody - Puntaje: 10/10
 Master of Puppets - Puntaje: 9/10
 Californication - Puntaje: 8/10
4. One - Puntaje: 7/10
5. Battery - Puntaje: 7/10
```

## Calificación persistente

Al calificar una canción (opción 7), el puntaje se guarda en `canciones.json` mediante `guardar_puntajes()`. La próxima vez que se ejecute el programa, `cargar_canciones()` recupera los puntajes con `dato.get("mi_puntaje", 0)`, por lo que el ranking persiste entre sesiones.

## Comparación Heap vs. Ordenamiento (opción 12)

| Estrategia | Complejidad |
|------------|-------------|
| Heap Top-N | O(n log n) construcción + O(k log n) extracciones |
| Ordenar todo | O(n log n) |

El heap es especialmente útil cuando la colección es grande y se necesita un Top-N pequeño: no hace falta ordenar todo el dataset, solo extraer los `k` mejores. En conjuntos pequeños, ordenar todo puede ser igual de eficiente o incluso más rápido en la práctica, ya que `sorted()` de Python está altamente optimizado.

## Justificación de la elección

Se eligió el heap porque permite insertar en O(log n) y extraer el máximo en O(log n). Para obtener los primeros `k` resultados el costo es O(k log n), una vez construido el heap. Ordenar todo el conjunto requiere O(n log n) independientemente de cuántos resultados se necesiten. Cuando `k` es mucho menor que `n`, el heap gana claramente.

# Estado del proyecto

| TP | Contenido |
|----|-----------|
| TP1 | Objetos y clases 
| TP2 | Análisis de complejidad, búsqueda secuencial vs árbol 
| TP3 | Árbol binario de búsqueda (BST), recorridos 
| TP4 | AVL, rotaciones, comparación contra BST desbalanceado 
| TP5 | Árbol general (n-ario) de categorías musicales 
| TP6 | Heap binaria, ranking Top-N, calificación persistente 

Versión actual: 4.0. 
Próxima etapa: grafos.

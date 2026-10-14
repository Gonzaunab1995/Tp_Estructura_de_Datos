# MusicBox

Sistema de recomendaciones musicales — Trabajo Práctico Integrador de Estructuras de Datos.

# Descripción

MusicBox permite cargar un catálogo de canciones, listarlas, buscarlas por
título o artista, y filtrarlas por género, a través de una interfaz de
terminal. Es un proyecto que va incorporando árboles, heaps y grafos en
sucesivas entregas.

# Estructura del repositorio

```
musicbox/
├── main.py              # clases del dominio + árboles (BST / AVL) + interfaz de terminal
├── datos/
│   └── canciones.json   # catálogo de canciones
└── README.md
```

# Requisitos

- Python 3.8 o superior (no requiere instalar librerías externas).

# Cómo ejecutar

1. Cloná o descargá este repositorio.
2. Parate en la carpeta musicbox/ (la que contiene main.py).
3. Ejecutá:

   ```
   python3 main.py
   ```

4. Vas a ver el menú principal:

   ```
   === MUSICBOX ===
   1. Lista de Temas
   2. Buscar canciones por titulo
   3. Buscar canciones por artista
   4. Explorar por genero
   5. Ver mi Top de favoritas
   6. Ver canciones relacionadas
   7. Calificar cancion
   8. Buscar titulo exacto con arbol
   9. Recorrer arbol binario
   10. Experimento de complejidad
   11. Comparar BST común vs. AVL
   0. Salir
   ```

# Funcionalidades actuales

1. Lista de Temas: muestra el catálogo completo, sin filtrar (cumple la operación "Listar").
2. Buscar canciones por título: te pide el nombre de tu tema preferido o el que buscas en el momento.
3. Buscar canciones por artista: te pide tu artista y muestra todos sus temas correspondientes.
4. Explorar por género: muestra todas las canciones de un género.
5. Ver mi Top de favoritas: pendiente.
6. Ver canciones relacionadas: pendiente.
7. Calificar canción: pendiente.
8. Buscar título exacto con árbol: busca una canción por título exacto en el árbol AVL.
9. Recorrer árbol binario: muestra el árbol en inorder, preorder o postorder.
10. Experimento de complejidad: compara búsqueda secuencial vs búsqueda en árbol con distintos tamaños de entrada (ver sección de abajo).
11. Comparar BST común vs. AVL: experimento de desbalance con títulos insertados en orden alfabético (ver sección TP4).

# Modelo de clases

- Artista: nombre y país.
- Genero: nombre del género musical.
- Album: título, año y el `Artista` al que pertenece.
- Cancion: título, Artista, Album, `Genero` y duración en segundos.
- NodoArbol: nodo de un árbol binario de búsqueda que almacena una Cancion, con referencias a izquierda y derecha. Se usa para indexar el catálogo por título, tanto en el BST común como en el AVL.

# Búsqueda por título: dos estrategias

Operación crítica: buscar canción por título. Implementada de dos formas
sobre el mismo catálogo:

- buscar_por_titulo: recorrido secuencial, coincidencia parcial (sirve para
  autocompletar).
- buscar_en_arbol + insertar_arbol: árbol ordenado por título, coincidencia
  exacta. Desde el TP4, `insertar_arbol` es un AVL que se rebalancea solo.

# Análisis de complejidad

| Estrategia                | Mejor caso | Promedio | Peor caso |
|---------------------------|------------|----------|-----------|
| Secuencial                | Θ(n)       | Θ(n)     | Θ(n)      |
| Árbol (BST no balanceado) | Ω(1)       | Θ(log n) | O(n)      |
| Árbol AVL                 | Ω(1)       | Θ(log n) | O(log n)  |

La secuencial siempre recorre las canciones (no corta, puede haber varias
coincidencias parciales), por eso mejor y peor caso coinciden en Θ(n). El
árbol descarta la mitad del subárbol en cada paso → Θ(log n) promedio, pero
como el BST común (`insertar_bst`) no rebalancea, un árbol degenerado (títulos
insertados ya ordenados) cae a O(n). El AVL evita ese caso con rotaciones y
garantiza O(log n) también en el peor caso.

# Experimento y resultados

Se corre con la opción 10 del menú ("experimento_complejidad"), que genera
catálogos de prueba de distinto tamaño y mide el tiempo de cada estrategia.

| N elementos | Secuencial  | Árbol     |
|-------------|-------------|-----------|
| 100         | 0.0084 ms   | 0.0054 ms |
| 1.000       | 0.0649 ms   | 0.0058 ms |
| 10.000      | 0.7615 ms   | 0.0102 ms |

A mayor cantidad de elementos ,el Árbol va ser mas rapido ; la secuencial crece
linealmente con "N" cantidad de elmentos, el árbol prácticamente no.

# Conclusión técnica

El árbol te conviene cuando tenés muchas canciones y buscás seguido: tarda un poco más en armarse, pero después cada búsqueda es mucho más rápida, así que vale la pena. La secuencial no se puede sacar del medio porque es la única que permite autocompletar (buscar por coincidencia parcial), cosa que el árbol no hace. Y si el catálogo es chico o cambia todo el tiempo, no tiene sentido complicarse con el árbol: como un BST común no se rebalancea, se puede terminar degenerando y rindiendo igual (o peor) que la secuencial. Eso se resuelve con el AVL implementado en el TP4 (ver sección siguiente).

# TP4: El árbol también puede enfermarse

## Objetivo

Investigar qué ocurre cuando un árbol binario de búsqueda (BST) pierde el equilibrio, implementar un árbol AVL que lo evite y comparar ambos en casos de desbalance.

## Implementación

- **BST común** (`insertar_bst`): inserta cada título según su orden alfabético (sin distinguir mayúsculas) y no realiza ningún reequilibrio.
- **AVL** (`insertar_arbol`): después de cada inserción calcula el factor de equilibrio (altura izquierda − altura derecha) de cada nodo del camino. Si queda fuera del rango [-1, 1], aplica la rotación correspondiente:
  - **Izquierda-izquierda:** rotación simple a la derecha.
  - **Derecha-derecha:** rotación simple a la izquierda.
  - **Izquierda-derecha:** rotación doble (izquierda y luego derecha).
  - **Derecha-izquierda:** rotación doble (derecha y luego izquierda).

## Experimento de desbalance

Se generaron conjuntos de 100, 500 y 900 canciones sintéticas (se usaron datos generados para poder escalar la cantidad de elementos). Los títulos se insertaron en **orden alfabético**, que es el peor caso para un BST común. Luego se buscó el último título insertado, que es el que más comparaciones exige en el BST. Se ejecuta desde la opción 11 del menú.

| Canciones | Altura BST | Altura AVL | Comparaciones BST | Comparaciones AVL |
|-----------|------------|------------|-------------------|-------------------|
| 100       | 100        | 7          | 100               | 7                 |
| 500       | 500        | 9          | 500               | 9                 |
| 900       | 900        | 10         | 900               | 10                |

Para 900 canciones la altura del AVL fue 10, lo esperado según la teoría, ya que log₂(900) ≈ 9,8.

## Limitaciones

- Solo se probó el orden ascendente, que es el peor caso. Con inserción aleatoria, el BST común queda mucho menos desbalanceado.
- La inserción del AVL es más costosa que la búsqueda, porque el factor de equilibrio se calcula recorriendo los subárboles. Una mejora posible es guardar la altura en cada nodo.
- Los títulos duplicados no se insertan en el árbol.


## Resultados del experimento: BST común vs. AVL

Se comparó un árbol binario de búsqueda común (BST) con un árbol AVL utilizando conjuntos de 100, 500 y 900 canciones cuyos títulos se insertaron en orden alfabético.

Los resultados mostraron que el BST común se desbalanceó por completo: su altura coincidió con la cantidad de canciones. Para 900 canciones, la búsqueda del título seleccionado necesitó 900 comparaciones.

En cambio, el AVL mantuvo una altura reducida gracias a las rotaciones de equilibrio. Para las mismas 900 canciones, la búsqueda necesitó solamente 10 comparaciones.

Esto demuestra que el orden de inserción puede afectar considerablemente el rendimiento de un BST común. En el peor caso, la búsqueda en un BST desbalanceado tiene complejidad O(n), mientras que en un AVL la búsqueda tiene complejidad O(log n), debido a que el árbol mantiene una altura logarítmica.

En conclusión, el equilibrio es fundamental para conservar la eficiencia de las búsquedas cuando aumenta la cantidad de elementos. El AVL evita que el árbol se degrade hasta comportarse como una lista enlazada.

# Estado del proyecto

TP1 (Objetos y clases)
TP2 (análisis de complejidad)
TP3 (árbol binario de búsqueda) 
TP4 (AVL y comparación contra BST común) completos.
A continuacion tp5...
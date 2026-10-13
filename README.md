# MusicBox

Sistema de recomendaciones musicales — Trabajo Práctico Integrador de Estructuras de Datos.

## Descripción

MusicBox permite cargar un catálogo de canciones, listarlas, buscarlas por
título o artista, filtrarlas por género, calificarlas y ver un ranking de favoritas,
todo desde la terminal. Es un proyecto que va incorporando árboles, heaps y grafos en
sucesivas entregas.

## Estructura del repositorio

```
musicbox/
├── main.py              # clases del dominio + árbol BST + interfaz de terminal
├── datos/
│   └── canciones.json   # catálogo de canciones
└── README.md
```

## Requisitos

- Python 3.8 o superior (no requiere instalar librerías externas).

## Cómo ejecutar

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
1.  Lista de temas
2.  Buscar por título (parcial)
3.  Buscar por artista
4.  Explorar por género
5.  Ver mis favoritas
6.  Calificar canción
7.  Buscar título exacto (árbol BST)
8.  Recorrer árbol binario
9.  Experimento de complejidad
0.  Salir
```

## Funcionalidades actuales

1. Lista de temas: muestra el catálogo completo con título, artista, género, año y duración.
2. Buscar por título (parcial): buscás escribiendo cualquier parte del nombre, devuelve todas las coincidencias.
3. Buscar por artista: mostrá todos los temas de un artista o banda.
4. Explorar por género: filtrá el catálogo por género musical.
5. Ver mis favoritas: muestra las canciones que calificaste, ordenadas de mayor a menor puntaje.
6. Calificar canción: le das un puntaje del 1 al 5 a cualquier tema del catálogo. Si hay varias coincidencias te deja elegir cuál.
7. Buscar título exacto (árbol BST): búsqueda exacta usando el árbol binario, más rápida que la secuencial para catálogos grandes.
8. Recorrer árbol binario: recorre el árbol en inorder (alfabético), preorder o postorder.
9. Experimento de complejidad: genera catálogos de prueba y compara los tiempos de búsqueda secuencial vs árbol BST.

## Modelo de clases

- Artista: nombre y país.
- Genero: nombre del género musical.
- Album: título, año y el Artista al que pertenece.
- Cancion: título, Artista, Album, Genero, duración en segundos y puntaje personal.
- NodoArbol: nodo del árbol binario de búsqueda (BST). Guarda una Cancion y referencias a los nodos izquierdo y derecho. El árbol se ordena por título para hacer búsquedas exactas rápidas.

## Árbol binario de búsqueda (TP3)

La clave de ordenamiento elegida es el título, porque es la operación de búsqueda más
frecuente del sistema. Ordenar por año o rating también sería válido, pero no resolvería
la necesidad principal.

El árbol se construye al iniciar el programa con construir_arbol(), que primero
mezcla las canciones aleatoriamente antes de insertarlas. Esto evita que el árbol
se degenere en una lista cuando los datos vienen ordenados del JSON.

### Funciones del árbol

- insertar_arbol(raiz, cancion): inserción recursiva por título.
- buscar_en_arbol(raiz, titulo): búsqueda exacta en O(log n) promedio.
- recorrido_inorder(raiz): devuelve las canciones ordenadas alfabéticamente.
- recorrido_preorder(raiz): raíz → izquierda → derecha.
- recorrido_postorder(raiz): izquierda → derecha → raíz.

## Búsqueda por título: dos estrategias

Operación crítica: buscar canción por título exacto. Implementada de dos formas:

- buscar_por_titulo: recorrido secuencial, coincidencia parcial (sirve para autocompletar).
- buscar_en_arbol: BST ordenado por título, coincidencia exacta, mucho más rápido en catálogos grandes.

Ambas conviven porque cubren necesidades distintas: la secuencial para autocompletar,
el árbol para búsqueda directa.

## Análisis de complejidad

| Estrategia                | Mejor caso | Promedio   | Peor caso |
|---------------------------|------------|------------|-----------|
| Secuencial                | Ω(1)       | Θ(n)       | O(n)      |
| Árbol (BST no balanceado) | Ω(1)       | Θ(log n)   | O(n)      |

La secuencial en la práctica siempre recorre todo el catálogo cuando se usa para
búsqueda exacta, por eso se comporta como Θ(n). El árbol descarta la mitad del
subárbol en cada paso, lo que lo lleva a Θ(log n) en promedio. El peor caso de
ambos es O(n): en la secuencial cuando el elemento no existe, en el árbol cuando
está degenerado (se resuelve con el shuffle al construirlo).

## Experimento y resultados

Se corre con la opción 9 del menú. Genera catálogos de prueba de distinto tamaño,
fuerza el peor caso buscando siempre el último elemento, y mide el tiempo de cada
estrategia.

| N elementos | Secuencial  | Árbol      |
|-------------|-------------|------------|
| 100         | 0.0084 ms   | 0.0054 ms  |
| 1.000       | 0.0649 ms   | 0.0058 ms  |
| 10.000      | 0.7615 ms   | 0.0102 ms  |
| 100.000     | 10.7458 ms  | 0.0152 ms  |

A mayor cantidad de elementos el árbol es notablemente más rápido. La secuencial
crece linealmente con N, el árbol prácticamente no.

## Conclusión técnica

El árbol vale la pena cuando el catálogo es grande y se busca seguido por título exacto:
tarda un poco más en armarse al inicio, pero después cada búsqueda es mucho más rápida.
La búsqueda secuencial no se puede eliminar porque es la única que permite autocompletar
(coincidencia parcial), cosa que el árbol no hace.

Si el catálogo es chico o cambia todo el tiempo, no tiene sentido complicarse con el árbol.
Como el BST no se rebalancea, si los datos se insertan en orden puede degenerarse y rendir
igual que la secuencial — eso se resuelve mezclando las canciones antes de insertar, que es
lo que hace construir_arbol(). A futuro se podría mejorar con un AVL para garantizar el
balance sin depender del orden de inserción.

## Estado del proyecto

- TP1: objetos y clases (Artista, Genero, Album, Cancion).
- TP2: análisis de complejidad, comparación de estrategias de búsqueda.
- TP3: árbol binario de búsqueda, recorridos, integración al menú, calificación y favoritas. (ok)
- Próxima etapa:  código AVL, experimentos de desbalance, comparación, conclusión técnica.

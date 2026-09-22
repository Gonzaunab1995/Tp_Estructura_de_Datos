# MusicBox

Sistema de recomendaciones musicales — Trabajo Práctico Integrador de Estructuras de Datos.

# Descripción

MusicBox permite cargar un catálogo de canciones, listarlas, buscarlas por
título o artista, y filtrarlas por género, a través de una interfaz de
terminal. Es un proyecto que va incorporando árboles, heaps y grafos en
sucesivas entregas.

# Estructura del repositorio


musicbox/
├── main.py              # clases del dominio + interfaz de terminal
├── datos/
│   └── canciones.json   # catálogo de canciones
└── README.md


# Requisitos

- Python 3.8 o superior (no requiere instalar librerías externas).

# Cómo ejecutar

1. Cloná o descargá este repositorio.
2. Parate en la carpeta musicbox/ (la que contiene main.py).
3. Ejecutá:

   
   python3 main.py
   

4. Vas a ver el menú principal:

   
   === MUSICBOX ===
   1. Lista de Temas
   2. Buscar canciones por titulo
   3. Buscar canciones por artista
   4. Explorar por genero
   5. Ver mi Top de favoritas
   6. Ver canciones relacionadas
   7. Calificar cancion
   8. Experimento de complejidad
   0. Salir
   

# Funcionalidades actuales

1. Lista de Temas: muestra el catálogo completo, sin filtrar (cumple la operación "Listar").
2. Buscar canciones por título: te pide el nombre de tu tema preferido o el que buscas en el momento.
3. Buscar canciones por artista: te pide tu artista y muestra todos sus temas correspondientes.
4. Explorar por género: muestra todas las canciones de un género.
5. Ver mi Top de favoritas: pendiente.
6. Ver canciones relacionadas: pendiente.
7. Calificar canción: pendiente.
8. Experimento de complejidad: compara búsqueda secuencial vs búsqueda en árbol con distintos tamaños de entrada (ver sección  de abajo).

# Modelo de clases

- Artista: nombre y país.
- Genero: nombre del género musical.
- Album: título, año y el Artista` al que pertenece.
- Cancion: título, Artista, Album, Genero` y duración en segundos.
- NodoArbol: nodo de un árbol binario de búsqueda (BST) que almacena una Cancion, con referencias a izquierda y     derecha. Se usa para indexar el catálogo por título.

# Búsqueda por título: dos estrategias

Operación crítica: buscar canción por título. Implementada de dos formas
sobre el mismo catálogo:

- buscar_por_titulo: recorrido secuencial, coincidencia parcial (sirve para
  autocompletar).
- buscar_en_arbol + insertar_arbol: BST ordenado por título, coincidencia
  exacta.

# Análisis de complejidad

| Estrategia                | Mejor caso | Promedio | Peor caso |

| Secuencial                | Θ(n)       | Θ(n)     | Θ(n)      |
| Árbol (BST no balanceado) | Ω(1)       | Θ(log n) | O(n)      |

La secuencial siempre recorre las canciones (no corta, puede haber varias
coincidencias parciales), por eso mejor y peor caso coinciden en Θ(n). El
árbol descarta la mitad del subárbol en cada paso → Θ(log n) promedio, pero
como "insertar_arbol" no rebalancea, un árbol degenerado (títulos insertados
ya ordenados) cae a O(n).

# Experimento y resultados

Se corre con la opción 8 del menú ("experimento_complejidad"), que genera
catálogos de prueba de distinto tamaño y mide el tiempo de cada estrategia.

| N elementos | Secuencial  | Árbol     |

| 100         | 0.0084 ms   | 0.0054 ms |
| 1.000       | 0.0649 ms   | 0.0058 ms |
| 10.000      | 0.7615 ms   | 0.0102 ms |
| 100.000     | 10.7458 ms  | 0.0152 ms |

A mayor cantidad de elementos ,el Árbol va ser mas rapido ; la secuencial crece
linealmente con "N" cantidad de elmentos, el árbol prácticamente no.

# Conclusión técnica

El árbol te conviene cuando tenés muchas canciones y buscás seguido: tarda un poco más en armarse, pero después cada búsqueda es mucho más rápida, así que vale la pena. La secuencial no se puede sacar del medio porque es la única que permite autocompletar (buscar por coincidencia parcial), cosa que el árbol no hace. Y si el catálogo es chico o cambia todo el tiempo, no tiene sentido complicarse con el árbol: como no se rebalancea, se puede terminar degenerando y rindiendo igual (o peor) que la secuencial. Eso se podría resolver más adelante con un AVL.

# Estado del proyecto

TP1 (Objetos y clases) y TP2 (análisis de complejidad, comparación de
estrategias de búsqueda) completos. Próxima etapa: tp3 Árbol binario de búsqueda

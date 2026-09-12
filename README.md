# MusicBox

Sistema de recomendaciones musicales — Trabajo Práctico Integrador de Estructuras de Datos.

## Descripción

MusicBox permite cargar un catálogo de canciones, listarlas, buscarlas por
título o artista, y filtrarlas por género, a través de una interfaz de
terminal. Es la primera etapa (TP1) de un proyecto que va incorporando
árboles, heaps y grafos en las siguientes entregas.

## Estructura del repositorio

```
musicbox/
├── main.py              # clases del dominio + interfaz de terminal
├── datos/
│   └── canciones.json   # catálogo de canciones (datos de prueba)
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
   === MUSICBOX ===
   1. Lista de Temas
   2. Buscar canciones por titulo
   3. Buscar canciones por artista
   4. Explorar por genero
   5. Ver mi Top de favoritas
   6. Ver canciones relacionadas
   7. Calificar cancion
   0. Salir

## Funcionalidades actuales

1. Lista de Temas: muestra el catálogo completo, sin filtrar (cumple la operación "Listar").
2. Buscar canciones por título:Te pide el nombre de tu tema preferido o el que buscas en el momento.
3. Buscar canciones por artista: Te pide a tu artista y muestra todos sus temas correspondientes-
4. Explorar por género: muestra todas las canciones de un género
5. Ver mi Top de favoritas: pendiente
6. Ver canciones relacionadas: pendiente
7. Calificar canción: pendiente
## Modelo de clases

- `Artista`: nombre y país.
- `Genero`: nombre del género musical.
- `Album`: título, año y el `Artista` al que pertenece.
- `Cancion`: título, `Artista`, `Album`, `Genero` y duración en segundos.



## Estado del proyecto

En desarrollo — TP1 (Objetos y clases) completo. Próxima etapa: TP2
(análisis de complejidad, comparación de estrategias de búsqueda).

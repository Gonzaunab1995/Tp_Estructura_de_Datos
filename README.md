# Tp_Estructura_de_Datos
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
   1. Listar canciones
   2. Buscar canciones (titulo o artista)
   3. Filtrar por genero
   0. Salir
   ```

## Funcionalidades actuales (TP1)

- **Listar**: muestra todas las canciones cargadas del catálogo.
- **Buscar**: busca coincidencias parciales por título o por nombre de artista.
- **Filtrar**: muestra todas las canciones de un género dado.

## Modelo de clases

- `Artista`: nombre y país.
- `Genero`: nombre del género musical.
- `Album`: título, año y el `Artista` al que pertenece.
- `Cancion`: título, `Artista`, `Album`, `Genero` y duración en segundos.



## Estado del proyecto

En desarrollo — TP1 (Objetos y clases) completo. Próxima etapa: TP2
(análisis de complejidad, comparación de estrategias de búsqueda).

import json
import os
import time
import random

RUTA_DATOS = os.path.join("datos", "canciones.json")


# ---------------------------------------------------------------------------
# CLASES DEL DOMINIO
# ---------------------------------------------------------------------------

class Artista:
    def __init__(self, nombre, pais):
        self._nombre = nombre
        self._pais = pais

    @property
    def nombre(self):
        return self._nombre

    @property
    def pais(self):
        return self._pais

    def __repr__(self):
        return self._nombre


class Genero:
    def __init__(self, nombre):
        self._nombre = nombre

    @property
    def nombre(self):
        return self._nombre

    def __repr__(self):
        return self._nombre


class Album:
    def __init__(self, titulo, anio, artista):
        self._titulo = titulo
        self._anio = anio
        self._artista = artista

    @property
    def titulo(self):
        return self._titulo

    @property
    def anio(self):
        return self._anio

    @property
    def artista(self):
        return self._artista

    def __repr__(self):
        return f"{self._titulo} ({self._anio})"


class Cancion:
    def __init__(self, titulo, artista, album, genero, duracion):
        self._titulo = titulo
        self._artista = artista
        self._album = album
        self._genero = genero
        self._duracion = duracion
        self._mi_puntaje = 0

    @property
    def titulo(self):
        return self._titulo

    @property
    def artista(self):
        return self._artista

    @property
    def album(self):
        return self._album

    @property
    def genero(self):
        return self._genero

    @property
    def duracion(self):
        return self._duracion

    @property
    def mi_puntaje(self):
        return self._mi_puntaje

    @mi_puntaje.setter
    def mi_puntaje(self, valor):
        self._mi_puntaje = valor

    def __repr__(self):
        estrellas = "★" * self._mi_puntaje + "☆" * (5 - self._mi_puntaje)
        return (
            f"{self._titulo} - {self._artista.nombre} ({self._artista.pais}) "
            f"({self._genero.nombre}, {self._album.anio}) "
            f"[{self._duracion}s] {estrellas}"
        )


# ---------------------------------------------------------------------------
# ÁRBOL BINARIO DE BÚSQUEDA (BST por título)
# ---------------------------------------------------------------------------

class NodoArbol:
    def __init__(self, cancion):
        self.cancion = cancion
        self.izquierda = None
        self.derecha = None


def insertar_arbol(raiz, cancion):
    if raiz is None:
        return NodoArbol(cancion)

    titulo_nuevo = cancion.titulo.casefold()
    titulo_actual = raiz.cancion.titulo.casefold()

    if titulo_nuevo < titulo_actual:
        raiz.izquierda = insertar_arbol(raiz.izquierda, cancion)
    else:
        raiz.derecha = insertar_arbol(raiz.derecha, cancion)

    return raiz


def buscar_en_arbol(raiz, titulo):
    if raiz is None:
        return None

    titulo_buscado = titulo.casefold()
    titulo_actual = raiz.cancion.titulo.casefold()

    if titulo_buscado == titulo_actual:
        return raiz.cancion

    if titulo_buscado < titulo_actual:
        return buscar_en_arbol(raiz.izquierda, titulo)

    return buscar_en_arbol(raiz.derecha, titulo)


def recorrido_inorder(raiz, resultado=None):
    """Inorder: devuelve canciones ordenadas alfabéticamente por título."""
    if resultado is None:
        resultado = []
    if raiz is not None:
        recorrido_inorder(raiz.izquierda, resultado)
        resultado.append(raiz.cancion)
        recorrido_inorder(raiz.derecha, resultado)
    return resultado


def recorrido_preorder(raiz, resultado=None):
    """Preorder: raíz → izquierda → derecha."""
    if resultado is None:
        resultado = []
    if raiz is not None:
        resultado.append(raiz.cancion)
        recorrido_preorder(raiz.izquierda, resultado)
        recorrido_preorder(raiz.derecha, resultado)
    return resultado


def recorrido_postorder(raiz, resultado=None):
    """Postorder: izquierda → derecha → raíz."""
    if resultado is None:
        resultado = []
    if raiz is not None:
        recorrido_postorder(raiz.izquierda, resultado)
        recorrido_postorder(raiz.derecha, resultado)
        resultado.append(raiz.cancion)
    return resultado


def construir_arbol(canciones):
    """Construye el BST shuffleando primero para evitar degeneración."""
    shuffled = canciones[:]
    random.shuffle(shuffled)
    raiz = None
    for cancion in shuffled:
        raiz = insertar_arbol(raiz, cancion)
    return raiz


# ---------------------------------------------------------------------------
# CARGA Y BÚSQUEDAS
# ---------------------------------------------------------------------------

def cargar_canciones(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    canciones = []
    for dato in datos:
        artista = Artista(dato["artista"], dato["pais"])
        genero = Genero(dato["genero"])
        album = Album(dato["album"], dato["anio"], artista)
        cancion = Cancion(
            dato["titulo"],
            artista,
            album,
            genero,
            dato["duracion"],
        )
        canciones.append(cancion)

    return canciones


def listar_canciones(canciones):
    return canciones


def buscar_por_titulo(canciones, texto):
    """Búsqueda parcial (autocompletar) — O(n)."""
    texto = texto.casefold()
    return [c for c in canciones if texto in c.titulo.casefold()]


def buscar_por_artista(canciones, texto):
    texto = texto.casefold()
    return [c for c in canciones if texto in c.artista.nombre.casefold()]


def filtrar_por_genero(canciones, genero):
    return [c for c in canciones if c.genero.nombre.casefold() == genero.casefold()]


def buscar_secuencial(canciones, titulo):
    """Búsqueda exacta secuencial — O(n)."""
    titulo = titulo.casefold()
    for cancion in canciones:
        if cancion.titulo.casefold() == titulo:
            return cancion
    return None


def mostrar_resultados(resultados, mensaje_vacio):
    if resultados:
        for cancion in resultados:
            print(cancion)
    else:
        print(mensaje_vacio)


# ---------------------------------------------------------------------------
# CALIFICAR Y FAVORITAS
# ---------------------------------------------------------------------------

def calificar_cancion(canciones):
    texto = input("Nombre del tema a calificar: ")
    resultados = buscar_por_titulo(canciones, texto)

    if not resultados:
        print("No se encontro esa cancion.")
        return

    if len(resultados) > 1:
        print("Se encontraron varias canciones:")
        for i, c in enumerate(resultados):
            print(f"  {i + 1}. {c.titulo} - {c.artista.nombre}")
        try:
            idx = int(input("Elegí el número: ")) - 1
            cancion = resultados[idx]
        except (ValueError, IndexError):
            print("Opción inválida.")
            return
    else:
        cancion = resultados[0]

    try:
        puntaje = int(input(f"Puntaje para '{cancion.titulo}' (1 a 5): "))
        if not 1 <= puntaje <= 5:
            raise ValueError
        cancion.mi_puntaje = puntaje
        print(f"Puntaje guardado: {'★' * puntaje}{'☆' * (5 - puntaje)}")
    except ValueError:
        print("Ingresá un número entre 1 y 5.")


def ver_favoritas(canciones):
    favoritas = [c for c in canciones if c.mi_puntaje > 0]
    if not favoritas:
        print("Todavía no calificaste ninguna cancion.")
        return
    favoritas.sort(key=lambda c: c.mi_puntaje, reverse=True)
    print(f"\n{'Tu top de favoritas':^50}")
    print("-" * 50)
    for c in favoritas:
        print(c)


# ---------------------------------------------------------------------------
# EXPERIMENTO DE COMPLEJIDAD  (bug corregido -La variable del loop pisaba el parametro de la fucion)
# ---------------------------------------------------------------------------

def generar_canciones_prueba(cantidad):
    canciones = []
    for i in range(cantidad):
        artista = Artista("Artista prueba", "Argentina")
        genero = Genero("Pop")
        album = Album("Album prueba", 2026, artista)
        cancion = Cancion(f"Cancion {i}", artista, album, genero, 180)
        canciones.append(cancion)
    random.shuffle(canciones)
    return canciones


def experimento_complejidad():
    tamanios = [100, 1_000, 10_000, 100_000]

    print("\n" + "=" * 70)
    print("EXPERIMENTO DE COMPLEJIDAD")
    print("=" * 70)
    print(
        f"{'N ELEMENTOS':<15}"
        f"{'BÚSQUEDA SECUENCIAL (ms)':<28}"
        f"{'BÚSQUEDA EN ÁRBOL (ms)':<25}"
    )
    print("-" * 70)

    for n in tamanios:
        # Variable local — no pisa la lista real de canciones
        muestra = generar_canciones_prueba(n)

        raiz = None
        for cancion in muestra:
            raiz = insertar_arbol(raiz, cancion)

        # Forzamos peor caso: buscamos el último elemento de la lista
        titulo_objetivo = muestra[-1].titulo

        inicio = time.perf_counter()
        buscar_secuencial(muestra, titulo_objetivo)
        tiempo_secuencial = (time.perf_counter() - inicio) * 1000

        inicio = time.perf_counter()
        buscar_en_arbol(raiz, titulo_objetivo)
        tiempo_arbol = (time.perf_counter() - inicio) * 1000

        print(
            f"{n:<15}"
            f"{tiempo_secuencial:<28.6f}"
            f"{tiempo_arbol:<25.6f}"
        )

    print("""
ANÁLISIS DE COMPLEJIDAD
=======================
Búsqueda secuencial:
  Mejor caso:  Ω(1)  — el elemento está primero
  Promedio:    Θ(n)  — recorre n/2 en media
  Peor caso:   O(n)  — no está o está al final

Búsqueda en árbol BST:
  Mejor caso:  Ω(1)  — la raíz es el elemento
  Promedio:    Θ(log n) — árbol balanceado
  Peor caso:   O(n)  — árbol degenerado (insertado en orden)

CONCLUSIÓN
==========
El árbol es notablemente más rápido a partir de ~1.000 elementos.
La búsqueda secuencial sigue siendo necesaria para búsquedas
parciales (autocompletar). Para evitar degeneración del BST,
las canciones se insertan en orden aleatorio (shuffle previo).
""")


# ---------------------------------------------------------------------------
# MENÚ
# ---------------------------------------------------------------------------

def menu(canciones, raiz):
    while True:
        print("\n" + "-" * 50)
        print("MusicBox".center(50))
        print("-" * 50)
        print("1.  Lista de temas")
        print("2.  Buscar por título (parcial)")
        print("3.  Buscar por artista")
        print("4.  Explorar por género")
        print("5.  Ver mis favoritas")
        print("6.  Calificar canción")
        print("7.  Buscar título exacto (árbol BST)")
        print("8.  Recorrer árbol binario")
        print("9.  Experimento de complejidad")
        print("0.  Salir")

        opcion = input("\nElegí una opción: ").strip()

        if opcion == "1":
            mostrar_resultados(listar_canciones(canciones), "El catálogo está vacío.")

        elif opcion == "2":
            texto = input("¿Qué tema buscás? ")
            mostrar_resultados(buscar_por_titulo(canciones, texto), "No se encontró ese título.")

        elif opcion == "3":
            texto = input("¿Qué artista o banda buscás? ")
            mostrar_resultados(buscar_por_artista(canciones, texto), "No se encontró ese artista.")

        elif opcion == "4":
            genero = input("¿Qué género querés explorar? ")
            mostrar_resultados(
                filtrar_por_genero(canciones, genero),
                "No hay canciones de ese género en el catálogo."
            )

        elif opcion == "5":
            ver_favoritas(canciones)

        elif opcion == "6":
            calificar_cancion(canciones)

        elif opcion == "7":
            titulo = input("Título exacto: ")
            resultado = buscar_en_arbol(raiz, titulo)
            if resultado:
                print("Canción encontrada:")
                print(resultado)
            else:
                print("No se encontró esa canción.")

        elif opcion == "8":
            print("\n1. Inorder  (alfabético)")
            print("2. Preorder (raíz primero)")
            print("3. Postorder (raíz último)")
            recorrido = input("Elegí un recorrido: ").strip()

            if recorrido == "1":
                mostrar_resultados(recorrido_inorder(raiz), "Árbol vacío.")
            elif recorrido == "2":
                mostrar_resultados(recorrido_preorder(raiz), "Árbol vacío.")
            elif recorrido == "3":
                mostrar_resultados(recorrido_postorder(raiz), "Árbol vacío.")
            else:
                print("Opción inválida.")

        elif opcion == "9":
            experimento_complejidad()

        elif opcion == "0":
            print("Gracias por usar MusicBox.")
            break

        else:
            print("Opción inválida.")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    canciones = cargar_canciones(RUTA_DATOS)
    print(f"Canciones cargadas: {len(canciones)}")

    # Construye el BST con shuffle para evitar degeneración
    raiz = construir_arbol(canciones)

    menu(canciones, raiz)


if __name__ == "__main__":
    main()

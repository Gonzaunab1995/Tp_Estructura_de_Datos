import json
import os
import time
import random

RUTA_DATOS = os.path.join("datos", "canciones.json")


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
        return (
            f"{self._titulo} - {self._artista.nombre} ({self._artista.pais}) "
            f"({self._genero.nombre}, {self._album.anio}) "
            f"[{self._duracion}s]"
        )
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

    titulo = titulo.casefold()
    titulo_actual = raiz.cancion.titulo.casefold()

    if titulo == titulo_actual:
        return raiz.cancion

    if titulo < titulo_actual:
        return buscar_en_arbol(raiz.izquierda, titulo)

    return buscar_en_arbol(raiz.derecha, titulo)

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
    texto = texto.casefold()
    return [c for c in canciones if texto in c.titulo.casefold()]


def buscar_por_artista(canciones, texto):
    texto = texto.casefold()
    return [c for c in canciones if texto in c.artista.nombre.casefold()]


def filtrar_por_genero(canciones, genero):
    return [c for c in canciones if c.genero.nombre.casefold() == genero.casefold()]

def generar_canciones_prueba(cantidad):
    canciones = []

    for i in range(cantidad):
        artista = Artista("Artista prueba", "Argentina")
        genero = Genero("Pop")
        album = Album("Album prueba", 2026, artista)

        cancion = Cancion(
            f"Cancion {i}",
            artista,
            album,
            genero,
            180
        )

        canciones.append(cancion)

    random.shuffle(canciones)

    return canciones

def buscar_secuencial(canciones, titulo):
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
def experimento_complejidad(canciones):

    

    exper_prueba = [100, 1000, 10000, 100000]

    print("\n" + "=" * 70)
    print("EXPERIMENTO DE COMPLEJIDAD")
    print("=" * 70)

    print(
        f"{'N ELEMENTOS':<15}"
        f"{'BÚSQUEDA SECUENCIAL':<25}"
        f"{'BÚSQUEDA EN ÁRBOL':<25}"
    )

    print("-" * 70)

    for n in exper_prueba:

        
        canciones = generar_canciones_prueba(n)

        # Creamos el árbol
        raiz = None

        for cancion in canciones:
            raiz = insertar_arbol(raiz, cancion)

        # Buscamos el último elemento
        # para forzar un caso de búsqueda largo
        titulo_objetivo = canciones[-1].titulo

        
        # BÚSQUEDA SECUENCIAL
       
        inicio = time.perf_counter()

        buscar_secuencial(canciones, titulo_objetivo)

        fin = time.perf_counter()

        tiempo_secuencial = (fin - inicio) * 1000

        
        # BÚSQUEDA EN ÁRBOL
        

        inicio = time.perf_counter()

        buscar_en_arbol(raiz, titulo_objetivo)

        fin = time.perf_counter()

        tiempo_arbol = (fin - inicio) * 1000

        # Mostrar resultados

        print(
            f"{n:<15}"
            f"{tiempo_secuencial:<25.6f}"
            f"{tiempo_arbol:<25.6f}"
        )

    print("\nComplejidad teórica:")
    print("Búsqueda secuencial: O(n)")
    print("Búsqueda en árbol:   O(log n) promedio")

def menu(canciones):
    while True:
        print("\n" + "-" * 50)
        print("MusicBox".center(50))
        print("-" * 50)
        print("1. Lista de Temas")
        print("2. Buscar canciones por titulo")
        print("3. Buscar canciones por artista")
        print("4. Explorar por genero")
        print("5. Ver mi Top de favoritas")
        print("6. Ver canciones relacionadas")
        print("7. Calificar cancion")
        print("8. Experimento de complejidad")
        print("0. Salir")

        opcion = input("Elegi una opcion: ")

        if opcion == "1":
            resultados = listar_canciones(canciones)
            mostrar_resultados(resultados, "El catalogo esta vacio.")

        elif opcion == "2":
            texto = input("Que tema buscas? ")
            resultados = buscar_por_titulo(canciones, texto)
            mostrar_resultados(resultados, "No se encontro ese titulo.")

        elif opcion == "3":
            texto = input("Que artista o banda buscas? ")
            resultados = buscar_por_artista(canciones, texto)
            mostrar_resultados(resultados, "No se encontro ese artista.")

        elif opcion == "4":
            genero = input("Que genero queres explorar? ")
            resultados = filtrar_por_genero(canciones, genero)
            mostrar_resultados(resultados, "No hay canciones de ese genero en el catalogo.")

        elif opcion == "5":
            print("Funcion de favoritas.")

        elif opcion == "6":
            print("Funcion de canciones relacionadas.")

        elif opcion == "7":
            print("Funcion de calificacion.")
        elif opcion == "8":
         experimento_complejidad(canciones)

        elif opcion == "0":
            print("Gracias por usar MusicBox.")
            break

        else:
            print("Opcion invalida.")


def main():
    canciones = cargar_canciones(RUTA_DATOS)
    print(f"Canciones cargadas: {len(canciones)}")
    menu(canciones)


if __name__ == "__main__":
    main()
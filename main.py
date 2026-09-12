import json
import os

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


def mostrar_resultados(resultados, mensaje_vacio):
    if resultados:
        for cancion in resultados:
            print(cancion)
    else:
        print(mensaje_vacio)


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

        elif opcion == "0":
            print("Nos vemos la proxima.")
            break

        else:
            print("Opcion invalida.")


def main():
    canciones = cargar_canciones(RUTA_DATOS)
    print(f"Canciones cargadas: {len(canciones)}")
    menu(canciones)


if __name__ == "__main__":
    main()

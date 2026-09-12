import json
import os

RUTA_DATOS = os.path.join("datos", "canciones.json")


# ------------------------- Clases del dominio -------------------------

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

    def __repr__(self):
        return (
            f"{self._titulo} - {self._artista.nombre} "
            f"({self._genero.nombre}, {self._album.anio}) "
            f"[{self._duracion}s]"
        )


# ------------------------- Carga de datos -------------------------

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


# ------------------------- Listar, Buscar, Filtrar -------------------------

def listar_canciones(canciones):
    for cancion in canciones:
        print(cancion)


def buscar_cancion(canciones, texto):
    
    texto = texto.casefold()
    return [
        cancion for cancion in canciones
        if texto in cancion.titulo.casefold()
        or texto in cancion.artista.nombre.casefold()
    ]


def filtrar_por_genero(canciones, genero):
    return [
        cancion for cancion in canciones
        if cancion.genero.nombre.casefold() == genero.casefold()
    ]


# ------------------------- Terminal -------------------------

def menu(canciones):
    while True:
        print("\n=== MUSICBOX ===")
        print("1. Listar canciones")
        print("2. Buscar canciones (titulo o artista)")
        print("3. Filtrar por genero")
        print("0. Salir")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            listar_canciones(canciones)

        elif opcion == "2":
            texto = input("Ingrese titulo o artista: ")
            resultados = buscar_cancion(canciones, texto)
            if resultados:
                for cancion in resultados:
                    print(cancion)
            else:
                print("No se encontraron coincidencias.")

        elif opcion == "3":
            genero = input("Ingrese el genero: ")
            resultados = filtrar_por_genero(canciones, genero)
            if resultados:
                for cancion in resultados:
                    print(cancion)
            else:
                print("No hay canciones de ese genero en el catalogo.")

        elif opcion == "0":
            print("Hasta luego.")
            break

        else:
            print("Opcion incorrecta.")


def main():
    canciones = cargar_canciones(RUTA_DATOS)
    print(f"Canciones cargadas: {len(canciones)}")
    menu(canciones)


if __name__ == "__main__":
    main()

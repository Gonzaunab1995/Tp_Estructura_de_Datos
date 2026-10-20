import json
import os
import time
import random
import unicodedata
from collections import deque

VERSION = "3.0"
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
            f"{self._titulo} - {self._artista.nombre} "
            f"({self._artista.pais}) "
            f"({self._genero.nombre}, {self._album.anio}) "
            f"[{self._duracion}s]"
        )


class NodoArbol:
    def __init__(self, cancion):
        self.cancion = cancion
        self.izquierda = None
        self.derecha = None


class NodoGeneral:
    #Nodo de un arbol general (n-ario): cualquier cantidad de hijos.

    #generos son los generos del catalogo que pertenecen directamente a
    #esta categoria. Si no se indica, se usa el propio nombre.#
    

    def __init__(self, nombre, generos=None):
        self.nombre = nombre
        self.hijos = []
        self.generos = generos if generos is not None else [nombre]

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)
        return hijo



def insertar_arbol(raiz, cancion):
    # Caso base: el lugar está vacío
    if raiz is None:
        return NodoArbol(cancion)

    titulo_nuevo = cancion.titulo.casefold()
    titulo_actual = raiz.cancion.titulo.casefold()

    # Inserción normal de un árbol binario
    if titulo_nuevo < titulo_actual:
        raiz.izquierda = insertar_arbol(
            raiz.izquierda, cancion
        )
    elif titulo_nuevo > titulo_actual:
        raiz.derecha = insertar_arbol(
            raiz.derecha, cancion
        )
    else:
        # No insertar títulos duplicados
        return raiz

    # Calcular el equilibrio del nodo
    equilibrio = factor_equilibrio(raiz)

    # Caso 1: izquierda-izquierda
    if equilibrio > 1:
        if cancion.titulo.casefold() < raiz.izquierda.cancion.titulo.casefold():
            return rotacion_derecha(raiz)

    # Caso 2: derecha-derecha
    if equilibrio < -1:
        if cancion.titulo.casefold() > raiz.derecha.cancion.titulo.casefold():
            return rotacion_izquierda(raiz)

    # Caso 3: izquierda-derecha
    if equilibrio > 1:
        if cancion.titulo.casefold() > raiz.izquierda.cancion.titulo.casefold():
            raiz.izquierda = rotacion_izquierda(raiz.izquierda)
            return rotacion_derecha(raiz)

    # Caso 4: derecha-izquierda
    if equilibrio < -1:
        if cancion.titulo.casefold() < raiz.derecha.cancion.titulo.casefold():
            raiz.derecha = rotacion_derecha(raiz.derecha)
            return rotacion_izquierda(raiz)

    return raiz

def insertar_bst(raiz, cancion):
    nuevo = NodoArbol(cancion)

    if raiz is None:
        return nuevo

    actual = raiz

    while True:
        if cancion.titulo.casefold() < actual.cancion.titulo.casefold():
            if actual.izquierda is None:
                actual.izquierda = nuevo
                break
            actual = actual.izquierda

        elif cancion.titulo.casefold() > actual.cancion.titulo.casefold():
            if actual.derecha is None:
                actual.derecha = nuevo
                break
            actual = actual.derecha

        else:
            break

    return raiz


def buscar_bst(raiz, titulo):
    actual = raiz
    comparaciones = 0

    while actual is not None:
        comparaciones += 1

        if titulo.casefold() == actual.cancion.titulo.casefold():
            return comparaciones

        elif titulo.casefold() < actual.cancion.titulo.casefold():
            actual = actual.izquierda

        else:
            actual = actual.derecha

    return comparaciones

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


def recorrido_inorder(raiz):
    if raiz is not None:
        recorrido_inorder(raiz.izquierda)
        print(raiz.cancion)
        recorrido_inorder(raiz.derecha)


def recorrido_preorder(raiz):
    if raiz is not None:
        print(raiz.cancion)
        recorrido_preorder(raiz.izquierda)
        recorrido_preorder(raiz.derecha)


def recorrido_postorder(raiz):
    if raiz is not None:
        recorrido_postorder(raiz.izquierda)
        recorrido_postorder(raiz.derecha)
        print(raiz.cancion)


def altura(raiz):
    if raiz is None:
        return 0

    return 1 + max(
        altura(raiz.izquierda),
        altura(raiz.derecha)
    )


def factor_equilibrio(raiz):
    if raiz is None:
        return 0

    return (
        altura(raiz.izquierda)
        - altura(raiz.derecha)
    )
def arbol_equilibrado(raiz):
    if raiz is None:
        return True

    equilibrio = factor_equilibrio(raiz)

    if equilibrio < -1 or equilibrio > 1:
        return False

    return (
        arbol_equilibrado(raiz.izquierda)
        and arbol_equilibrado(raiz.derecha)
    )


def rotacion_derecha(y):
    x = y.izquierda
    auxiliar = x.derecha

    x.derecha = y
    y.izquierda = auxiliar

    return x


def rotacion_izquierda(x):
    y = x.derecha
    auxiliar = y.izquierda

    y.izquierda = x
    x.derecha = auxiliar

    return y


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
            dato["duracion"]
        )

        canciones.append(cancion)

    return canciones


def listar_canciones(canciones):
    return canciones


def buscar_por_titulo(canciones, texto):
    texto = texto.casefold()

    return [
        c for c in canciones
        if texto in c.titulo.casefold()
    ]


def buscar_por_artista(canciones, texto):
    texto = texto.casefold()

    return [
        c for c in canciones
        if texto in c.artista.nombre.casefold()
    ]


def filtrar_por_genero(canciones, genero):
    return [
        c for c in canciones
        if c.genero.nombre.casefold() == genero.casefold()
    ]


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
def experimento_desbalance():
    print("\n" + "=" * 75)
    print("COMPARACION: BST COMUN VS AVL")
    print("=" * 75)

    cantidades = [100, 500, 900]

    print(
        f"{'CANCIONES':<12}"
        f"{'ALTURA BST':<15}"
        f"{'ALTURA AVL':<15}"
        f"{'COMPARACIONES BST':<22}"
        f"{'COMPARACIONES AVL':<22}"
    )

    for cantidad in cantidades:
        canciones = generar_canciones_prueba(cantidad)

        # Ordenamos los títulos para provocar el peor caso del BST.
        canciones.sort(key=lambda c: c.titulo.casefold())

        raiz_bst = None
        raiz_avl = None

        for cancion in canciones:
            raiz_bst = insertar_bst(raiz_bst, cancion)
            raiz_avl = insertar_arbol(raiz_avl, cancion)

        # Buscamos el último título insertado.
        titulo_objetivo = canciones[-1].titulo

        comparaciones_bst = buscar_bst(
            raiz_bst, titulo_objetivo
        )

        # La búsqueda AVL existente devuelve la canción o None.
        actual = raiz_avl
        comparaciones_avl = 0

        while actual is not None:
            comparaciones_avl += 1
            titulo_actual = actual.cancion.titulo.casefold()

            if titulo_objetivo.casefold() == titulo_actual:
                break
            elif titulo_objetivo.casefold() < titulo_actual:
                actual = actual.izquierda
            else:
                actual = actual.derecha

        # Altura iterativa: evita problemas con el BST muy profundo.
        def altura_iterativa(raiz):
            if raiz is None:
                return 0

            pila = [(raiz, 1)]
            altura_maxima = 0

            while pila:
                nodo, nivel = pila.pop()
                altura_maxima = max(altura_maxima, nivel)

                if nodo.izquierda is not None:
                    pila.append((nodo.izquierda, nivel + 1))

                if nodo.derecha is not None:
                    pila.append((nodo.derecha, nivel + 1))

            return altura_maxima

        print(
            f"{cantidad:<12}"
            f"{altura_iterativa(raiz_bst):<15}"
            f"{altura_iterativa(raiz_avl):<15}"
            f"{comparaciones_bst:<22}"
            f"{comparaciones_avl:<22}"
        )

    print("\nComplejidad teórica:")
    print("BST común desbalanceado: O(n)")
    print("AVL equilibrado: O(log n)")

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
    cantidades = [100, 1000, 10000]

    print("\n" + "=" * 75)
    print("EXPERIMENTO DE COMPLEJIDAD")
    print("=" * 75)

    print(
        f"{'CANCIONES':<15}"
        f"{'SECUENCIAL (ms)':<25}"
        f"{'AVL (ms)':<20}"
    )

    print("-" * 75)

    for n in cantidades:
        canciones_prueba = generar_canciones_prueba(n)

        # Crear el arbol AVL
        raiz = None

        for cancion in canciones_prueba:
            raiz = insertar_arbol(raiz, cancion)

        # Buscar una cancion existente
        titulo_objetivo = canciones_prueba[-1].titulo

        # Medir busqueda secuencial
        inicio = time.perf_counter()

        buscar_secuencial(canciones_prueba, titulo_objetivo)

        fin = time.perf_counter()
        tiempo_secuencial = (fin - inicio) * 1000

        # Medir busqueda AVL
        inicio = time.perf_counter()

        buscar_en_arbol(raiz, titulo_objetivo)

        fin = time.perf_counter()
        tiempo_avl = (fin - inicio) * 1000

        print(
            f"{n:<15}"
            f"{tiempo_secuencial:<25.6f}"
            f"{tiempo_avl:<20.6f}"
        )

    print("\nComplejidad teorica:")
    print("Busqueda secuencial: O(n)")
    print("Busqueda AVL: O(log n)")

def crear_arbol_categorias():
    #Jerarquia de la musica construida con los generos del catalogo.
    raiz = NodoGeneral("Música", generos=[])

    rock = raiz.agregar_hijo(NodoGeneral("Rock"))
    rock.agregar_hijo(NodoGeneral("Alternative Rock"))
    rock.agregar_hijo(NodoGeneral("Funk Rock"))
    rock.agregar_hijo(NodoGeneral("Grunge"))
    rock.agregar_hijo(NodoGeneral("Hard Rock"))

    metal = raiz.agregar_hijo(NodoGeneral("Metal", generos=[]))
    metal.agregar_hijo(NodoGeneral("Heavy Metal"))
    metal.agregar_hijo(NodoGeneral("Thrash Metal"))
    metal.agregar_hijo(NodoGeneral("Nu Metal"))
    metal.agregar_hijo(NodoGeneral("Industrial Metal"))

    pop = raiz.agregar_hijo(NodoGeneral("Pop"))
    pop.agregar_hijo(NodoGeneral("Pop Latino"))

    argentina = raiz.agregar_hijo(
        NodoGeneral("Música popular argentina", generos=[])
    )
    argentina.agregar_hijo(NodoGeneral("Folclore"))
    argentina.agregar_hijo(NodoGeneral("Chacarera"))
    argentina.agregar_hijo(NodoGeneral("Cuarteto"))
    argentina.agregar_hijo(NodoGeneral("Cumbia Villera"))

    electronica = raiz.agregar_hijo(
        NodoGeneral("Electrónica", generos=[])
    )
    electronica.agregar_hijo(NodoGeneral("Dubstep"))
    electronica.agregar_hijo(NodoGeneral("House"))

    jazz_funk = raiz.agregar_hijo(NodoGeneral("Jazz y Funk", generos=[]))
    jazz_funk.agregar_hijo(NodoGeneral("Jazz"))
    jazz_funk.agregar_hijo(NodoGeneral("Funk"))

    return raiz


def normalizar(texto):
    #Minusculas y sin acentos, para comparar nombres de manera mas sencilla
    texto = unicodedata.normalize("NFD", texto.casefold())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def generos_de_categoria(nodo):
    #Generos del catalogo que pertenecen a la categoria y sus descendientes.
    generos = list(nodo.generos)

    for hijo in nodo.hijos:
        generos.extend(generos_de_categoria(hijo))

    return generos


def agregar_generos_faltantes(raiz, canciones):
    #Cuelga de 'Otros' los generos del catalogo que no estan en el arbol.
    conocidos = {normalizar(g) for g in generos_de_categoria(raiz)}
    faltantes = []

    for cancion in canciones:
        genero = cancion.genero.nombre

        if normalizar(genero) not in conocidos and genero not in faltantes:
            faltantes.append(genero)

    if faltantes:
        otros = raiz.agregar_hijo(NodoGeneral("Otros", generos=[]))

        for genero in faltantes:
            otros.agregar_hijo(NodoGeneral(genero))


def canciones_de_categoria(nodo, canciones):
    #Canciones cuyo genero pertenece a la categoria o a sus subcategorias.
    generos = {normalizar(g) for g in generos_de_categoria(nodo)}

    return [
        c for c in canciones
        if normalizar(c.genero.nombre) in generos
    ]


def mostrar_categorias(nodo, nivel=0):
    #Muestra el arbol indentado (recorrido en preorden).
    if nodo is not None:
        print("  " * nivel + nodo.nombre)

        for hijo in nodo.hijos:
            mostrar_categorias(hijo, nivel + 1)


def buscar_categoria(nodo, nombre):
    #Busca una categoria por nombre en cualquier nivel (sin acentos).
    if nodo is None:
        return None

    if normalizar(nodo.nombre) == normalizar(nombre):
        return nodo

    for hijo in nodo.hijos:
        resultado = buscar_categoria(hijo, nombre)

        if resultado is not None:
            return resultado

    return None


def camino_a_categoria(nodo, nombre):
    #Lista de nombres desde la raiz hasta la categoria, o None.
    if nodo is None:
        return None

    if normalizar(nodo.nombre) == normalizar(nombre):
        return [nodo.nombre]

    for hijo in nodo.hijos:
        camino = camino_a_categoria(hijo, nombre)

        if camino is not None:
            return [nodo.nombre] + camino

    return None


def recorrido_preorden_categorias(nodo):
    #Primero el nodo y despues sus hijos (de arriba hacia abajo).
    if nodo is None:
        return []

    nombres = [nodo.nombre]

    for hijo in nodo.hijos:
        nombres.extend(recorrido_preorden_categorias(hijo))

    return nombres


def recorrido_postorden_categorias(nodo):
    #Primero los hijos y despues el nodo (de abajo hacia arriba).
    if nodo is None:
        return []

    nombres = []

    for hijo in nodo.hijos:
        nombres.extend(recorrido_postorden_categorias(hijo))

    nombres.append(nodo.nombre)

    return nombres


def recorrido_por_niveles_categorias(raiz):
    #Recorrido en anchura (BFS): nivel por nivel, con una cola.
    if raiz is None:
        return []

    niveles = []
    cola = deque([(raiz, 0)])

    while cola:
        nodo, nivel = cola.popleft()

        if nivel == len(niveles):
            niveles.append([])

        niveles[nivel].append(nodo.nombre)

        for hijo in nodo.hijos:
            cola.append((hijo, nivel + 1))

    return niveles


def contar_categorias(nodo):
    if nodo is None:
        return 0

    return 1 + sum(contar_categorias(hijo) for hijo in nodo.hijos)


def mostrar_categoria(nodo, raiz, canciones, maximo=10):
    #Muestra ruta, subcategorias y canciones de una categoria.
    camino = camino_a_categoria(raiz, nodo.nombre)
    print("\nRuta: " + " > ".join(camino))

    if nodo.hijos:
        print("Subcategorias: " + ", ".join(h.nombre for h in nodo.hijos))
    else:
        print("Subcategorias: (ninguna, es una categoria final)")

    resultados = canciones_de_categoria(nodo, canciones)
    print(f"Canciones en esta categoria: {len(resultados)}")

    for cancion in resultados[:maximo]:
        print("  " + str(cancion))

    if len(resultados) > maximo:
        print(f"  ... y {len(resultados) - maximo} mas.")


def menu_categorias(arbol_categorias, canciones):
    while True:
        print("\n--- Explorar categorias ---")
        print("1. Ver el arbol completo")
        print("2. Buscar una categoria")
        print("3. Recorridos del arbol")
        print("0. Volver")

        eleccion = input("Elegi una opcion: ")

        if eleccion == "1":
            print()
            mostrar_categorias(arbol_categorias)
            print(
                f"\nTotal de categorias: "
                f"{contar_categorias(arbol_categorias)}"
            )

        elif eleccion == "2":
            nombre = input("Que categoria buscas? ")
            nodo = buscar_categoria(arbol_categorias, nombre)

            if nodo is not None:
                mostrar_categoria(
                    nodo, arbol_categorias, canciones
                )
            else:
                print("No se encontro esa categoria.")

        elif eleccion == "3":
            print("\n1. Preorden (de arriba hacia abajo)")
            print("2. Postorden (de abajo hacia arriba)")
            print("3. Por niveles (en anchura)")

            recorrido = input("Elegi un recorrido: ")

            if recorrido == "1":
                print(" -> ".join(
                    recorrido_preorden_categorias(arbol_categorias)
                ))
            elif recorrido == "2":
                print(" -> ".join(
                    recorrido_postorden_categorias(arbol_categorias)
                ))
            elif recorrido == "3":
                niveles = recorrido_por_niveles_categorias(
                    arbol_categorias
                )

                for numero, nombres in enumerate(niveles):
                    print(f"Nivel {numero}: " + ", ".join(nombres))
            else:
                print("Opcion invalida.")

        elif eleccion == "0":
            break

        else:
            print("Opcion invalida.")


def menu(canciones, raiz, arbol_categorias):
    while True:
        print("\n" + "-" * 50)
        print(f"MusicBox v{VERSION}".center(50))
        print("-" * 50)
        print("1. Lista de Temas")
        print("2. Buscar canciones por titulo")
        print("3. Buscar canciones por artista")
        print("4. Explorar por genero o categorias")
        print("5. Ver mi Top de favoritas")
        print("6. Ver canciones relacionadas")
        print("7. Calificar cancion")
        print("8. Buscar titulo exacto con arbol")
        print("9. Recorrer arbol binario")
        print("10. Experimento de complejidad")
        print("11. Comparar BST común vs. AVL")
        print("0. Salir")

        opcion = input("Elegi una opcion: ")

        if opcion == "1":
            resultados = listar_canciones(canciones)
            mostrar_resultados(
                resultados, "El catalogo esta vacio."
            )

        elif opcion == "2":
            texto = input("Que tema buscas? ")
            resultados = buscar_por_titulo(canciones, texto)
            mostrar_resultados(
                resultados, "No se encontro ese titulo."
            )

        elif opcion == "3":
            texto = input("Que artista o banda buscas? ")
            resultados = buscar_por_artista(canciones, texto)
            mostrar_resultados(
                resultados, "No se encontro ese artista."
            )

        elif opcion == "4":
            print("\n1. Explorar canciones por genero")
            print("2. Explorar arbol de categorias")

            eleccion = input("Elegi una opcion: ")

            if eleccion == "1":
                genero = input("Que genero queres explorar? ")
                resultados = filtrar_por_genero(canciones, genero)
                mostrar_resultados(
                    resultados,
                    "No hay canciones de ese genero en el catalogo."
                )

            elif eleccion == "2":
                menu_categorias(arbol_categorias, canciones)

            else:
                print("Opcion invalida.")

        elif opcion == "5":
            print("Funcion de favoritas.")

        elif opcion == "6":
            print("Funcion de canciones relacionadas.")

        elif opcion == "7":
            print("Funcion de calificacion.")

        elif opcion == "8":
            titulo = input("Ingresa el titulo exacto: ")
            resultado = buscar_en_arbol(raiz, titulo)

            if resultado is not None:
                print("Cancion encontrada:")
                print(resultado)
            else:
                print("No se encontro esa cancion.")

        elif opcion == "9":
            print("\n1. Inorder")
            print("2. Preorder")
            print("3. Postorder")

            recorrido = input("Elegi un recorrido: ")

            if recorrido == "1":
                recorrido_inorder(raiz)
            elif recorrido == "2":
                recorrido_preorder(raiz)
            elif recorrido == "3":
                recorrido_postorder(raiz)
            else:
                print("Opcion invalida.")

        elif opcion == "10":
            experimento_complejidad(canciones)

        elif opcion == "11":
            experimento_desbalance()

        elif opcion == "0":
            print("Gracias por usar MusicBox.")
            break

        else:
            print("Opcion invalida.")


def main():
    canciones = cargar_canciones(RUTA_DATOS)
    print(f"MusicBox version {VERSION}")
    print(f"Canciones cargadas: {len(canciones)}")

    raiz = None

    for cancion in canciones:
        raiz = insertar_arbol(raiz, cancion)

    print("Altura del arbol:", altura(raiz))
    print("Factor de equilibrio de la raiz:", factor_equilibrio(raiz))
    print("¿Arbol AVL equilibrado?:", arbol_equilibrado(raiz))

    arbol_categorias = crear_arbol_categorias()
    agregar_generos_faltantes(arbol_categorias, canciones)
    print("Categorias cargadas:", contar_categorias(arbol_categorias))

    menu(canciones, raiz, arbol_categorias)


if __name__ == "__main__":
    main()

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

    def calificar(self, puntaje):
        if 1 <= puntaje <= 10:
            self._mi_puntaje = puntaje
            return True
        return False

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


# ---------------------------------------------------------------------------
# ÁRBOL BINARIO (AVL + BST común)
# ---------------------------------------------------------------------------

class NodoArbol:
    def __init__(self, cancion):
        self.cancion = cancion
        self.izquierda = None
        self.derecha = None


# ---------------------------------------------------------------------------
# ÁRBOL GENERAL (n-ario)
# ---------------------------------------------------------------------------

class NodoGeneral:
    def __init__(self, nombre):
        self.nombre = nombre
        self.hijos = []


# ---------------------------------------------------------------------------
# HEAP DE RECOMENDACIONES (TP6)
# ---------------------------------------------------------------------------

class HeapRecomendaciones:
    def __init__(self):
        self.datos = []

    def esta_vacio(self):
        return len(self.datos) == 0

    def insertar(self, prioridad, cancion):
        self.datos.append((prioridad, cancion))
        self._subir(len(self.datos) - 1)

    def _subir(self, indice):
        while indice > 0:
            padre = (indice - 1) // 2
            if self.datos[indice][0] <= self.datos[padre][0]:
                break
            self.datos[indice], self.datos[padre] = (
                self.datos[padre],
                self.datos[indice]
            )
            indice = padre

    def extraer_maximo(self):
        if self.esta_vacio():
            return None
        maximo = self.datos[0]
        ultimo = self.datos.pop()
        if self.datos:
            self.datos[0] = ultimo
            self._bajar(0)
        return maximo

    def _bajar(self, indice):
        cantidad = len(self.datos)
        while True:
            mayor = indice
            izquierda = 2 * indice + 1
            derecha = 2 * indice + 2
            if (
                izquierda < cantidad
                and self.datos[izquierda][0] > self.datos[mayor][0]
            ):
                mayor = izquierda
            if (
                derecha < cantidad
                and self.datos[derecha][0] > self.datos[mayor][0]
            ):
                mayor = derecha
            if mayor == indice:
                break
            self.datos[indice], self.datos[mayor] = (
                self.datos[mayor],
                self.datos[indice]
            )
            indice = mayor


def calcular_prioridad(cancion):
    return cancion.mi_puntaje


def obtener_top_n(canciones, n=5):
    heap = HeapRecomendaciones()
    for cancion in canciones:
        prioridad = calcular_prioridad(cancion)
        if prioridad > 0:
            heap.insertar(prioridad, cancion)
    recomendaciones = []
    while len(recomendaciones) < n and not heap.esta_vacio():
        resultado = heap.extraer_maximo()
        recomendaciones.append(resultado)
    return recomendaciones


def comparar_heap_vs_ordenamiento(canciones, n=5):
    inicio = time.perf_counter()
    top_heap = obtener_top_n(canciones, n)
    tiempo_heap = time.perf_counter() - inicio

    inicio = time.perf_counter()
    canciones_ordenadas = sorted(
        [
            (calcular_prioridad(cancion), cancion)
            for cancion in canciones
            if calcular_prioridad(cancion) > 0
        ],
        key=lambda elemento: elemento[0],
        reverse=True
    )
    top_ordenamiento = canciones_ordenadas[:n]
    tiempo_ordenamiento = time.perf_counter() - inicio

    print("\n===== COMPARACIÓN HEAP VS ORDENAMIENTO =====")
    print(f"Canciones analizadas: {len(canciones)}")
    print(f"Top solicitado: {n}")
    print(f"Tiempo con Heap:       {tiempo_heap * 1000:.6f} ms")
    print(f"Tiempo ordenando todo: {tiempo_ordenamiento * 1000:.6f} ms")

    return top_heap, top_ordenamiento


# ---------------------------------------------------------------------------
# AVL
# ---------------------------------------------------------------------------

def insertar_arbol(raiz, cancion):
    if raiz is None:
        return NodoArbol(cancion)

    titulo_nuevo = cancion.titulo.casefold()
    titulo_actual = raiz.cancion.titulo.casefold()

    if titulo_nuevo < titulo_actual:
        raiz.izquierda = insertar_arbol(raiz.izquierda, cancion)
    elif titulo_nuevo > titulo_actual:
        raiz.derecha = insertar_arbol(raiz.derecha, cancion)
    else:
        return raiz

    equilibrio = factor_equilibrio(raiz)

    if equilibrio > 1:
        if cancion.titulo.casefold() < raiz.izquierda.cancion.titulo.casefold():
            return rotacion_derecha(raiz)

    if equilibrio < -1:
        if cancion.titulo.casefold() > raiz.derecha.cancion.titulo.casefold():
            return rotacion_izquierda(raiz)

    if equilibrio > 1:
        if cancion.titulo.casefold() > raiz.izquierda.cancion.titulo.casefold():
            raiz.izquierda = rotacion_izquierda(raiz.izquierda)
            return rotacion_derecha(raiz)

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
    titulo_buscado = titulo.casefold()
    titulo_actual = raiz.cancion.titulo.casefold()
    if titulo_buscado == titulo_actual:
        return raiz.cancion
    if titulo_buscado < titulo_actual:
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
    return 1 + max(altura(raiz.izquierda), altura(raiz.derecha))


def factor_equilibrio(raiz):
    if raiz is None:
        return 0
    return altura(raiz.izquierda) - altura(raiz.derecha)


def arbol_equilibrado(raiz):
    if raiz is None:
        return True
    equilibrio = factor_equilibrio(raiz)
    if equilibrio < -1 or equilibrio > 1:
        return False
    return arbol_equilibrado(raiz.izquierda) and arbol_equilibrado(raiz.derecha)


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


# ---------------------------------------------------------------------------
# CARGA Y GUARDADO
# ---------------------------------------------------------------------------

def cargar_canciones(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    canciones = []
    for dato in datos:
        artista = Artista(dato["artista"], dato["pais"])
        genero = Genero(dato["genero"])
        album = Album(dato["album"], dato["anio"], artista)
        cancion = Cancion(dato["titulo"], artista, album, genero, dato["duracion"])
        cancion.mi_puntaje = dato.get("mi_puntaje", 0)
        canciones.append(cancion)
    return canciones


def guardar_puntajes(canciones, ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    puntajes = {cancion.titulo: cancion.mi_puntaje for cancion in canciones}
    for dato in datos:
        if dato["titulo"] in puntajes:
            dato["mi_puntaje"] = puntajes[dato["titulo"]]
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)


# ---------------------------------------------------------------------------
# BÚSQUEDAS Y FILTROS
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# ÁRBOL GENERAL DE CATEGORÍAS
# ---------------------------------------------------------------------------

def crear_arbol_categorias():
    raiz = NodoGeneral("Música")

    rock = NodoGeneral("Rock")
    pop = NodoGeneral("Pop")
    electronica = NodoGeneral("Electrónica")

    raiz.hijos.append(rock)
    raiz.hijos.append(pop)
    raiz.hijos.append(electronica)

    rock.hijos.append(NodoGeneral("Rock nacional"))
    rock.hijos.append(NodoGeneral("Hard rock"))

    pop.hijos.append(NodoGeneral("Pop latino"))
    pop.hijos.append(NodoGeneral("K-pop"))

    electronica.hijos.append(NodoGeneral("Techno"))
    electronica.hijos.append(NodoGeneral("House"))

    return raiz


def mostrar_categorias(nodo, nivel=0):
    if nodo is not None:
        print("  " * nivel + nodo.nombre)
        for hijo in nodo.hijos:
            mostrar_categorias(hijo, nivel + 1)


def buscar_categoria(nodo, nombre):
    if nodo is None:
        return None
    if nodo.nombre.lower() == nombre.lower():
        return nodo
    for hijo in nodo.hijos:
        resultado = buscar_categoria(hijo, nombre)
        if resultado is not None:
            return resultado
    return None


# ---------------------------------------------------------------------------
# EXPERIMENTOS
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
        muestra = generar_canciones_prueba(cantidad)
        muestra.sort(key=lambda c: c.titulo.casefold())

        raiz_bst = None
        raiz_avl = None

        for cancion in muestra:
            raiz_bst = insertar_bst(raiz_bst, cancion)
            raiz_avl = insertar_arbol(raiz_avl, cancion)

        titulo_objetivo = muestra[-1].titulo
        comparaciones_bst = buscar_bst(raiz_bst, titulo_objetivo)

        actual = raiz_avl
        comparaciones_avl = 0
        while actual is not None:
            comparaciones_avl += 1
            if titulo_objetivo.casefold() == actual.cancion.titulo.casefold():
                break
            elif titulo_objetivo.casefold() < actual.cancion.titulo.casefold():
                actual = actual.izquierda
            else:
                actual = actual.derecha

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

        raiz = None
        for cancion in canciones_prueba:
            raiz = insertar_arbol(raiz, cancion)

        titulo_objetivo = canciones_prueba[-1].titulo

        inicio = time.perf_counter()
        buscar_secuencial(canciones_prueba, titulo_objetivo)
        tiempo_secuencial = (time.perf_counter() - inicio) * 1000

        inicio = time.perf_counter()
        buscar_en_arbol(raiz, titulo_objetivo)
        tiempo_avl = (time.perf_counter() - inicio) * 1000

        print(f"{n:<15}{tiempo_secuencial:<25.6f}{tiempo_avl:<20.6f}")

    print("\nComplejidad teorica:")
    print("Busqueda secuencial: O(n)")
    print("Busqueda AVL: O(log n)")


# ---------------------------------------------------------------------------
# MENÚ
# ---------------------------------------------------------------------------

def menu(canciones, raiz):
    while True:
        print("\n" + "-" * 50)
        print("MusicBox".center(50))
        print("-" * 50)
        print("1.  Lista de Temas")
        print("2.  Buscar canciones por titulo")
        print("3.  Buscar canciones por artista")
        print("4.  Explorar por genero o categorias")
        print("5.  Ver mi Top de favoritas")
        print("6.  Ver canciones relacionadas")
        print("7.  Calificar cancion")
        print("8.  Buscar titulo exacto con arbol")
        print("9.  Recorrer arbol binario")
        print("10. Experimento de complejidad")
        print("11. Comparar BST común vs. AVL")
        print("12. Comparar Heap vs. ordenamiento")
        print("0.  Salir")

        opcion = input("\nElegi una opcion: ")

        if opcion == "1":
            mostrar_resultados(listar_canciones(canciones), "El catalogo esta vacio.")

        elif opcion == "2":
            texto = input("Que tema buscas? ")
            mostrar_resultados(buscar_por_titulo(canciones, texto), "No se encontro ese titulo.")

        elif opcion == "3":
            texto = input("Que artista o banda buscas? ")
            mostrar_resultados(buscar_por_artista(canciones, texto), "No se encontro ese artista.")

        elif opcion == "4":
            print("\n1. Explorar canciones por genero")
            print("2. Explorar arbol de categorias")
            eleccion = input("Elegi una opcion: ")
            if eleccion == "1":
                genero = input("Que genero queres explorar? ")
                mostrar_resultados(
                    filtrar_por_genero(canciones, genero),
                    "No hay canciones de ese genero en el catalogo."
                )
            elif eleccion == "2":
                arbol_categorias = crear_arbol_categorias()
                mostrar_categorias(arbol_categorias)
            else:
                print("Opcion invalida.")

        elif opcion == "5":
            recomendaciones = obtener_top_n(canciones, 5)
            print("\n===== TOP 5 DE CANCIONES FAVORITAS =====")
            if not recomendaciones:
                print("No hay canciones calificadas todavia.")
            else:
                medallas = ["🥇", "🥈", "🥉"]
                for puesto, resultado in enumerate(recomendaciones, start=1):
                    puntaje, cancion = resultado
                    prefijo = medallas[puesto - 1] if puesto <= 3 else f"{puesto}."
                    print(f"{prefijo} {cancion.titulo} - Puntaje: {puntaje}/10")

        elif opcion == "6":
            print("Funcion de canciones relacionadas.")

        elif opcion == "7":
            titulo = input("Ingrese el titulo de la cancion: ")
            cancion_encontrada = None
            for cancion in canciones:
                if cancion.titulo.lower() == titulo.lower():
                    cancion_encontrada = cancion
                    break
            if cancion_encontrada is None:
                print("No se encontro la cancion.")
            else:
                try:
                    puntaje = int(input("Califique la cancion del 1 al 10: "))
                    if cancion_encontrada.calificar(puntaje):
                        guardar_puntajes(canciones, RUTA_DATOS)
                        print("Cancion calificada y guardada correctamente.")
                    else:
                        print("El puntaje debe estar entre 1 y 10.")
                except ValueError:
                    print("Debe ingresar un numero entero.")

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

        elif opcion == "12":
            comparar_heap_vs_ordenamiento(canciones, 5)

        elif opcion == "0":
            print("Saliendo de MusicBox...")
            break

        else:
            print("Opcion invalida.")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    canciones = cargar_canciones(RUTA_DATOS)
    print(f"Canciones cargadas: {len(canciones)}")

    raiz = None
    for cancion in canciones:
        raiz = insertar_arbol(raiz, cancion)

    print("Altura del arbol:", altura(raiz))
    print("Factor de equilibrio de la raiz:", factor_equilibrio(raiz))
    print("¿Arbol AVL equilibrado?:", arbol_equilibrado(raiz))

    menu(canciones, raiz)


if __name__ == "__main__":
    main()

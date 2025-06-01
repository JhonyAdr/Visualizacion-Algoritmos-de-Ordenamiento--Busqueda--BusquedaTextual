import time

class AlgoritmosBusqueda:
    def __init__(self):
        self.contador_comparaciones = 0

    def establecer_contador_comparaciones(self, valor):
        self.contador_comparaciones = valor

    def obtener_contador_comparaciones(self):
        return self.contador_comparaciones

    def busqueda_lineal(self, conjunto, valor_buscar, dibujar_datos, velocidad):
        self.establecer_contador_comparaciones(0)
        for i in range(len(conjunto)):
            self.contador_comparaciones += 1
            dibujar_datos(conjunto, ['#764AF1' if x == i else '#FF597B' for x in range(len(conjunto))])
            time.sleep(velocidad)
            if conjunto[i] == valor_buscar:
                dibujar_datos(conjunto, ['#019267' if x == i else '#FF597B' for x in range(len(conjunto))])
                return i
        return -1

    def busqueda_binaria(self, conjunto, valor_buscar, dibujar_datos, velocidad):
        self.establecer_contador_comparaciones(0)
        izquierda = 0
        derecha = len(conjunto) - 1

        while izquierda <= derecha:
            self.contador_comparaciones += 1
            medio = (izquierda + derecha) // 2
            
            # Colorear el rango de búsqueda
            colores = ['#FF597B' for _ in range(len(conjunto))]
            for i in range(izquierda, derecha + 1):
                colores[i] = '#764AF1'
            colores[medio] = '#019267'
            dibujar_datos(conjunto, colores)
            time.sleep(velocidad)

            if conjunto[medio] == valor_buscar:
                dibujar_datos(conjunto, ['#019267' if x == medio else '#FF597B' for x in range(len(conjunto))])
                return medio
            elif conjunto[medio] < valor_buscar:
                izquierda = medio + 1
            else:
                derecha = medio - 1

        return -1

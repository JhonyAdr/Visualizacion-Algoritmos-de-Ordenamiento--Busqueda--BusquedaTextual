import time

class AlgoritmosOrdenamiento:
    def __init__(self):
        self.contador_comparaciones = 0

    def establecer_contador_comparaciones(self, valor):
        self.contador_comparaciones = valor

    def obtener_contador_comparaciones(self):
        return self.contador_comparaciones

    def ordenamiento_burbuja(self, conjunto, dibujar_datos, velocidad, bandera_detener):
        self.establecer_contador_comparaciones(0)
        i = 0
        while i < len(conjunto):
            j = 0
            while j < len(conjunto) - i - 1:
                if bandera_detener:
                    time.sleep(0.1)
                    continue
                comparaciones = self.obtener_contador_comparaciones() + 1
                self.establecer_contador_comparaciones(comparaciones)
                if conjunto[j] > conjunto[j + 1]:
                    conjunto[j], conjunto[j + 1] = conjunto[j + 1], conjunto[j]
                    dibujar_datos(conjunto, ['#019267' if c == j or c == j + 1 else '#FF597B' for c in range(len(conjunto))])
                    time.sleep(velocidad)
                j += 1
            i += 1
        dibujar_datos(conjunto, ['#019267' for i in range(len(conjunto))])

    def ordenamiento_rapido(self, conjunto, inicio, fin, dibujar_datos, velocidad):
        comparaciones = 0
        self.establecer_contador_comparaciones(0)
        if inicio < fin:
            pivote, comparaciones = self.particionar(conjunto, inicio, fin, dibujar_datos, velocidad, comparaciones)
            comparaciones_izq = self.ordenamiento_rapido(conjunto, inicio, pivote - 1, dibujar_datos, velocidad)
            comparaciones_der = self.ordenamiento_rapido(conjunto, pivote + 1, fin, dibujar_datos, velocidad)
            comparaciones += comparaciones_izq + comparaciones_der
            self.establecer_contador_comparaciones(comparaciones)
        return self.obtener_contador_comparaciones()

    def particionar(self, conjunto, inicio, fin, dibujar_datos, velocidad, comparaciones):
        pivote = conjunto[fin]
        dibujar_datos(conjunto, self.obtener_colores(len(conjunto), inicio, fin, inicio, inicio))
        time.sleep(velocidad)

        for i in range(inicio, fin):
            comparaciones += 1
            self.establecer_contador_comparaciones(comparaciones + self.obtener_contador_comparaciones())

            if conjunto[i] < pivote:
                dibujar_datos(conjunto, self.obtener_colores(len(conjunto), inicio, fin, inicio, i, True))
                time.sleep(velocidad)

                conjunto[i], conjunto[inicio] = conjunto[inicio], conjunto[i]
                inicio += 1
            dibujar_datos(conjunto, self.obtener_colores(len(conjunto), inicio, fin, inicio, i))
            time.sleep(velocidad)

        dibujar_datos(conjunto, self.obtener_colores(len(conjunto), inicio, fin, inicio, fin, True))
        time.sleep(velocidad)
        conjunto[fin], conjunto[inicio] = conjunto[inicio], conjunto[fin]

        return inicio, self.obtener_contador_comparaciones()

    def obtener_colores(self, n, inicio, fin, s, ci, es_intercambio=False):
        colores = []
        for i in range(n):
            if inicio <= i <= fin:
                colores.append('#FF597B')
            else:
                colores.append('#764AF1')
            if i == fin:
                colores[i] = '#019267'
            elif i == s:
                colores[i] = '#FF597B'
            elif i == ci:
                colores[i] = '#764AF1'
            if es_intercambio:
                if i == s or i == ci:
                    colores[i] = '#019267'
        return colores

    def ordenamiento_seleccion(self, conjunto, dibujar_datos, velocidad):
        self.establecer_contador_comparaciones(0)
        for i in range(len(conjunto)):
            minimo = i
            for j in range(i + 1, len(conjunto)):
                comparaciones = self.obtener_contador_comparaciones() + 1
                self.establecer_contador_comparaciones(comparaciones)
                if conjunto[minimo] > conjunto[j]:
                    minimo = j
                    dibujar_datos(conjunto, ['#764AF1' if c == minimo or c == i else '#FF597B' for c in range(len(conjunto))])
                    time.sleep(velocidad)
            conjunto[i], conjunto[minimo] = conjunto[minimo], conjunto[i]
            dibujar_datos(conjunto, ['#019267' if c == i or c == minimo else '#FF597B' for c in range(len(conjunto))])
            time.sleep(velocidad)
        dibujar_datos(conjunto, ['#019267' for i in range(len(conjunto))])

    def ordenamiento_mezcla(self, conjunto, dibujar_datos, velocidad):
        self.establecer_contador_comparaciones(0)
        self.ordenamiento_mezcla_recursivo(conjunto, 0, len(conjunto) - 1, dibujar_datos, velocidad)

    def ordenamiento_mezcla_recursivo(self, conjunto, izquierda, derecha, dibujar_datos, velocidad):
        if izquierda < derecha:
            medio = (izquierda + derecha) // 2
            self.ordenamiento_mezcla_recursivo(conjunto, izquierda, medio, dibujar_datos, velocidad)
            self.ordenamiento_mezcla_recursivo(conjunto, medio + 1, derecha, dibujar_datos, velocidad)
            self.mezclar(conjunto, izquierda, medio, derecha, dibujar_datos, velocidad)

    def mezclar(self, conjunto, izquierda, medio, derecha, dibujar_datos, velocidad):
        dibujar_datos(conjunto, self.colorear_arreglo(len(conjunto), izquierda, medio, derecha))
        time.sleep(velocidad)
        datos_izquierda = conjunto[izquierda:medio + 1]
        datos_derecha = conjunto[medio + 1:derecha + 1]

        li = ri = 0
        for i in range(izquierda, derecha + 1):
            if li < len(datos_izquierda) and ri < len(datos_derecha):
                comparaciones = self.obtener_contador_comparaciones() + 1
                self.establecer_contador_comparaciones(comparaciones)
                if datos_izquierda[li] <= datos_derecha[ri]:
                    conjunto[i] = datos_izquierda[li]
                    li += 1
                else:
                    conjunto[i] = datos_derecha[ri]
                    ri += 1
            elif li < len(datos_izquierda):
                conjunto[i] = datos_izquierda[li]
                li += 1
            else:
                conjunto[i] = datos_derecha[ri]
                ri += 1

        dibujar_datos(conjunto, ['#019267' if izquierda <= c <= derecha else '#FF597B' for c in range(len(conjunto))])
        time.sleep(velocidad)

    def colorear_arreglo(self, n, izquierda, medio, derecha):
        colores = []
        for i in range(n):
            if izquierda <= i <= derecha:
                if izquierda <= i <= medio:
                    colores.append('#764AF1')
                else:
                    colores.append('#FF597B')
            else:
                colores.append('#ECF2FF')
        return colores

    def ordenamiento_insercion(self, conjunto, dibujar_datos, velocidad):
        self.establecer_contador_comparaciones(0)
        for i in range(1, len(conjunto)):
            clave = conjunto[i]
            j = i - 1
            while j >= 0 and conjunto[j] > clave:
                conjunto[j + 1] = conjunto[j]
                j -= 1
                dibujar_datos(conjunto, ['#019267' if x == j + 1 else '#FF597B' for x in range(len(conjunto))])
                time.sleep(velocidad)
                comparaciones = self.obtener_contador_comparaciones() + 1
                self.establecer_contador_comparaciones(comparaciones)
            conjunto[j + 1] = clave
            dibujar_datos(conjunto, ['#019267' if x == j + 1 else '#FF597B' for x in range(len(conjunto))])
            time.sleep(velocidad)

        dibujar_datos(conjunto, ['#019267' for x in range(len(conjunto))])
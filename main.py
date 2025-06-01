# Bibliotecas necesarias
from tkinter import *
import tkinter.ttk
from algoritmos_ordenamiento import *
import random
import time

root = Tk()
root.title('Visualización de Algoritmos de Ordenamiento y Búsqueda')
root.geometry('1200x800')
root.config(background='#fff')

# Variables globales
conjunto_datos = []
conjunto_original = []  # Nueva variable para mantener el conjunto original
bandera_detener = False
algoritmo_ordenamiento = StringVar()
tipo_grafico = StringVar()
algoritmo_busqueda = StringVar()
texto_buscar = StringVar()
algoritmos = AlgoritmosOrdenamiento()
contador_comparaciones = 0

# Funciones de los botones
def reiniciar_contador():
    global contador_comparaciones
    contador_comparaciones = 0

def incrementar_contador():
    global contador_comparaciones
    contador_comparaciones += 1

def iniciar_ordenamiento():
    global conjunto_datos, bandera_detener
    if not conjunto_datos:
        etiqueta_resultado.config(text="Primero genera un conjunto de datos")
        return

    # Restaurar el conjunto original antes de cada ordenamiento
    conjunto_datos = conjunto_original.copy()
    dibujar_datos(conjunto_datos, ['#FF597B' for _ in range(len(conjunto_datos))])
    root.update()
    time.sleep(velocidad_animacion.get())

    boton_generar.config(state=DISABLED)
    boton_iniciar.config(state=DISABLED)
    boton_detener.config(state=NORMAL)
    boton_reiniciar.config(state=DISABLED)

    if bandera_detener:
        bandera_detener = False
    
    tiempo_inicio = time.time()
    
    if algoritmo_ordenamiento.get() == 'Ordenamiento Burbuja':
        algoritmos.ordenamiento_burbuja(conjunto_datos, dibujar_datos, velocidad_animacion.get(), bandera_detener)
        actualizar_etiquetas(algoritmos.obtener_contador_comparaciones(), 'O(n²)')

    elif algoritmo_ordenamiento.get() == 'Ordenamiento Rápido':
        algoritmos.ordenamiento_rapido(conjunto_datos, 0, len(conjunto_datos) - 1, dibujar_datos, velocidad_animacion.get())
        dibujar_datos(conjunto_datos, ['green' for i in range(len(conjunto_datos))])
        actualizar_etiquetas(algoritmos.obtener_contador_comparaciones(), 'O(n log n)')

    elif algoritmo_ordenamiento.get() == 'Ordenamiento por Inserción':
        algoritmos.ordenamiento_insercion(conjunto_datos, dibujar_datos, velocidad_animacion.get())
        actualizar_etiquetas(algoritmos.obtener_contador_comparaciones(), 'O(n²)')

    elif algoritmo_ordenamiento.get() == 'Ordenamiento por Selección':
        algoritmos.ordenamiento_seleccion(conjunto_datos, dibujar_datos, velocidad_animacion.get())
        actualizar_etiquetas(algoritmos.obtener_contador_comparaciones(), 'O(n²)')

    elif algoritmo_ordenamiento.get() == 'Ordenamiento por Mezcla':
        algoritmos.ordenamiento_mezcla(conjunto_datos, dibujar_datos, velocidad_animacion.get())
        dibujar_datos(conjunto_datos, ['green' for i in range(len(conjunto_datos))])
        actualizar_etiquetas(algoritmos.obtener_contador_comparaciones(), 'O(n log n)')

    tiempo_fin = time.time()
    tiempo_ejecucion = tiempo_fin - tiempo_inicio
    etiqueta_tiempo.config(text=f"Tiempo de ejecución: {tiempo_ejecucion:.3f} segundos")

    boton_generar.config(state=NORMAL)
    boton_iniciar.config(state=NORMAL)
    boton_detener.config(state=DISABLED)
    boton_reiniciar.config(state=NORMAL)

def reiniciar():
    global conjunto_datos, conjunto_original, bandera_detener, contador_comparaciones
    conjunto_datos = []
    conjunto_original = []
    bandera_detener = False
    contador_comparaciones = 0
    etiqueta_comparaciones.config(text="")
    etiqueta_complejidad.config(text="")
    etiqueta_tiempo.config(text="")
    etiqueta_resultado.config(text="")
    dibujar_datos(conjunto_datos, [])

def dibujar_datos(conjunto, colores):
    if tipo_grafico.get() == 'Barras':
        canvas.delete('all')
        altura_canvas = 380
        ancho_canvas = 700
        ancho_x = ancho_canvas / (len(conjunto) + 1)
        offset = 30
        espacio_entre = 5
        datos = [i / max(conjunto) for i in conjunto]

        for i, h in enumerate(datos):
            x0 = i * ancho_x + offset + espacio_entre
            y0 = altura_canvas - h * 320
            x1 = (i + 1) * ancho_x + offset
            y1 = altura_canvas

            canvas.create_rectangle(x0, y0, x1, y1, fill=colores[i])
            canvas.create_text(x0 + 2, y0, anchor=SW, text=str(conjunto[i]))

    elif tipo_grafico.get() == 'Líneas':
        canvas.delete('all')
        altura_canvas = 380
        ancho_canvas = 700
        ancho_x = ancho_canvas / (len(conjunto) + 1)
        offset = 30
        datos = [i / max(conjunto) for i in conjunto]

        for i, h in enumerate(datos):
            x = i * ancho_x + offset
            y = altura_canvas - h * 320

            canvas.create_line(x, altura_canvas, x, y, fill=colores[i], width=2)
            canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=colores[i])
            canvas.create_text(x + 5, y - 5, anchor=SW, text=str(conjunto[i]))

    elif tipo_grafico.get() == 'Puntos':
        canvas.delete('all')
        altura_canvas = 380
        ancho_canvas = 700
        ancho_x = ancho_canvas / (len(conjunto) + 1)
        offset = 30
        datos = [i / max(conjunto) for i in conjunto]

        for i, h in enumerate(datos):
            x = i * ancho_x + offset
            y = altura_canvas - h * 320

            canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=colores[i])
            canvas.create_text(x + 5, y - 5, anchor=SW, text=str(conjunto[i]))

    root.update_idletasks()

def generar_conjunto():
    global conjunto_datos, conjunto_original
    valor_min = int(escala_valor_min.get())
    valor_max = int(escala_valor_max.get())
    tamano_datos = int(escala_tamano.get())

    conjunto_datos = []
    for i in range(tamano_datos):
        conjunto_datos.append(random.randrange(valor_min, valor_max + 1))
    
    # Guardar una copia del conjunto original
    conjunto_original = conjunto_datos.copy()
    dibujar_datos(conjunto_datos, ['#FF597B' for i in range(len(conjunto_datos))])

def procesar_entrada():
    global conjunto_datos, conjunto_original
    entrada_usuario = entrada.get()
    array = [int(x) for x in entrada_usuario.split(",")]
    conjunto_datos = []
    for i in array:
        conjunto_datos.append(i)
    
    # Guardar una copia del conjunto original
    conjunto_original = conjunto_datos.copy()
    dibujar_datos(conjunto_datos, ['#FF597B' for i in range(len(conjunto_datos))])
    entrada.delete(0, END)

def actualizar_etiquetas(contador_comparaciones, complejidad):
    etiqueta_comparaciones.config(text=f"Número de comparaciones: {contador_comparaciones}")
    etiqueta_complejidad.config(text=f"Complejidad del algoritmo: {complejidad}")

def iniciar_busqueda():
    global conjunto_datos, bandera_detener, contador_comparaciones
    if not conjunto_datos:
        etiqueta_resultado.config(text="Primero genera un conjunto de datos")
        return

    if algoritmo_busqueda.get() == 'Seleccione un algoritmo':
        etiqueta_resultado.config(text="Seleccione un algoritmo de búsqueda")
        return

    try:
        valor_buscar = int(entrada_buscar.get()) if entrada_buscar.get() else conjunto_datos[0]
    except ValueError:
        etiqueta_resultado.config(text="Por favor ingrese un número válido")
        return

    # Deshabilitar botones durante la búsqueda
    boton_generar.config(state=DISABLED)
    boton_buscar.config(state=DISABLED)
    boton_iniciar.config(state=DISABLED)
    boton_detener.config(state=NORMAL)
    boton_reiniciar.config(state=DISABLED)

    bandera_detener = False
    tiempo_inicio = time.time()

    try:
        # Ordenar el conjunto antes de buscar
        conjunto_ordenado = sorted(conjunto_datos)
        dibujar_datos(conjunto_ordenado, ['#FF597B' for _ in range(len(conjunto_ordenado))])
        root.update()
        time.sleep(velocidad_animacion.get())

        if algoritmo_busqueda.get() == 'Búsqueda Lineal':
            posicion = busqueda_lineal(conjunto_ordenado, valor_buscar)
            actualizar_etiquetas(contador_comparaciones, 'O(n)')
        elif algoritmo_busqueda.get() == 'Búsqueda Binaria':
            posicion = busqueda_binaria(conjunto_ordenado, valor_buscar)
            actualizar_etiquetas(contador_comparaciones, 'O(log n)')

        tiempo_fin = time.time()
        tiempo_ejecucion = tiempo_fin - tiempo_inicio
        etiqueta_tiempo.config(text=f"Tiempo de ejecución: {tiempo_ejecucion:.3f} segundos")
        
        if posicion != -1:
            etiqueta_resultado.config(text=f"Valor encontrado en la posición: {posicion}")
            colores = ['#FF597B' for _ in range(len(conjunto_ordenado))]
            colores[posicion] = 'green'
            dibujar_datos(conjunto_ordenado, colores)
        else:
            etiqueta_resultado.config(text="Valor no encontrado")
            dibujar_datos(conjunto_ordenado, ['#FF597B' for _ in range(len(conjunto_ordenado))])

    except Exception as e:
        etiqueta_resultado.config(text=f"Error durante la búsqueda: {str(e)}")
    finally:
        # Restaurar estado de los botones
        boton_generar.config(state=NORMAL)
        boton_buscar.config(state=NORMAL)
        boton_iniciar.config(state=NORMAL)
        boton_detener.config(state=DISABLED)
        boton_reiniciar.config(state=NORMAL)

def busqueda_lineal(conjunto, valor):
    reiniciar_contador()
    for i in range(len(conjunto)):
        if bandera_detener:
            return -1
            
        incrementar_contador()
        colores = ['#FF597B' for _ in range(len(conjunto))]
        colores[i] = 'yellow'
        dibujar_datos(conjunto, colores)
        root.update()
        time.sleep(velocidad_animacion.get())
        
        if conjunto[i] == valor:
            return i
    return -1

def busqueda_binaria(conjunto, valor):
    reiniciar_contador()
    izquierda = 0
    derecha = len(conjunto) - 1
    
    while izquierda <= derecha:
        if bandera_detener:
            return -1
            
        incrementar_contador()
        medio = (izquierda + derecha) // 2
        
        colores = ['#FF597B' for _ in range(len(conjunto))]
        for i in range(izquierda, derecha + 1):
            colores[i] = 'yellow'
        colores[medio] = 'orange'
        dibujar_datos(conjunto, colores)
        root.update()
        time.sleep(velocidad_animacion.get())
        
        if conjunto[medio] == valor:
            return medio
        elif conjunto[medio] < valor:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    
    return -1

def detener_ordenamiento():
    global bandera_detener
    bandera_detener = True

# Configuración de la interfaz gráfica
marco_lateral = Frame(root, width=220, height=230, background='#ECF2FF')
marco_lateral.grid(row=0, column=0, rowspan=3, sticky='ns')

encabezado = Frame(root, width=820, height=130, background='#F3F1F5', padx=0, pady=0)
encabezado.grid(row=0, column=1, padx=0, pady=5, columnspan=1)

etiqueta_comparaciones = Label(encabezado, text="", bg='#fff', font=('consolas', 12, "bold"), pady=8)
etiqueta_comparaciones.pack()

etiqueta_complejidad = Label(encabezado, text="", bg='#fff', font=('consolas', 12, "bold"), pady=8)
etiqueta_complejidad.pack()

etiqueta_tiempo = Label(encabezado, text="", bg='#fff', font=('consolas', 12, "bold"), pady=8)
etiqueta_tiempo.pack()

etiqueta_resultado = Label(encabezado, text="", bg='#fff', font=('consolas', 12, "bold"), pady=8)
etiqueta_resultado.pack()

canvas = Canvas(root, width=820, height=480, background='#fff')
canvas.grid(row=1, column=1, padx=0, pady=5, columnspan=1)

# Controles de ordenamiento
Label(marco_lateral, text="Algoritmos de Ordenamiento", bg='#ECF2FF', font=('consolas', 12, "bold")).grid(row=0, column=0, padx=5, pady=5)

algoritmos_ordenamiento = tkinter.ttk.Combobox(marco_lateral, values=[
    'Seleccione un algoritmo',
    'Ordenamiento Burbuja',
    'Ordenamiento Rápido',
    'Ordenamiento por Inserción',
    'Ordenamiento por Selección',
    'Ordenamiento por Mezcla'
], textvariable=algoritmo_ordenamiento)
algoritmos_ordenamiento.grid(row=1, column=0, padx=5, pady=5)
algoritmos_ordenamiento.current(0)

# Controles de búsqueda
Label(marco_lateral, text="Algoritmos de Búsqueda", bg='#ECF2FF', font=('consolas', 12, "bold")).grid(row=2, column=0, padx=5, pady=5)

algoritmos_busqueda = tkinter.ttk.Combobox(marco_lateral, values=[
    'Seleccione un algoritmo',
    'Búsqueda Lineal',
    'Búsqueda Binaria'
], textvariable=algoritmo_busqueda)
algoritmos_busqueda.grid(row=3, column=0, padx=5, pady=5)
algoritmos_busqueda.current(0)

Label(marco_lateral, text="Valor a buscar:", bg='#ECF2FF', font=('consolas', 10)).grid(row=4, column=0, padx=5, pady=5)
entrada_buscar = Entry(marco_lateral, width=20)
entrada_buscar.grid(row=5, column=0, padx=5, pady=5)

boton_buscar = Button(marco_lateral, text='Buscar', command=iniciar_busqueda, 
                     bg='#019267', fg='white', height=1, width=20)
boton_buscar.grid(row=6, column=0, padx=5, pady=5)

tipo_visualizacion = tkinter.ttk.Combobox(marco_lateral, values=[
    'Tipo de Visualización',
    'Barras',
    'Puntos',
    'Líneas'
], textvariable=tipo_grafico)
tipo_visualizacion.grid(row=7, column=0, padx=5, pady=5)
tipo_visualizacion.current(0)

escala_tamano = Scale(marco_lateral, from_=3, to=50, resolution=1, orient=HORIZONTAL, 
                     label="Tamaño del Conjunto", background='#fff', length=150)
escala_tamano.grid(row=8, column=0, padx=5, pady=5, sticky=W)

escala_valor_min = Scale(marco_lateral, from_=1, to=100, resolution=1, orient=HORIZONTAL, 
                        label="Valor Mínimo", background='#fff', length=150)
escala_valor_min.grid(row=9, column=0, padx=5, pady=5, sticky=W)

escala_valor_max = Scale(marco_lateral, from_=100, to=1000, resolution=1, orient=HORIZONTAL, 
                        label="Valor Máximo", background='#fff', length=150)
escala_valor_max.grid(row=10, column=0, padx=5, pady=5, sticky=W)

velocidad_animacion = Scale(marco_lateral, from_=0.1, to=5.0, length=150, digits=2, resolution=0.1, 
                          orient=HORIZONTAL, label='Velocidad (seg)', background='#fff')
velocidad_animacion.grid(row=11, column=0, padx=5, pady=5, sticky=W)

boton_generar = Button(marco_lateral, text='Generar Conjunto', command=generar_conjunto, 
                      bg='#764AF1', fg='white', width=20)
boton_generar.grid(row=12, column=0, padx=5, pady=5)

boton_iniciar = Button(marco_lateral, text='Iniciar', command=iniciar_ordenamiento, 
                      bg='#019267', fg='white', height=1, width=20)
boton_iniciar.grid(row=13, column=0, padx=5, pady=5)

boton_reiniciar = Button(marco_lateral, text='Reiniciar', command=reiniciar, 
                        bg='#FF597B', fg='white', height=1, width=20)
boton_reiniciar.grid(row=14, column=0, padx=5, pady=5)

boton_detener = Button(marco_lateral, text='Detener', command=detener_ordenamiento, 
                      bg='orange', fg='white', height=1, width=20, state=DISABLED)
boton_detener.grid(row=15, column=0, padx=5, pady=5)

Label(marco_lateral, text="---------O---------", bg='#ECF2FF', font=('consolas', 10, "bold")).grid(row=16, column=0, padx=5, pady=5)
Label(marco_lateral, text="Ingrese números (,)", bg='#ECF2FF', font=('consolas', 10, "bold")).grid(row=17, column=0, padx=5, pady=5)

entrada = Entry(marco_lateral, width=25)
entrada.grid(row=18, column=0, padx=5, pady=5)

boton_procesar = Button(marco_lateral, text="Procesar Entrada", height=1, width=20,
                       fg='#fff', bg='purple', command=procesar_entrada)
boton_procesar.grid(row=19, column=0, padx=5, pady=5)

# Iniciar el bucle principal de la aplicación
root.mainloop()
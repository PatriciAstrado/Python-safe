import numpy as np  # Importamos Numpy

puntos_paralelogramo = []  # Puntos del paralelogramo

# MENU PRINCIPAL


def main():
    print("---.---.---.---.---.---.---.---")
    print("     Rotacion, Traslacion      ")
    print("             de                ")
    print("      Un Paralelogramo         ")
    print("---.---.---.---.---.---.---.---")

    try:
        # Paso 1: Solicita al usuario la cantidad de puntos del paralelogramo (debe ser 4 o 5)
        cantidad_puntos = int(
            input("Ingrese la cantidad de puntos del paralelogramo de 4-5 puntos: "))
        # Paso 2: Verifica que la cantidad de puntos sea válida
        while cantidad_puntos < 4 or cantidad_puntos > 5:
            print("[!] Cantidad Inválida")
            cantidad_puntos = int(input("Cantidad de Puntos: "))
        # Paso 3: Llama a la función para obtener los puntos del paralelogramo
        obtenerPuntos(cantidad_puntos)
        while True:
            try:
                # Paso 4: Llama a la función para mostrar las opciones de transformación
                mostrar_opciones(cantidad_puntos)
            except Exception as e:
                # Maneja cualquier error que ocurra durante las transformaciones
                print(
                    f"[ERROR] Ha ocurrido un error en las transformaciones: {e}")
    except ValueError:
        # Maneja el error si la entrada del usuario no es un número entero
        print("[ERROR] Cantidad de puntos debe ser un número entero.")
    except Exception as ex:
        # Maneja cualquier otro error inesperado
        print(f"[ERROR] {ex}")


def obtenerPuntos(cantidad_puntos):
    # Bucle para ingresar las coordenadas de cada punto
    for p in range(cantidad_puntos):
        print(f"\n|----    Datos Punto {p+1} ----|")
        # Paso 1: Solicita al usuario la coordenada X del punto
        cord_x = float(input("Coordenada X: "))
        # Paso 2: Solicita al usuario la coordenada Y del punto
        cord_y = float(input("Coordenada Y: "))
        # Paso 3: Agrega las coordenadas del punto a la lista puntos_paralelogramo
        puntos_paralelogramo.append([cord_x, cord_y])
        # Muestra un mensaje de confirmación
        print(f"Punto {p+1} Agregado!")
    # Muestra los puntos ingresados
    print("\nPuntos Ingresados: ")
    for i in range(cantidad_puntos):
        print(
            f"P{i+1}: [{puntos_paralelogramo[i][0]}, {puntos_paralelogramo[i][1]}]")


def mostrar_opciones(cantidad_puntos):
    opt = 0
    print("\n--- Opciones ---")
    print("[1] Rotacion\n[2] Traslacion\n[3] Sesgado\n[4] Rotacion desde Punto Arbitrario\n[5] Salir")
    opt = int(input("Opcion: "))
    while opt < 1 or opt > 5:
        opt = int(input("Opcion: "))
    print("")
    if opt == 1:
        mostrar_rotacion(cantidad_puntos)
    elif opt == 2:
        mostrar_traslacion(cantidad_puntos)
    elif opt == 3:
        mostrar_sesgado(cantidad_puntos)
    elif opt == 4:
        mostrar_rotacion_desde_punto(cantidad_puntos)
    elif opt == 5:
        exit()


# MATRICES DE TRANSFORMACION


def rotacion(angulo):  # Matriz de rotacion de los puntos
    matriz_rotacion = np.array([
        [np.cos(angulo), -np.sin(angulo), 0],
        [np.sin(angulo), np.cos(angulo), 0],
        [0, 0, 1],
    ])
    return matriz_rotacion


def traslacion(dx, dy):  # Matriz de traslacion de los Puntos
    matriz_traslacion = np.array([[1, 0, dx], [0, 1, dy], [0, 0, 1]])
    return matriz_traslacion


def sesgado(sx, sy):  # Matriz de sesgado de los puntos
    matriz_sesgado = np.array([[1, sx, 0],
                               [sy, 1, 0],
                               [0, 0, 1]])
    return matriz_sesgado


def rotacion_punto_centro(punto, angulo, centro_rotacion):
    # Paso 1: Conversión del ángulo a radianes
    angulo_rad = np.radians(angulo)
    # Paso 2: Traslación del punto al centro de rotación
    punto_transladado = punto - centro_rotacion
    # Paso 3: Rotación del punto alrededor del origen
    punto_rotado_xy = np.dot(np.array([[np.cos(angulo_rad), -np.sin(angulo_rad)],
                                       [np.sin(angulo_rad), np.cos(angulo_rad)]]), punto_transladado)
    # Paso 4: Traslación del punto de nuevo al lugar original
    punto_rotado_final = punto_rotado_xy + centro_rotacion
    # Paso 5: Devuelve el punto rotado
    return punto_rotado_final


# APLICACION DE LAS TRANSFORMACIONES

def aplicar_transformacion(cant_puntos, puntos, matriz_transformacion):
    puntos_transformados = []  # Lista para almacenar los puntos transformados
    # Itera sobre cada punto
    for p in range(cant_puntos):
        punto = puntos[p]  # Obtiene las coordenadas del punto
        # Paso 1: Convierte el punto a coordenadas homogéneas
        punto_homogeneo = np.array([punto[0], punto[1], 1])
        # Paso 2: Aplica la matriz de transformación al punto homogéneo
        punto_transformado = np.dot(matriz_transformacion, punto_homogeneo)
        # Paso 3: Extrae las coordenadas x, y del punto transformado y las agrega a la lista
        puntos_transformados.append(punto_transformado[:2])
    # Devuelve la lista de puntos transformados
    return puntos_transformados


def rotacion_paralelogramo(cant_puntos, angulo):
    # Paso 1: Calcula el ángulo de rotación en radianes
    angulo_rotacion = np.radians(angulo)
    # Paso 2: Obtiene la matriz de rotación utilizando la función rotacion
    matriz_rotacion = rotacion(angulo_rotacion)
    # Paso 3: Aplica la matriz de rotación a los puntos del
    # paralelogramo utilizando la función aplicar_transformacion
    puntos_transformados_rotacion = aplicar_transformacion(
        cant_puntos, puntos_paralelogramo, matriz_rotacion
    )
    # Paso 4: Devuelve los puntos transformados después de la rotación
    return puntos_transformados_rotacion


def rotacion_paralelogramo_punto(cant_puntos, angulo, punto_rotacion):
    puntos_rotados = []  # Lista para almacenar los puntos rotados
    # Itera sobre cada punto del paralelogramo
    for p in range(cant_puntos):
        # Paso 1: Obtiene el punto actual del paralelogramo
        punto = puntos_paralelogramo[p]
        # Paso 2: Llama a la función de rotación y agrega el punto rotado a la lista
        punto_rotado = np.array(rotacion_punto_centro(
            punto, angulo, punto_rotacion))
        puntos_rotados.append(punto_rotado)
    # Paso 3: Devuelve la lista de puntos rotados
    return puntos_rotados


def traslacion_paralelogramo(cant_puntos, dx_traslacion, dy_traslacion):
    # Paso 1: Calcula la matriz de traslación
    matriz_traslacion = traslacion(dx_traslacion, dy_traslacion)
    # Paso 2: Aplica la matriz de traslación a los puntos del paralelogramo
    puntos_transformados_traslacion = aplicar_transformacion(
        cant_puntos, puntos_paralelogramo, matriz_traslacion
    )
    # Paso 3: Devuelve los puntos transformados después de la traslación
    return puntos_transformados_traslacion


def sesgado_paralelogramo(cant_puntos, sx, sy):
    # Paso 1: Calcula la matriz de sesgado
    matriz_sesgado = sesgado(sx, sy)
    # Paso 2: Aplica la matriz de sesgado a los puntos del paralelogramo
    puntos_transformados_sesgados = aplicar_transformacion(
        cant_puntos, puntos_paralelogramo, matriz_sesgado
    )
    # Paso 3: Devuelve los puntos transformados después del sesgado
    return puntos_transformados_sesgados

# APLICACION DE LAS TRANSFORMACIONES A LOS DATOS


def mostrar_rotacion(cantidad_puntos):
    print("Ángulos positivos para sentido antihorario y negativos para sentido horario")
    print("Rotación desde el punto (0,0)")
    # Paso 1: Solicita al usuario el ángulo de rotación
    angulo = float(input("Ángulo de rotación: "))
    print("\nPuntos del paralelogramo original:")
    # Paso 2: Imprime los puntos originales del paralelogramo
    imprimir_matriz(cantidad_puntos, puntos_paralelogramo)
    # Paso 3: Obtiene los puntos rotados después de la rotación
    puntos_rotados = rotacion_paralelogramo(cantidad_puntos, angulo)
    print("\nPuntos después de la rotación:")
    # Paso 4: Imprime los puntos rotados
    imprimir_matriz(cantidad_puntos, puntos_rotados)


def mostrar_rotacion_desde_punto(cantidad_puntos):
    print("Ángulos positivos para sentido antihorario y negativos para sentido horario")
    # Paso 1: Solicita al usuario el ángulo de rotación
    angulo = float(input("Ángulo de rotación: "))
    # Paso 2: Solicita al usuario las coordenadas del punto de rotación
    punto_rotacion = np.array([
        float(input("Punto de rotación - X: ")),
        float(input("Punto de rotación - Y: "))
    ])
    print("\nPuntos del paralelogramo original:")
    # Paso 3: Imprime los puntos originales del paralelogramo
    imprimir_matriz(cantidad_puntos, puntos_paralelogramo)
    # Paso 4: Obtiene los puntos rotados desde un punto específico después de la rotación
    puntos_rotados = rotacion_paralelogramo_punto(
        cantidad_puntos, angulo, punto_rotacion)
    print("\nPuntos después de la rotación:")
    # Paso 5: Imprime los puntos rotados desde un punto específico
    imprimir_matriz(cantidad_puntos, puntos_rotados)


def mostrar_traslacion(cantidad_puntos):
    print("Ingrese Medidas de Traslación")
    # Paso 1: Solicita al usuario la medida de traslación en el eje X
    trasl_x = float(input("Medida en X: "))
    # Paso 2: Solicita al usuario la medida de traslación en el eje Y
    tresl_y = float(input("Medida en Y: "))
    print("\nPuntos del paralelogramo original:")
    # Paso 3: Imprime los puntos originales del paralelogramo
    imprimir_matriz(cantidad_puntos, puntos_paralelogramo)
    # Paso 4: Obtiene los puntos trasladados después de la traslación
    puntos_trasladados = traslacion_paralelogramo(
        cantidad_puntos, trasl_x, tresl_y)
    print("\nPuntos después de la traslación:")
    # Paso 5: Imprime los puntos trasladados
    imprimir_matriz(cantidad_puntos, puntos_trasladados)


def mostrar_sesgado(cantidad_puntos):
    print("Ingrese Medidas del Sesgado")
    # Paso 1: Solicita al usuario la medida de sesgado en el eje X
    sesg_x = float(input("Medida en X: "))
    # Paso 2: Solicita al usuario la medida de sesgado en el eje Y
    sesg_y = float(input("Medida en Y: "))
    print("\nPuntos del paralelogramo original:")
    # Paso 3: Imprime los puntos originales del paralelogramo
    imprimir_matriz(cantidad_puntos, puntos_paralelogramo)
    # Paso 4: Obtiene los puntos sesgados después del sesgado
    puntos_sesgados = sesgado_paralelogramo(cantidad_puntos, sesg_x, sesg_y)
    print("\nPuntos después del sesgado:")
    # Paso 5: Imprime los puntos sesgados
    imprimir_matriz(cantidad_puntos, puntos_sesgados)


# UTILIDADES DEL CODIGO
def imprimir_matriz(cant_matriz, matriz):
    for m in range(cant_matriz):
        fila = matriz[m]
        print(fila)


if __name__ == "__main__":
    main()

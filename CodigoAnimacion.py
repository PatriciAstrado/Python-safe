import numpy as np  # Importamos Numpy
import matplotlib.pyplot as plt  # Importamos MathplotLib
from matplotlib.animation import FuncAnimation  # Importamos AN

PUNTOS_PARALELOGRAMO = []  # Puntos del paralelogramo

# MENU PRINCIPAL


def main():
    print("---.---.---.---.---.---.---.---")
    print("   Matrices de Transformacion  ")
    print("             de                ")
    print("      Con uso de PYTHON        ")
    print("---.---.---.---.---.---.---.---")

    try:
        cantidad_puntos = obtener_cantidad_puntos()
        obtener_puntos(cantidad_puntos)

        while True:
            try:
                mostrar_opciones(cantidad_puntos)
            except Exception as e:
                print(
                    f"[ERROR] Ha ocurrido un error en las transformaciones: {e}"
                )

    except ValueError:
        print("[ERROR] Cantidad de puntos debe ser un número entero.")
    except Exception as ex:
        print(f"[ERROR] {ex}")


def obtener_cantidad_puntos():
    cantidad_puntos = int(
        input(
            "Ingrese la cantidad de puntos del paralelogramo de 1-5 puntos: "))

    while cantidad_puntos < 1 or cantidad_puntos > 5:
        print("[!] Cantidad Inválida")
        cantidad_puntos = int(input("Cantidad de Puntos: "))

    return cantidad_puntos


def obtener_puntos(cantidad_puntos):
    PUNTOS_PARALELOGRAMO.clear()

    for p in range(cantidad_puntos):
        print(f"\n|----    Datos Punto {p + 1} ----|")
        cord_x = float(input("Coordenada X: "))
        cord_y = float(input("Coordenada Y: "))
        PUNTOS_PARALELOGRAMO.append([cord_x, cord_y])
        print(f"Punto {p + 1} Agregado!")

    print("\nPuntos Ingresados: ")
    for i in range(cantidad_puntos):
        print(
            f"P{i + 1}: [{PUNTOS_PARALELOGRAMO[i][0]}, {PUNTOS_PARALELOGRAMO[i][1]}]"
        )


def mostrar_opciones(cantidad_puntos):
    # Paso 1: Imprime las opciones disponibles
    print("\n--- Opciones ---")
    print(
        "[1] Rotacion\n[2] Traslacion\n[3] Sesgado\n[4] Rotacion desde Punto Arbitrario\n[5] Reflexion\n[6] Salir"
    )

    # Paso 2: Solicita al usuario seleccionar una opción
    opt = int(input("Opcion: "))

    # Paso 3: Verifica que la opción seleccionada sea válida
    while opt not in range(1, 7):
        print("[!] Opcion Invalida")
        opt = int(input("Opcion: "))
    print("")

    # Paso 4: Llama a la función correspondiente según la opción seleccionada
    if opt == 1:
        mostrar_rotacion(cantidad_puntos)
    elif opt == 2:
        mostrar_traslacion(cantidad_puntos)
    elif opt == 3:
        mostrar_sesgado(cantidad_puntos)
    elif opt == 4:
        mostrar_rotacion_desde_punto(cantidad_puntos)
    elif opt == 5:
        mostrar_reflexion(cantidad_puntos)
    elif opt == 6:
        exit()


# MATRICES DE TRANSFORMACION


def rotacion(angulo):  # Matriz de rotacion de los puntos
    return np.array([[np.cos(angulo), -np.sin(angulo), 0],
                     [np.sin(angulo), np.cos(angulo), 0]])


def traslacion(dx, dy):  # Matriz de traslacion de los Puntos
    return np.array([[1, 0, dx], [0, 1, dy]])


def sesgado(tipo, sval, angulo=False):
    # Paso 1: Inicializa la variable sesg_val con el valor proporcionado
    sesg_val = sval
    # Paso 2: Calcula el valor del sesgo si se especifica un ángulo en radianes
    if angulo:
        sesg_val = np.tan(np.radians(sval))
    # Paso 3: Devuelve una matriz de sesgado según el tipo especificado
    if tipo == "EjeX":
        # Matriz de sesgado en el eje X:
        return np.array([[1, sesg_val, 0], [0, 1, 0]])
    elif tipo == "EjeY":
        # Matriz de sesgado en el eje Y:
        return np.array([[1, 0, 0], [sesg_val, 1, 0]])


def reflexion(tipo):
    # Devuelve una matriz de reflexión según el tipo especificado
    if tipo == "EjeX":
        # Matriz de reflexión en el eje X:
        return np.array([[1, 0, 0], [0, -1, 0]])
    elif tipo == "EjeY":
        # Matriz de reflexión en el eje Y:
        return np.array([[-1, 0, 0], [0, 1, 0]])
    # Matriz de reflexión desde el origen:
    return np.array([[-1, 0, 0], [0, -1, 0]])


def rotacion_punto_centro(punto, angulo, centro_rotacion):
    # Paso 1: Conversión del ángulo a radianes
    angulo_rad = np.radians(angulo)
    # Paso 2: Traslación del punto al centro de rotación
    punto_transladado = punto - centro_rotacion
    # Paso 3: Rotación del punto alrededor del origen
    punto_rotado_xy = np.dot(
        np.array([[np.cos(angulo_rad), -np.sin(angulo_rad)],
                  [np.sin(angulo_rad), np.cos(angulo_rad)]]),
        punto_transladado,
    )
    # Paso 4: Traslación del punto de nuevo al lugar original
    return punto_rotado_xy + centro_rotacion


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
    return aplicar_transformacion(cant_puntos, PUNTOS_PARALELOGRAMO,
                                  matriz_rotacion)


def rotacion_paralelogramo_punto(cant_puntos, angulo, punto_rotacion):
    puntos_rotados = []  # Lista para almacenar los puntos rotados
    # Itera sobre cada punto del paralelogramo
    for p in range(cant_puntos):
        # Paso 1: Obtiene el punto actual del paralelogramo
        punto = PUNTOS_PARALELOGRAMO[p]
        # Paso 2: Llama a la función de rotación y agrega el punto rotado a la lista
        punto_rotado = np.array(
            rotacion_punto_centro(punto, angulo, punto_rotacion))
        puntos_rotados.append(punto_rotado)
    # Paso 3: Devuelve la lista de puntos rotados
    return puntos_rotados


def traslacion_paralelogramo(cant_puntos, dx_traslacion, dy_traslacion):
    # Paso 1: Calcula la matriz de traslación
    matriz_traslacion = traslacion(dx_traslacion, dy_traslacion)
    # Paso 2: Aplica la matriz de traslación a los puntos del paralelogramo
    return aplicar_transformacion(cant_puntos, PUNTOS_PARALELOGRAMO,
                                  matriz_traslacion)


def sesgado_paralelogramo(cant_puntos, tipo, sval, angulo=False):
    # Paso 1: Calcula la matriz de sesgado
    matriz_sesgado = sesgado(tipo, sval, angulo)
    # Paso 2: Aplica la matriz de sesgado a los puntos del paralelogramo
    return aplicar_transformacion(cant_puntos, PUNTOS_PARALELOGRAMO,
                                  matriz_sesgado)


def reflexion_paralelogramo(cant_puntos, tipo):
    # Paso 1: Calcula la matriz de reflexion
    matriz_reflexion = reflexion(tipo)
    # Paso 2: Aplica la matriz de reflexion a los puntos del paralelogramo
    return aplicar_transformacion(cant_puntos, PUNTOS_PARALELOGRAMO,
                                  matriz_reflexion)


# APLICACION DE LAS TRANSFORMACIONES A LOS DATOS


def mostrar_rotacion(cantidad_puntos):
    print(
        "Ángulos positivos para sentido antihorario y negativos para sentido horario"
    )
    print("Rotación desde el punto (0,0)")
    # Paso 1: Solicita al usuario el ángulo de rotación
    angulo = float(input("Ángulo de rotación: "))
    print("\nPuntos del paralelogramo original:")
    # Paso 2: Imprime los puntos originales del paralelogramo
    imprimir_matriz(cantidad_puntos, PUNTOS_PARALELOGRAMO)
    # Paso 3: Obtiene los puntos rotados después de la rotación
    puntos_rotados = rotacion_paralelogramo(cantidad_puntos, angulo)
    print("\nPuntos después de la rotación:")
    # Paso 4: Imprime los puntos rotados
    imprimir_matriz(cantidad_puntos, puntos_rotados)

    animar_transformacion("Rotacion", angulo, [0, 0])


def mostrar_rotacion_desde_punto(cantidad_puntos):
    print(
        "Ángulos positivos para sentido antihorario y negativos para sentido horario"
    )
    # Paso 1: Solicita al usuario el ángulo de rotación
    angulo = float(input("Ángulo de rotación: "))
    # Paso 2: Solicita al usuario las coordenadas del punto de rotación
    punto_rotacion = np.array([
        float(input("Punto de rotación - X: ")),
        float(input("Punto de rotación - Y: "))
    ])
    print("\nPuntos del paralelogramo original:")
    # Paso 3: Imprime los puntos originales del paralelogramo
    imprimir_matriz(cantidad_puntos, PUNTOS_PARALELOGRAMO)
    # Paso 4: Obtiene los puntos rotados desde un punto específico después de la rotación
    puntos_rotados = rotacion_paralelogramo_punto(cantidad_puntos, angulo,
                                                  punto_rotacion)
    print("\nPuntos después de la rotación:")
    # Paso 5: Imprime los puntos rotados desde un punto específico
    imprimir_matriz(cantidad_puntos, puntos_rotados)
    
    animar_transformacion("Rotacion Punto Arbitrario",  angulo, punto_rotacion)


def mostrar_sesgado(cantidad_puntos):
    # Paso 1: Solicita al usuario el tipo de sesgado (Ángulo o Medidas)
    print("Ingrese datos del sesgado\nTipo de dato:")
    print("[1] Angulo\n[2] Medidas")

    tipo = int(input("Opcion: "))
    while tipo not in [1, 2]:
        print("! Opcion Invalida")
        tipo = int(input("Opcion: "))

    # Paso 2: Determina si el sesgado es por ángulo
    angulo = (tipo == 1)  #Si tipo es igual a uno devuelve True
    # Paso 3: Presenta opciones de eje de sesgado según el tipo
    if angulo:
        print(
            "\nSeleccione el eje de Sesgado:\n[1] Eje X (Positivos para sentido derecha)\n"
            + "[2] Eje Y (Positivos para Sentido Arriba)")
    else:
        print("\nSeleccione el eje de Sesgado:\n[1] Eje X\n[2] Eje Y")
    # Paso 4: Solicita al usuario seleccionar el eje de sesgado
    eje_seleccionado = int(input("Opcion: "))
    while eje_seleccionado not in [1, 2]:
        print("! Opcion Invalida")
        eje_seleccionado = int(input("Opcion: "))
    # Paso 5: Solicita al usuario ingresar el valor de sesgado
    valor = float(input("Ingrese Valor: "))
    # Paso 6: Imprime los puntos originales del paralelogramo
    print("\nPuntos del paralelogramo original:")
    imprimir_matriz(cantidad_puntos, PUNTOS_PARALELOGRAMO)
    # Paso 7: Determina el eje de sesgado según la selección del usuario
    eje = "EjeX" if eje_seleccionado == 1 else "EjeY"  # "EjeX" si eje_seleccionado es 1 de lo contrario EjeY
    # Paso 8: Calcula y almacena los puntos después del sesgado
    puntos_sesgados = sesgado_paralelogramo(cantidad_puntos, eje, valor,
                                            angulo)
    # Paso 9: Imprime los puntos después del sesgado
    print("\nPuntos después del sesgado:")
    imprimir_matriz(cantidad_puntos, puntos_sesgados)
    # Paso 10: Grafica la transformación de sesgado
    animar_transformacion("Sesgado", eje, valor,angulo)


def mostrar_traslacion(cantidad_puntos):
    print("Ingrese Medidas de Traslación")
    # Paso 1: Solicita al usuario la medida de traslación en el eje X
    trasl_x = float(input("Medida en X: "))
    # Paso 2: Solicita al usuario la medida de traslación en el eje Y
    tresl_y = float(input("Medida en Y: "))
    print("\nPuntos del paralelogramo original:")
    # Paso 3: Imprime los puntos originales del paralelogramo
    imprimir_matriz(cantidad_puntos, PUNTOS_PARALELOGRAMO)
    # Paso 4: Obtiene los puntos trasladados después de la traslación
    puntos_trasladados = traslacion_paralelogramo(cantidad_puntos, trasl_x,
                                                  tresl_y)
    print("\nPuntos después de la traslación:")
    # Paso 5: Imprime los puntos trasladados
    imprimir_matriz(cantidad_puntos, puntos_trasladados)
    
    # Llama a la función de animación
    animar_transformacion("Traslacion", trasl_x,tresl_y)
    

def mostrar_reflexion(cantidad_puntos):
    # Paso 1: Solicita al usuario seleccionar el tipo de reflexión
    print("Seleccione tipo de reflexion")
    print(
        "[1] Reflexion desde el origen\n[2] Reflexion eje X\n[3] Reflexion eje Y"
    )
    tipo = float(input("Opcion: "))

    # Paso 2: Verifica que la opción sea válida
    while tipo not in [1, 2, 3]:
        print("! Opcion Invalida")
        tipo = float(input("Opcion: "))

    # Paso 3: Aplica la reflexión según la opción seleccionada
    if tipo == 1:
        tipo_reflexion = "Origen"
    elif tipo == 2:
        tipo_reflexion= "EjeX"
    elif tipo == 3:
        tipo_reflexion = "EjeY"

    puntos_reflejados = reflexion_paralelogramo(cantidad_puntos, tipo_reflexion)
    # Paso 4: Imprime los puntos originales del paralelogramo
    print("\nPuntos del paralelogramo original:")
    imprimir_matriz(cantidad_puntos, PUNTOS_PARALELOGRAMO)

    # Paso 5: Imprime los puntos después de la reflexión
    print("\nPuntos después de la reflexion:")
    imprimir_matriz(cantidad_puntos, puntos_reflejados)

    # Paso 6: Grafica la reflexión
    graficarReflexion(puntos_reflejados)


# UTILIDADES DEL CODIGO
def imprimir_matriz(cant_matriz, matriz):
    for m in range(cant_matriz):
        fila = matriz[m]
        print(fila)


def ordenar_puntos_en_sentido_horario(puntos):
    # Paso 1: Calcula el centroide de los puntos
    centroide = np.mean(puntos, axis=0)
    # Paso 2: Utiliza la función sorted con una función lambda como clave para ordenar los puntos
    return np.array(
        sorted(puntos,
               key=lambda p: np.arctan2(p[1] - centroide[1], p[0] - centroide[
                   0])))


# GRAFICACION DE LOS PARALELOGRAMOS
def plot_paralelogramo(PUNTOS_PARALELOGRAMO, color, titulo):
    puntos = ordenar_puntos_en_sentido_horario(PUNTOS_PARALELOGRAMO)
    x = [p[0] for p in puntos]
    y = [p[1] for p in puntos]

    # Agregar el primer punto al final para cerrar la figura
    x.append(x[0])
    y.append(y[0])

    plt.plot(x, y, color=color, label=titulo)
    plt.scatter(x, y, color=color)

def graficarReflexion(puntos_reflejados):
    # Paso 1: Grafica el paralelogramo original en color deeppink
    plot_paralelogramo(PUNTOS_PARALELOGRAMO, "deeppink",
                       "Paralelogramo Original")

    # Paso 2: Grafica el paralelogramo transformado en color purple
    plot_paralelogramo(puntos_reflejados, "purple", f"Paralelogramo Reflejado")

    plt.axvline(x=0, color='red', linestyle='--')
    plt.axhline(y=0, color='green', linestyle='-.')
    plt.axis("equal")
    plt.legend()
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"Paralelogramos Original y Reflejado")
    plt.grid(True)
    plt.show()

# ANIMACIONES DE LAS TRASNFORMACIONES

def animar_transformacion(transformacion, param1=None, param2=None, param3=None):
    # Paso 1: Configura la figura y el eje para la animación
    fig, ax = plt.subplots()
    frames = 50
    
    # Paso 2: Define la función para actualizar cada frame
    def actualizar_frame(frame):
        ax.clear()
        plot_paralelogramo(PUNTOS_PARALELOGRAMO, "deeppink", "Paralelogramo Original")
        
        # Paso 3: Aplica la transformación según el tipo especificado
        if transformacion == "Rotacion":
            puntos_transformados = rotacion_paralelogramo(
                len(PUNTOS_PARALELOGRAMO), round(param1 * frame / frames))
            plt.scatter(param2[0], param2[1], color="black", label="Eje de Rotación")
        elif transformacion == "Rotacion Punto Arbitrario":
            puntos_transformados = rotacion_paralelogramo_punto(
                len(PUNTOS_PARALELOGRAMO), round(param1 * frame / frames), param2)
            plt.scatter(param2[0], param2[1], color="black", label="Eje de Rotación")
        elif transformacion == "Traslacion":
            puntos_transformados = traslacion_paralelogramo(
                len(PUNTOS_PARALELOGRAMO), round(param1 * frame / frames, 2), 
                round(param2 * frame / frames, 2))
        elif transformacion == "Sesgado":
            puntos_transformados = sesgado_paralelogramo(
                len(PUNTOS_PARALELOGRAMO), param1, round(param2 * frame / frames, 3), param3
            )
        
        # Paso 4: Grafica el paralelogramo transformado animado
        plot_paralelogramo(
            puntos_transformados, "purple", f"Paralelogramo {transformacion} Animado"
        )
        
        # Paso 5: Ajusta el aspecto y muestra la leyenda
        plt.axis("equal")
        plt.legend()
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title(f"Animación de {transformacion}")
        plt.grid(True)

    # Paso 6: Crea la animación utilizando FuncAnimation
    animacion = FuncAnimation(
        fig,
        func=actualizar_frame,
        frames=frames,
        interval=50,
        repeat=False,
        repeat_delay=2000
    )

    # Paso 7: Muestra la animación
    plt.show()



if __name__ == "__main__":
    main()

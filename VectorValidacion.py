def leer_vector(n, numero_vector):
    """Lee un vector de n elementos, valida los datos y permite confirmar antes de continuar"""
    while True:
        print(f"\nIngrese los {n} elementos del vector v{numero_vector}:")
        vector = []
        valido = True
        # Se leen n elementos
        for i in range(n):
            valor = input(f"  Elemento {i + 1}: ")
            # Validar que el valor sea un número entero (permite negativos)
            if not valor.lstrip('-').isdigit():
                print("Error: solo se permiten números enteros.")
                valido = False
                break
            vector.append(int(valor))  # Convertir a entero y agregarlo al vector
        
        if not valido:
            continue  # Reintenta si hubo un error en la entrada
        
        # Mostrar el vector ingresado
        print(f"Vector ingresado v{numero_vector} = {vector}")
        confirmacion = input("¿El vector ingresado es correcto? (s/n): ").strip().lower()
        if confirmacion == 's':
            return vector  # Devuelve el vector confirmado
        else:
            print("Reingresando el vector...\n")


def imprimir_matriz(matriz, titulo="Matriz actual:"):
    """Imprime la matriz en forma aumentada, con separación visual"""
    print("\n" + titulo)
    for fila in matriz:
        # Imprime cada fila con formato y separa la última columna con '|'
        print("  [", end="")
        for j in range(len(fila)):
            if j == len(fila) - 1:
                print("|", end=" ")  # Separador visual
            print(f"{int(fila[j]):4}", end=" " if j != len(fila) - 1 else "")
        print(" ]")
    print()


def gauss_reduccion(matriz):
    """Aplica eliminación de Gauss mostrando cada paso con detalle"""
    filas = len(matriz)
    columnas = len(matriz[0]) - 1  # Se ignora la columna de ceros
    paso = 1

    print("\n================= ELIMINACIÓN DE GAUSS =================")
    for i in range(filas):
        # Buscar pivote distinto de cero
        if matriz[i][i] == 0:
            for k in range(i + 1, filas):
                if matriz[k][i] != 0:
                    print(f"\nPaso {paso}: Intercambiamos F{i + 1} ↔ F{k + 1} (para obtener pivote distinto de 0)")
                    matriz[i], matriz[k] = matriz[k], matriz[i]  # Intercambio de filas
                    imprimir_matriz(matriz, f"Resultado después del intercambio:")
                    paso += 1
                    break
        
        pivote = matriz[i][i]
        if pivote == 0:
            continue  # Si no hay pivote válido, salta la iteración

        # Normalizar pivote a 1
        if pivote != 1:
            print(f"Paso {paso}: Normalizamos F{i + 1} dividiendo toda la fila entre {pivote}")
            for j in range(len(matriz[i])):
                matriz[i][j] = matriz[i][j] / pivote
            imprimir_matriz(matriz, f"Resultado tras normalizar F{i + 1}:")
            paso += 1
        
        # Eliminar valores debajo del pivote
        for k in range(i + 1, filas):
            factor = matriz[k][i]
            if factor != 0:
                print(f"Paso {paso}: F{k + 1} = F{k + 1} - ({factor})·F{i + 1}")
                for j in range(len(matriz[i])):
                    matriz[k][j] -= factor * matriz[i][j]
                imprimir_matriz(matriz, f"Resultado después de eliminar debajo del pivote:")
                paso += 1

    return matriz


def retroceso_simplificado(matriz):
    """Limpia los valores sobre los pivotes (hacia atrás)"""
    filas = len(matriz)
    columnas = len(matriz[0]) - 1
    paso = 1

    print("\n================= RETROCESO (FORMA ESCALONADA REDUCIDA) =================")
    # Recorre de la última fila hacia arriba
    for i in range(filas - 1, -1, -1):
        pivote_col = -1
        # Encuentra la posición del pivote (primer valor no cero)
        for j in range(columnas):
            if matriz[i][j] != 0:
                pivote_col = j
                break
        if pivote_col == -1:
            continue  # Si la fila es nula, la salta
        # Elimina los valores sobre el pivote
        for k in range(i - 1, -1, -1):
            factor = matriz[k][pivote_col]
            if factor != 0:
                print(f"Paso {paso}: F{k + 1} = F{k + 1} - ({factor})·F{i + 1}")
                for j in range(len(matriz[i])):
                    matriz[k][j] -= factor * matriz[i][j]
                imprimir_matriz(matriz, f"Resultado del paso {paso}:")
                paso += 1
    return matriz


def limpiar_matriz(matriz):
    """Elimina -0 y decimales exactos para presentación más limpia"""
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            # Convierte números muy pequeños en 0
            if abs(matriz[i][j]) < 1e-9:
                matriz[i][j] = 0
            # Si el número es flotante pero entero exacto, conviértelo a int
            elif isinstance(matriz[i][j], float) and matriz[i][j].is_integer():
                matriz[i][j] = int(matriz[i][j])
    return matriz


def main():
    print("====================================================")
    print("   PROGRAMA PARA DETERMINAR INDEPENDENCIA LINEAL    ")
    print("====================================================")

    # Leer dimensión de los vectores
    while True:
        n = input("\nIngrese la dimensión de los vectores (por ejemplo 3): ")
        if n.isdigit() and int(n) > 0:
            n = int(n)
            break
        else:
            print("Error: ingrese un número entero positivo.")

    # Leer cantidad de vectores
    while True:
        p = input("Ingrese la cantidad de vectores a evaluar: ")
        if p.isdigit() and int(p) > 0:
            p = int(p)
            break
        else:
            print("Error: ingrese un número entero positivo.")

    # Leer los vectores ingresados por el usuario
    vectores = []
    for i in range(p):
        v = leer_vector(n, i + 1)
        vectores.append(v)

    # Construcción de la matriz aumentada (última columna = 0)
    matriz = []
    for i in range(n):
        fila = []
        for j in range(p):
            fila.append(vectores[j][i])
        fila.append(0)  # Columna de términos independientes
        matriz.append(fila)

    imprimir_matriz(matriz, "Matriz aumentada formada por los vectores:")

    # Aplicar eliminación de Gauss hacia adelante
    matriz = gauss_reduccion(matriz)
    # Aplicar retroceso hacia atrás
    matriz = retroceso_simplificado(matriz)
    # Limpiar los resultados finales
    matriz = limpiar_matriz(matriz)

    imprimir_matriz(matriz, "Matriz aumentada final (forma escalonada reducida):")

    # Determinar independencia o dependencia lineal
    rango = sum(any(valor != 0 for valor in fila[:-1]) for fila in matriz)
    print("====================================================")
    print("ANÁLISIS FINAL:")
    print(f" - Rango de la matriz: {rango}")
    print(f" - Cantidad de vectores: {p}")

    # Si el rango = cantidad de vectores → son independientes
    if rango == p:
        print("\nConclusión: Los vectores son *linealmente independientes*.")
        print("   La única solución al sistema homogéneo es la trivial (todos los coeficientes = 0).")
    else:
        print("\nConclusión: Los vectores son *linealmente dependientes*.")
        print("   Existen soluciones no triviales al sistema homogéneo.")
        print("\nEcuaciones resultantes del sistema:")
        for i, fila in enumerate(matriz):
            ecuacion = " + ".join(f"{fila[j]}·x{j+1}" for j in range(p) if fila[j] != 0)
            if ecuacion == "":
                ecuacion = "0"
            print(f"  {ecuacion} = 0")

    print("====================================================")
    print("Proceso finalizado. ¡Gracias por usar el programa!")
    print("====================================================")


# Ejecutar el programa principal solo si se ejecuta directamente
if __name__ == "__main__":
    main()


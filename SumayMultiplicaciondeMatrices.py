def leer_entero(mensaje, minimo=None):
    """
    Lee un número entero con validación desde teclado.
    - mensaje: texto que se muestra al usuario
    - minimo: valor mínimo permitido (ej. 1 para que no existan dimensiones negativas o cero)
    """
    while True:
        valor = input(mensaje)
        if not valor.isdigit():  # Validar que sea un número entero positivo
            print("Error: debe ingresar un número entero positivo.")
            continue
        valor = int(valor)
        if minimo is not None and valor < minimo:  # Validar mínimo
            print(f"Error: el número debe ser mayor o igual a {minimo}.")
            continue
        return valor


def leer_fila(columnas, num_fila):
    """
    Lee una fila de la matriz con validación de cantidad y tipo de datos.
    - columnas: número de valores esperados
    - num_fila: número de fila (para mostrar al usuario)
    """
    while True:
        fila = input(f"Ingrese los {columnas} valores de la fila {num_fila} separados por espacio: ").split()
        if len(fila) != columnas:
            print(f"Error: debe ingresar exactamente {columnas} valores.")
            continue
        try:
            fila = [int(x) for x in fila]  # Convertir a enteros
            return fila
        except ValueError:
            print("Error: solo se permiten números enteros.")


def leer_matriz(filas, columnas, nombre="Matriz"):
    """
    Construye una matriz leyendo fila por fila.
    Retorna una lista de listas (la matriz).
    """
    print(f"\nIngresando datos para {nombre}:")
    matriz = []
    for i in range(1, filas + 1):
        fila = leer_fila(columnas, i)
        matriz.append(fila)
    return matriz


def imprimir_matriz(matriz):
    """Imprime una matriz fila por fila."""
    for fila in matriz:
        print(fila)


def sumar_matrices_paso_a_paso(A, B):
    """
    Suma dos matrices y muestra paso a paso cómo se calcula cada elemento.
    """
    filas = len(A)
    columnas = len(A[0])
    resultado = []
    print("\n=== Paso a paso de la suma de matrices ===")
    for i in range(filas):
        fila_resultado = []
        for j in range(columnas):
            suma = A[i][j] + B[i][j]
            print(f"A[{i+1}][{j+1}] + B[{i+1}][{j+1}] = {A[i][j]} + {B[i][j]} = {suma}")
            fila_resultado.append(suma)
        resultado.append(fila_resultado)
    return resultado


def multiplicar_matrices_paso_a_paso(A, B):
    """
    Multiplica dos matrices y muestra paso a paso cómo se calcula cada elemento.
    """
    filas_A, cols_A = len(A), len(A[0])
    filas_B, cols_B = len(B), len(B[0])
    
    resultado = []
    print("\n=== Paso a paso de la multiplicación de matrices ===")
    for i in range(filas_A):
        fila_resultado = []
        for j in range(cols_B):
            suma = 0
            pasos = []
            for k in range(cols_A):
                producto = A[i][k] * B[k][j]
                suma += producto
                pasos.append(f"A[{i+1}][{k+1}] * B[{k+1}][{j+1}] = {A[i][k]} * {B[k][j]} = {producto}")
            print(f"\nCalculando elemento C[{i+1}][{j+1}]:")
            for paso in pasos:
                print(paso)
            print(f"Suma de productos = {suma}")
            fila_resultado.append(suma)
        resultado.append(fila_resultado)
    return resultado


def multiplicar_matriz_vector_paso_a_paso(A, v):
    """
    Multiplica una matriz A por un vector columna v y explica paso a paso
    como combinación lineal de columnas de la matriz.
    """
    m = len(A)
    n = len(A[0])
    if len(v) != n:
        print(f"Error: el vector debe tener {n} elementos.")
        return None

    # Obtener las columnas de la matriz
    columnas = [[A[i][j] for i in range(m)] for j in range(n)]

    # Explicación introductoria
    print("\n=== Multiplicación de Matriz por Vector Columna ===")
    print("Multiplicar una matriz por un vector columna equivale a hacer")
    print("una combinación lineal de las columnas de la matriz, usando como pesos")
    print("los elementos del vector.\n")

    print("Matriz A escrita por columnas:")
    for j, col in enumerate(columnas):
        print(f"Columna {j+1}: {col}")

    print("\nVector columna v = ", v)
    print("\nInterpretación matemática: ")
    print("Resultado = (v1 * Columna1) + (v2 * Columna2) + ... + (vn * Columna n)\n")

    # Contribución de cada columna
    contribuciones = []
    for j in range(n):
        scalar = v[j]
        col = columnas[j]
        contrib = [scalar * x for x in col]
        contribuciones.append(contrib)
        print(f"Paso {j+1}: Multiplicamos el elemento {j+1} del vector (v[{j+1}] = {scalar})")
        print(f"         por la columna {j+1} de la matriz {col}")
        print(f"         → Contribución: {scalar} * {col} = {contrib}\n")

    # Sumar contribuciones elemento por elemento
    resultado = [0] * m
    print("Sumamos todas las contribuciones elemento por elemento:")
    for i in range(m):
        suma_elemento = 0
        detalles = []
        for j in range(n):
            suma_elemento += contribuciones[j][i]
            detalles.append(str(contribuciones[j][i]))
        resultado[i] = suma_elemento
        print(f"Componente {i+1} del resultado = " + " + ".join(detalles) + f" = {suma_elemento}")

    print("\n=== Vector resultado final ===")
    print(resultado)
    return resultado


def main():
    """
    Menú principal del programa:
    1) Sumar matrices
    2) Multiplicar matrices
    3) Multiplicar matriz por vector columna
    0) Salir
    """
    print("=== Operaciones con matrices paso a paso ===")
    
    while True:
        print("\nMenú principal:")
        print("1: Sumar matrices")
        print("2: Multiplicar matrices")
        print("3: Multiplicar matriz por vector (columna)")
        print("0: Salir")
        
        opcion = input("Elige una opción: ")
        if opcion not in ["0", "1", "2", "3"]:
            print("Opción no válida. Intente de nuevo.")
            continue
        opcion = int(opcion)
        
        if opcion == 0:
            print("Programa finalizado.")
            break

        if opcion == 1:
            # Suma de matrices
            filas = leer_entero("Número de filas: ", 1)
            columnas = leer_entero("Número de columnas: ", 1)
            A = leer_matriz(filas, columnas, "Matriz A")
            B = leer_matriz(filas, columnas, "Matriz B")
            print("\nMatriz A:")
            imprimir_matriz(A)
            print("\nMatriz B:")
            imprimir_matriz(B)
            resultado = sumar_matrices_paso_a_paso(A, B)
            print("\nResultado final de la suma:")
            imprimir_matriz(resultado)
        
        elif opcion == 2:
            # Multiplicación de matrices
            filas_A = leer_entero("Número de filas de la Matriz A: ", 1)
            cols_A = leer_entero("Número de columnas de la Matriz A: ", 1)
            filas_B = leer_entero("Número de filas de la Matriz B: ", 1)
            cols_B = leer_entero("Número de columnas de la Matriz B: ", 1)
            if cols_A != filas_B:
                print("Error: no se pueden multiplicar. Columnas de A deben ser iguales a filas de B.")
                continue
            A = leer_matriz(filas_A, cols_A, "Matriz A")
            B = leer_matriz(filas_B, cols_B, "Matriz B")
            print("\nMatriz A:")
            imprimir_matriz(A)
            print("\nMatriz B:")
            imprimir_matriz(B)
            resultado = multiplicar_matrices_paso_a_paso(A, B)
            print("\nResultado final de la multiplicación:")
            imprimir_matriz(resultado)
        
        elif opcion == 3:
            # Multiplicación de matriz por vector columna
            filas_A = leer_entero("Número de filas de la Matriz A: ", 1)
            cols_A = leer_entero("Número de columnas de la Matriz A: ", 1)
            A = leer_matriz(filas_A, cols_A, "Matriz A")
            print(f"\nIngrese el vector columna de {cols_A} elementos:")
            while True:
                entrada = input().split()
                if len(entrada) != cols_A:
                    print(f"Error: debe ingresar exactamente {cols_A} valores.")
                    continue
                try:
                    v = [int(x) for x in entrada]
                    break
                except ValueError:
                    print("Error: solo se permiten números enteros.")
            multiplicar_matriz_vector_paso_a_paso(A, v)


if __name__ == "__main__":
    main()


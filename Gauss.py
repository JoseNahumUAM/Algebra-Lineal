from fractions import Fraction  # Importar módulo para trabajar con fracciones exactas

# ---------- FORMATEO Y VISUALIZACIÓN ----------
def formatearnumero(numero):
    """Convierte un número en string legible (entero o fracción)."""
    if isinstance(numero, Fraction):              # Si es fracción exacta
        if numero.denominator == 1:              # Si es fracción con denominador 1 (entero)
            return str(numero.numerator)
        else:                                    # Si no, se muestra como num/den
            return f"{numero.numerator}/{numero.denominator}"
    else:
        return str(round(numero, 2))             # Para decimales normales, redondea a 2 cifras

def imprimirMatriz(matrix, mensaje=""):
    """Muestra la matriz en consola con formato tipo tabla."""
    if mensaje:
        print(f"\n{mensaje}")                     # Mensaje opcional arriba
    for fila in matrix:
        print("[\t" + "".join(formatearnumero(num) + "\t" for num in fila) + "]")

# ---------- GAUSS (TRIANGULAR SUPERIOR) ----------
def gaussEliminacionDetalle(matrix):
    """Aplica el método de Gauss paso a paso, mostrando cada operación."""
    filas = len(matrix)
    columnas = len(matrix[0])

    # Recorremos las columnas pivote hasta min(filas, columnas-1)
    for i in range(min(filas, columnas-1)):
        print(f"\n--- Iteración {i+1}: trabajando con columna {i+1} ---")

        # Selección del pivote: fila con valor absoluto más grande en la columna actual
        max_fila = max(range(i, filas), key=lambda r: abs(matrix[r][i]))
        if abs(matrix[max_fila][i]) < 1e-12:     # Si no se encuentra pivote (columna libre)
            print(f"No se encuentra pivote en columna {i+1}, columna libre")
            continue

        # Intercambiar filas si el pivote no está en la fila actual
        if max_fila != i:
            matrix[i], matrix[max_fila] = matrix[max_fila], matrix[i]
            print(f"Paso: F{i+1} <-> F{max_fila+1}")
            imprimirMatriz(matrix, "Matriz tras intercambio:")

        # Pivote encontrado
        pivote = matrix[i][i]
        print(f"Pivote seleccionado: {formatearnumero(pivote)} en fila {i+1}")

        # Eliminación hacia abajo (triangular superior)
        for j in range(i+1, filas):
            factor = matrix[j][i] / pivote       # Factor para anular elemento
            if abs(factor) > 1e-12:
                print(f"Paso: F{j+1} = F{j+1} - ({formatearnumero(factor)})*F{i+1}")
            matrix[j] = [matrix[j][k] - factor * matrix[i][k] for k in range(columnas)]
            imprimirMatriz(matrix, f"Matriz tras actualizar F{j+1}")

    return matrix

# ---------- ANÁLISIS DEL SISTEMA ----------
def analizarSistema(matrix):
    """Analiza si el sistema tiene solución única, ninguna o infinitas."""
    filas = len(matrix)
    columnas = len(matrix[0])
    n = columnas - 1                             # Número de variables

    pivotes = []
    for i in range(filas):
        fila = matrix[i]
        pivote_col = -1
        for j in range(n):
            if abs(fila[j]) > 1e-12:            # Buscar primer coeficiente distinto de 0
                pivote_col = j
                pivotes.append(j)               # Guardar columna con pivote
                break
        if pivote_col == -1 and abs(fila[-1]) > 1e-12:
            return "incompatible", []           # Caso: 0x+0y+0z = c (c≠0)

    # Variables libres = columnas sin pivote
    variables_libres = [j for j in range(n) if j not in pivotes]

    if len(pivotes) < n:                        # Menos pivotes que variables → infinitas
        return "infinitas", variables_libres
    else:
        return "unica", variables_libres        # Si cada variable tiene pivote → única

# ---------- SUSTITUCIÓN REGRESIVA ----------
def sustitucionRegresiva(matrix):
    """Resuelve el sistema por sustitución regresiva, mostrando cálculos."""
    filas = len(matrix)
    columnas = len(matrix[0])
    n = columnas - 1
    soluciones = [Fraction(0) for _ in range(n)]

    for i in range(filas-1, -1, -1):            # Recorremos de abajo hacia arriba
        fila = matrix[i]
        pivote_col = -1
        for j in range(n):
            if abs(fila[j]) > 1e-12:            # Identificar pivote en la fila
                pivote_col = j
                break
        if pivote_col == -1:                    # Fila sin pivote, se ignora
            continue

        # Calcular sumatoria de coef*solución ya encontrada
        suma = sum(fila[j] * soluciones[j] for j in range(pivote_col+1, n))
        soluciones[pivote_col] = (fila[-1] - suma) / fila[pivote_col]

        # Mostrar detalle de la sustitución
        operaciones = []
        for j in range(pivote_col+1, n):
            if abs(fila[j]) > 1e-12:
                operaciones.append(f"{formatearnumero(fila[j])}*x{j+1}({formatearnumero(soluciones[j])})")

        if operaciones:
            print(f"x{pivote_col+1} = ({formatearnumero(fila[-1])} - ({' + '.join(operaciones)})) / {formatearnumero(fila[pivote_col])} = {formatearnumero(soluciones[pivote_col])}")
        else:
            print(f"x{pivote_col+1} = {formatearnumero(fila[-1])} / {formatearnumero(fila[pivote_col])} = {formatearnumero(soluciones[pivote_col])}")

    return soluciones

# ---------- ENTRADAS SEGURAS ----------
def pedirEnteroPositivo(mensaje):
    """Solicita al usuario un entero positivo con validación."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor >= 1:
                return valor
            print("Ingrese un número entero mayor o igual a 1.")
        except ValueError:
            print("Entrada inválida. Ingrese un número entero.")

def pedirFilaValida(numero_fila, cantidad_elementos):
    """Solicita una fila de la matriz y valida que tenga la cantidad correcta de números."""
    while True:
        entrada = input(f"Fila {numero_fila}: ")
        partes = entrada.strip().split()
        if len(partes) != cantidad_elementos:    # Validar tamaño correcto
            print(f"Ingrese exactamente {cantidad_elementos} números.")
            continue
        try:
            fila = [Fraction(p) for p in partes] # Convertir cada valor a fracción exacta
            return fila
        except ValueError:
            print("Ingrese solo números o fracciones (ej: 1/2, -3/4, 5).")

# ---------- MAIN ----------
def main():
    print("=== Método de Eliminación de Gauss (Paso a Paso Detallado) ===")
    
    # Pedir dimensiones del sistema
    m = pedirEnteroPositivo("Número de ecuaciones: ")
    n = pedirEnteroPositivo("Número de incógnitas: ")

    # Ingreso de matriz aumentada
    print(f"\nIngrese la matriz aumentada ({m}x{n+1}):")
    matrix = [pedirFilaValida(i+1, n+1) for i in range(m)]

    imprimirMatriz(matrix, "Matriz inicial:")

    # Etapa 1: eliminación hacia forma triangular superior
    triangular = gaussEliminacionDetalle(matrix)

    imprimirMatriz(triangular, "Matriz triangular superior:")

    # Etapa 2: análisis del sistema
    estado, variables_libres = analizarSistema(triangular)

    # Etapa 3: sustitución regresiva
    soluciones = sustitucionRegresiva(triangular)

    # Mostrar conclusión
    if estado == "incompatible":
        print("\nConclusión: El sistema no tiene solución")
    elif estado == "infinitas":
        print("\nConclusión: El sistema tiene infinitas soluciones.")
        if variables_libres:
            print(f"Variables libres: {', '.join(f'x{i+1}' for i in variables_libres)}")
        if soluciones:
            print("Una posible solución parcial:")
            for i, val in enumerate(soluciones, 1):
                print(f"x{i} = {formatearnumero(val)}")
    else:
        print("\nConclusión: El sistema es de solución única.")
        for i, val in enumerate(soluciones, 1):
            print(f"x{i} = {formatearnumero(val)}")

if __name__ == "__main__":
    main()

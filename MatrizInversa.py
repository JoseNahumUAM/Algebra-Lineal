from fractions import Fraction

# ===================== FUNCIÓN PARA MOSTRAR MATRICES =====================
def mostrar_matriz(matriz, titulo=""):
    """Muestra una matriz de forma ordenada usando fracciones"""
    if titulo:
        print(titulo)
    for fila in matriz:
        print("[", end="")
        for j, elemento in enumerate(fila):
            # Mostrar fracciones de forma legible
            if isinstance(elemento, Fraction):
                if elemento.denominator == 1:
                    print(f"{elemento.numerator:>6}", end="")
                else:
                    print(f"{elemento.numerator:>3}/{elemento.denominator:<2}", end="")
            else:
                # Convertir decimales a fracciones limitadas
                if elemento == int(elemento):
                    print(f"{int(elemento):>6}", end="")
                else:
                    frac = Fraction(elemento).limit_denominator()
                    if frac.denominator == 1:
                        print(f"{frac.numerator:>6}", end="")
                    else:
                        print(f"{frac.numerator:>3}/{frac.denominator:<2}", end="")
            if j < len(fila) - 1:
                print(" ", end="")
        print(" ]")
    print()

# ===================== FUNCIONES AUXILIARES =====================
def crear_matriz_aumentada(A):
    """Crea la matriz aumentada [A | I] para el método Gauss-Jordan"""
    n = len(A)
    aumentada = []
    for i in range(n):
        fila = A[i][:]  # Copiar fila de A
        fila.extend([1 if j == i else 0 for j in range(n)])  # Agregar la matriz identidad
        aumentada.append(fila)
    return aumentada

def intercambiar_filas(matriz, i, j):
    """Intercambia dos filas de la matriz"""
    matriz[i], matriz[j] = matriz[j], matriz[i]
    return matriz

def multiplicar_fila(matriz, fila, escalar):
    """Multiplica una fila por un escalar"""
    n_columnas = len(matriz[0])
    for j in range(n_columnas):
        matriz[fila][j] *= escalar
    return matriz

def sumar_multiplo_fila(matriz, fila_destino, fila_origen, escalar):
    """Suma a una fila un múltiplo de otra fila"""
    n_columnas = len(matriz[0])
    for j in range(n_columnas):
        matriz[fila_destino][j] += escalar * matriz[fila_origen][j]
    return matriz

def encontrar_pivote(matriz, columna, fila_actual):
    """Encuentra la posición de un pivote en una columna"""
    n = len(matriz)
    for i in range(fila_actual, n):
        if matriz[i][columna] != 0:
            return i
    return -1

# ===================== CÁLCULO DE MATRIZ INVERSA =====================
def calcular_inversa(A):
    """Determina si una matriz es invertible y calcula su inversa"""
    n = len(A)
    
    print("=" * 60)
    print("CÁLCULO DE MATRIZ INVERSA")
    print("=" * 60)
    
    mostrar_matriz(A, "Matriz A =")
    
    # Si es 2x2 se usa fórmula directa
    if n == 2:
        inversa = calcular_inversa_2x2(A)
    else:
        # Para matrices mayores, usar método Gauss-Jordan
        inversa = calcular_inversa_gauss_jordan(A)
    
    # Si se obtuvo una inversa, verificar la identidad
    if inversa:
        verificar_identidad(A, inversa)
    
    return inversa

def calcular_inversa_2x2(A):
    """Calcula la inversa de una matriz 2x2 usando la fórmula directa"""
    a, b = A[0]
    c, d = A[1]
    
    # Determinante
    det = a * d - b * c
    print("PASO 1: Calcular determinante")
    print(f"det(A) = {a}×{d} - {b}×{c} = {a*d} - {b*c} = {det}")
    
    if det == 0:
        print("\n" + "=" * 60)
        print("RESULTADO FINAL: La matriz NO ES INVERTIBLE")
        print("=" * 60)
        return None
    
    print(f"\nRESULTADO: det(A) = {det} ≠ 0 → La matriz ES INVERTIBLE\n")
    
    # Fórmula de la inversa
    inversa = [
        [d/det, -b/det],
        [-c/det, a/det]
    ]
    
    mostrar_matriz(inversa, "MATRIZ INVERSA A⁻¹ =")
    return inversa

def calcular_inversa_gauss_jordan(A):
    """Calcula la inversa usando el método de Gauss-Jordan paso a paso"""
    n = len(A)
    aumentada = crear_matriz_aumentada(A)
    
    print("MÉTODO: Eliminación de Gauss-Jordan con matriz aumentada [A|I]")
    mostrar_matriz(aumentada, "Matriz aumentada [A | I]:")
    
    fila_pivote = 0
    paso = 1
    
    for col in range(n):
        print(f"\n--- COLUMNA {col+1} ---")
        
        # Buscar pivote
        fila_pivot = encontrar_pivote(aumentada, col, fila_pivote)
        
        if fila_pivot == -1:
            print("No hay pivote → matriz no invertible")
            return None
        
        # Intercambio si el pivote no está en la posición esperada
        if fila_pivot != fila_pivote:
            print(f"PASO {paso}: Intercambiar F{fila_pivote+1} ↔ F{fila_pivot+1}")
            aumentada = intercambiar_filas(aumentada, fila_pivote, fila_pivot)
            mostrar_matriz(aumentada, "Después del intercambio:")
            paso += 1
        
        # Normalizar fila pivote
        pivote = aumentada[fila_pivote][col]
        if pivote != 1:
            print(f"PASO {paso}: F{fila_pivote+1} = F{fila_pivote+1} ÷ {Fraction(pivote)}")
            aumentada = multiplicar_fila(aumentada, fila_pivote, 1/pivote)
            mostrar_matriz(aumentada, "Después de normalizar:")
            paso += 1
        
        # Eliminar los elementos de la columna actual
        for i in range(n):
            if i != fila_pivote and aumentada[i][col] != 0:
                factor = -aumentada[i][col]
                print(f"PASO {paso}: F{i+1} = F{i+1} + ({Fraction(factor)})×F{fila_pivote+1}")
                aumentada = sumar_multiplo_fila(aumentada, i, fila_pivote, factor)
                mostrar_matriz(aumentada, "Resultado:")
                paso += 1
        
        fila_pivote += 1
    
    # Extraer la matriz inversa (parte derecha de la aumentada)
    inversa = [fila[n:] for fila in aumentada]
    
    print("\n" + "=" * 60)
    print("RESULTADO FINAL: La matriz ES INVERTIBLE")
    print("=" * 60)
    mostrar_matriz(inversa, "MATRIZ INVERSA A⁻¹ =")
    
    return inversa

# ===================== VERIFICACIÓN DE LA IDENTIDAD =====================

from fractions import Fraction

# ------------------- FUNCIÓN mostrar (equivalente a imprimir_matriz) -------------------
def mostrar(matriz, titulo=None):
    """
    Imprime una matriz línea por línea.
    Compatible con elementos tipo int, float o Fraction.
    Uso: mostrar(matriz, "Título opcional")
    """
    if titulo:
        print(titulo)
    for fila in matriz:
        # Convertir cada elemento a una representación legible
        fila_str = []
        for x in fila:
            if isinstance(x, Fraction):
                if x.denominator == 1:
                    fila_str.append(str(x.numerator))
                else:
                    fila_str.append(f"{x.numerator}/{x.denominator}")
            else:
                # intentar convertir a Fraction para mostrar fracciones si aplica
                try:
                    fr = Fraction(x).limit_denominator()
                    if fr.denominator == 1:
                        fila_str.append(str(fr.numerator))
                    else:
                        fila_str.append(f"{fr.numerator}/{fr.denominator}")
                except Exception:
                    fila_str.append(str(x))
        print("[ " + "  ".join(f"{s:>6}" for s in fila_str) + " ]")
    print()

# ------------------- FUNCIÓN resolver (multiplicación paso a paso) -------------------
def resolver(A, B):
    """
    Multiplica dos matrices A x B mostrando paso a paso el cálculo de cada elemento.
    Retorna la matriz resultado con elementos tipo Fraction.
    Requisitos: len(A[0]) == len(B)
    """
    filas_A, cols_A = len(A), len(A[0])
    filas_B, cols_B = len(B), len(B[0])
    if cols_A != filas_B:
        raise ValueError("No se pueden multiplicar: columnas de A != filas de B")
    
    resultado = [[Fraction(0, 1) for _ in range(cols_B)] for _ in range(filas_A)]
    print("\n=== Paso a paso de la multiplicación (resolver) ===")
    for i in range(filas_A):
        for j in range(cols_B):
            suma = Fraction(0, 1)
            print(f"\nCalculando elemento C[{i+1}][{j+1}]:")
            for k in range(cols_A):
                # Convertir operandos a Fraction si no lo son
                a_ik = A[i][k] if isinstance(A[i][k], Fraction) else Fraction(A[i][k])
                b_kj = B[k][j] if isinstance(B[k][j], Fraction) else Fraction(B[k][j])
                
                producto = a_ik * b_kj
                suma += producto
                
                # Mostrar el producto parcial con formato de fracción
                if producto.denominator == 1:
                    prod_str = str(producto.numerator)
                else:
                    prod_str = f"{producto.numerator}/{producto.denominator}"
                print(f"  - k={k+1}: A[{i+1},{k+1}] * B[{k+1},{j+1}] = {a_ik} * {b_kj} = {prod_str}")
                # Mostrar suma acumulada como fracción legible
                if suma.denominator == 1:
                    print(f"    → Suma acumulada = {suma.numerator}")
                else:
                    print(f"    → Suma acumulada = {suma.numerator}/{suma.denominator}")
            
            resultado[i][j] = suma
            # Mostrar resultado final del elemento
            if suma.denominator == 1:
                print(f"Resultado final C[{i+1}][{j+1}] = {suma.numerator}")
            else:
                print(f"Resultado final C[{i+1}][{j+1}] = {suma.numerator}/{suma.denominator}")
    print("\n=== Fin multiplicación ===\n")
    return resultado


# ===================== FUNCIÓN PARA INGRESAR MATRICES =====================
def ingresar_matriz():
    """Permite al usuario ingresar una matriz cuadrada manualmente"""
    print("\n" + "=" * 40)
    print("INGRESO DE MATRIZ")
    print("=" * 40)
    
    n = int(input("Tamaño de la matriz cuadrada: "))
    
    print(f"\nIngrese los elementos de la matriz {n}×{n}:")
    print("• Separar números por espacios (ej: '1 2 3')")
    print("• Usar fracciones si es necesario (ej: '1/2 -3 4/5')\n")
    
    matriz = []
    for i in range(n):
        while True:
            try:
                fila_input = input(f"Fila {i+1}: ").strip()
                elementos = fila_input.split()
                fila = []
                for elemento in elementos:
                    if '/' in elemento:
                        num, den = elemento.split('/')
                        fila.append(Fraction(int(num), int(den)))
                    else:
                        fila.append(Fraction(int(elemento), 1))
                if len(fila) != n:
                    print(f"Error: Debe ingresar {n} elementos")
                    continue
                matriz.append(fila)
                break
            except (ValueError, ZeroDivisionError):
                print("Error: Ingrese números válidos (ej: 2, -3, 1/2)")
    return matriz

def verificar_identidad(A, A_inv):
    """
    Verifica que A × A⁻¹ = I mostrando paso a paso la multiplicación.
    Usa la función resolver() para mostrar cada operación.
    """
    print("\n" + "=" * 60)
    print("VERIFICACIÓN: A × A⁻¹ = I")
    print("=" * 60)
    
    mostrar(A, "Matriz A =")
    mostrar(A_inv, "Matriz A⁻¹ =")
    
    print("\nMultiplicando A × A⁻¹ para comprobar que da la identidad...\n")
    producto = resolver(A, A_inv)
    
    mostrar(producto, "Resultado A × A⁻¹ =")
    
    # Comprobación si es identidad
    n = len(producto)
    es_identidad = True
    for i in range(n):
        for j in range(n):
            if i == j and producto[i][j] != 1:
                es_identidad = False
            elif i != j and producto[i][j] != 0:
                es_identidad = False
    
    if es_identidad:
        print("Verificación exitosa: A × A⁻¹ = I")
    else:
        print("Error: A × A⁻¹ no es la identidad")

# ===================== FUNCIÓN PRINCIPAL =====================
def main():
    """Función principal del programa"""
    print("CALCULADORA DE MATRICES INVERSAS")
    print("=" * 60)
    
    while True:
        print("\nOPCIONES:")
        print("1. Calcular inversa de una matriz")
        print("2. Salir")
        
        opcion = input("\nSeleccione una opción (1-2): ").strip()
        
        if opcion == "1":
            matriz = ingresar_matriz()
            calcular_inversa(matriz)
        elif opcion == "2":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")
        
        continuar = input("\n¿Desea calcular otra matriz? (s/n): ").lower()
        if continuar != 's':
            print("¡Hasta luego!")
            break

# ===================== EJECUCIÓN =====================
if _name_ == "_main_":
    main()
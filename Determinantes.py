from fractions import Fraction

def mostrar_matriz(matriz, titulo=""):
    """Muestra una matriz de forma ordenada usando fracciones"""
    if titulo:
        print(titulo)
    for fila in matriz:
        print("[", end="")
        for j, elemento in enumerate(fila):
            if isinstance(elemento, Fraction):
                if elemento.denominator == 1:
                    print(f"{elemento.numerator:>6}", end="")
                else:
                    print(f"{elemento.numerator:>3}/{elemento.denominator:<2}", end="")
            else:
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

def obtener_submatriz(matriz, fila_eliminar, col_eliminar):
    """Obtiene la submatriz eliminando una fila y columna"""
    return [
        [matriz[i][j] for j in range(len(matriz)) if j != col_eliminar]
        for i in range(len(matriz)) if i != fila_eliminar
    ]

def es_matriz_triangular(matriz):
    """Verifica si una matriz es triangular superior"""
    n = len(matriz)
    for i in range(n):
        for j in range(i):
            if matriz[i][j] != 0:
                return False
    return True

def calcular_determinante(matriz):
    """Calcula el determinante mostrando todos los pasos en formato de matrices"""
    n = len(matriz)
    
    print("=" * 60)
    print("CÁLCULO DE DETERMINANTE")
    print("=" * 60)
    mostrar_matriz(matriz, "MATRIZ ORIGINAL:")
    
    # Caso base: matriz 1x1
    if n == 1:
        print("MATRIZ 1×1:")
        print(f"det(A) = {matriz[0][0]}")
        det = matriz[0][0]
        print("\n" + "=" * 60)
        print(f"RESULTADO: det(A) = {det}")
        print("=" * 60)
        return det
    
    # Caso base: matriz 2x2
    if n == 2:
        print("MATRIZ 2×2:")
        a, b = matriz[0]
        c, d = matriz[1]
        print("Fórmula: det(A) = a×d - b×c")
        print(f"det(A) = ({a})×({d}) - ({b})×({c})")
        print(f"       = {a*d} - {b*c}")
        det = a * d - b * c
        print(f"       = {det}")
        print("\n" + "=" * 60)
        print(f"RESULTADO: det(A) = {det}")
        print("=" * 60)
        return det
    
    # Verificar si es matriz triangular
    if es_matriz_triangular(matriz):
        print("MATRIZ TRIANGULAR:")
        print("El determinante es el producto de los elementos de la diagonal principal")
        
        # Mostrar la matriz con la diagonal resaltada
        print("Matriz triangular:")
        for i, fila in enumerate(matriz):
            print("[", end="")
            for j, elemento in enumerate(fila):
                if i == j:
                    print(f" \033[1m{elemento:>6}\033[0m", end="")  # Negrita para diagonal
                else:
                    if isinstance(elemento, Fraction):
                        if elemento.denominator == 1:
                            print(f"{elemento.numerator:>6}", end="")
                        else:
                            print(f"{elemento.numerator:>3}/{elemento.denominator:<2}", end="")
                    else:
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
        
        producto = 1
        print("Producto de la diagonal = ", end="")
        elementos_diagonal = []
        for i in range(n):
            elemento = matriz[i][i]
            producto *= elemento
            elementos_diagonal.append(str(elemento))
            if i > 0:
                print(" × ", end="")
            print(f"{elemento}", end="")
        print(f" = {producto}")
        
        det = producto
        print("\n" + "=" * 60)
        print(f"RESULTADO: det(A) = {det}")
        print("=" * 60)
        return det
    
    # Expansión por cofactores en la primera fila
    print("EXPANSIÓN POR COFACTORES EN LA PRIMERA FILA:")
    print("Fórmula: det(A) = a₁₁·det(A₁₁) - a₁₂·det(A₁₂) + a₁₃·det(A₁₃) - ...")
    print()
    
    det_total = 0
    print("DESARROLLO:")
    
    for j in range(n):
        elemento = matriz[0][j]
        signo = (-1) ** j
        submatriz = obtener_submatriz(matriz, 0, j)
        
        # Mostrar el término actual
        print(f"\nTÉRMINO {j+1}:")
        if signo > 0:
            print(f" + ({elemento}) × det(A₁{'+' if j+1>9 else ''}{j+1})")
        else:
            print(f" - ({elemento}) × det(A₁{'+' if j+1>9 else ''}{j+1})")
        
        # Mostrar la submatriz
        print(f"Submatriz A₁{'+' if j+1>9 else ''}{j+1} (eliminar fila 1, columna {j+1}):")
        mostrar_matriz(submatriz)
        
        # Calcular determinante de la submatriz
        if len(submatriz) == 1:
            det_sub = submatriz[0][0]
            print(f"det(A₁{'+' if j+1>9 else ''}{j+1}) = {det_sub}")
        elif len(submatriz) == 2:
            a, b = submatriz[0]
            c, d = submatriz[1]
            det_sub = a * d - b * c
            print(f"det(A₁{'+' if j+1>9 else ''}{j+1}) = ({a})×({d}) - ({b})×({c})")
            print(f"                = {a*d} - {b*c}")
            print(f"                = {det_sub}")
        else:
            # Para submatrices más grandes, calcular recursivamente
            print(f"Cálculo de det(A₁{'+' if j+1>9 else ''}{j+1}):")
            det_sub = calcular_determinante_simple(submatriz)
            print(f"det(A₁{'+' if j+1>9 else ''}{j+1}) = {det_sub}")
        
        termino = signo * elemento * det_sub
        print(f"Término {j+1} = {signo} × {elemento} × {det_sub} = {termino}")
        det_total += termino
        
        if j < n - 1:
            print("-" * 40)
    
    print(f"\nSUMA DE TÉRMINOS: {det_total}")
    
    print("\n" + "=" * 60)
    print(f"RESULTADO: det(A) = {det_total}")
    print("=" * 60)
    
    return det_total

def calcular_determinante_simple(matriz, nivel=1):
    """Calcula el determinante mostrando los pasos de 2×2 dentro del cálculo recursivo"""
    n = len(matriz)

    # Si es 1×1
    if n == 1:
        return matriz[0][0]
    
    # Si es 2×2 — aquí añadimos el detalle de la fórmula
    if n == 2:
        a, b = matriz[0]
        c, d = matriz[1]
        det = a * d - b * c
        print(" " * (nivel * 2) + "MATRIZ 2×2:")
        print(" " * (nivel * 2) + f"[{a} {b}]")
        print(" " * (nivel * 2) + f"[{c} {d}]")
        print(" " * (nivel * 2) + f"det = ({a})×({d}) - ({b})×({c}) = {a*d} - {b*c} = {det}")
        return det
    
    # Si es triangular, simplificar
    if es_matriz_triangular(matriz):
        producto = 1
        for i in range(n):
            producto *= matriz[i][i]
        return producto

    # Expansión por cofactores en la primera fila
    det = 0
    for j in range(n):
        signo = (-1) ** j
        submatriz = obtener_submatriz(matriz, 0, j)
        elemento = matriz[0][j]
        print(" " * (nivel * 2) + f"→ Expandiendo elemento ({elemento}) en posición (1,{j+1})")
        print(" " * (nivel * 2) + f"Submatriz resultante:")
        mostrar_matriz(submatriz)
        det_sub = calcular_determinante_simple(submatriz, nivel + 1)
        termino = signo * elemento * det_sub
        print(" " * (nivel * 2) + f"Término = {signo} × {elemento} × {det_sub} = {termino}")
        det += termino
        if j < n - 1:
            print(" " * (nivel * 2) + "-" * 30)
    
    if nivel == 1:
        print(" " * (nivel * 2) + f"→ Suma de términos (nivel {nivel}): {det}")
    return det


def ingresar_matriz():
    """Función para que el usuario ingrese una matriz"""
    print("\n" + "=" * 40)
    print("INGRESO DE MATRIZ")
    print("=" * 40)
    
    n = int(input("Tamaño de la matriz cuadrada: "))
    
    print(f"\nIngrese los elementos de la matriz {n}×{n}:")
    print("• Separar números por espacios")
    print("• Una fila por línea")
    print("• Ejemplos: '1 2 3' o '1/2 -3 4/5'")
    
    matriz = []
    for i in range(n):
        while True:
            try:
                fila_input = input(f"Fila {i+1}: ").strip()
                if not fila_input:
                    continue
                
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

def main():
    """Función principal"""
    print("CALCULADORA DE DETERMINANTES")
    print("=" * 60)
    
    while True:
        try:
            print("\nOPCIONES:")
            print("1. Calcular determinante")
            print("2. Salir")
            
            opcion = input("\nSeleccione una opción (1-2): ").strip()
            
            if opcion == "1":
                matriz = ingresar_matriz()
                det = calcular_determinante(matriz)
                
                # Mostrar interpretación del resultado
                print("\n" + "=" * 60)
                if det == 0:
                    print("INTERPRETACIÓN: det(A) = 0")
                    print("   • La matriz NO es invertible")
                    print("   • Las columnas son linealmente dependientes")
                    print("   • El sistema Ax=0 tiene soluciones no triviales")
                else:
                    print("INTERPRETACIÓN: det(A) ≠ 0")
                    print("   • La matriz ES invertible")
                    print("   • Las columnas son linealmente independientes")
                    print("   • El sistema Ax=0 tiene solo la solución trivial")
                print("=" * 60)
                
            elif opcion == "2":
                print("¡Hasta luego!")
                break
                
            else:
                print("Opción no válida. Por favor seleccione 1-2.")
                continue
            
            # Preguntar si desea continuar
            continuar = input("\n¿Calcular otro determinante? (s/n): ").lower()
            if continuar != 's':
                print("¡Hasta luego!")
                break
                    
        except KeyboardInterrupt:
            print("\nPrograma finalizado")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Por favor, intente nuevamente")

if __name__ == "__main__":
    main()
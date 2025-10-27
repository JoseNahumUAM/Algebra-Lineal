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

def calcular_determinante_simple(matriz):
    """Calcula el determinante sin mostrar el proceso"""
    n = len(matriz)
    
    if n == 1:
        return matriz[0][0]
    
    if n == 2:
        a, b = matriz[0]
        c, d = matriz[1]
        return a * d - b * c
    
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
        det += signo * matriz[0][j] * calcular_determinante_simple(submatriz)
    
    return det

def resolver_sistema_cramer(A, b):
    """Resuelve un sistema de ecuaciones usando la Regla de Cramer"""
    n = len(A)
    
    print("=" * 70)
    print("RESOLUCIÓN DE SISTEMA DE ECUACIONES - REGLA DE CRAMER")
    print("=" * 70)
    
    # Mostrar el sistema de ecuaciones
    print("SISTEMA DE ECUACIONES:")
    for i in range(n):
        ecuacion = ""
        for j in range(n):
            coef = A[i][j]
            if coef != 0:
                if ecuacion and coef > 0:
                    ecuacion += " + "
                elif ecuacion and coef < 0:
                    ecuacion += " - "
                elif not ecuacion and coef < 0:
                    ecuacion += "-"
                
                abs_coef = abs(coef)
                if abs_coef != 1:
                    if isinstance(abs_coef, Fraction) and abs_coef.denominator != 1:
                        ecuacion += f"({abs_coef})"
                    else:
                        ecuacion += f"{abs_coef}"
                ecuacion += f"x{j+1}"
        ecuacion += f" = {b[i]}"
        print(f"  {ecuacion}")
    print()
    
    # Mostrar matriz de coeficientes
    mostrar_matriz(A, "MATRIZ DE COEFICIENTES A:")
    
    # Mostrar vector de términos independientes
    print("VECTOR DE TÉRMINOS INDEPENDIENTES b:")
    for i in range(n):
        print(f"  b{i+1} = {b[i]}")
    print()
    
    # Calcular determinante de A
    print("PASO 1: Calcular el determinante de la matriz A")
    det_A = calcular_determinante_simple(A)
    print(f"det(A) = {det_A}")
    
    if det_A == 0:
        print("\n" + "=" * 70)
        print("EL SISTEMA NO TIENE SOLUCIÓN ÚNICA")
        print("   porque el determinante de A es cero")
        print("=" * 70)
        return None
    
    print(f"Como det(A) = {det_A} ≠ 0, el sistema tiene solución única")
    print()
    
    # Resolver para cada variable usando la Regla de Cramer
    soluciones = []
    
    for i in range(n):
        print(f"PASO {i+2}: Calcular x{i+1}")
        print(f"x{i+1} = det(A{i+1}) / det(A)")
        print(f"     = det(A{i+1}) / {det_A}")
        print()
        
        # Crear matriz A_i (reemplazar columna i por vector b)
        A_i = [fila[:] for fila in A]  # Copiar A
        for j in range(n):
            A_i[j][i] = b[j]
        
        print(f"Matriz A{i+1} (columna {i+1} reemplazada por b):")
        mostrar_matriz(A_i)
        
        # Calcular determinante de A_i
        det_A_i = calcular_determinante_simple(A_i)
        print(f"det(A{i+1}) = {det_A_i}")
        
        # Calcular x_i
        x_i = det_A_i / det_A
        soluciones.append(x_i)
        
        print(f"x{i+1} = {det_A_i} / {det_A} = {x_i}")
        print("-" * 50)
    
    # Mostrar solución completa
    print("\n" + "=" * 70)
    print("SOLUCIÓN DEL SISTEMA:")
    for i in range(n):
        print(f"x{i+1} = {soluciones[i]}")
    print("=" * 70)
    
    return soluciones

def ingresar_sistema_ecuaciones():
    """Función para que el usuario ingrese un sistema de ecuaciones"""
    print("\n" + "=" * 40)
    print("INGRESO DEL SISTEMA DE ECUACIONES")
    print("=" * 40)
    
    n = int(input("Número de variables (tamaño del sistema): "))
    
    print(f"\nIngrese los coeficientes de la matriz {n}×{n}:")
    print("• Separar números por espacios")
    print("• Una ecuación por línea")
    print("• Ejemplos: '1 2 3' o '1/2 -3 4/5'")
    
    A = []
    for i in range(n):
        while True:
            try:
                fila_input = input(f"Ecuación {i+1} (coeficientes): ").strip()
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
                    print(f"Error: Debe ingresar {n} coeficientes")
                    continue
                
                A.append(fila)
                break
            except (ValueError, ZeroDivisionError):
                print("Error: Ingrese números válidos (ej: 2, -3, 1/2)")
    
    print(f"\nIngrese los términos independientes (vector b):")
    b = []
    for i in range(n):
        while True:
            try:
                b_input = input(f"Término independiente {i+1}: ").strip()
                if '/' in b_input:
                    num, den = b_input.split('/')
                    b.append(Fraction(int(num), int(den)))
                else:
                    b.append(Fraction(int(b_input), 1))
                break
            except (ValueError, ZeroDivisionError):
                print("Error: Ingrese un número válido")
    
    return A, b

def main():
    """Función principal"""
    print("CALCULADORA DE SISTEMAS DE ECUACIONES")
    print("Método: Regla de Cramer")
    print("=" * 70)
    
    while True:
        try:
            print("\nOPCIONES:")
            print("1. Resolver sistema de ecuaciones")
            print("2. Salir")
            
            opcion = input("\nSeleccione una opción (1-2): ").strip()
            
            if opcion == "1":
                A, b = ingresar_sistema_ecuaciones()
                solucion = resolver_sistema_cramer(A, b)
                
                if solucion is not None:
                    # Verificar la solución
                    print("\n" + "=" * 70)
                    print("VERIFICACIÓN:")
                    print("Sustituyendo las soluciones en las ecuaciones originales:")
                    
                    for i in range(len(A)):
                        resultado = 0
                        ecuacion_verif = ""
                        for j in range(len(A)):
                            termino = A[i][j] * solucion[j]
                            resultado += termino
                            
                            if j > 0 and termino >= 0:
                                ecuacion_verif += " + "
                            elif j > 0 and termino < 0:
                                ecuacion_verif += " - "
                            elif j == 0 and termino < 0:
                                ecuacion_verif += "-"
                            
                            abs_termino = abs(termino)
                            if isinstance(abs_termino, Fraction) and abs_termino.denominator != 1:
                                ecuacion_verif += f"({abs_termino})"
                            else:
                                ecuacion_verif += f"{abs_termino}"
                        
                        print(f"  Ecuación {i+1}: {ecuacion_verif} = {resultado}")
                        print(f"  Término independiente: {b[i]}")
                        if abs(resultado - b[i]) < 1e-10:
                            print(f"  ✓ Correcto")
                        else:
                            print(f"  ✗ Diferencia: {resultado - b[i]}")
                        print()
                    
            elif opcion == "2":
                print("¡Hasta luego!")
                break
                
            else:
                print("Opción no válida. Por favor seleccione 1-2.")
                continue
            
            # Preguntar si desea continuar
            continuar = input("\n¿Resolver otro sistema? (s/n): ").lower()
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
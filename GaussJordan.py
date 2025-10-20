from fractions import Fraction   # Importar clase Fraction para manejar fracciones exactas

# ---------- utilidades ----------
def fmt(fr: Fraction):
    """Formatea Fraction: entero si denom =1, sino 'num/den' con signo."""
    if fr is None:   # caso raro: None
        return "None"
    if fr.denominator == 1:   # si el denominador es 1, se muestra como entero
        return str(fr.numerator)
    return f"{fr.numerator}/{fr.denominator}"   # si no, mostrar num/den

def imprimir_matriz(M):
    """Imprime la matriz aumentada M (coeficientes y término independiente)."""
    for fila in M:
        # formatear coeficientes
        fila_s = [fmt(x) for x in fila[:-1]]
        # imprimir fila con separación clara entre coeficientes y término independiente
        print("| " + "  ".join(f"{v:>7}" for v in fila_s) + " || " + f"{fmt(fila[-1]):>7}")
    print()

# ---------- Gauss-Jordan (RREF) con pasos ----------
def gauss_jordan_rref(M, m, n):
    """
    Aplica el método Gauss-Jordan hasta obtener RREF (forma reducida por filas).
    M: matriz aumentada de tamaño m x (n+1) con Fracciones
    m: número de ecuaciones (filas)
    n: número de incógnitas (columnas sin el término independiente)
    Devuelve la matriz en RREF, la lista de columnas pivote y el mapa columna→fila_pivote
    """
    row = 0                # fila actual que buscamos reducir
    pivot_cols = []        # lista de columnas que contienen pivotes
    col_to_row = {}        # diccionario columna→fila donde está el pivote

    print("\nMatriz inicial:")
    imprimir_matriz(M)

    # recorrer columnas de variables
    for col in range(n):
        if row >= m:   # si ya no hay filas, salimos
            break
        # buscar fila con pivote != 0 en la columna actual (desde row hacia abajo)
        sel = None
        for r in range(row, m):
            if M[r][col] != 0:
                sel = r
                break
        if sel is None:   # si no se encuentra pivote, columna libre
            continue

        # si la fila seleccionada no es la actual, se intercambian
        if sel != row:
            M[row], M[sel] = M[sel], M[row]
            print(f"Paso: F{row+1} ↔ F{sel+1}")
            imprimir_matriz(M)

        # normalizar fila pivote para que el pivote sea 1
        piv = M[row][col]
        if piv != 1:
            factor = Fraction(1, 1) / piv
            M[row] = [x * factor for x in M[row]]
            print(f"Paso: F{row+1} -> ({fmt(factor)}) * F{row+1}   (normaliza pivote {fmt(piv)} a 1)")
            imprimir_matriz(M)

        # eliminar todos los elementos distintos de 0 en esta columna (arriba y abajo)
        for r in range(m):
            if r == row:
                continue
            factor = M[r][col]
            if factor != 0:
                M[r] = [a - factor * b for a, b in zip(M[r], M[row])]
                print(f"Paso: F{r+1} -> F{r+1} - ({fmt(factor)}) * F{row+1}")
                imprimir_matriz(M)

        # guardar columna como pivote
        pivot_cols.append(col)
        col_to_row[col] = row
        row += 1   # pasar a la siguiente fila

    print("Matriz en RREF (resultado Gauss-Jordan):")
    imprimir_matriz(M)
    return M, pivot_cols, col_to_row

# ---------- análisis de soluciones ----------
def analizar_y_construir_solucion(M, m, n, pivot_cols, col_to_row):
    """
    Determina el tipo de solución:
    - inconsistente (sin solución)
    - única
    - infinitas (paramétricas)
    Devuelve también las soluciones (lista o expresiones paramétricas).
    """
    # detectar inconsistencia: fila con todos coeficientes = 0 y término independiente != 0
    for r in range(m):
        all_zero = all(M[r][c] == 0 for c in range(n))
        if all_zero and M[r][-1] != 0:
            return "inconsistente", None

    # identificar variables libres = columnas que no son pivote
    libres = [c for c in range(n) if c not in pivot_cols]
    if libres:
        # si hay libres -> soluciones infinitas
        param_names = {c: f"t{idx+1}" for idx, c in enumerate(libres)}  # asignar parámetros
        soluciones = {}

        # variables libres toman directamente su parámetro
        for c in libres:
            soluciones[c] = param_names[c]

        # variables pivote se expresan en función de las libres
        for c in pivot_cols:
            r = col_to_row[c]
            const = M[r][-1]
            terms = []
            if const != 0:
                terms.append(fmt(const))
            # restar aportes de variables libres
            for lf in libres:
                coef = M[r][lf]
                if coef != 0:
                    term_coef = -coef
                    term = f"{fmt(term_coef)}*{param_names[lf]}"
                    terms.append(term)
            expr = " + ".join(terms).replace("+ -", "- ")
            if not terms:
                expr = "0"
            soluciones[c] = expr
        return "infinitas", (soluciones, libres)

    else:
        # si todas son pivote -> solución única
        sol = [Fraction(0) for _ in range(n)]
        for c in pivot_cols:
            r = col_to_row[c]
            sol[c] = M[r][-1]
        return "unica", sol

# ---------- entrada y flujo principal ----------
def pedir_entero_positivo(mensaje):
    """Pide un número entero positivo por consola con validación."""
    while True:
        try:
            v = int(input(mensaje))
            if v >= 1:
                return v
            print("Ingrese un entero >= 1.")
        except ValueError:
            print("Entrada inválida. Intente de nuevo.")

def pedir_fila(i, esperados):
    """Pide una fila de la matriz aumentada con validación."""
    while True:
        linea = input(f"Fila {i+1} (ingrese {esperados} números separados por espacios): ").strip()
        if not linea:
            print("Entrada vacía. Intente de nuevo.")
            continue
        partes = linea.split()
        if len(partes) != esperados:
            print(f"Debe ingresar exactamente {esperados} valores (coeficientes + término independiente).")
            continue
        try:
            fila = [Fraction(p) for p in partes]   # convierte a fracción
            return fila
        except Exception:
            print("Valores inválidos. Use enteros o fracciones como 3/4, -2, 5.")

def main():
    print("=== Gauss-Jordan (RREF) paso a paso ===")
    m = pedir_entero_positivo("Número de ecuaciones (filas): ")
    n = pedir_entero_positivo("Número de variables: ")

    print(f"Ingrese cada fila con {n} coeficientes y 1 término independiente (total {n+1} números).")
    M = []
    for i in range(m):
        fila = pedir_fila(i, n+1)
        M.append(fila)

    # aplicar Gauss-Jordan
    M_rref, pivot_cols, col_to_row = gauss_jordan_rref(M, m, n)
    estado, datos = analizar_y_construir_solucion(M_rref, m, n, pivot_cols, col_to_row)

    # mostrar resultado final según el tipo de solución
    if estado == "inconsistente":
        print("\nConclusión: El sistema no tiene solución.")
        return

    if estado == "unica":
        sol = datos
        print("\nConclusión: El sistema es de solución única.")
        for i, val in enumerate(sol, start=1):
            print(f"x{i} = {fmt(val)}")
    else:
        soluciones_dict, libres = datos
        print("\nConclusión: El sistema tiene infinitas soluciones.")
        print("Variables libres:", ", ".join(f"x{c+1}" for c in libres))
        print("\nExpresiones paramétricas:")
        for c in range(n):
            if c in soluciones_dict:
                print(f"x{c+1} = {soluciones_dict[c]}")
            else:
                print(f"x{c+1} = 0")  # seguridad por si falta algo

if __name__ == "__main__":
    main()

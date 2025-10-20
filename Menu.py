import sys  # Importar módulo para funcionalidades del sistema
from Gauss import main as gaussMain  # Importar función principal de Gauss
from GaussJordan import main as gaussJordanMain  # Importar función principal de Gauss-Jordan
from SumayMultiplicaciondeMatrices import main as matricesMain  # Importar función principal de suma y multiplicación de matrices
from VectorValidacion import main as vectorMain  # Importar función principal de validación de vectores
from MatrizInversa import main as matrizInversaMain  # Importar función principal de matriz inversa
# Función que muestra el menú principal y gestiona las opciones
def menu():
    while True:  # Bucle infinito para mantener el menú activo
        print("\n===== CALCULADORA GENERAL =====")
        print("1. Resolver sistema de ecuaciones (Gauss)")
        print("2. Resolver sistema de ecuaciones (Gauss-Jordan)")
        print("3. Sumar y multiplicar matrices")
        print("4. Determinar independencia lineal de vectores")
        print("5. Calcular la inversa de una matriz")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")  # Solicitar opción al usuario

        # Ejecutar la opción seleccionada
        if opcion == "1":
            gaussMain()  # Llamar al método de Gauss
        elif opcion == "2":
            gaussJordanMain()  # Llamar al método de Gauss-Jordan
        elif opcion == "3":
            matricesMain()  # Llamar al método de suma y multiplicación de matrices
        elif opcion == "4":
            vectorMain()  # Llamar al método de matriz inversa
        elif opcion == "5":
            matrizInversaMain()  # Llamar al método de validación de vectores
        elif opcion == "0":
            print("Saliendo de la calculadora. ¡Hasta luego!")
            sys.exit()  # Salir del programa
        else:
            print("Opción inválida, intenta de nuevo.")  # Manejar opción no válida

# Punto de entrada principal del programa
if __name__ == "__main__":
    menu()  # Iniciar el menú principal
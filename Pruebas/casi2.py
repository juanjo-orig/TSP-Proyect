import math

clientes = {}
capacidades_vehiculos = []
almacen = {}
num_vehiculos = 0
num_objetos = 0 
pesos_objetos = []

def calcular_distancia(punto1, punto2):
    x1, y1 = punto1
    x2, y2 = punto2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def obtener_entero(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            return valor
        except ValueError:
            print("ERROR. Ingrese un valor entero válido.")

def obtener_float(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            return valor
        except ValueError:
            print("ERROR. Ingrese un valor numérico válido.")

def obtener_str(mensaje):
    while True:
        try:
            valor = input(mensaje)
            return valor
        except ValueError:
            print("ERROR. Ingrese un caracter válido.")

def info_clients():
    global num_objetos, pesos_objetos
    config_almacen()

    num_clientes = obtener_entero("Ingrese el numero de clientes: ")

    for i in range(1, num_clientes + 1):
        coord_x = obtener_float(f"Ingrese la coordenada X para el Cliente {i}: ")
        coord_y = obtener_float(f"Ingrese la coordenada Y para el Cliente {i}: ")
        clientes[f"C{i}"] = (coord_x, coord_y)

    print("\nAlmacén y sus coordenadas:")
    print(f"Almacén: {almacen}")

    print("\nClientes y sus coordenadas:")
    for cliente, coordenadas in clientes.items():
        print(f"{cliente}: {coordenadas}")
    
    num_objetos = obtener_entero("\nIngrese el numero de objetos que llevará: ")
    pesos_objetos = [obtener_float(f"\nIngresar el peso en KG del objeto {i+1}: ")
                    for i in range(num_objetos)]
    
    distribuir_objetos(num_vehiculos, capacidades_vehiculos, num_objetos, pesos_objetos, clientes)
    menu()

def distribuir_objetos(num_vehiculos, capacidades_vehiculos, num_objetos, pesos_objetos, clientes):
    vehiculos = {i + 1: {'capacidad': capacidades_vehiculos[i], 'objetos': []} for i in range(num_vehiculos)}
    
    objetos_ordenados = sorted(enumerate(pesos_objetos, start=1), key=lambda x: x[1], reverse=True)

    for obj, peso in objetos_ordenados:
        asignado = False
        for vehiculo, info_vehiculo in vehiculos.items():
            if info_vehiculo['capacidad'] >= peso:
                info_vehiculo['capacidad'] -= peso
                info_vehiculo['objetos'].append(obj)
                asignado = True
                break
        
        if not asignado:
            print(f"No hay vehículo disponible para el objeto {obj} con peso {peso} Kg.")

    for vehiculo, info_vehiculo in vehiculos.items():
        print(f"\nVehiculo {vehiculo}: objetos {', '.join(map(str, info_vehiculo['objetos']))}. "
              f"Total de objetos: {len(info_vehiculo['objetos'])}, Pesando en total {capacidades_vehiculos[vehiculo-1] - info_vehiculo['capacidad']} Kg")


def config_vehiculos():
    global num_vehiculos, capacidades_vehiculos

    if num_vehiculos > 0:
        edit = obtener_str("Ya se han ingresado valores para los vehiculos. ¿Desea editarlos? (S/N)").lower()
        if edit != 's':
            print("Regresando al menu...")

    num_vehiculos = obtener_entero("Ingrese el numero de vehiculos que tiene: ")
    capacidades_vehiculos.extend([obtener_float(f"Ingrese el peso que soporta el vehiculo {i+1} en KG: ") 
                          for i in range(num_vehiculos)])
    
    print("Regresando al menu...\n")
    menu()

def config_almacen():
    global almacen

    if almacen:
        edit = obtener_str("Ya se han ingresado coordenadas del almacen, ¿Desea editarlos? (S/N)").lower()
        if edit != 's':
            print("Regresando al Menu...")
    almacen_x = obtener_float("Ingrese las coordenadas X del almacen: ")
    almacen_y = obtener_float("Ingrese las coordenadas Y del almacen: ")
    almacen= (almacen_x, almacen_y)

def menu():
    print("Bienvenido\n\n")

    print("1.- Ingresar datos\n2.- Configurar Vehiculos\n3.- Salir")
    opc = obtener_entero("Ingrese una opcion: ")

    if opc == 1:
        info_clients()
    elif opc == 2:
        print("Aqui puede configurar cuantos vehiculos tiene y su capacidad")
        config_vehiculos()
    elif opc == 3:
        exit()
    else:
        print("\nERROR. Ingrese una opcion correcta")
        menu()

menu()

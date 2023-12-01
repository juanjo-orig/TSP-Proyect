import math
import networkx as nx
import matplotlib.pyplot as plt

clientes = {}
capacidades_vehiculos = []
almacen = ()
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
    global almacen

    if not almacen:
        print("Almacén no registrado, ir a configuración\nRegresando a Menú...")
        menu()

    if num_vehiculos == 0:
        print("Aún no se registran vehículos\nRegresando a Menú...")
        menu()

    num_clientes = obtener_entero("Ingrese el número de clientes: ")

    for i in range(1, num_clientes + 1):
        coord_x = obtener_float(f"Ingrese la coordenada X para el Cliente {i}: ")
        coord_y = obtener_float(f"Ingrese la coordenada Y para el Cliente {i}: ")
        clientes[f"C{i}"] = (coord_x, coord_y)

    G = crear_grafo(almacen, clientes)
    arbol_expansion_minima = nx.minimum_spanning_tree(G)

    # Visualizar el grafo y el árbol de expansión mínima
    visualizar_grafo(G, arbol_expansion_minima)

    menu()

def crear_grafo(almacen, clientes):
    G = nx.Graph()

    # Agregar nodos al grafo
    G.add_node("Almacén", pos=almacen)
    for cliente, coord in clientes.items():
        G.add_node(cliente, pos=coord)

    # Calcular distancias y agregar aristas al grafo
    for u, pos_u in G.nodes(data="pos"):
        for v, pos_v in G.nodes(data="pos"):
            if u != v:
                distancia = calcular_distancia(pos_u, pos_v)
                G.add_edge(u, v, weight=distancia)

    return G

def visualizar_grafo(G, arbol_expansion_minima):
    posiciones = nx.get_node_attributes(G, 'pos')
    labels = nx.get_edge_attributes(G, 'weight')

    nx.draw(G, posiciones, with_labels=True)
    nx.draw_networkx_edge_labels(G, posiciones, edge_labels=labels)
    nx.draw_networkx_edges(arbol_expansion_minima, posiciones, edge_color='r', width=2)

    plt.show()

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
        edit= obtener_str("Ya se han ingresado valores para los vehiculos. ¿Desea editarlos? 'S' para editar. Enter o cualquier caracter para salir").lower()
        if edit != 's':
            print("Regresando al menu...")
            menu()

    num_vehiculos = obtener_entero("Ingrese el numero de vehiculos que tiene: ")
    capacidades_vehiculos.extend([obtener_float(f"Ingrese el peso que soporta el vehiculo {i+1} en KG: ") 
                          for i in range(num_vehiculos)])
    
    print("Regresando al menu...\n")
    menu()

def config_almacen():
    global almacen

    if not almacen:  
        almacen_x= obtener_float("Ingrese las coordenadas X del almacen: ")
        almacen_y= obtener_float("Ingrese las coordenadas Y del almacen: ")
        almacen= (almacen_x, almacen_y)
        
        print(f"Almacén: {almacen}")
            
        menu()
    
    edit= obtener_str("Ya se han ingresado coordenadas del almacen, ¿Desea editarlos? 'S' para editar. Enter o cualquier caracter para salir").lower()
    if edit != 's':
        print("Regresando al Menu...")
        menu()


def menu():
    print("\nBienvenido\n\n")

    print("1.- Ingresar datos\n2.- Configuración\n3.- Salir")
    opc=obtener_entero("Ingrese una opcion: ")

    if opc == 1:
        info_clients()
    elif opc == 2:
        print("\n1.- Configurar almacen\n2.- Configurar vehiculos\n")
        opc= obtener_entero("\nIngrese una opcion: ")
        if opc == 1:
            config_almacen()
        elif opc == 2:  
            config_vehiculos()
        else:
            print("\nERROR. Ingrese una opcion correcta")
    elif opc == 3:
        exit()
    else:
        print("\nERROR. Ingrese una opcion correcta")
        menu()

menu()
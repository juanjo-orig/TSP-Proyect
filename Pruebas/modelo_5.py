import networkx as nx
import folium
import math

clientes = {}
capacidades_vehiculos = []
almacen = (0, 0)
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

def obtener_ruta_prim(G):
    MST = nx.minimum_spanning_tree(G)
    ruta = list(nx.dfs_preorder_nodes(MST, source="Almacén"))
    return ruta

def dibujar_ruta_folium(mapa, ruta, color, posiciones):
    coordenadas_ruta = [posiciones[nodo] for nodo in ruta]
    folium.PolyLine(locations=coordenadas_ruta, color=color, weight=5, opacity=1).add_to(mapa)

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
    
def mapa():
    G = nx.Graph()
    posiciones = {}  # Nuevo diccionario para almacenar las posiciones de los nodos

    # Agregar nodos y aristas al grafo G y posiciones
    for cliente, coord_cliente in clientes.items():
        G.add_node(cliente)
        G.add_edge("Almacén", cliente, weight=calcular_distancia(almacen, coord_cliente))
        posiciones[cliente] = coord_cliente
    posiciones["Almacén"] = almacen

    # Calcular rutas utilizando el árbol de expansión mínima (Prim)
    ruta_prim = obtener_ruta_prim(G)

    # Imprimir la ruta del árbol de expansión mínima
    print(f"\nRuta del árbol de expansión mínima (Prim): {' -> '.join(ruta_prim)}")

    # Crear un mapa folium
    mapa = folium.Map(location=almacen, zoom_start=12)

    # Dibujar la ruta del árbol de expansión mínima en el mapa
    dibujar_ruta_folium(mapa, ruta_prim, color='blue', posiciones=posiciones)

    # Calcular rutas más cortas desde el almacén a cada cliente
    rutas_entrega = {}
    for cliente in clientes:
        ruta = obtener_ruta(G, "Almacén", cliente)
        rutas_entrega[cliente] = ruta

    # Obtener el orden de visita de los clientes para minimizar la distancia total
    clientes_ordenados = obtener_orden_visita_clientes(G, rutas_entrega)

    # Construir la ruta completa que visita todos los clientes antes de regresar al almacén
    ruta_completa = ["Almacén"] + [cliente for cliente in clientes_ordenados] + ["Almacén"]

    # Imprimir la ruta de entrega completa
    print(f"\nRuta de entrega: {' -> '.join(ruta_completa)}")

    # Dibujar la ruta de entrega en el mapa folium
    dibujar_ruta_folium(mapa, ruta_completa, color='green', posiciones=posiciones)

    # Mostrar el mapa folium
    mapa.save('ruta_entrega.html')

def obtener_orden_visita_clientes(G, rutas_entrega):
    return sorted(rutas_entrega.keys(), key=lambda cliente: calcular_distancia_entrega(G, rutas_entrega[cliente]))

def calcular_distancia_entrega(G, ruta):
    distancia = 0
    for i in range(len(ruta) - 1):
        distancia += G[ruta[i]][ruta[i+1]]['weight']
    return distancia

def obtener_ruta(G, origen, destino):
    ruta = nx.shortest_path(G, source=origen, target=destino, weight='weight')
    return ruta

def config_vehiculos():
    global num_vehiculos, capacidades_vehiculos

    if num_vehiculos > 0:
        edit = obtener_str("Ya se han ingresado valores para los vehiculos. ¿Desea editarlos? 'S' para editar. Enter o cualquier caracter para salir").lower()
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

    if almacen != (0, 0):
        edit = obtener_str("Ya se han ingresado coordenadas del almacen, ¿Desea editarlos? 'S' para editar. Enter o cualquier caracter para salir").lower()
        if edit != 's':
            print("Regresando al Menu...")
            menu()

    almacen_x = obtener_float("Ingrese las coordenadas X del almacen: ")
    almacen_y = obtener_float("Ingrese las coordenadas Y del almacen: ")
    almacen = (almacen_x, almacen_y)
    
    print(f"Almacén: {almacen}")
            
    menu()

def info_clients():
    if almacen == (0, 0):
        print("Almacen no registrado, ir a configuracion\nRegresando a Menu...")
        menu()
    if num_vehiculos == 0:
        print("Aun no registra vehiculos\nRegresando a Menu...")
        menu()

    num_clientes = obtener_entero("Ingrese el numero de clientes: ")

    for i in range(1, num_clientes + 1):
        coord_x = obtener_float(f"Ingrese la coordenada X para el Cliente {i}: ")
        coord_y = obtener_float(f"Ingrese la coordenada Y para el Cliente {i}: ")
        clientes[f"C{i}"] = (coord_x, coord_y)
    
    num_objetos = obtener_entero("\nIngrese el numero de objetos que llevará: ")
    pesos_objetos = [obtener_float(f"\nIngresar el peso en KG del objeto {i+1}: ")
                    for i in range(num_objetos)]
    
    print(f"Almacén: {almacen}")
    print("\nClientes y sus coordenadas:")
    for cliente, coordenadas in clientes.items():
        print(f"{cliente}: {coordenadas}")
    
    distribuir_objetos(num_vehiculos, capacidades_vehiculos, num_objetos, pesos_objetos, clientes)

    mapa()
    print("Se ha generado un archivo de la ruta")

    print("Volviendo al menu...")
    menu()

def menu():
    print("\nBienvenido\n\n")

    print("1.- Ingresar datos\n2.- Configuración\n3.- Salir")
    opc = obtener_entero("Ingrese una opcion: ")

    if opc == 1:
        info_clients()
    elif opc == 2:
        print("\n1.- Configurar almacen\n2.- Configurar vehiculos\n")
        opc = obtener_entero("\nIngrese una opcion: ")
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

if __name__ == "__main__":
    menu()
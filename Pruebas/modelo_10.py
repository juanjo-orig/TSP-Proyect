# Autor: Juan José Garcia Gutiérrez

# Importar las bibliotecas necesarias
import networkx as nx
import folium
import math
import webbrowser

# Inicialización de variables
clientes = {}
capacidades_vehiculos = []
almacen = (0, 0)
num_vehiculos = 0
num_objetos = 0
pesos_objetos = []

# Función para calcular la distancia entre dos puntos
def calcular_distancia(punto1, punto2):
    x1, y1 = punto1
    x2, y2 = punto2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Funciones para obtener valores del usuario con manejo de errores
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

# Funciones para construir y visualizar rutas
def obtener_ruta_prim(G):
    # Crear un árbol de expansión mínima utilizando el algoritmo de Prim
    MST = nx.minimum_spanning_tree(G)
    # Obtener una ruta DFS (Depth-First Search) a partir del árbol de expansión mínima
    ruta = list(nx.dfs_preorder_nodes(MST, source="Almacén"))
    return ruta

def dibujar_ruta_folium(mapa, ruta, posiciones, etiquetas, color):
    # Obtener las coordenadas de la ruta
    coordenadas_ruta = [posiciones[nodo] for nodo in ruta]

    # Dibujar la ruta en el mapa folium
    folium.PolyLine(locations=coordenadas_ruta, color=color, weight=5, opacity=1).add_to(mapa)

    # Agregar marcadores en cada nodo de la ruta
    for nodo in ruta:
        folium.Marker(location=posiciones[nodo], popup=etiquetas[nodo], icon=folium.Icon(color='red')).add_to(mapa)

# Funciones para la distribución de objetos y cálculo de rutas
def distribuir_objetos(num_vehiculos, capacidades_vehiculos, num_objetos, pesos_objetos, clientes):
    # Inicializar información sobre los vehículos
    vehiculos = {i + 1: {'capacidad': capacidades_vehiculos[i], 'objetos': []} for i in range(num_vehiculos)}
    
    # Ordenar los objetos de mayor a menor peso
    objetos_ordenados = sorted(enumerate(pesos_objetos, start=1), key=lambda x: x[1], reverse=True)

    # Asignar objetos a los vehículos según su capacidad
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

    # Mostrar la distribución de objetos en cada vehículo
    for vehiculo, info_vehiculo in vehiculos.items():
        print(f"\nVehiculo {vehiculo}: objetos {', '.join(map(str, info_vehiculo['objetos']))}. "
              f"Total de objetos: {len(info_vehiculo['objetos'])}, Pesando en total {capacidades_vehiculos[vehiculo-1] - info_vehiculo['capacidad']} Kg")
    
    # Visualizar la ruta en el mapa
    mapa()

def mapa():
    G = nx.Graph()
    posiciones = {}
    etiquetas = {}

    for cliente, coord_cliente in clientes.items():
        G.add_node(cliente)
        G.add_edge("Almacén", cliente, weight=calcular_distancia(almacen, coord_cliente))
        posiciones[cliente] = coord_cliente
        etiquetas[cliente] = cliente
    posiciones["Almacén"] = almacen
    etiquetas["Almacén"] = "Almacén"

    ruta_prim = obtener_ruta_prim(G)
    print(f"\nRuta de Entrega: {' -> '.join(ruta_prim)}")

    # Crear el mapa folium
    mapa_folium = folium.Map(location=almacen, zoom_start=12)

    # Dibujar la ruta del árbol de expansión mínima
    dibujar_ruta_folium(mapa_folium, ruta_prim, posiciones, etiquetas, color='blue')

    rutas_entrega = {}
    for cliente in clientes:
        ruta = obtener_ruta(G, "Almacén", cliente)
        rutas_entrega[cliente] = ruta

    clientes_ordenados = obtener_orden_visita_clientes(G, rutas_entrega)
    ruta_completa = ["Almacén"] + [cliente for cliente in clientes_ordenados] + ["Almacén"]

    # Dibujar la ruta de entrega
    dibujar_ruta_folium(mapa_folium, ruta_completa, posiciones, etiquetas, color='green')

    # Guardar el mapa en un archivo HTML (opcional)
    mapa_folium.save('ruta_entrega.html')

    # Abre el mapa en el navegador web local
    mapa_folium.save('ruta_entrega.html')
    webbrowser.open('ruta_entrega.html')

    # Esta línea es solo necesaria si ejecutas este script desde la consola.
    input("Presiona Enter para salir...")


def obtener_orden_visita_clientes(G, rutas_entrega):
    # Ordenar los clientes según la distancia de entrega
    return sorted(rutas_entrega.keys(), key=lambda cliente: calcular_distancia_entrega(G, rutas_entrega[cliente]))

def calcular_distancia_entrega(G, ruta):
    # Calcular la distancia total de entrega para una ruta dada
    distancia = 0
    for i in range(len(ruta) - 1):
        distancia += G[ruta[i]][ruta[i+1]]['weight']
    return distancia

def obtener_ruta(G, origen, destino):
    # Obtener la ruta más corta entre dos nodos en el grafo G
    ruta = nx.shortest_path(G, source=origen, target=destino, weight='weight')
    return ruta

def config_vehiculos():
    global num_vehiculos, capacidades_vehiculos

    # Verificar si ya se han ingresado valores para los vehículos
    if num_vehiculos > 0:
        edit = obtener_str("Ya se han ingresado valores para los vehículos. ¿Desea editarlos? 'S' para editar. Enter o cualquier caracter para salir").lower()
        if edit != 's':
            print("Regresando al menú...")
            menu()

    # Ingresar el número de vehículos y sus capacidades
    num_vehiculos = obtener_entero("Ingrese el número de vehículos que tiene: ")
    capacidades_vehiculos.extend([obtener_float(f"Ingrese el peso que soporta el vehículo {i+1} en KG: ") 
                          for i in range(num_vehiculos)])
    
    print("Regresando al menú...\n")
    menu()

def config_almacen():
    global almacen

    # Verificar si ya se han ingresado coordenadas del almacén
    if almacen != (0, 0):
        edit = obtener_str("Ya se han ingresado coordenadas del almacén. ¿Desea editarlos? 'S' para editar. Enter o cualquier caracter para salir").lower()
        if edit != 's':
            print("Regresando al Menú...")
            menu()

    # Ingresar las coordenadas del almacén
    coords = input("Ingrese las coordenadas (X, Y) del almacén separadas por coma: ")
    almacen_x, almacen_y = map(float, coords.split(','))
    almacen = (almacen_x, almacen_y)

    print(f"Almacén: {almacen}")

    menu()

def info_clients():
    global clientes

    # Verificar si el almacén y los vehículos están registrados
    if almacen == (0, 0):
        print("Almacén no registrado, ir a configuración\nRegresando a Menú...")
        menu()

    if num_vehiculos == 0:
        print("Aún no registra vehículos\nRegresando a Menú...")
        menu()

    # Preguntar al usuario si desea agregar más clientes o hacer una nueva ruta
    agregar_clientes = obtener_str("¿Desea hacer una nueva ruta? 'S', Enter o cualquier caracter para agregar más clientes: ").lower()

    # Reiniciar la variable clientes solo si se va a agregar más clientes
    if agregar_clientes == 's':
        clientes_nuevos = {}
        num_clientes = obtener_entero("Ingrese el número de nuevos clientes: ")

        for i in range(1, num_clientes + 1):
            while True:
                coords = input(f"Ingrese las coordenadas (X, Y) para el Cliente {i} separadas por coma: ")
                if ',' in coords:
                    coord_x, coord_y = map(float, coords.split(','))
                    clientes_nuevos[f"C{i}"] = (coord_x, coord_y)
                    break
                else:
                    print("ERROR. Debe ingresar las coordenadas separadas por coma.")

        # Agregar los nuevos clientes a la lista existente
        clientes.update(clientes_nuevos)

    num_objetos = obtener_entero("\nIngrese el número de objetos que llevará: ")
    pesos_objetos = [obtener_float(f"\nIngresar el peso en KG del objeto {i+1}: ")
                    for i in range(num_objetos)]

    # Mostrar la información del almacén, clientes y realizar la distribución de objetos
    print(f"Almacén: {almacen}")
    print("\nClientes y sus coordenadas:")
    for cliente, coordenadas in clientes.items():
        print(f"{cliente}: {coordenadas}")

    distribuir_objetos(num_vehiculos, capacidades_vehiculos, num_objetos, pesos_objetos, clientes)

    print("Se ha generado un archivo de la ruta\n")

    print("Volviendo al menú...")
    menu()

def menu():
    print("\nBienvenido\n\n")

    # Menú principal
    print("1.- Ingresar datos\n2.- Configuración\n3.- Salir")
    opc = obtener_entero("Ingrese una opción: ")

    # Opciones del menú
    if opc == 1:
        info_clients()
    elif opc == 2:
        print("\n1.- Configurar almacén\n2.- Configurar vehículos\n")
        opc = obtener_entero("\nIngrese una opción: ")
        if opc == 1:
            config_almacen()
        elif opc == 2:
            config_vehiculos()
        else:
            print("\nERROR. Ingrese una opción correcta")
    elif opc == 3:
        exit()
    else:
        print("\nERROR. Ingrese una opción correcta")
        menu()

# Inicio del programa
if __name__ == "__main__":
    menu()

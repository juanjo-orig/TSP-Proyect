import networkx as nx
import matplotlib.pyplot as plt

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
        print(f"Vehiculo {vehiculo}: objetos {', '.join(map(str, info_vehiculo['objetos']))}. "
              f"Total de objetos: {len(info_vehiculo['objetos'])}, Pesando en total {capacidades_vehiculos[vehiculo-1] - info_vehiculo['capacidad']} Kg")


def calcular_distancia(coordenadas1, coordenadas2):
    return ((coordenadas1[0] - coordenadas2[0])**2 + (coordenadas1[1] - coordenadas2[1])**2)**0.5

def prim_algorithm(clientes, almacen):
    G = nx.Graph()

    for cliente, coordenadas in clientes.items():
        G.add_node(cliente, pos=coordenadas)
    
    G.add_node('almacen', pos=almacen)

    for cliente1, coord1 in clientes.items():
        for cliente2, coord2 in clientes.items():
            if cliente1 != cliente2:
                distancia = calcular_distancia(coord1, coord2)
                G.add_edge(cliente1, cliente2, weight=distancia)

    for cliente, coord in clientes.items():
        distancia_almacen = calcular_distancia(coord, almacen)
        G.add_edge('almacen', cliente, weight=distancia_almacen)

    MST = nx.minimum_spanning_tree(G)

    pos = nx.get_node_attributes(MST, 'pos')
    nx.draw(MST, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_color='black', font_size=8, edge_color='gray', width=1.5, alpha=0.7)
    labels = nx.get_edge_attributes(MST, 'weight')
    nx.draw_networkx_edge_labels(MST, pos, edge_labels=labels, font_color='red')

    plt.title('Rutas de entrega con el árbol de expansión mínima')
    plt.show()

if __name__ == "__main__":
    num_clientes = int(input("Ingrese el numero de clientes: "))
    clientes = {i + 1: tuple(map(float, input(f"Ingrese las coordenadas del cliente {i + 1} (latitud, longitud): ").split(','))) for i in range(num_clientes)}

    almacen = tuple(map(float, input("Ingrese las coordenadas del almacén (latitud, longitud): ").split(',')))

    num_vehiculos = int(input("Ingrese el numero de vehiculos: "))
    capacidades_vehiculos = [float(input(f"Ingrese el peso que soporta el vehiculo {i+1} en KG: ")) for i in range(num_vehiculos)]

    num_objetos = int(input("Ingrese el numero de objetos que llevará: "))
    pesos_objetos = [float(input(f"Ingrese el peso en Kg del objeto {i+1}: ")) for i in range(num_objetos)]

    distribuir_objetos(num_vehiculos, capacidades_vehiculos, num_objetos, pesos_objetos, clientes)

    prim_algorithm(clientes, almacen)

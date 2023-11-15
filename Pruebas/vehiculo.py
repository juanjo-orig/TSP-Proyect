#Prueba del algoritmo de la mochila 
#Pero con vehiculos para el proyecto
def distribuir_objetos(num_vehiculos, capacidades_vehiculos, num_objetos, pesos_objetos):
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


if __name__ == "__main__":
    num_vehiculos = int(input("Ingrese el numero de vehiculos: "))
    capacidades_vehiculos = [float(input(f"Ingrese el peso que soporta el vehiculo {i+1} en KG: ")) for i in range(num_vehiculos)]

    num_objetos = int(input("Ingrese el numero de objetos que llevará: "))
    pesos_objetos = [float(input(f"Ingrese el peso en Kg del objeto {i+1}: ")) for i in range(num_objetos)]

    distribuir_objetos(num_vehiculos, capacidades_vehiculos, num_objetos, pesos_objetos)
    
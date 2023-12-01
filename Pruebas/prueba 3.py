import math

def calcular_distancia(punto1, punto2):
    x1, y1 = punto1
    x2, y2 = punto2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def prim(distancias):
    n = len(distancias)
    visitado = [False] * n
    visitado[0] = True
    ruta = [0]
    
    while len(ruta) < n:
        menor_peso = float('inf')
        mejor_nodo = None
        
        for i in range(n):
            if visitado[i]:
                for j in range(n):
                    if not visitado[j] and distancias[i][j] < menor_peso:
                        menor_peso = distancias[i][j]
                        mejor_nodo = j
        
        ruta.append(mejor_nodo)
        visitado[mejor_nodo] = True
    
    return ruta

def fuerza_bruta_mochila(capacidad_vehiculo, objetos):
    mejor_asignacion = None
    mejor_peso_total = float('-inf')
    
    for asignacion_posible in range(2 ** len(objetos)):
        peso_total = 0
        asignacion_actual = []
        
        for i in range(len(objetos)):
            if (asignacion_posible >> i) & 1:
                asignacion_actual.append(objetos[i])
                peso_total += objetos[i][1]
        
        if peso_total <= capacidad_vehiculo and peso_total > mejor_peso_total:
            mejor_asignacion = asignacion_actual
            mejor_peso_total = peso_total
    
    return mejor_asignacion

# Preguntar al usuario el número de clientes
num_clientes = int(input("Ingrese el número de clientes: "))

# Preguntar al usuario las coordenadas de los clientes
clientes = {}
for i in range(1, num_clientes + 1):
    coord_x = float(input(f"Ingrese la coordenada x para el Cliente {i}: "))
    coord_y = float(input(f"Ingrese la coordenada y para el Cliente {i}: "))
    clientes[f"C{i}"] = (coord_x, coord_y)

# Calcular distancias entre todos los puntos
distancias = [[calcular_distancia(clientes[i], clientes[j]) for j in clientes] for i in clientes]

# Ordenar los clientes según su proximidad al almacén
orden_clientes = prim(distancias)

# Preguntar al usuario el número de vehículos y sus capacidades
num_vehiculos = int(input("Ingrese el número de vehículos: "))
capacidades_vehiculos = {}
for i in range(1, num_vehiculos + 1):
    capacidad = float(input(f"Ingrese la capacidad en KG del Vehículo {i}: "))
    capacidades_vehiculos[i] = capacidad

# Inicializar variables para la asignación de objetos a vehículos
objetos_por_cliente = {}
for cliente in clientes:
    objetos_por_cliente[cliente] = []

# Preguntar al usuario qué objetos entregar y su peso por cliente
for cliente in clientes:
    while True:
        objeto = input(f"Ingrese el nombre del objeto para {cliente} (o 'fin' para terminar): ")
        if objeto.lower() == 'fin':
            break
        peso = float(input(f"Ingrese el peso en KG del objeto para {cliente}: "))
        objetos_por_cliente[cliente].append((objeto, peso))

# Asignar objetos a vehículos utilizando fuerza bruta
asignacion_total = []
for cliente, objetos in objetos_por_cliente.items():
    asignacion_cliente = fuerza_bruta_mochila(capacidades_vehiculos[int(cliente[1])], objetos)
    asignacion_total.extend(asignacion_cliente)

# Imprimir resultados
print("\nRuta óptima de entrega:")
for i in orden_clientes:
    print(f"Cliente {i}: {clientes[f'C{i}']}")

print("\nAsignación óptima de objetos a vehículos:")
for vehiculo, capacidad in capacidades_vehiculos.items():
    print(f"\nVehículo {vehiculo} (Capacidad: {capacidad} KG):")
    for obj, peso in asignacion_total:
        if obj.startswith(f"Vehiculo {vehiculo}"):
            print(f"- {obj} ({peso} KG)")

print("\nDistancia total de la ruta óptima:")
distancia_total_optima = sum(distancias[orden_clientes[i]][orden_clientes[i + 1]] for i in range(len(orden_clientes) - 1))
print(distancia_total_optima)

#Autor: Ruiz Hernandez Oscar Alejandro
#Autor: Juan José Garcia Gutiérrez

import networkx as nx
import folium
import math
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox

clientes = {}
almacen = (0, 0)
num_vehiculos = 0
num_objetos = 0
capacidades_vehiculos = []
coordenadas_x_clientes = []
coordenadas_y_clientes = []
pesos_objetos = []

class InterfazGrafica(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Servicio de Entregas Locales")
        self.geometry("700x400")

        self.frame_inicio = ttk.Frame(self)
        self.frame_inicio.grid(row=1, column=0, sticky="nsew")

        self.frame_cantidad_clientes = ttk.Frame(self)
        self.frame_cantidad_clientes.grid(row=1, column=0, sticky="nsew")

        self.frame_coordenadas_clientes = ttk.Frame(self)
        self.frame_coordenadas_clientes.grid(row=1, column=0, sticky="nsew")

        self.frame_cantidad_de_objetos = ttk.Frame(self)
        self.frame_cantidad_de_objetos.grid(row=1, column=0, sticky="nsew")

        self.frame_cantidad_de_objetos_pesos = ttk.Frame(self)
        self.frame_cantidad_de_objetos_pesos.grid(row=1, column=0, sticky="nsew")

        self.frame_resultados_finales = ttk.Frame(self)
        self.frame_resultados_finales.grid(row=1, column=0, sticky="nsew")

        self.etiqueta_iniciar_programa= ttk.Label(self.frame_cantidad_clientes, text="Iniciando programa")
        self.etiqueta_iniciar_programa.grid(row=0, column=0, padx=300, pady=20)

        self.label_cantidad_clientes = ttk.Label(self.frame_cantidad_clientes, text="Ingrese el numero de clientes:")
        self.entry_cantidad_clientes = ttk.Entry(self.frame_cantidad_clientes)
        self.label_cantidad_clientes.grid(row=2, column=0, pady=10, ipadx=150, columnspan=2)
        self.entry_cantidad_clientes.grid(row=2, column=0, pady=10, padx=(300, 0))

        self.btn_guardar_cantidad_clientes = ttk.Button(
            self.frame_cantidad_clientes,
            text="Continuar",
            command=self.guardar_cantidad_clientes,
            width=50
        )
        self.btn_guardar_cantidad_clientes.grid(row=3 ,column=0, pady=20)

        self.etiqueta_cantidad_clientes = ttk.Label(self.frame_coordenadas_clientes, text="Coordenadas de los clientes")
        self.etiqueta_cantidad_clientes.grid(row=0, column=1, padx=50, pady=20)

        self.btn_guardar_coordenadas_clientes = ttk.Button(
            self.frame_coordenadas_clientes,
            text="Continuar",
            command=self.guardar_coordenadas_clientes,
            width=50
        )

        self.etiqueta_cantidad_objetos= ttk.Label(self.frame_cantidad_de_objetos, text="Cantidad de objetos")
        self.etiqueta_cantidad_objetos.grid(row=0, column=0, padx=300, pady=20)
 
        self.label_cantidad_objetos = ttk.Label(self.frame_cantidad_de_objetos, text="Ingrese el numero de objetos:")
        self.entry_cantidad_objetos = ttk.Entry(self.frame_cantidad_de_objetos)
        self.label_cantidad_objetos.grid(row=2, column=0, pady=10, ipadx=150, columnspan=2)
        self.entry_cantidad_objetos.grid(row=2, column=0, pady=10, padx=(300, 0))

        self.btn_guardar_cantidad_objetos = ttk.Button(
            self.frame_cantidad_de_objetos,
            text="Continuar",
            command=self.guardar_cantidad_objetos,
            width=50
        )
        self.btn_guardar_cantidad_objetos.grid(row=3, column=0, pady=20)

        self.etiqueta_pesos_objetos = ttk.Label(self.frame_cantidad_de_objetos_pesos, text="Pesos (kg) de los objetos")
        self.etiqueta_pesos_objetos.grid(row=0, column=1, padx=50, pady=20)

        self.btn_guardar_pesos_objetos = ttk.Button(
            self.frame_cantidad_de_objetos_pesos,
            text="Continuar",
            command=self.guardar_pesos_objetos,
            width=50
        )

        self.etiqueta_resultados_finales = ttk.Label(self.frame_resultados_finales, text="Resultados de entregas locales")

        self.frame_configuracion = ttk.Frame(self)
        self.frame_configuracion.grid(row=1, column=0, sticky="nsew")

        self.frame_configuracion_almacen = ttk.Frame(self)
        self.frame_configuracion_almacen.grid(row=1, column=0, sticky="nsew")

        self.label_almacen_x = ttk.Label(self.frame_configuracion_almacen, text="Ingrese las coordenadas X del almacen:")
        self.entry_almacen_x = ttk.Entry(self.frame_configuracion_almacen)
        self.label_almacen_y = ttk.Label(self.frame_configuracion_almacen, text="Ingrese las coordenadas Y del almacen:")
        self.entry_almacen_y = ttk.Entry(self.frame_configuracion_almacen)

        self.frame_configuracion_vehiculos = ttk.Frame(self)
        self.frame_configuracion_vehiculos.grid(row=1, column=0, sticky="nsew")

        self.frame_configuracion_vehiculos_pesos = ttk.Frame(self)
        self.frame_configuracion_vehiculos_pesos.grid(row=1, column=0, sticky="nsew")

        self.btn_iniciar = ttk.Button(self, text="Iniciar programa", command=self.iniciar_programa, width=50)
        self.btn_configuracion = ttk.Button(self, text="Configuración del programa", command=self.configuracion_programa, width=50)
        self.btn_salir = ttk.Button(self, text="Salir del programa", command=self.salir_programa, width=50)

        self.btn_iniciar.grid(row=1, column=0, pady=10)
        self.btn_configuracion.grid(row=2, column=0, pady=10)
        self.btn_salir.grid(row=3, column=0, pady=10)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        self.etiqueta_configuracion = ttk.Label(self.frame_configuracion, text="Configuración del programa")
        self.etiqueta_configuracion.grid(row=0, column=0, padx=20, pady=20)
        self.btn_configuracion_almacen = ttk.Button(self.frame_configuracion, text="Configurar almacen", command=self.configuracion_programa_almacen, width=50)
        self.btn_configuracion_vehiculo = ttk.Button(self.frame_configuracion, text="Configurar vehiculos", command=self.configuracion_programa_vehiculos, width=50)

        self.etiqueta_configuracion_almacen = ttk.Label(self.frame_configuracion_almacen, text="Configuracion del almacen")
        self.etiqueta_configuracion_almacen.grid(row=0, column=0, padx=20, pady=20)

        self.label_almacen_x.grid(row=1, column=0, pady=10, ipadx=100, columnspan=2)
        self.entry_almacen_x.grid(row=1, column=0, pady=10, padx=(270, 0))
        self.label_almacen_y.grid(row=2, column=0, pady=10, ipadx=100, columnspan=2)
        self.entry_almacen_y.grid(row=2, column=0, pady=10, padx=(270, 0))

        self.btn_guardar_configuracion_almacen = ttk.Button(
            self.frame_configuracion_almacen,
            text="Guardar configuración",
            command=self.guardar_configuracion_almacen,
            width=50
        )
        self.btn_guardar_configuracion_almacen.grid(row=3, column=0, pady=20)

        self.etiqueta_configuracion_vehiculos = ttk.Label(self.frame_configuracion_vehiculos, text="Configuracion de vehiculos")
        self.etiqueta_configuracion_vehiculos.grid(row=0, column=0, padx=20, pady=20)

        self.etiqueta_configuracion_vehiculos_pesos = ttk.Label(self.frame_configuracion_vehiculos_pesos, text="Configuracion de pesos (kg) de los vehiculos")
        self.etiqueta_configuracion_vehiculos_pesos.grid(row=0, column=1, padx=20, pady=20)

        self.label_cantidad_vehiculos = ttk.Label(self.frame_configuracion_vehiculos, text="Ingrese el numero de vehiculos que tiene:")
        self.entry_cantidad_vehiculos = ttk.Entry(self.frame_configuracion_vehiculos)
        self.label_cantidad_vehiculos.grid(row=2, column=0, pady=10, ipadx=100, columnspan=2)
        self.entry_cantidad_vehiculos.grid(row=2, column=0, pady=10, padx=(270, 0))

        self.btn_guardar_configuracion_vehiculos = ttk.Button(
            self.frame_configuracion_vehiculos,
            text="Continuar",
            command=self.guardar_configuracion_vehiculos,
            width=50
        )
        self.btn_guardar_configuracion_vehiculos.grid(row=3, column=0, pady=20)

        self.btn_guardar_configuracion_vehiculos_pesos = ttk.Button(
            self.frame_configuracion_vehiculos_pesos,
            text="Guardar configuración",
            command=self.guardar_configuracion_vehiculos_pesos,
            width=50
        )

        self.btn_regresar_menu_principal = ttk.Button(self.frame_cantidad_clientes, text="Regresar al Menú Principal", command=self.mostrar_inicio, width=50)
        self.btn_regresar_menu_principal.grid(row=4, column=0, pady=10)

        self.btn_regresar_menu_anterior = ttk.Button(self.frame_coordenadas_clientes, text="Regresar al Menú anterior", command=self.iniciar_programa, width=50)

        self.btn_regresar_menu_anterior2 = ttk.Button(self.frame_cantidad_de_objetos, text="Regresar al Menú anterior", command=self.iniciar_programa_cantidad_usuarios, width=50)

        self.btn_regresar_menu_anterior3 = ttk.Button(self.frame_cantidad_de_objetos_pesos, text="Regresar al Menú anterior", command=self.iniciar_programa_cantidad_objetos, width=50)

        self.btn_regresar_menu_principal = ttk.Button(self.frame_resultados_finales, text="Regresar al Menú Principal", command=self.mostrar_inicio, width=50)
        self.btn_regresar_menu_principal.grid(row=20, column=0, pady=10, padx=10, sticky="nsew")

        self.btn_regresar_menu_principal = ttk.Button(self.frame_configuracion, text="Regresar al Menú Principal", command=self.mostrar_inicio, width=50)
        self.btn_regresar_menu_principal.grid(row=1, column=0, pady=10)

        self.btn_regresar_sub_menu = ttk.Button(self.frame_configuracion_almacen, text="Regresar a la configuracion del programa", command=self.configuracion_programa, width=50)
        self.btn_regresar_sub_menu.grid(row=1, column=0, pady=10)

        self.btn_regresar_sub_menu1 = ttk.Button(self.frame_configuracion_vehiculos, text="Regresar a la configuracion del programa", command=self.configuracion_programa, width=50)
        self.btn_regresar_sub_menu1.grid(row=1, column=0, pady=10)

        self.btn_regresar_sub_menu2 = ttk.Button(self.frame_configuracion_vehiculos_pesos, text="Regresar a la configuracion de vehiculos", command=self.configuracion_programa_vehiculos, width=50)

        self.frame_configuracion.columnconfigure(0, weight=1)
        self.frame_configuracion.rowconfigure(2, weight=1)
        self.frame_configuracion_almacen.columnconfigure(0, weight=1)
        self.frame_configuracion_almacen.rowconfigure(2, weight=1)
        self.frame_configuracion_vehiculos.columnconfigure(0, weight=1)
        self.frame_configuracion_vehiculos.rowconfigure(3, weight=1)

        self.frame_cantidad_clientes.grid_remove()
        self.frame_coordenadas_clientes.grid_remove()
        self.frame_cantidad_de_objetos.grid_remove()
        self.frame_cantidad_de_objetos_pesos.grid_remove()
        self.frame_resultados_finales.grid_remove()
        self.frame_configuracion.grid_remove()
        self.frame_configuracion_almacen.grid_remove()

        self.frame_configuracion_vehiculos.grid_remove()
        self.frame_configuracion_vehiculos_pesos.grid_remove()

        self.configuracion_realizada_parte1 = False
        self.configuracion_realizada_parte2 = False

    def iniciar_programa(self):
        if not self.configuracion_realizada_parte1 or not self.configuracion_realizada_parte2:
            messagebox.showerror("Error", "Debe configurar el programa antes de iniciar.")
            return
        self.frame_inicio.grid_remove()
        self.btn_iniciar.grid_remove()
        self.btn_configuracion.grid_remove()
        self.btn_salir.grid_remove()
        self.frame_coordenadas_clientes.grid_remove() 
        self.frame_cantidad_clientes.grid()

    def iniciar_programa_cantidad_usuarios(self):
        coordenadas_x_clientes.clear()
        coordenadas_y_clientes.clear()
        self.frame_cantidad_de_objetos.grid_remove()
        self.frame_cantidad_clientes.grid_remove()
        self.frame_coordenadas_clientes.grid()
        for widget in self.frame_coordenadas_clientes.winfo_children():
            if widget not in [self.btn_guardar_coordenadas_clientes ,self.btn_regresar_menu_anterior, self.etiqueta_cantidad_clientes]:
                widget.destroy()
        clientes = int(self.entry_cantidad_clientes.get())
        for i in range(clientes):
            label1 = ttk.Label(self.frame_coordenadas_clientes, text=f"Ingrese las coordenadas x del cliente {i + 1}:")
            entry1 = ttk.Entry(self.frame_coordenadas_clientes)
            label1.grid(row=i*2+1, column=0, pady=10, padx=(100, 0))  
            entry1.grid(row=i*2+1, column=1, pady=10)
            label2 = ttk.Label(self.frame_coordenadas_clientes, text=f"Ingrese las coordenadas y del cliente {i + 1}:")
            entry2 = ttk.Entry(self.frame_coordenadas_clientes)
            label2.grid(row=i*2+2, column=0, pady=10, padx=(100, 0)) 
            entry2.grid(row=i*2+2, column=1, pady=10)
            coordenadas_x_clientes.append(entry1)
            coordenadas_y_clientes.append(entry2)
        self.btn_guardar_coordenadas_clientes.grid(row=30, column=1, pady=20)
        self.btn_regresar_menu_anterior.grid(row=31, column=1, pady=10)
    
    def iniciar_programa_cantidad_objetos(self):
        self.frame_coordenadas_clientes.grid_remove()
        self.frame_cantidad_de_objetos_pesos.grid_remove()
        self.frame_cantidad_de_objetos.grid()
        self.btn_regresar_menu_anterior2.grid(row=4, column=0, pady=10)

    def pesos_objetos(self):
        pesos_objetos.clear()
        self.frame_cantidad_de_objetos.grid_remove()
        self.frame_cantidad_de_objetos_pesos.grid()
        for widget in self.frame_cantidad_de_objetos_pesos.winfo_children():
            if widget not in [self.btn_guardar_pesos_objetos ,self.btn_regresar_menu_anterior3, self.etiqueta_pesos_objetos]:
                widget.destroy()
        objetos = int(self.entry_cantidad_objetos.get())
        for i in range(objetos):
            label = ttk.Label(self.frame_cantidad_de_objetos_pesos, text=f"Ingrese el peso en KG del objeto {i + 1}:")
            entry = ttk.Entry(self.frame_cantidad_de_objetos_pesos)
            label.grid(row=i*2+1, column=0, pady=10, padx=(100, 0))  
            entry.grid(row=i*2+1, column=1, pady=10)
            pesos_objetos.append(entry)
        self.btn_guardar_pesos_objetos.grid(row=30, column=1, pady=20)
        self.btn_regresar_menu_anterior3.grid(row=31, column=1, pady=10)
        
    def guardar_cantidad_clientes(self):
        global clientes
        
        cantidad_clientes = self.entry_cantidad_clientes.get()
        if cantidad_clientes != None:
            clientes= {}

        try:
            cantidad_clientes = int(cantidad_clientes)
            if cantidad_clientes > 0:
                messagebox.showinfo("Guardar", "Cantidad de clientes guardada con éxito.")
                self.iniciar_programa_cantidad_usuarios()
            else:
                messagebox.showerror("Error", "Ingrese un número entero positivo.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número entero válido.")

    def guardar_coordenadas_clientes(self):
        if not coordenadas_x_clientes or not coordenadas_y_clientes:
            messagebox.showerror("Error", "Ingrese coordenadas para al menos un cliente.")
            return
        for i, (coord_x, coord_y) in enumerate(zip(coordenadas_x_clientes, coordenadas_y_clientes)):
            x = coord_x.get()
            y = coord_y.get()
            try:
                x_float = float(x)
                y_float = float(y)
                clientes[f"C{i}"] = (float(x), float(y))
            except ValueError:
                messagebox.showerror("Error", f"Ingrese coordenadas válidas para el cliente {i + 1}.")
                return

        messagebox.showinfo("Guardar", "Configuración de coordenadas de clientes guardada con éxito.")
        self.iniciar_programa_cantidad_objetos()
    
    def guardar_cantidad_objetos(self):
        cantidad_objetos = self.entry_cantidad_objetos.get()
        try:
            cantidad_objetos = int(cantidad_objetos)
            if cantidad_objetos > 0:
                messagebox.showinfo("Guardar", "Configuración de cantidad de objetos guardada con éxito.")
                self.pesos_objetos()
            else:
                messagebox.showerror("Error", "La cantidad de objetos debe ser un número entero positivo.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número entero válido para la cantidad de objetos.")

    def guardar_pesos_objetos(self):
        global num_vehiculos, capacidades_vehiculos, num_objetos, pesos_objetos, clientes, valores_pesos_objetos, pesos_objetos_float
        for i, entrada in enumerate(pesos_objetos):
            peso = entrada.get()
            if not peso or not (peso.isdigit() or (('.' in peso or ',' in peso) and peso.replace('.', '').replace(',', '').isdigit())):
                messagebox.showerror("Error", f"Ingrese un peso válido (entero o flotante positivo) para el objeto {i + 1}.")
                return
        messagebox.showinfo("Guardar", "Configuración de pesos de objetos guardada con éxito.")
        num_objetos = int(self.entry_cantidad_objetos.get())
        pesos_objetos = [float(entry.get()) for entry in pesos_objetos]
        self.distribuir_objetos(num_vehiculos, capacidades_vehiculos, num_objetos, pesos_objetos, clientes)

    def configuracion_programa(self):
        self.frame_inicio.grid_remove()
        self.btn_iniciar.grid_remove()
        self.btn_configuracion.grid_remove()
        self.btn_salir.grid_remove()
        self.frame_configuracion_almacen.grid_remove()
        self.frame_configuracion_vehiculos.grid_remove()
        self.frame_configuracion.grid()
        self.btn_configuracion_almacen.grid(row=1, column=0, pady=10)
        self.btn_configuracion_vehiculo.grid(row=2, column=0, pady=10)
        self.btn_regresar_menu_principal.grid(row=3, column=0, pady=10)

    def configuracion_programa_almacen(self):
        self.frame_configuracion.grid_remove()
        self.btn_configuracion_almacen.grid_remove()
        self.frame_configuracion_almacen.grid()
        self.btn_regresar_sub_menu.grid(row=4, column=0, pady=10)
    
    def guardar_configuracion_almacen(self):
        global almacen
        almacen_x = self.entry_almacen_x.get()
        almacen_y = self.entry_almacen_y.get()
        if almacen_x.replace('.', '', 1).lstrip('-').isdigit():
            if almacen_y.replace('.', '', 1).lstrip('-').isdigit():
                self.configuracion_realizada_parte1 = True
                messagebox.showinfo("Guardar", "Configuración de almacen guardada con éxito.")
                almacen = (float(almacen_x), float(almacen_y))
            else:
                messagebox.showerror("Error", "Ingrese un valor válido para las coordenadas Y del almacen.")
        else:
            messagebox.showerror("Error", "Ingrese un valor válido para las coordenadas X del almacen.")

    def configuracion_programa_vehiculos(self):
        self.frame_configuracion.grid_remove() 
        self.btn_configuracion_vehiculo.grid_remove()
        self.frame_configuracion_vehiculos_pesos.grid_remove() 
        self.frame_configuracion_vehiculos.grid()
        self.btn_regresar_sub_menu1.grid(row=4, column=0, pady=10)

    def configuracion_programa_vehiculos_cantidad_peso(self,cantidad):
        global capacidades_vehiculos
        capacidades_vehiculos.clear()
        self.frame_configuracion_vehiculos.grid_remove()
        self.frame_configuracion_vehiculos_pesos.grid()
        for widget in self.frame_configuracion_vehiculos_pesos.winfo_children():
            if widget not in [self.btn_guardar_configuracion_vehiculos_pesos, self.btn_regresar_sub_menu2, self.etiqueta_configuracion_vehiculos_pesos]:
                widget.destroy()
        vehiculos = int(cantidad)
        for i in range(vehiculos):
            label = ttk.Label(self.frame_configuracion_vehiculos_pesos, text=f"Ingrese el peso (kg) del vehiculo {i + 1}:")
            entry = ttk.Entry(self.frame_configuracion_vehiculos_pesos)
            label.grid(row=i+1, column=0, pady=10)
            entry.grid(row=i+1, column=1, pady=10, sticky="we")
            capacidades_vehiculos.append(entry)
        self.configuracion_realizada_parte2 = True
        self.btn_guardar_configuracion_vehiculos_pesos.grid(row=i+2, column=1, pady=20)
        self.btn_regresar_sub_menu2.grid(row=i+3, column=1, pady=10)

    def guardar_configuracion_vehiculos(self):
        cantidad_vehiculos = self.entry_cantidad_vehiculos.get()
        num_vehiculos = int(cantidad_vehiculos)
        if cantidad_vehiculos.isdigit() and int(cantidad_vehiculos) > 0:
            messagebox.showinfo("Guardar", "Cantidad de vehículos guardada con éxito.")
            self.configuracion_programa_vehiculos_cantidad_peso(num_vehiculos)
        else:
            messagebox.showerror("Error", "Ingrese un número entero y positivo de vehículos.")

    def guardar_configuracion_vehiculos_pesos(self):
        for i, entrada in enumerate(capacidades_vehiculos):
            peso = entrada.get()
            if not peso or not peso.isdigit() or int(peso) <= 0:
                messagebox.showerror("Error", f"Ingrese un peso válido y positivo para el vehículo {i + 1}.")
                return
        messagebox.showinfo("Guardar", "Configuración de pesos de vehículos guardada con éxito.")

    def mostrar_inicio(self):
        self.frame_coordenadas_clientes.grid_remove()
        self.frame_cantidad_clientes.grid_remove()
        self.frame_resultados_finales.grid_remove()
        self.frame_configuracion.grid_remove()
        self.frame_cantidad_de_objetos_pesos.grid_remove()
        self.frame_inicio.grid()
        self.btn_iniciar.grid()
        self.btn_configuracion.grid()
        self.btn_salir.grid()

    def salir_programa(self):
        respuesta = messagebox.askquestion("Salir", "¿Estás seguro de que quieres salir del programa?")
        if respuesta == 'yes':
            self.destroy()

    def calcular_distancia(self, punto1, punto2):
        x1, y1 = punto1
        x2, y2 = punto2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def obtener_ruta_prim(self, G):
        MST = nx.minimum_spanning_tree(G)
        ruta = list(nx.dfs_preorder_nodes(MST, source="Almacén"))
        return ruta

    def dibujar_ruta_folium(self, mapa, ruta, posiciones, etiquetas, color):
        coordenadas_ruta = [posiciones[nodo] for nodo in ruta]
        folium.PolyLine(locations=coordenadas_ruta, color=color, weight=5, opacity=1).add_to(mapa)
        for nodo in ruta:
            folium.Marker(location=posiciones[nodo], popup=etiquetas[nodo], icon=folium.Icon(color='red')).add_to(mapa)
    
    def distribuir_objetos(self,num_vehiculos, capacidades_vehiculos, num_objetos, pesos_objetos, clientes):
        self.configuracion_realizada_parte1 = False
        self.configuracion_realizada_parte2 = False
        self.frame_cantidad_de_objetos_pesos.grid_remove()
        self.frame_resultados_finales.grid()
        self.etiqueta_resultados_finales.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.etiqueta_almacen = ttk.Label(self.frame_resultados_finales, text=f"Almacén: {almacen}")
        self.etiqueta_almacen.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.label_clientes = ttk.Label(self.frame_resultados_finales, text="")
        self.label_clientes.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")
        clientes_texto = "\n".join([f"{cliente}: {coordenadas}" for cliente, coordenadas in clientes.items()])
        self.label_clientes.config(text=f"Clientes y sus coordenadas:\n{clientes_texto}")
        self.label_distribucion = ttk.Label(self.frame_resultados_finales, text="")
        self.label_distribucion.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")

        objetos_sin_vehiculo = []  
        cantidad_vehiculos = self.entry_cantidad_vehiculos.get()
        numero_vehiculos = int(cantidad_vehiculos)
        capacidades_vehiculos_original = [float(entry.get()) for entry in capacidades_vehiculos]
        capacidades_vehiculos_enteros = [int(valor) for valor in capacidades_vehiculos_original]
        vehiculos = {i + 1: {'capacidad': capacidades_vehiculos_enteros[i], 'objetos': []} for i in range(numero_vehiculos)}
    
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
                objetos_sin_vehiculo.append((obj, peso))

        texto_distribucion = "\n".join([f"Vehiculo {vehiculo}: objetos {', '.join(map(str, info_vehiculo['objetos']))}. "
                                        f"Total de objetos: {len(info_vehiculo['objetos'])}, Pesando en total "
                                        f"{capacidades_vehiculos_enteros[vehiculo-1] - info_vehiculo['capacidad']} Kg"
                                        for vehiculo, info_vehiculo in vehiculos.items()])
        if objetos_sin_vehiculo:
            texto_sin_vehiculo = "\n".join([f"No hay vehículo disponible para el objeto {obj} con peso {peso} Kg."
                                            for obj, peso in objetos_sin_vehiculo])
            texto_distribucion += f"\n\nObjetos sin vehículo disponible:\n{texto_sin_vehiculo}"

        self.label_distribucion.config(text=texto_distribucion)
        self.mapa()
    
    def mapa(self):
        self.label_ruta_entrega = ttk.Label(self.frame_resultados_finales, text="")
        self.label_ruta_entrega.grid(row=4, column=0, pady=10, padx=20, sticky="nswe")
        
        G = nx.Graph()
        posiciones = {}
        etiquetas = {}

        for cliente, coord_cliente in clientes.items():
            G.add_node(cliente)
            G.add_edge("Almacén", cliente, weight=self.calcular_distancia(almacen, coord_cliente))
            posiciones[cliente] = coord_cliente
            etiquetas[cliente] = cliente
        posiciones["Almacén"] = almacen
        etiquetas["Almacén"] = "Almacén"

        ruta_prim = self.obtener_ruta_prim(G)
        self.label_ruta_entrega.config(text=f"Ruta de Entrega: {' -> '.join(ruta_prim)}")

        mapa_folium = folium.Map(location=almacen, zoom_start=12)

        self.dibujar_ruta_folium(mapa_folium, ruta_prim, posiciones, etiquetas, color='blue')

        rutas_entrega = {}
        for cliente in clientes:
            ruta = self.obtener_ruta(G, "Almacén", cliente)
            rutas_entrega[cliente] = ruta

        clientes_ordenados = self.obtener_orden_visita_clientes(G, rutas_entrega)
        ruta_completa = ["Almacén"] + [cliente for cliente in clientes_ordenados] + ["Almacén"]

        self.dibujar_ruta_folium(mapa_folium, ruta_completa, posiciones, etiquetas, color='green')

        mapa_folium.save('ruta_entrega.html')
        webbrowser.open('ruta_entrega.html')
    
    def obtener_orden_visita_clientes(self, G, rutas_entrega):
        return sorted(rutas_entrega.keys(), key=lambda cliente: self.calcular_distancia_entrega(G, rutas_entrega[cliente]))

    def calcular_distancia_entrega(self, G, ruta):
        distancia = 0
        for i in range(len(ruta) - 1):
            distancia += G[ruta[i]][ruta[i+1]]['weight']
        return distancia

    def obtener_ruta(self, G, origen, destino):
        ruta = nx.shortest_path(G, source=origen, target=destino, weight='weight')
        return ruta
    
if __name__ == "__main__":
    app = InterfazGrafica()
    app.mainloop()
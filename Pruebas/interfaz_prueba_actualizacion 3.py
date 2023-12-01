import tkinter as tk
from tkinter import ttk, messagebox

pesos_vehiculos = []

class InterfazGrafica(tk.Tk):
    def __init__(self):
        super().__init__()

        #Nombre de la interfaz y tamaño inicial 
        self.title("Interfaz Prueba")
        self.geometry("700x400")

        #Fondo de imagen para el menú principal
        #self.background_image = tk.PhotoImage(file="C:/Users/Alex/Documents/ALEX/archivos/Estudio/Ingenieria/5 semestre/Analisis de algoritmos/Proyecto final/imagen.png")  
        #self.background_label = tk.Label(self, image=self.background_image)
        #self.background_label.place(relwidth=1, relheight=1)

        #Frame de inicio
        self.frame_inicio = ttk.Frame(self)
        self.frame_inicio.grid(row=1, column=0, sticky="nsew")

        #Frame de configuraciónm
        self.frame_configuracion = ttk.Frame(self)
        self.frame_configuracion.grid(row=1, column=0, sticky="nsew")

        #Frame de configuracion almacen
        self.frame_configuracion_almacen = ttk.Frame(self)
        self.frame_configuracion_almacen.grid(row=1, column=0, sticky="nsew")

        #Widgets dentro del frame
        self.label_almacen_x = ttk.Label(self.frame_configuracion_almacen, text="Ingrese las coordenadas X del almacen:")
        self.entry_almacen_x = ttk.Entry(self.frame_configuracion_almacen)
        self.label_almacen_y = ttk.Label(self.frame_configuracion_almacen, text="Ingrese las coordenadas Y del almacen:")
        self.entry_almacen_y = ttk.Entry(self.frame_configuracion_almacen)

        #Frame de configuracion vehiculo
        self.frame_configuracion_vehiculos = ttk.Frame(self)
        self.frame_configuracion_vehiculos.grid(row=1, column=0, sticky="nsew")

        #Frame de configuracion vehiculo peso
        self.frame_configuracion_vehiculos_pesos = ttk.Frame(self)
        self.frame_configuracion_vehiculos_pesos.grid(row=1, column=0, sticky="nsew")

        #Creacion de los botones, su nombre y tamaño del menu principal
        self.btn_iniciar = ttk.Button(self, text="Iniciar programa", command=self.iniciar_programa, width=50)
        self.btn_configuracion = ttk.Button(self, text="Configuración del programa", command=self.configuracion_programa, width=50)
        self.btn_salir = ttk.Button(self, text="Salir del programa", command=self.salir_programa, width=50)

        # Colocar los botones en el centro del menu principal
        self.btn_iniciar.grid(row=1, column=0, pady=10)
        self.btn_configuracion.grid(row=2, column=0, pady=10)
        self.btn_salir.grid(row=3, column=0, pady=10)

        # Centrar los botones del menu principal 
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        #Configurar los elementos del frame de configuración
        self.etiqueta_configuracion = ttk.Label(self.frame_configuracion, text="Configuración del programa")
        self.etiqueta_configuracion.grid(row=0, column=0, padx=20, pady=20)
        self.btn_configuracion_almacen = ttk.Button(self.frame_configuracion, text="Configurar almacen", command=self.configuracion_programa_almacen, width=50)
        self.btn_configuracion_vehiculo = ttk.Button(self.frame_configuracion, text="Configurar vehiculos", command=self.configuracion_programa_vehiculos, width=50)

        #Configurar los elementos del frame de configuración de almacen 
        self.etiqueta_configuracion_almacen = ttk.Label(self.frame_configuracion_almacen, text="Configuracion del almacen")
        self.etiqueta_configuracion_almacen.grid(row=0, column=0, padx=20, pady=20)
        
        #Creacion de la entrada de datos del almacen 
        self.label_almacen_x.grid(row=1, column=0, pady=10, ipadx=100, columnspan=2)
        self.entry_almacen_x.grid(row=1, column=0, pady=10, padx=(270, 0))
        self.label_almacen_y.grid(row=2, column=0, pady=10, ipadx=100, columnspan=2)
        self.entry_almacen_y.grid(row=2, column=0, pady=10, padx=(270, 0))

        #Creacion guardar configuracion del almacen
        self.btn_guardar_configuracion_almacen = ttk.Button(
            self.frame_configuracion_almacen,
            text="Guardar configuración",
            command=self.guardar_configuracion_almacen,
            width=50
        )
        self.btn_guardar_configuracion_almacen.grid(row=3, column=0, pady=20)

        #Configurar los elementos del frame de configuración de vehiculos 
        self.etiqueta_configuracion_vehiculos = ttk.Label(self.frame_configuracion_vehiculos, text="Configuracion de vehiculos")
        self.etiqueta_configuracion_vehiculos.grid(row=0, column=0, padx=20, pady=20)

        #Configurar los elementos del frame de configuración de vehiculos pesos
        self.etiqueta_configuracion_vehiculos_pesos = ttk.Label(self.frame_configuracion_vehiculos_pesos, text="Configuracion de pesos (kg) de los vehiculos")
        self.etiqueta_configuracion_vehiculos_pesos.grid(row=0, column=1, padx=20, pady=20)
        
        #Creacion de la entrada de datos de vehiculos 
        self.label_cantidad_vehiculos = ttk.Label(self.frame_configuracion_vehiculos, text="Ingrese el numero de vehiculos que tiene:")
        self.entry_cantidad_vehiculos = ttk.Entry(self.frame_configuracion_vehiculos)
        self.label_cantidad_vehiculos.grid(row=2, column=0, pady=10, ipadx=100, columnspan=2)
        self.entry_cantidad_vehiculos.grid(row=2, column=0, pady=10, padx=(270, 0))

        #Creacion guardar configuracion de vehiculos
        self.btn_guardar_configuracion_vehiculos = ttk.Button(
            self.frame_configuracion_vehiculos,
            text="Continuar",
            command=self.guardar_configuracion_vehiculos,
            width=50
        )
        self.btn_guardar_configuracion_vehiculos.grid(row=3, column=0, pady=20)

        #Creacion guardar configuracion de pesos de vehiculos
        self.btn_guardar_configuracion_vehiculos_pesos = ttk.Button(
            self.frame_configuracion_vehiculos_pesos,
            text="Guardar configuración",
            command=self.guardar_configuracion_vehiculos_pesos,
            width=50
        )
        
        #Botón para regresar al menú principal desde la configuración
        self.btn_regresar_menu_principal = ttk.Button(self.frame_configuracion, text="Regresar al Menú Principal", command=self.mostrar_inicio, width=50)
        self.btn_regresar_menu_principal.grid(row=1, column=0, pady=10)

        #Boton para regresar al sub menu de la configuracion del programa
        self.btn_regresar_sub_menu = ttk.Button(self.frame_configuracion_almacen, text="Regresar a la configuracion del programa", command=self.configuracion_programa, width=50)
        self.btn_regresar_sub_menu.grid(row=1, column=0, pady=10)

        #Boton para regresar al sub menu de la configuracion del programa
        self.btn_regresar_sub_menu1 = ttk.Button(self.frame_configuracion_vehiculos, text="Regresar a la configuracion del programa", command=self.configuracion_programa, width=50)
        self.btn_regresar_sub_menu1.grid(row=1, column=0, pady=10)

        #Boton para regresar al sub menu de la configuracion del programa de vehiculos
        self.btn_regresar_sub_menu2 = ttk.Button(self.frame_configuracion_vehiculos_pesos, text="Regresar a la configuracion de vehiculos", command=self.configuracion_programa_vehiculos, width=50)

        #Ajustes para centrar los botones del frame de configuracion
        self.frame_configuracion.columnconfigure(0, weight=1)
        self.frame_configuracion.rowconfigure(2, weight=1)
        self.frame_configuracion_almacen.columnconfigure(0, weight=1)
        self.frame_configuracion_almacen.rowconfigure(2, weight=1)
        self.frame_configuracion_vehiculos.columnconfigure(0, weight=1)
        self.frame_configuracion_vehiculos.rowconfigure(3, weight=1)

        #Ocultar el frame de configuración inicialmente
        self.frame_configuracion.grid_remove()

        #Ocultar el frame de configuración de almacen
        self.frame_configuracion_almacen.grid_remove()

        #Ocultar el frame de configuración de vehiculos
        self.frame_configuracion_vehiculos.grid_remove()

        #Ocultal el frame de configuracion de vehiculos pesos
        self.frame_configuracion_vehiculos_pesos.grid_remove()

        # Variable de configuración
        self.configuracion_realizada_parte1 = False
        self.configuracion_realizada_parte2 = False

    def iniciar_programa(self):
        if not self.configuracion_realizada_parte1 or not self.configuracion_realizada_parte2:
            messagebox.showerror("Error", "Debe configurar el programa antes de iniciar.")
            return
        # Aquí corre todo lo que está dentro del programa
        print("Iniciando programa")

    def configuracion_programa(self):
        #Ocultar el frame de inicio
        self.frame_inicio.grid_remove()
        self.btn_iniciar.grid_remove()
        self.btn_configuracion.grid_remove()
        self.btn_salir.grid_remove()
        self.frame_configuracion_almacen.grid_remove()
        self.frame_configuracion_vehiculos.grid_remove()
        #Mostrar el frame de configuracion
        self.frame_configuracion.grid()
        self.btn_configuracion_almacen.grid(row=1, column=0, pady=10)
        self.btn_configuracion_vehiculo.grid(row=2, column=0, pady=10)
        self.btn_regresar_menu_principal.grid(row=3, column=0, pady=10)

    def configuracion_programa_almacen(self):
        #Ocultar el frame de configuracion y boton de almacen
        self.frame_configuracion.grid_remove()
        self.btn_configuracion_almacen.grid_remove()
        #Mostrar el frame de configuracion
        self.frame_configuracion_almacen.grid()
        self.btn_regresar_sub_menu.grid(row=4, column=0, pady=10)
    
    def guardar_configuracion_almacen(self):
        almacen_x = self.entry_almacen_x.get()#Obtener el valor ingresado en la entrada
        almacen_y = self.entry_almacen_y.get()#Obtener el valor ingresado en la entrada
        #Aquí puedes agregar la lógica para guardar la configuración de vehículos
        if almacen_x and almacen_y:
            # Configuración realizada correctamente
            self.configuracion_realizada_parte1 = True
            messagebox.showinfo("Guardar", "Configuración de almacen guardada con éxito.")
        else:
            messagebox.showerror("Error", "Ingrese las coordenadas del almacen.")

    def configuracion_programa_vehiculos(self):
        #Ocultar el frame de configuracion y boton de vehiculos
        self.frame_configuracion.grid_remove() 
        self.btn_configuracion_vehiculo.grid_remove()
        self.frame_configuracion_vehiculos_pesos.grid_remove() 
        #Mostrar el frame de configuracion
        self.frame_configuracion_vehiculos.grid()
        self.btn_regresar_sub_menu1.grid(row=4, column=0, pady=10)

    def configuracion_programa_vehiculos_cantidad_peso(self,cantidad):
        pesos_vehiculos.clear()
        #Ocultar el frame de configuracion y boton de vehiculos
        self.frame_configuracion_vehiculos.grid_remove()
        self.frame_configuracion_vehiculos_pesos.grid()
        #Elimina toda la cantidad de botones de pesos para cada vehiculo para volver a crear solo los necesarios
        for widget in self.frame_configuracion_vehiculos_pesos.winfo_children():
            if widget not in [self.btn_guardar_configuracion_vehiculos_pesos, self.btn_regresar_sub_menu2, self.etiqueta_configuracion_vehiculos_pesos]:
                widget.destroy()
        vehiculos = int(cantidad)
        #Crear y agregar botones de entrada
        for i in range(vehiculos):
            label = ttk.Label(self.frame_configuracion_vehiculos_pesos, text=f"Ingrese el peso (kg) del vehiculo {i + 1}:")
            entry = ttk.Entry(self.frame_configuracion_vehiculos_pesos)
            label.grid(row=i+1, column=0, pady=10)
            entry.grid(row=i+1, column=1, pady=10, sticky="we")
            pesos_vehiculos.append(entry)
        #Configuración realizada correctamente
        self.configuracion_realizada_parte2 = True
        self.btn_guardar_configuracion_vehiculos_pesos.grid(row=i+2, column=1, pady=20)
        self.btn_regresar_sub_menu2.grid(row=i+3, column=1, pady=10)

    def guardar_configuracion_vehiculos(self):
        cantidad_vehiculos = self.entry_cantidad_vehiculos.get()#Obtener el valor ingresado en la entrada
        if cantidad_vehiculos:
            messagebox.showinfo("Guardar", "Cantidad de vehículos guardada con éxito.")
            self.configuracion_programa_vehiculos_cantidad_peso(cantidad_vehiculos)
        else:
            messagebox.showerror("Error", "Ingrese un número válido de vehículos.")

    def guardar_configuracion_vehiculos_pesos(self):
        for i, entrada in enumerate(pesos_vehiculos):
            peso = entrada.get()
            # Verificar si la entrada está vacía o no es un número válido
            if not peso or not peso.isdigit():
                messagebox.showerror("Error", f"Ingrese un peso válido para el vehículo {i + 1}.")
                return
        messagebox.showinfo("Guardar", "Configuración de pesos de vehículos guardada con éxito.")

    def mostrar_inicio(self):
        #Ocultar el frame de configuración
        self.frame_configuracion.grid_remove()
        #Mostrar el frame de inicio 
        self.frame_inicio.grid()
        self.btn_iniciar.grid()
        self.btn_configuracion.grid()
        self.btn_salir.grid()

    def salir_programa(self):
        #Confirmacion de salir del programa
        respuesta = messagebox.askquestion("Salir", "¿Estás seguro de que quieres salir del programa?")
        if respuesta == 'yes':
            #Salir del programa
            self.destroy()

if __name__ == "__main__":
    app = InterfazGrafica()
    app.mainloop()
import tkinter as tk
from tkinter import ttk
import customtkinter as Ctk
from PIL import Image, ImageTk
from funciones import *
from conexion import conexion

#archivo donde se guardan los multiples menus del programa

#frame del menu de inicio
def crearInicio(frmMenuPrincipal):

    # Crear Frame
    frmInicio = tk.Frame(
        frmMenuPrincipal,
        bg="#151519"
    )

    # Colocarlo en el área principal
    frmInicio.grid(
        row=0,
        column=0,
        sticky="nsew"
    )


    # Contenido de ejemplo
    lblTitulo = tk.Label(
        frmInicio,
        text="INICIO",
        font=("Arial", 28, "bold"),
        bg="#151519",
        fg="#FFFFFF"
    )

    lblTitulo.pack(
        pady=30
    )


    return frmInicio

#frame clientes
def crearClientes(frmMenuPrincipal,ventanaPrincipal):
    #funciones a usar en el menu
    def listarClientes():
        conec = None
        txtBusqueda.delete(0,tk.END)
        try:
            conec = conexion(frmClientes)
            cursor = conec.cursor()
            cursor.execute("exec sp_listarClientes")
            #ejecutamos un procedimiento almacenado que lista los clientes

            registros = cursor.fetchall()
            #limpiar la tabla antes de cargar los datos
            for elemento in tablaClientes.get_children():
                tablaClientes.delete(elemento)
            #insertar cada registro en la tabla
            for evento in registros:
                tablaClientes.insert(
                    "",
                    tk.END,
                    values=(
                        evento[0],    
                        evento[1],    
                        evento[2],    
                        evento[3],    
                        evento[4],
                        evento[5]
                    )
                )
        except pyodbc.Error as error:
            mostrarError(frmClientes,"Error de conexion", f"No se pudieron consultar los registros.\n\n{error}")
        finally:
            if conec is not None:
                conec.close()
    #funcion con la que funciona el buscador
    def buscador(evento = None):#le agregamos el parametro evento para cuando reciba la llamada desde un bind
        conec = None
        busqueda = txtBusqueda.get()
        try:
            conec = conexion(frmClientes)
            cursor = conec.cursor()
            cursor.execute("exec sp_BuscadorClientes ?",(busqueda))

            registros = cursor.fetchall()
            #limpiar la tabla antes de cargar los datos
            for elemento in tablaClientes.get_children():
                tablaClientes.delete(elemento)
            #insertar cada registro en la tabla
            for evento in registros:
                tablaClientes.insert(
                    "",
                    tk.END,
                    values=(
                        evento[0],    
                        evento[1],    
                        evento[2],    
                        evento[3],    
                        evento[4],
                        evento[5]    
                    )
                )
        except pyodbc.Error as error:
            mostrarError(frmClientes,"Error de conexion", f"No se pudieron consultar los registros.\n\n{error}")
        finally:
            if conec is not None:
                conec.close()
    #funcion para modificar los eventos
    def modificarClientes():
        seleccion = tablaClientes.selection()
        if not seleccion:
            mostrarAdvertencia(frmMenuPrincipal,"Seleccion requerida",
            "Selecciona un cliente de la tabla para modificarlo")
            return
        #recuperar los datos de la fila seleccionada 
        datos = tablaClientes.item(seleccion[0], "values")
        idCliente = int(datos[0])
        generarModalRegistrarCliente(ventanaPrincipal,listarClientes,idCliente=idCliente,datos=datos)
        
    def eliminarEventos():
        seleccion = tablaClientes.selection()
        if not seleccion:
            mostrarAdvertencia(frmMenuPrincipal,"Seleccion requerida",
            "Selecciona un cliente de la tabla para eliminarlo")
            return
        confirmar = preguntarSiNo(frmMenuPrincipal,"Eliminar cliente","¿Desea eliminar el cliente seleccionado?")
        if not confirmar:
            return
        #recuperar los datos de la fila seleccionada 
        datos = tablaClientes.item(seleccion[0], "values")
        idEvento = int(datos[0])
        
        conec = None
        try:
            conec = conexion(frmMenuPrincipal)
            cursor = conec.cursor()
            cursor.execute("EXEC sp_InactivarCliente ?;",(idEvento))
            if cursor.rowcount == 0:
                mostrarAdvertencia(frmMenuPrincipal,"Registro no encontrado","La persona ya no existe en la base de datos")
                return
            mostrarExito(None,"Operacion exitosa","Se ha eliminado con exito el cliente")
            #guardamos los cambios
            conec.commit()
            listarClientes()
        except pyodbc.Error as error:
            if conec is not None:
                conec.rollback()
            mostrarError(frmMenuPrincipal,"Error de base de datos",f"No se pudieron guardar los cambios\n\n{error}")
        finally:
            if conec is not None:
                conec.close()
    # Crear Frame 
    frmClientes = tk.Frame(
        frmMenuPrincipal,
        bg="#151519"
    )

    # Colocarlo en el área principal
    frmClientes.grid(
        row=0,
        column=0,
        sticky="nsew"
    )


    # Contenido de ejemplo
    lblTitulo = tk.Label(
        frmClientes,
        text="CLIENTES",
        font=("Arial", 28, "bold"),
        bg="#151519",
        fg="#FFFFFF"
    )

    lblTitulo.pack(
        pady=(20,10)
    )
    #frame donde estara el buscador
    frmBusqueda = tk.Frame(
        frmClientes,
        bg="#151519",
        height=50
    )
    frmBusqueda.pack(fill="x", padx=20, pady=(0, 10))
    frmBusqueda.pack_propagate(False)
    frmBusqueda.grid_columnconfigure(0, weight=1)

    txtBusqueda = CTk.CTkEntry(
        frmBusqueda,
        width=300,
        height=42,
        fg_color="#212227",
        text_color="#FFFFFF",
        placeholder_text_color="#C9C8C8",
        placeholder_text="Buscar cliente",
        font=("Ubuntu", 14),
        border_color="#322F2F"
    )
    txtBusqueda.grid(row=0, column=1, sticky="e", padx=(0, 5))
    #creamos un bind que se active cuando se escriba en el buscador para que se muestren los resultados rapidamente
    #en la tabla 
    txtBusqueda.bind("<KeyRelease>",buscador)
    lupaBusqueda = Image.open("img/busqueda.png")
    lupaBusquedaIcon = Ctk.CTkImage(
        light_image=lupaBusqueda, 
        dark_image=lupaBusqueda, 
        size=(35, 35)
    )
    
    btnlupaBusqueda = Ctk.CTkButton(
        frmBusqueda,
        text="",
        image=lupaBusquedaIcon,
        width=42,
        height=42,
        fg_color="#151519",
        hover_color="#151519",
        corner_radius=8,
        command=buscador
    )
    btnlupaBusqueda.image = lupaBusquedaIcon
    btnlupaBusqueda.grid(row=0, column=2, sticky="e")
    #creamos un frame donde crearemos los botones para tener un crud con los clientes
    frmBotones = tk.Frame(
        frmClientes,
        bg="#151519"
    )
    frmBotones.pack(fill="x", padx=20, pady=(0, 15))
    
    # Botón Registrar Evento
    btnRegistrarEvento = Ctk.CTkButton(
        frmBotones,
        text="Registrar Clientes",
        width=180,
        height=40,
        fg_color="#BC72FF",
        hover_color="#975DD2",
        corner_radius=20,
        font=("Ubuntu", 13, "bold"),
        command=lambda: generarModalRegistrarCliente(ventanaPrincipal,listarClientes)#le enviamos la funcion para actualizar los datos al ingresarse todos
    )
    btnRegistrarEvento.pack(side="left", padx=(0, 10))
    
    # Botón Modificar
    btnModificar = Ctk.CTkButton(
        frmBotones,
        text="Modificar",
        width=130,
        height=40,
        fg_color="#3E4B5B",
        hover_color="#596C82",
        corner_radius=20,
        font=("Ubuntu", 13, "bold"),
        command= modificarClientes
    )
    btnModificar.pack(side="left", padx=(0, 10))

    # Botón Eliminar
    btnEliminar = Ctk.CTkButton(
        frmBotones,
        text="Eliminar",
        width=130,
        height=40,
        fg_color="#C94A4A",
        hover_color="#A03737",
        corner_radius=20,
        font=("Ubuntu", 13, "bold"),
        command=eliminarEventos
    )
    btnEliminar.pack(side="left", padx=(0, 10))

    # Botón Actualizar / Refrescar Tabla
    btnActualizar = Ctk.CTkButton(
        frmBotones,
        text="Actualizar",
        width=130,
        height=40,
        fg_color="#327555",
        hover_color="#265A41",
        corner_radius=20,
        font=("Ubuntu", 13, "bold"),
        command= listarClientes
    )
    btnActualizar.pack(side="left")
    #frame donde se alojara la tabla
    frmTabla = tk.Frame(
        frmClientes,
        bg="#151519"
    )
    frmTabla.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    frmTabla.pack_propagate(False)
    #usamos estilo para aplicarselo a la tabla
    estilo = ttk.Style()
    estilo.theme_use("clam")
    
    estilo.configure(
        "Custom.Treeview.Heading",
        background="#3E4B5B",
        foreground="#FFFFFF",
        font=("Ubuntu", 12, "bold"),
        relief="flat"
    )
    estilo.map("Custom.Treeview.Heading", background=[('active', '#596C82')])
    
    estilo.configure(
        "Custom.Treeview",
        background="#212227",
        foreground="#FFFFFF",
        fieldbackground="#212227",
        font=("Ubuntu", 11),
        rowheight=35
    )
    estilo.map("Custom.Treeview", background=[('selected', '#BC72FF')], foreground=[('selected', '#FFFFFF')])

    columnas = ("ID", "Nombre", "Apellido","Telefono", "Dui", "Edad")
    
    tablaClientes = ttk.Treeview(
        frmTabla,
        columns=columnas,
        show="headings",
        style="Custom.Treeview"
    )
    
    tablaClientes.heading("ID", text="ID")
    tablaClientes.heading("Nombre", text="Nombre")
    tablaClientes.heading("Apellido", text="Apellido")
    tablaClientes.heading("Telefono", text="Telefono")
    tablaClientes.heading("Dui", text="Dui")
    tablaClientes.heading("Edad", text="Edad")
    
    tablaClientes.column("ID", width=30, anchor="center")
    tablaClientes.column("Nombre", width=195, anchor="w")
    tablaClientes.column("Apellido", width=195, anchor="w")
    tablaClientes.column("Telefono", width=100, anchor="center")
    tablaClientes.column("Dui", width=100, anchor="center")
    tablaClientes.column("Edad", width=100, anchor="center")
    #le agregamos una scrollbar a la derecha
    barraVertical = ttk.Scrollbar( 
        frmTabla, 
        orient="vertical", 
        command=tablaClientes.yview 
    ) 
    tablaClientes.configure( 
        yscrollcommand=barraVertical.set
    ) 
    frmTabla.columnconfigure(0,weight=1)
    frmTabla.rowconfigure(0,weight=1)
    tablaClientes.grid(row=0, column=0, sticky="nsew") 
    barraVertical.grid(row=0, column=1, sticky="ns") 
    listarClientes()#llenamos la tabla con los eventos registrados
    return frmClientes


#frame eventos
def crearEventos(frmMenuPrincipal,ventanaPrincipal):
    #funciones a usar en el menu
    def listarEventos():
        conec = None
        txtBusqueda.delete(0,tk.END)
        try:
            conec = conexion(frmEventos)
            cursor = conec.cursor()
            cursor.execute("exec sp_listarEventos")
            #ejecutamos un procedimiento almacenado que lista los eventos

            registros = cursor.fetchall()
            #limpiar la tabla antes de cargar los datos
            for elemento in tablaEventos.get_children():
                tablaEventos.delete(elemento)
            #insertar cada registro en la tabla
            for evento in registros:
                tablaEventos.insert(
                    "",
                    tk.END,
                    values=(
                        evento[0],    
                        evento[1],    
                        evento[2],    
                        evento[3],    
                        evento[4]    
                    )
                )
        except pyodbc.Error as error:
            mostrarError(frmEventos,"Error de conexion", f"No se pudieron consultar los registros.\n\n{error}")
        finally:
            if conec is not None:
                conec.close()
    #funcion con la que funciona el buscador
    def buscador(evento = None):#le agregamos el parametro evento para cuando reciba la llamada desde un bind
        conec = None
        busqueda = txtBusqueda.get()
        try:
            conec = conexion(frmEventos)
            cursor = conec.cursor()
            cursor.execute("exec sp_Buscador ?",(busqueda))

            registros = cursor.fetchall()
            #limpiar la tabla antes de cargar los datos
            for elemento in tablaEventos.get_children():
                tablaEventos.delete(elemento)
            #insertar cada registro en la tabla
            for evento in registros:
                tablaEventos.insert(
                    "",
                    tk.END,
                    values=(
                        evento[0],    
                        evento[1],    
                        evento[2],    
                        evento[3],    
                        evento[4]    
                    )
                )
        except pyodbc.Error as error:
            mostrarError(frmEventos,"Error de conexion", f"No se pudieron consultar los registros.\n\n{error}")
        finally:
            if conec is not None:
                conec.close()
    #funcion para modificar los eventos
    def modificarEventos():
        seleccion = tablaEventos.selection()
        if not seleccion:
            mostrarAdvertencia(frmMenuPrincipal,"Seleccion requerida",
            "Selecciona un evento de la tabla para modificarlo")
            return
        #recuperar los datos de la fila seleccionada 
        datos = tablaEventos.item(seleccion[0], "values")
        idEvento = int(datos[0])
        generarModalRegistrarEventos(ventanaPrincipal,listarEventos,idEvento=idEvento,datos=datos)
        
    def eliminarEventos():
        seleccion = tablaEventos.selection()
        if not seleccion:
            mostrarAdvertencia(frmMenuPrincipal,"Seleccion requerida",
            "Selecciona un evento de la tabla para eliminarlo")
            return
        confirmar = preguntarSiNo(frmMenuPrincipal,"Eliminar evento","¿Desea eliminar el evento seleccionado?")
        if not confirmar:
            return
        #recuperar los datos de la fila seleccionada 
        datos = tablaEventos.item(seleccion[0], "values")
        idEvento = int(datos[0])
        
        conec = None
        try:
            conec = conexion(frmMenuPrincipal)
            cursor = conec.cursor()
            cursor.execute("EXEC sp_InactivarEvento ?;",(idEvento))
            if cursor.rowcount == 0:
                mostrarAdvertencia(frmMenuPrincipal,"Registro no encontrado","El evento ya no existe en la base de datos")
                return
            mostrarExito(None,"Operacion exitosa","Se ha eliminado con exito el evento")
            #guardamos los cambios
            conec.commit()
            listarEventos()
        except pyodbc.Error as error:
            if conec is not None:
                conec.rollback()
            mostrarError(frmMenuPrincipal,"Error de base de datos",f"No se pudieron guardar los cambios\n\n{error}")
        finally:
            if conec is not None:
                conec.close()
    # Crear Frame 
    frmEventos = tk.Frame(
        frmMenuPrincipal,
        bg="#151519"
    )

    # Colocarlo en el área principal
    frmEventos.grid(
        row=0,
        column=0,
        sticky="nsew"
    )


    # Contenido de ejemplo
    lblTitulo = tk.Label(
        frmEventos,
        text="EVENTOS",
        font=("Arial", 28, "bold"),
        bg="#151519",
        fg="#FFFFFF"
    )

    lblTitulo.pack(
        pady=(20,10)
    )
    #frame donde estara el buscador
    frmBusqueda = tk.Frame(
        frmEventos,
        bg="#151519",
        height=50
    )
    frmBusqueda.pack(fill="x", padx=20, pady=(0, 10))
    frmBusqueda.pack_propagate(False)
    frmBusqueda.grid_columnconfigure(0, weight=1)

    txtBusqueda = CTk.CTkEntry(
        frmBusqueda,
        width=300,
        height=42,
        fg_color="#212227",
        text_color="#FFFFFF",
        placeholder_text_color="#C9C8C8",
        placeholder_text="Buscar evento",
        font=("Ubuntu", 14),
        border_color="#322F2F"
    )
    txtBusqueda.grid(row=0, column=1, sticky="e", padx=(0, 5))
    #creamos un bind que se active cuando se escriba en el buscador para que se muestren los resultados rapidamente
    #en la tabla 
    txtBusqueda.bind("<KeyRelease>",buscador)
    lupaBusqueda = Image.open("img/busqueda.png")
    lupaBusquedaIcon = Ctk.CTkImage(
        light_image=lupaBusqueda, 
        dark_image=lupaBusqueda, 
        size=(35, 35)
    )
    
    btnlupaBusqueda = Ctk.CTkButton(
        frmBusqueda,
        text="",
        image=lupaBusquedaIcon,
        width=42,
        height=42,
        fg_color="#151519",
        hover_color="#151519",
        corner_radius=8,
        command=buscador
    )
    btnlupaBusqueda.image = lupaBusquedaIcon
    btnlupaBusqueda.grid(row=0, column=2, sticky="e")
    #creamos un frame donde crearemos los botones para tener un crud con los eventos
    frmBotones = tk.Frame(
        frmEventos,
        bg="#151519"
    )
    frmBotones.pack(fill="x", padx=20, pady=(0, 15))
    
    # Botón Registrar Evento
    btnRegistrarEvento = Ctk.CTkButton(
        frmBotones,
        text="Registrar Evento",
        width=180,
        height=40,
        fg_color="#BC72FF",
        hover_color="#975DD2",
        corner_radius=20,
        font=("Ubuntu", 13, "bold"),
        command=lambda: generarModalRegistrarEventos(ventanaPrincipal,listarEventos)#le enviamos la funcion para actualizar los datos al ingresarse todos
    )
    btnRegistrarEvento.pack(side="left", padx=(0, 10))
    
    # Botón Modificar
    btnModificar = Ctk.CTkButton(
        frmBotones,
        text="Modificar",
        width=130,
        height=40,
        fg_color="#3E4B5B",
        hover_color="#596C82",
        corner_radius=20,
        font=("Ubuntu", 13, "bold"),
        command= modificarEventos
    )
    btnModificar.pack(side="left", padx=(0, 10))

    # Botón Eliminar
    btnEliminar = Ctk.CTkButton(
        frmBotones,
        text="Eliminar",
        width=130,
        height=40,
        fg_color="#C94A4A",
        hover_color="#A03737",
        corner_radius=20,
        font=("Ubuntu", 13, "bold"),
        command=eliminarEventos
    )
    btnEliminar.pack(side="left", padx=(0, 10))

    # Botón Actualizar / Refrescar Tabla
    btnActualizar = Ctk.CTkButton(
        frmBotones,
        text="Actualizar",
        width=130,
        height=40,
        fg_color="#327555",
        hover_color="#265A41",
        corner_radius=20,
        font=("Ubuntu", 13, "bold"),
        command= listarEventos
    )
    btnActualizar.pack(side="left")
    #frame donde se alojara la tabla
    frmTabla = tk.Frame(
        frmEventos,
        bg="#151519"
    )
    frmTabla.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    frmTabla.pack_propagate(False)
    #usamos estilo para aplicarselo a la tabla
    estilo = ttk.Style()
    estilo.theme_use("clam")
    
    estilo.configure(
        "Custom.Treeview.Heading",
        background="#3E4B5B",
        foreground="#FFFFFF",
        font=("Ubuntu", 12, "bold"),
        relief="flat"
    )
    estilo.map("Custom.Treeview.Heading", background=[('active', '#596C82')])
    
    estilo.configure(
        "Custom.Treeview",
        background="#212227",
        foreground="#FFFFFF",
        fieldbackground="#212227",
        font=("Ubuntu", 11),
        rowheight=35
    )
    estilo.map("Custom.Treeview", background=[('selected', '#BC72FF')], foreground=[('selected', '#FFFFFF')])

    columnas = ("ID", "Nombre", "Tipo","Fecha", "Estado")
    
    tablaEventos = ttk.Treeview(
        frmTabla,
        columns=columnas,
        show="headings",
        style="Custom.Treeview"
    )
    
    tablaEventos.heading("ID", text="ID")
    tablaEventos.heading("Nombre", text="Nombre del Evento")
    tablaEventos.heading("Tipo", text="Tipo de Evento")
    tablaEventos.heading("Fecha", text="Fecha")
    tablaEventos.heading("Estado", text="Direccion")
    
    tablaEventos.column("ID", width=30, anchor="center")
    tablaEventos.column("Nombre", width=205, anchor="w")
    tablaEventos.column("Tipo", width=165, anchor="w")
    tablaEventos.column("Fecha", width=75, anchor="center")
    tablaEventos.column("Estado", width=245, anchor="center")
    
    barraVertical = ttk.Scrollbar( 
        frmTabla, 
        orient="vertical", 
        command=tablaEventos.yview 
    ) 
    tablaEventos.configure( 
        yscrollcommand=barraVertical.set
    ) 
    frmTabla.columnconfigure(0,weight=1)
    frmTabla.rowconfigure(0,weight=1)
    tablaEventos.grid(row=0, column=0, sticky="nsew") 
    barraVertical.grid(row=0, column=1, sticky="ns") 
    listarEventos()#llenamos la tabla con los eventos registrados
    
    return frmEventos
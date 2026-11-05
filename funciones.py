from datetime import datetime
import tkinter as tk
import customtkinter as CTk
from customMessagebox import *
from conexion import conexion
import re
import pyodbc

#variables que ocupan el sistema
TIPOEVENTO = [
    "Bodas",
    "Fiestas de Cumpleaños",
    "Fiestas de Quinceaños",
    "Graduaciones",
    "Despedidas de Solter@",
    "Baby Shower",
    "Bautizos / Primeras Comuniones",
    "Aniversarios de Boda",
    "Eventos Corporativos",
    "Ferias y Exposiciones",
    "Eventos de Lanzamiento / Aperturas",
    "Fiestas Temáticas",
    "Eventos Benéficos / Galas",
    "Conferencias y Seminarios"
]

PRECIOSEVENTO = {
    "Bodas":                          500.00,
    "Fiestas de Cumpleaños":          200.00,
    "Fiestas de Quinceaños":          400.00,
    "Graduaciones":                   350.00,
    "Despedidas de Solter@":          220.00,
    "Baby Shower":                    180.00,
    "Bautizos / Primeras Comuniones": 160.00,
    "Aniversarios de Boda":           300.00,
    "Eventos Corporativos":           800.00,
    "Ferias y Exposiciones":          600.00,
    "Eventos de Lanzamiento / Aperturas": 700.00,
    "Fiestas Temáticas":              250.00,
    "Eventos Benéficos / Galas":      400.00,
    "Conferencias y Seminarios":      450.00,
}
#funciones del sistema
def crearMenu(ventanaPrincipal):

    # --------------------------------------------------
    # CONTENEDOR GENERAL
    # --------------------------------------------------

    frmMenu = tk.Frame(
        ventanaPrincipal
    )
    
    frmMenu.pack(
        fill="both",
        expand=True
    )


    # --------------------------------------------------
    # BARRA LATERAL
    # --------------------------------------------------

    frmMenuLateral = tk.Frame(
        frmMenu,
        width=150,
        bg="#222328"
    )

    frmMenuLateral.pack(
        side="left",
        fill="y"
    )

    # Evita que los elementos internos
    # cambien el ancho de la barra
    frmMenuLateral.pack_propagate(False)


    # --------------------------------------------------
    # ÁREA PRINCIPAL
    # --------------------------------------------------

    frmMenuPrincipal = tk.Frame(
        frmMenu,
        bg="lightgray"
    )

    frmMenuPrincipal.pack(
        side="left",
        fill="both",
        expand=True
    )

    

    # --------------------------------------------------
    # CONFIGURAR GRID
    # --------------------------------------------------

    frmMenuPrincipal.grid_rowconfigure(
        0,
        weight=1
    )

    frmMenuPrincipal.grid_columnconfigure(
        0,
        weight=1
    )


    # Devolver los dos Frames
    return frmMenuLateral, frmMenuPrincipal



def mostrarFrame(frame):

    """
    Muestra el Frame seleccionado.
    """

    frame.tkraise()

def centrar_ventana(ventana_principal,ventana, ancho, alto):
    #actualizamos la ventana para que tkinter conozca
    #correctamente dus dimensiones y posiciones
    ventana.update_idletasks()

    # obtener posicion de la ventana principal
    posicion_x = ventana_principal.winfo_x()

    #winfo_y obtiene la posicion vertical
    posicion_y = ventana_principal.winfo_y()

    #obtiene el ancho actual de la ventana principal
    ancho_principal = ventana_principal.winfo_width()

    #obtiene el alto actual de la ventana principal
    alto_principal = ventana_principal.winfo_height()


    # calcular posicion del formulario
    x = posicion_x + (ancho_principal - ancho)//2

    y = posicion_y + (alto_principal - alto)//2

    # establecer tamaño y posicion 
    ventana.geometry(
        f"{ancho}x{alto}+{x}+{y}"    
    )
    

#fun
# cion que creara la ventana modal donde se registraran los clientes
def generarModalRegistrarCliente(VentanaPrincipal,listarEventos=None,idCliente=None,datos=None):
    #funcion para validar que se ingresen enteros en la entrada
    def validarEntero(entrada):
        if entrada == "" or entrada == "Edad":#si la entrada esta vacia o si es entera deja que se digite
            return True #asi permitiendo borrar o escribir unicamente numeros y que cargue el placeholder
        if entrada.isdigit():
            return True
        return False
    
    #funcion para validar la entrada para el dui y el numero de telefono
    def validarTelefono(entrada):
        if entrada == "":
            return True
        if entrada == "12345678":
            return True
        if entrada.isdigit() and len(entrada) < 9:
            return True
        return False
    #creamos el toplevel
    RegistrarClientes = CTk.CTkToplevel(
        VentanaPrincipal
    )
    RegistrarClientes.title("Registro de clientes")
    #Generamos la ventana centrada y con un tamaño adecuado para un formulario
    centrar_ventana(VentanaPrincipal,RegistrarClientes,500,625)
    RegistrarClientes.resizable(False,False)
    #agregamos la relacion del top level y lo convertimos en una ventana modal
    RegistrarClientes.transient(VentanaPrincipal)
    RegistrarClientes.grab_set()
    
    #creamos las validaciones
    validacionEntero = RegistrarClientes.register(validarEntero)
    validacionTelefono = RegistrarClientes.register(validarTelefono)
    #creamos un frame para almacenar todos los elementos 
    frmRegistro = tk.Frame(
        RegistrarClientes,
        bg="#212227"
    )
    #hacemos que cubra toda la ventana modal
    frmRegistro.pack(
        fill="both",
        expand=True
    )
    if idCliente is None:
        lblEncabezadoRegistro = tk.Label(
            frmRegistro,
            text="Registrar Evento",
            font=("Ubuntu",16,"bold"),
            bg="#212227",
            fg="#FFFFFF"
        )
        RegistrarClientes.title("Registrar Cliente")
        textBtn = "Registrar"
    else:
        lblEncabezadoRegistro = tk.Label(
            frmRegistro,
            text="Modificar Evento",
            font=("Ubuntu",16,"bold"),
            bg="#212227",
            fg="#FFFFFF"
        )
        RegistrarClientes.title("Modificar cliente")
        textBtn = "Modificar"
    lblEncabezadoRegistro.grid(
        row=0,
        column=0,
        padx=(20,0),
        pady=(25,0),
        sticky="sw"
    )
    #agregamos un subtitulo a el formulario
    lblSubtituloRegistro = tk.Label(
        frmRegistro,
        text="Ingrese los datos del cliente",
        font=("Ubuntu",14),
        bg="#212227",
        fg="#76838F"
    )
    lblSubtituloRegistro.grid(
        row=1,
        column=0,
        sticky="w",
        padx=(20,0),
        pady=(5,0)    
    )
    
    #pedimos el nombre del cliente
    lblNombreCliente = tk.Label(
        frmRegistro,
        text="Nombre",
        font=("Ubuntu",14),
        bg="#212227",
        fg="#FFFFFF"  
    )
    
    lblNombreCliente.grid(
        row=2,
        column=0,
        sticky="w",
        padx=(20,0),
        pady=(20,0) 
    )
    
    txtNombreCliente = CTk.CTkEntry(
        frmRegistro,
        width=455,
        height=45,
        fg_color="#212227",
        text_color="#FFFFFF",
        placeholder_text_color="#C9C8C8",
        placeholder_text="Nombre",
        font=("Ubuntu",14),
        border_color="#322F2F"
    )
    txtNombreCliente.grid(
        row=3,
        column=0,
        columnspan=2,
        sticky="w",
        padx=(20,0),
        pady=(3,0)
    )
    
    #pedimos los apellidos del cliente
    lblApellidoCliente = tk.Label(
        frmRegistro,
        text="Apellido",
        font=("Ubuntu",14),
        bg="#212227",
        fg="#FFFFFF"   
    )
    
    lblApellidoCliente.grid(
        row=4,
        column=0,
        sticky="w",
        padx=(20,0),
        pady=(20,0) 
    )
    
    txtApellidoCliente = CTk.CTkEntry(
        frmRegistro,
        width=455,
        height=45,
        fg_color="#212227",
        text_color="#FFFFFF",
        placeholder_text_color="#C9C8C8",
        placeholder_text="Apellido",
        font=("Ubuntu",14),
        border_color="#322F2F"
    )
    txtApellidoCliente.grid(
        row=5,
        column=0,
        sticky="w",
        padx=(20,0),
        pady=(3,0)
    )
    
    #pedimos la edad del cliente
    lblEdadCliente = tk.Label(
        frmRegistro,
        text="Edad",
        font=("Ubuntu",14),
        bg="#212227",
        fg="#FFFFFF"   
    )
    
    lblEdadCliente.grid(
        row=6,
        column=0,
        sticky="w",
        padx=(20,0),
        pady=(20,0) 
    )
    
    txtEdadCliente = CTk.CTkEntry(
        frmRegistro,
        width=455,
        height=45,
        fg_color="#212227",
        text_color="#FFFFFF",
        placeholder_text_color="#C9C8C8",
        placeholder_text="Edad",
        font=("Ubuntu", 14),
        border_color="#322F2F",
        validate="key",
        validatecommand=(validacionEntero, "%P")
    )
    txtEdadCliente.grid(
        row=7,
        column=0,
        sticky="w",
        padx=(20,0),
        pady=(3,0)
    )
    
    #le pedimos el telefono al cliente
    lblTelefonoCliente = tk.Label(
        frmRegistro,
        text="Telefono",
        font=("Ubuntu",14),
        bg="#212227",
        fg="#FFFFFF"   
    )
    
    lblTelefonoCliente.grid(
        row=8,
        column=0,
        sticky="w",
        padx=(20,0),
        pady=(20,0) 
    )
    
    txtTelefonoCliente = CTk.CTkEntry(
        frmRegistro,
        width=455,
        height=45,
        fg_color="#212227",
        text_color="#FFFFFF",
        placeholder_text_color="#C9C8C8",
        placeholder_text="12345678",
        font=("Ubuntu", 14),
        border_color="#322F2F",
        validate="key",
        validatecommand=(validacionTelefono,"%P")
    )
    txtTelefonoCliente.grid(
        row=9,
        column=0,
        sticky="w",
        padx=(20,0),
    )
    
    #le pedimos el telefono al cliente
    lblDUICliente = tk.Label(
        frmRegistro,
        text="DUI",
        font=("Ubuntu",14),
        bg="#212227",
        fg="#FFFFFF"   
    )
    
    lblDUICliente.grid(
        row=10,
        column=0,
        sticky="w",
        padx=(20,0),
        pady=(20,0) 
    )
    
    txtDUICliente = CTk.CTkEntry(
        frmRegistro,
        width=455,
        height=45,
        fg_color="#212227",
        text_color="#FFFFFF",
        placeholder_text_color="#C9C8C8",
        placeholder_text="12345678-9",
        font=("Ubuntu", 14),
        border_color="#322F2F"
    )
    txtDUICliente.grid(
        row=11,
        column=0,
        sticky="w",
        padx=(20,0)
    )
    #frame donde de alojaran los botones
    if datos is not None:
            txtNombreCliente.insert(0,datos[1])
            txtApellidoCliente.insert(0,datos[2])
            txtTelefonoCliente.insert(0,datos[3])
            txtDUICliente.insert(0,datos[4])
            txtEdadCliente.insert(0,datos[5])
    frmBotones = tk.Frame(frmRegistro,bg="#212227")
    frmBotones.grid(columnspan=2,row=12,column=0,sticky="nsew")
    #boton para registrar los clientes
    btnRegistrar = CTk.CTkButton(
        frmBotones,
        text=textBtn,
        height=45,
        fg_color="#BC72FF",
        text_color="#FFFFFF",
        hover_color="#975DD2",
        command= lambda: ingresoCliente(txtNombreCliente,txtApellidoCliente,txtEdadCliente,txtTelefonoCliente,txtDUICliente,RegistrarClientes,idCliente)
    )
    
    btnRegistrar.grid(
        row=0,
        column=0,
        sticky="w",
        padx=(20,0),
        pady=(30,0)
    )
    def ingresoCliente(txtNombre,txtApellido,txtEdad, txtTelefono, txtDui,formulario, idCliente):
        nombre = txtNombre.get()
        apellido = txtApellido.get()
        edad = txtEdad.get()
        telefono = txtTelefono.get()
        dui = txtDui.get()
        if nombre.strip() == "":
            cerrado = mostrarAdvertencia(formulario,"Ingrese nombre","Debe ingresar un nombre")
            if cerrado:
                formulario.grab_set()
            cerrado = None
            return
        if apellido.strip() == "":
            cerrado = mostrarAdvertencia(formulario,"Ingrese apellido","Debe ingresar un apellido")
            if cerrado: 
                formulario.grab_set()
            cerrado = None
            return
        if edad.strip() == "":
            cerrado = mostrarAdvertencia(formulario,"Ingrese edad","Debe ingresar una edad")
            if cerrado:
                formulario.grab_set()
            cerrado = None
            return
        edad = int(edad)
        if edad < 18 or edad > 120:
            cerrado = mostrarAdvertencia(formulario,"Edad invalida","Debe ingresar una edad entre 18 y 120")
            if cerrado:
                formulario.grab_set()
            cerrado = None
            return
        if telefono.strip() == "":
            cerrado = mostrarAdvertencia(formulario,"Ingrese telefono","Debe ingresar un telefono")
            if cerrado:
                formulario.grab_set()
            cerrado = None
            return
        if not ValidarTelefono(telefono):
            cerrado = mostrarAdvertencia(formulario,"Telefono invalido","El telefono debe estar en el formato 12345678")
            if cerrado:
                formulario.grab_set()
            cerrado = None
            return
        if dui.strip() == "":
            cerrado = mostrarAdvertencia(formulario,"Ingrese DUI","Debe ingresar un DUI")
            if cerrado:
                formulario.grab_set()
            cerrado = None
            return
        if not ValidarDUI(dui):
            cerrado = mostrarAdvertencia(formulario,"DUI invalido","El DUI es invalido\nIngrese un dui en el formato 12345678-9\nO ingrese un DUI que sea valido")
            if cerrado:
                formulario.grab_set()
            cerrado = None
            return
        #realizamos las conexiones para enviar a la base de datos los datos
        conec = None
        try:
            conec = conexion(formulario)
            cursor = conec.cursor()
            if idCliente is None:
                cursor.execute("insert into clientes(nombre,apellido,edad,telefono,Dui) values (?,?,?,?,?)",(nombre,apellido,edad,telefono,dui))
                conec.commit()
                formulario.destroy()
                mostrarExito(None,"Operacion exitosa","Se ha registrado con exito al cliente")
                listarEventos()
            else:#se modifica un cliente ya existente
                cursor.execute("EXEC sp_ModClientes ?,?,?,?,?,?;",(idCliente,nombre,apellido,telefono,dui,edad))
                if cursor.rowcount == 0:
                    mostrarAdvertencia(formulario,"Registro no encontrado","La persona ya no existe en la base de datos")
                    return
                #guardamos los cambios
                conec.commit()
                mostrarExito(None,"Operacion exitosa","Se ha actualizado con exito el cliente")
                formulario.destroy()
                listarEventos()
                
        except pyodbc.Error as error:
            if conec is not None:
                conec.rollback()
            mostrarError(formulario,"Error de base de datos",f"No se pudieron guardar los cambios\n\n{error}")
        finally:
            if conec is not None:
                conec.close()
    #boton para cancelar
    btnCancelar = CTk.CTkButton(
        frmBotones,
        text="Cancelar",
        height=45,
        fg_color="#3E4B5B",
        text_color="#FFFFFF",
        hover_color="#596C82",
        command=RegistrarClientes.destroy
    )
    
    btnCancelar.grid(
        row=0,
        column=1,
        sticky="w",
        padx=(20,0),
        pady=(30,0)
    )

#funcion para enviar a la base de datos el registro del cliente

#funciones para validaciones
#funcion para validar el telefono
def ValidarTelefono(Telefono):
    # Patron para validar la expresion regular"
    patron = re.compile(r"^\d{8}$")
    # Se verifica si cumple el patron  para continuar con la validacion
    if patron.match(Telefono):
        return True
    else:
        return False
    
#funcion que validara el DUI
def ValidarDUI(dui):
    # expresion regular para validar dui
    patron = re.compile("^\\d{8}-\\d$")
    # Variables globales a utilizar
    global residuo
    # Se verifica si cumple el patron  para continuar con la validacion
    if patron.match(dui):
        # Se obtiene la posicion del digito verificador
        digitoVerificador = int(dui[9])

        # se inicia Variable de posiciones a operar dentro de la cadena
        numero = 10
        # Obtenemos la cadena sin guion
        cadenaDui = dui[0:8]
        # contador
        sum = 0
        # Se itera la cadena operando segun las posiciones
        for indice in range(len(cadenaDui)):
            caracter = cadenaDui[indice]
            numero = numero - 1
            # sumamos  el resultado de multiplicar las posiciones * cada elemento de la cadena o #Dui
            sum = sum + (numero * int(caracter))
            residuo = sum % 10
            # Obtenemos el residuo y lo evaluamos
            if residuo > 0:
                residuo = residuo - 10
        # Si el residuo es mayor que 0  se realiza la resta de 10
        # luego se realiza la validacion del documento
        if abs(residuo) == digitoVerificador or residuo == 0:
            # Si el residuo es igual al digito verificador o igual a cero
            # El documento se da por validado y devuelve Verdadero, si no significa que es invalido entonces devolvera Falso
            return True
        else:
            return False
    else:
        return False
#la funcion tambien servira para modificar los eventos
def generarModalRegistrarEventos(VentanaPrincipal,listarEventos,idEvento = None, datos = None):
    #creamos el toplevel
    RegistrarEventos = CTk.CTkToplevel(
        VentanaPrincipal
    )
    
    
    #Generamos la ventana centrada y con un tamaño adecuado para un formulario
    centrar_ventana(VentanaPrincipal,RegistrarEventos,500,600)
    RegistrarEventos.resizable(False,False)
    #agregamos la relacion del top level y lo convertimos en una ventana modal
    RegistrarEventos.transient(VentanaPrincipal)
    RegistrarEventos.grab_set()
    #creamos un frame para almacenar todos los elementos 
    frmRegistro = tk.Frame(
        RegistrarEventos,
        bg="#212227"
    )
    #hacemos que cubra toda la ventana modal
    frmRegistro.pack(
        fill="both",
        expand=True
    )
    if idEvento is None:
        lblEncabezadoRegistro = tk.Label(
            frmRegistro,
            text="Registrar Evento",
            font=("Ubuntu",16,"bold"),
            bg="#212227",
            fg="#FFFFFF"
        )
        RegistrarEventos.title("Registro de eventos")
        textBtn = "Registrar"
    else:
        lblEncabezadoRegistro = tk.Label(
            frmRegistro,
            text="Modificar Evento",
            font=("Ubuntu",16,"bold"),
            bg="#212227",
            fg="#FFFFFF"
        )
        RegistrarEventos.title("Modificar de evento")
        textBtn = "Modificar"
        
    lblEncabezadoRegistro.grid(
        row=0,
        column=0,
        padx=(20,0),
        pady=(25,0),
        sticky="sw"
    )
    #agregamos un subtitulo a el formulario
    lblSubtituloRegistro = tk.Label(
        frmRegistro,
        text="Ingrese los datos del evento",
        font=("Ubuntu",14),
        bg="#212227",
        fg="#76838F"
    )
    lblSubtituloRegistro.grid(
        row=1,
        column=0,
        sticky="w",
        padx=(20,0),
        pady=(5,0)    
    )
    
    #pedimos el nombre del cliente
    lblNombreEvento = tk.Label(
        frmRegistro,
        text="Nombre del evento",
        font=("Ubuntu",14),
        bg="#212227",
        fg="#FFFFFF"  
    )
    
    lblNombreEvento.grid(
        row=2,
        column=0,
        sticky="w",
        padx=(20,0),
        pady=(20,0) 
    )
    
    txtNombreEvento = CTk.CTkEntry(
        frmRegistro,
        width=455,
        height=45,
        fg_color="#212227",
        text_color="#FFFFFF",
        placeholder_text_color="#C9C8C8",
        placeholder_text="Nombre del evento",
        font=("Ubuntu",14),
        border_color="#322F2F"
    )
    txtNombreEvento.grid(
        row=3,
        column=0,
        columnspan=2,
        sticky="w",
        padx=(20,0),
        pady=(3,0)
    )
    # pedimos la fecha del evento
    lblFechaEvento = tk.Label(
        frmRegistro,
        text="Fecha del evento",
        font=("Ubuntu",14),
        bg="#212227",
        fg="#FFFFFF"  
    )
    
    lblFechaEvento.grid(
        row=4,
        column=0,
        sticky="w",
        padx=(20,0),
        pady=(20,0) 
    )
    #se ingresa en un entry la fecha
    txtFechaEvento = CTk.CTkEntry(
        frmRegistro,
        width=455,#si se puede cambiar por un calendario se realizara si logra ser conveniente
        height=45,
        fg_color="#212227",
        text_color="#FFFFFF",
        placeholder_text_color="#C9C8C8",
        placeholder_text="YYYY-mm-dd",
        font=("Ubuntu",14),
        border_color="#322F2F"
    )
    txtFechaEvento.grid(
        row=5,
        column=0,
        columnspan=2,
        sticky="w",
        padx=(20,0),
        pady=(3,0)
    )
    #pedimos el tipo de evento que es
    lblTipoEvento = tk.Label(
        frmRegistro,
        text="Tipo de evento",
        font=("Ubuntu",14),
        bg="#212227",
        fg="#FFFFFF"  
    )
    
    lblTipoEvento.grid(
        row=6,
        column=0,
        sticky="w",
        padx=(20,0),
        pady=(20,0) 
    )
    #se ingresa en un ctkcombobox
    cmbTipoEvento = CTk.CTkComboBox(
        frmRegistro,
        width=455,
        height=45,
        values=TIPOEVENTO,
        fg_color="#212227",
        text_color="#FFFFFF",
        font=("Ubuntu",14),
        border_color="#322F2F",
        state="readonly"
    )
    #le damos el valor predeterminado de Bodas
    cmbTipoEvento.set("Bodas")
    cmbTipoEvento.grid(
        row=7,
        column=0,
        columnspan=2,
        sticky="w",
        padx=(20,0),
        pady=(3,0)
    )
    #Creamos el campo donde ingresara la direccion
    lblDireccionEvento = tk.Label(
        frmRegistro,
        text="Direccion del evento",
        font=("Ubuntu",14),
        bg="#212227",
        fg="#FFFFFF"  
    )
    
    lblDireccionEvento.grid(
        row=8,
        column=0,
        sticky="w",
        padx=(20,0),
        pady=(20,0) 
    )
    #se ingresa en un ctktextbox
    txtDireccionEvento = CTk.CTkTextbox(
        frmRegistro,
        width=455,
        height=90,
        fg_color="#212227",
        text_color="#FFFFFF",
        font=("Ubuntu",14),
        border_color="#322F2F",
        border_width=2
    )
    txtDireccionEvento.grid(
        row=9,
        column=0,
        columnspan=2,
        sticky="w",
        padx=(20,0),
        pady=(3,0)
    )
    #si hay datos se ingresan aqui para poder cargarse en los entry
    if datos is not None:
        txtNombreEvento.insert(0,datos[1])
        cmbTipoEvento.set(datos[2])
        txtFechaEvento.insert(0,datos[3])
        txtDireccionEvento.insert("1.0",datos[4])
    #frame donde de alojaran los botones
    frmBotones = tk.Frame(frmRegistro,bg="#212227")
    frmBotones.grid(columnspan=2,row=12,column=0,sticky="nsew")
    #boton para registrar los clientes
    
    btnRegistrar = CTk.CTkButton(
        frmBotones,
        text=textBtn,
        height=45,
        fg_color="#BC72FF",
        text_color="#FFFFFF",
        hover_color="#975DD2",
        command= lambda: ingresoEvento(txtNombreEvento,txtFechaEvento,cmbTipoEvento,txtDireccionEvento,RegistrarEventos,idEvento)
    )
    btnRegistrar.grid(
        row=0,
        column=0,
        sticky="w",
        padx=(20,0),
        pady=(30,0)
    )
    #funcion para insertar el evento a la base de datos
    def ingresoEvento(txtNombreEvento,txtFecha,cmbTipo, txtDireccion,formulario,idEvento):
        nombre = txtNombreEvento.get()
        fecha = txtFecha.get()
        tipo = cmbTipo.get()
        direccion = txtDireccion.get("1.0",tk.END)

        if nombre.strip() == "":
            cerrado = mostrarAdvertencia(formulario,"Ingrese nombre","Debe ingresar un nombre del evento")
            if cerrado: #volvemos a fijar el formulario despues que se cierra el mensaje,
                formulario.grab_set()# esto es debido al comportamiento de la libreria que le quita la propiedad de ser
            cerrado = None 
            return  # ventana modal al formulario cuando este mensaje se muestra
        
        if fecha.strip() == "":
            cerrado = mostrarAdvertencia(formulario,"Ingrese fecha","Debe ingresar la fecha del evento")
            if cerrado:
                formulario.grab_set()
            cerrado = None
            return
        if not validarFecha(fecha):
            cerrado = mostrarAdvertencia(formulario,"Formato incorrecto","Solo se permite el siguiente formato año-mes-dia")
            if cerrado:
                formulario.grab_set()
            cerrado = None
            return
        else:
            fecha = datetime.strptime(fecha, "%Y-%m-%d")
        if fecha <= datetime.today():
            cerrado = mostrarAdvertencia(formulario,"Ingrese fecha","Debe ingresar una fecha mayor a la actual")
            if cerrado:
                formulario.grab_set()
            cerrado = None
            return
        
        if direccion.strip() == "":
            cerrado = mostrarAdvertencia(formulario,"Ingrese direccion","Debe ingresar una direccion")
            if cerrado:
                formulario.grab_set()
            cerrado = None
            return
        
        #realizamos las conexiones para enviar a la base de datos los datos
        conec = None
        try:
            conec = conexion(formulario)
            cursor = conec.cursor()
            if idEvento is None:#se inserta un evento nuevo
                cursor.execute("insert into eventos(nombre,tipo,fecha,lugar) values (?,?,?,?);",(nombre,tipo,fecha,direccion))
                conec.commit()
                formulario.destroy()
                mostrarExito(None,"Operacion exitosa","Se ha registrado con exito el evento")
                listarEventos()
            else:#se modifica un evento ya existente
                cursor.execute("EXEC sp_ModEventos ?,?,?,?,?;",(idEvento,nombre,tipo,fecha,direccion))
                if cursor.rowcount == 0:
                    mostrarAdvertencia(formulario,"Registro no encontrado","El evento ya no existe en la base de datos")
                    return
                #guardamos los cambios
                conec.commit()
                mostrarExito(None,"Operacion exitosa","Se ha actualizado con exito el evento")
                formulario.destroy()
                listarEventos()
        except pyodbc.Error as error:
            if conec is not None:
                conec.rollback()
            mostrarError(formulario,"Error de base de datos",f"No se pudieron guardar los cambios\n\n{error}")
        finally:
            if conec is not None:
                conec.close()
    
    
    #boton para cancelar
    btnCancelar = CTk.CTkButton(
        
        frmBotones,
        text="Cancelar",
        height=45,
        fg_color="#3E4B5B",
        text_color="#FFFFFF",
        hover_color="#596C82",
        command=RegistrarEventos.destroy
    )
    
    btnCancelar.grid(
        row=0,
        column=1,
        sticky="w",
        padx=(20,0),
        pady=(30,0)
    )



#funcion para validar la fecha para que este en un formato compatible para sql server
def validarFecha(fecha):
    try:
        # Intenta convertir la cadena a fecha
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    #Si la fecha esta mal se disparara uno de estos errores
    except ValueError:
        return False
    except AttributeError:
        return False
    except:
        return False

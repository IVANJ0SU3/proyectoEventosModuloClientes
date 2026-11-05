# Bibliotecas a usar para el código
import tkinter as tk
import customtkinter as Ctk
from PIL import Image, ImageTk

# Funciones del menú
from funciones import crearMenu, mostrarFrame
#variables
ventanaPrincipal = None
# Funciones de las páginas
from framesMenus import (
    crearInicio,
    crearClientes,
    crearEventos
)


def generarVentanaPrincipal():

    ventanaPrincipal = Ctk.CTk()
    ventanaPrincipal.block_update_dimensions_event()
    ventanaPrincipal.title("Agencia De Eventos")
    # CONFIGURACIÓN DE LA VENTANA
    ancho_ventana = 1000
    altura_ventana = 700
    # Obtener dimensiones de la pantalla
    ancho_pantalla = ventanaPrincipal.winfo_screenwidth()
    altura_pantalla = ventanaPrincipal.winfo_screenheight()

    # Calcular posición para centrar
    x = ((ancho_pantalla) - (ancho_ventana)) // 2
    y = ((altura_pantalla) - (altura_ventana)) // 2

    # Aplicar geometría
    ventanaPrincipal.geometry(
        f"{ancho_ventana}x{altura_ventana}+{x}+{y}"
    )

    # No permitir cambiar tamaño
    ventanaPrincipal.resizable(False, False)



    # CREAR MENÚ PRINCIPAL

    #creamos el frame donde estara el menu lateral y el frame donde estara el menu principal
    frmMenuLateral, frmMenuPrincipal = crearMenu(
        ventanaPrincipal
    )

    #le agregamos la imagen del logo --es provicional la que agregue
    #obtenemos la imagen sin escalar
    ruta = "img/logo.png"
    LogoOrigen = Image.open(ruta)
    #lo redimensionamos y lo enpaquetamos en un una ctkimage
    Logo = Ctk.CTkImage(
        light_image=LogoOrigen, 
        dark_image=LogoOrigen, 
        size=(150, 75)
    )

    btnLogo = Ctk.CTkButton(
        frmMenuLateral,
        image=Logo,
        text="",
        command=lambda: mostrarFrame(frmInicio),
        fg_color="#222328",
        hover_color="#222328"
    ) #lo metemos en un CTkButton y lo agregamos para cuando se presione lo lleve al menu (posible acciona a futuro, abrir opciones como cerrar o minimizar el programa)
    btnLogo.pack()
    
    # CREAR LOS DIFERENTES FRAMES DE CADA MENU
    frmInicio = crearInicio(
        frmMenuPrincipal
    )

    frmClientes = crearClientes(
        frmMenuPrincipal,
        ventanaPrincipal
    )

    frmEventos = crearEventos(
        frmMenuPrincipal,
        ventanaPrincipal
    )
    # BOTONES DEL MENÚ LATERAL
    #boton para acceder al menu de inicio
    btnInicio = Ctk.CTkButton(
            frmMenuLateral,
            text="Inicio",
            command=lambda: mostrarFrame(frmInicio),
            corner_radius=0,
            fg_color="#222328",
            height=55,
            font=("Ubuntu",14,"bold")
        )
    
    btnInicio.pack(
        fill="x",
        pady=(10,0)
    )
    
    #boton para acceder al menu de los clientes
    
    btnClientes = Ctk.CTkButton(
        frmMenuLateral,
        text="Clientes",
        command=lambda: mostrarFrame(frmClientes),
        corner_radius=0,
        fg_color="#222328",
        height=55,
        font=("Ubuntu",14,"bold")
    )

    btnClientes.pack(
        fill="x"
    )

    #boton para accederal menu de eventos
    btnEventos = Ctk.CTkButton(
        frmMenuLateral,
        text="Eventos",
        command=lambda: mostrarFrame(frmEventos),
        corner_radius=0,
        fg_color="#222328",
        height=55,
        font=("Ubuntu",14,"bold")
    )

    btnEventos.pack(
        fill="x"
    )


    # --------------------------------------------------
    # MOSTRAR EL FRAME INICIAL
    # --------------------------------------------------

    mostrarFrame(frmInicio)


    # --------------------------------------------------
    # INICIAR APLICACIÓN
    # --------------------------------------------------

    ventanaPrincipal.mainloop()


# Ejecutar programa
generarVentanaPrincipal()
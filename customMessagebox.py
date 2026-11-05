#Creamos un archivo para generar messagebox personalizados para que queden acorde a la estetica del programa
from CTkMessagebox import CTkMessagebox #importamos la biblioteca basada en customTkinter para crear los
#messagebox

def mostrarInfo(ventana,titulo,msg):
    # mensaje para mostrar informacion
    acept = CTkMessagebox(master=ventana,title=titulo, message=msg, option_1="Aceptar")
    #devuelve para confirmar que se cerro
    retorno = (acept.get() == "Aceptar")
    return retorno

def mostrarExito(ventana,titulo,msg):
    # Muestra cuando se realizo exitosamente una accion
    acept = CTkMessagebox(master=ventana,title=titulo,message=msg,icon="check", option_1="Aceptar")
    #devuelve para confirmar que se cerro
    retorno = (acept.get() == "Aceptar")
    return retorno
    
def mostrarError(ventana,titulo,msg):
    # Muestra cuando hubo un error
    acept = CTkMessagebox(master=ventana,title=titulo, message=msg, icon="cancel",option_1="Aceptar")
    #devuelve para confirmar que se cerro
    retorno = (acept.get() == "Aceptar")
    return retorno
    
def mostrarAdvertencia(ventana,titulo,msg):
    # Muestra una advertencia
    acept = CTkMessagebox(master=ventana,title=titulo, message=msg,icon="warning", option_1="Aceptar")
    #devuelve para confirmar que se cerro
    retorno = (acept.get() == "Aceptar")
    return retorno

        
def preguntarSiNo(ventana,titulo,msg):
    # Hace una pregunta de si o no
    respuesta = CTkMessagebox(master=ventana,title=titulo, message=msg,icon="question", option_1="Si", option_2="No")
    yesNo = (respuesta.get() == "Si")#variable booleana que se devuelve
    return yesNo

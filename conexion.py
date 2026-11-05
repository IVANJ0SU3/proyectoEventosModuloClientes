import pyodbc   #Base de datos
from customMessagebox import mostrarError

def conexion(ventana):
    try:
        server = '192.168.134.176'  
        database = 'SistemaEventos'
        username = 'SistemaEvento'
        password = 'Eventos123'
        driver = '{ODBC Driver 17 for SQL Server}'  

        conn_str = (
            f'DRIVER={driver};'
            f'SERVER={server},1433;'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password};'
            f'Encrypt=yes;'  
            f'TrustServerCertificate=yes;'  
        )
        conec = pyodbc.connect(conn_str)
        return conec
    except pyodbc.Error as e:
        mostrarError(None, "Error", f"No se ha podido conectar a la base de datos\n\nDetalle: {e}")
        exit()
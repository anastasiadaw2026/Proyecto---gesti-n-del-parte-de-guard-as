import mysql.connector

try:
    conexion = mysql.connector.connect(user='root', password='root',
                                       host='127.0.0.1', database='gestion_guardias')
    conexion.autocommit = True
    CONTRASENIA = 'root'

except Exception:
    print('No se ha podido establecer la conexión a la base de datos.\n'
          'Verifique que la base de datos está activa e intente ejecutar la '
          'aplicación de nuevo.')
    raise SystemExit

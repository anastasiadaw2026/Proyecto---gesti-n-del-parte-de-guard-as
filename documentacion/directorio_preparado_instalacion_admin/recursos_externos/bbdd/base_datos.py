import datetime
import subprocess

import bcrypt

from claves.conexion_bbdd import conexion, CONTRASENIA
from lib.aula import Aula
from lib.curso import Curso
from lib.guardia import Guardia
from lib.hora import Hora
from lib.profesor import Profesor


class BaseDatos:
    @staticmethod
    def hacer_backup():
        try:
            fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            archivo_backup = f"../backups/backup_{fecha_hora}.sql"
            with open(archivo_backup, "w", encoding="utf-8") as archivo:
                proceso = subprocess.run(
                    ["docker", "exec", "-e", f"MYSQL_PWD={CONTRASENIA}",
                        "mysql_daw1", "mysqldump", "-u", "root",
                        "--single-transaction", "--set-gtid-purged=OFF",
                        "gestion_guardias"], stdout=archivo,
                    stderr=subprocess.PIPE, text=True)
            if proceso.returncode == 0:
                return True, archivo_backup
            return False, 'No se pudo realizar la copia de seguridad.'
        except:
            return False, 'No se pudo realizar la copia de seguridad.'

    # todo: cuando acabare de hacer los test tengo que crear el truncate
    #  guardias también
    @staticmethod
    def vaciar_bbdd():
        conexion.autocommit = False
        cursor = None
        try:
            cursor = conexion.cursor()
            vaciar = ['SET FOREIGN_KEY_CHECKS = 0',
                      'DELETE FROM AULAS',
                      'DELETE FROM PROFESORES',
                      'DELETE FROM aulas',
                      'DELETE FROM cursos',
                      'DELETE FROM horas',
                      'SET FOREIGN_KEY_CHECKS = 1']
            for truncate in vaciar:
                cursor.execute(truncate)
            conexion.commit()
            return True
        except:
            conexion.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            conexion.autocommit = True


    @staticmethod
    def recoger_info_ficheros():
        cursos = []
        aulas = []
        horas = []
        profesores = []
        cursor = None
        try:
            cursor = conexion.cursor()
            with open('../recursos_externos/ficheros/cursos.csv', mode='r',
                      encoding='utf-8-sig') as f:
                for linea in f.readlines():
                    curso, letras = linea.strip().split(',')
                    for letra in letras.strip().split(';'):
                        cursos.append(str(curso + "-" + letra))
            with open('../recursos_externos/ficheros/aulas.txt', mode='r',
                      encoding='utf-8') as f:
                for aula in f.readlines():
                    aulas.append(aula.upper().strip())
            with open('../recursos_externos/ficheros/horas.txt', mode='r',
                      encoding='utf-8') as f:
                for hora in f.readlines():
                    horas.append(hora.strip())
            with (open('../recursos_externos/ficheros/profesores.csv', 'r',
                       encoding
                  = 'utf-8') as f):
                for index, line in enumerate(f.readlines()):
                    if index > 0:
                        datos_profesor = line.strip('').replace('\"',
                                        '').split(',')
                        profesor = Profesor(datos_profesor[0].strip(),
                                            datos_profesor[1].strip())
                        profesores.append(profesor)
            return cursos, aulas, horas, profesores
        except:
            return False
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def guardar_claves_profesores():
        try:
            profesores = BaseDatos.recoger_info_ficheros()[3]
            with open('../claves/claves_profesores.txt', 'w', encoding =
                        'utf-8') as fclaves:
                for profesor in profesores:
                    fclaves.write(profesor.id + ' - ' + profesor.clave + '\n')
            return ('Las claves de acceso de los profesores se han guardado '
                    'en un fichero externo en caso de que las quiera '
                    'consultar.')
        except:
            return ('El fichero para guardar las claves no se pudo abrir, '
                    'por tanto, las claves de los profesores no se pueden '
                    'ver.')

    @staticmethod
    def cargar_tablas():
        cursor = None
        try:
            if BaseDatos.recoger_info_ficheros():
                cursor = conexion.cursor()
                cursos, aulas, horas, profesores = (
                    BaseDatos.recoger_info_ficheros())
                for curso in cursos:
                    aniadir_curso = f'INSERT INTO cursos VALUES("{curso}")'
                    cursor.execute(aniadir_curso)
                for aula in aulas:
                    aniadir_aulas = (f'INSERT INTO AULAS VALUES("'
                                     f'{aula.strip().upper()}")')
                    cursor.execute(aniadir_aulas)
                for hora in horas:
                    aniadir_horas = f'INSERT INTO HORAS VALUES("{hora.strip()}")'
                    cursor.execute(aniadir_horas)
                for profesor in profesores:
                    aniadir_profesor = (
                        f"INSERT INTO PROFESORES VALUES('{profesor.id}',"
                        f"'{profesor.nombre}','{profesor.apellidos}',"
                        f"'{profesor.clave_encriptada}')")
                    cursor.execute(aniadir_profesor)
                return True
            else:
                return False
        except:
            return False
        finally:
            if cursor:
                cursor.close()


    @staticmethod
    def sacar_profesores():
        cursor = None
        try:
            cursor = conexion.cursor()
            profesores = []
            selecioonar_profe = ('select nombre, apellidos from profesores '
                                 'order by nombre, apellidos')
            cursor.execute(selecioonar_profe)
            for profesor in cursor:
                profesores.append(Profesor(profesor[0], profesor[1]))
            return profesores
        except:
            return False
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def sacar_horas():
        cursor = None
        try:
            cursor = conexion.cursor()
            horas = []
            seleccionar_horas = ('select nombre from horas '
                                 'order by length(nombre)')
            cursor.execute(seleccionar_horas)
            for nombre in cursor:
                hora = Hora()
                hora.nombre = nombre[0]
                horas.append(hora)
            return horas
        except:
            return False
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def sacar_cursos():
        cursor = None
        try:
            cursor = conexion.cursor()
            cursos = []
            seleccionar_cursos = ('select nombre from cursos '
                                  'order by nombre')
            cursor.execute(seleccionar_cursos)
            for nombre in cursor:
                curso = Curso()
                curso.nombre = nombre[0].strip()
                cursos.append(curso)
            return cursos
        except:
            return False
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def sacar_aulas():
        cursor = None
        try:
            cursor = conexion.cursor()
            aulas = []
            seleccionar_aulas = ('select nombre from aulas '
                                 'order by nombre')
            cursor.execute(seleccionar_aulas)
            for nombre in cursor:
                aula = Aula()
                aula.nombre = nombre[0].strip()
                aulas.append(aula)
            return aulas
        except:
            return False
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def autentificar_profesor(id_introducido, clave_introducida):
        cursor = None
        try:
            cursor = conexion.cursor()
            comprobacion = (f'select clave from profesores '
                            f'where id = "{id_introducido}"')
            cursor.execute(comprobacion)
            clave = cursor.fetchone()
            if clave:
                clave = clave[0]
                resultado = bcrypt.checkpw(clave_introducida.encode('utf-8'),
                                      clave.encode('utf-8'))
                if not resultado:
                    return ''
                return resultado
            else:
                return ''
        except:
            return False
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def sacar_prof_por_id(id_prof):
        cursor = None
        try:
            cursor = conexion.cursor()
            selecionar_profe = (f'select nombre, apellidos from profesores '
                                 f'where id = "{id_prof}"')
            cursor.execute(selecionar_profe)
            profesor = cursor.fetchone()
            return profesor
        except:
            return False
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def almacenar_guardias(cursor) -> list[Guardia]:
        guardias = []
        for guardia in cursor:
            guardia_creada = Guardia()
            guardia_creada.id = Profesor(guardia[0], guardia[1])
            guardia_creada.dia = guardia[2]
            guardia_creada.hora = guardia[3]
            guardia_creada.curso = guardia[4]
            guardia_creada.clase = guardia[5]
            guardia_creada.tarea = guardia[6]
            guardia_creada.ficheros = guardia[7]
            guardias.append(guardia_creada)
        return guardias

    @staticmethod
    def seleccionar_guardias_por_fechas(fecha_inicio, fecha_fin) -> list[
        Guardia]|bool:
        cursor = None
        guardias = []
        try:
            cursor = conexion.cursor()
            seleccion_guardias = (
                'select nombre, apellidos, dia, hora, curso, aula, tarea, ficheros '
                'from guardias natural join profesores '
                'where dia between %s and %s '
                'order by dia, hora')
            cursor.execute(seleccion_guardias, (fecha_inicio, fecha_fin))
            guardias = BaseDatos.almacenar_guardias(cursor)
            return guardias
        except:
            return False
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def sacar_las_guardias_existentes():
        cursor = None
        try:
            cursor = conexion.cursor()
            seleccion_guardias = (
                'select nombre, apellidos, dia, hora, curso, aula, tarea, ficheros '
                'from guardias natural join profesores '
                'order by dia, hora')
            cursor.execute(seleccion_guardias)
            guardias = BaseDatos.almacenar_guardias(cursor)
            return guardias
        except:
            return False
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def sacar_guardias_profesor(id_prof):
        cursor = None
        try:
            cursor = conexion.cursor()
            seleccion_guardias = (
                f'select nombre, apellidos, dia, hora, curso, aula, tarea, '
                f'ficheros from guardias natural join profesores '
                f'where id = "{id_prof}" '
                f'order by dia, hora')
            cursor.execute(seleccion_guardias)
            guardias = BaseDatos.almacenar_guardias(cursor)
            cursor.close()
            return guardias
        except:
            return False
        finally:
            if cursor:
                cursor.close()

import unittest
import bcrypt
from claves.conexion_bbdd import conexion
from recursos_externos.bbdd.base_datos import BaseDatos


class TestAutentificarProfesor(unittest.TestCase):
    def test_autentificar_profesor_exitoso(self):
        conexion = conexion
        conexion.autocommit = False

        try:
            clave = "clave123"
            clave_encriptada = bcrypt.hashpw(clave.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO PROFESORES (id, nombre, apellidos, clave) VALUES "
                           "('prof1', 'Juan', 'Pérez', %s)", (clave_encriptada,))
            cursor.close()

            es_autenticado = BaseDatos.autentificar_profesor('prof1', clave)
            self.assertTrue(es_autenticado)

        finally:
            conexion.rollback()
            conexion.autocommit = True

    def test_autentificar_profesor_clave_incorrecta(self):
        conexion = conexion
        conexion.autocommit = False

        try:
            clave_correcta = "clave123"
            clave_incorrecta = "clave_erronea"
            clave_encriptada = bcrypt.hashpw(clave_correcta.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO PROFESORES (id, nombre, apellidos, clave) VALUES "
                           "('prof2', 'Ana', 'Gómez', %s)", (clave_encriptada,))
            cursor.close()

            es_autenticado = BaseDatos.autentificar_profesor('prof2', clave_incorrecta)
            self.assertFalse(es_autenticado)

        finally:
            conexion.rollback()
            conexion.autocommit = True

    def test_autentificar_profesor_id_incorrecto(self):
        conexion = conexion
        conexion.autocommit = False

        try:
            clave = "clave123"
            clave_encriptada = bcrypt.hashpw(clave.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO PROFESORES (id, nombre, apellidos, clave) VALUES "
                           "('prof3', 'Carlos', 'López', %s)", (clave_encriptada,))
            cursor.close()

            es_autenticado = BaseDatos.autentificar_profesor('prof_inexistente', clave)
            self.assertFalse(es_autenticado)

        finally:
            conexion.rollback()
            conexion.autocommit = True


if __name__ == "__main__":
    unittest.main()

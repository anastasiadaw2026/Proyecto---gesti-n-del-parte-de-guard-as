import unittest
from claves.conexion_bbdd import conexion
from recursos_externos.bbdd.base_datos import BaseDatos


class TestSacarProfesores(unittest.TestCase):
    def test_sacar_profesores(self):
        conexion = conexion
        conexion.autocommit = False

        try:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO PROFESORES (id, nombre, apellidos, clave) VALUES "
                           "('prof1', 'Juan', 'Pérez', 'clave1')")
            cursor.execute("INSERT INTO PROFESORES (id, nombre, apellidos, clave) VALUES "
                           "('prof2', 'María', 'López', 'clave2')")

            profesores = BaseDatos.sacar_profesores()

            self.assertTrue(len(profesores) > 0)
            self.assertTrue(all(profesor.nombre and profesor.apellidos for profesor in profesores))

        finally:
            conexion.rollback()
            conexion.autocommit = True


if __name__ == "__main__":
    unittest.main()

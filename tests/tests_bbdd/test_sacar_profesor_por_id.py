import unittest
from claves.conexion_bbdd import conexion
from recursos_externos.bbdd.base_datos import BaseDatos


class TestSacarProfPorId(unittest.TestCase):
    def test_profesor_existente(self):
        conexion = conexion
        conexion.autocommit = False

        try:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO PROFESORES (id, nombre, apellidos, clave) VALUES "
                           "('prof1', 'Ana', 'Sánchez', 'clave123')")
            cursor.close()

            profesor = BaseDatos.sacar_prof_por_id('prof1')

            self.assertIsNotNone(profesor)
            self.assertEqual(profesor[0], 'Ana')
            self.assertEqual(profesor[1], 'Sánchez')

        finally:
            conexion.rollback()
            conexion.autocommit = True

    def test_profesor_inexistente(self):
        conexion = conexion
        profesor = BaseDatos.sacar_prof_por_id('prof_inexistente')
        self.assertIsNone(profesor)


if __name__ == "__main__":
    unittest.main()

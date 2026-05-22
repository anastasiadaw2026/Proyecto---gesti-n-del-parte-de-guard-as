import unittest
from claves.conexion_bbdd import conexion
from recursos_externos.bbdd.base_datos import BaseDatos


class TestSacarAulas(unittest.TestCase):
    def test_sacar_aulas(self):
        conexion = conexion
        conexion.autocommit = False

        try:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO aulas (nombre) VALUES ('Aula 101')")
            cursor.execute("INSERT INTO aulas (nombre) VALUES ('Aula 102')")

            aulas = BaseDatos.sacar_aulas()

            self.assertTrue(len(aulas) > 0)
            self.assertTrue(all(aula.nombre for aula in aulas))

        finally:
            conexion.rollback()
            conexion.autocommit = True


if __name__ == "__main__":
    unittest.main()

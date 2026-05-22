import unittest
from claves.conexion_bbdd import conexion
from recursos_externos.bbdd.base_datos import BaseDatos


class TestSacarHoras(unittest.TestCase):
    def test_sacar_horas(self):
        conexion = conexion
        conexion.autocommit = False

        try:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO horas (nombre) VALUES ('09:00 - 10:00')")
            cursor.execute("INSERT INTO horas (nombre) VALUES ('10:00 - 11:00')")

            horas = BaseDatos.sacar_horas()

            self.assertTrue(len(horas) > 0)
            self.assertTrue(all(hora.nombre for hora in horas))

        finally:
            conexion.rollback()
            conexion.autocommit = True


if __name__ == "__main__":
    unittest.main()

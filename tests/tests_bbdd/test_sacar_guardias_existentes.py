import unittest

from claves.conexion_bbdd import conexion
from lib.guardia import Guardia
from recursos_externos.bbdd.base_datos import BaseDatos


class TestBaseDatos(unittest.TestCase):
    conexion.autocommit = False

    def test_sacar_las_guardias_existentes_with_results(self):
        cursor = conexion.cursor()
        cursor.execute('INSERT INTO guardias values('
                       '"napellido_2aapellido_2b", CURRENT_DATE + 1, '
                       '"8:00 - 8:55", "1BACH-CS", "102", "S", null)')

        result = BaseDatos.sacar_las_guardias_existentes()
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(item, Guardia) for item in result))
        cursor.close()
        conexion.rollback()

    def test_sacar_las_guardias_existentes_no_results(self):
        cursor = conexion.cursor()
        cursor.execute('DELETE from GUARDIAS')

        result = BaseDatos.sacar_las_guardias_existentes()
        self.assertEqual(result, [])
        cursor.close()
        conexion.rollback()
        conexion.autocommit = True


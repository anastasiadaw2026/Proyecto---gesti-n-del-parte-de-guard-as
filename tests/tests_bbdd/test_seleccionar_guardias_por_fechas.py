import unittest
from datetime import date, timedelta

from claves.conexion_bbdd import conexion
from lib.guardia import Guardia
from recursos_externos.bbdd.base_datos import BaseDatos


class TestSeleccionarGuardiasPorFechas(unittest.TestCase):

    def test_seleccionar_guardias_por_fechas_no_results(self):
        conexion.autocommit = False
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM guardias")

        fecha_inicio = date.today() + timedelta(days=5)
        fecha_fin = fecha_inicio + timedelta(days=3)
        result = BaseDatos.seleccionar_guardias_por_fechas(fecha_inicio,
                                                           fecha_fin)

        self.assertEqual(result, [])
        self.assertEqual(len(result), 0)

        cursor.close()
        conexion.rollback()

    def test_seleccionar_guardias_por_fechas_with_results(self):
        conexion.autocommit = False
        cursor = conexion.cursor()
        cursor.execute('DELETE FROM GUARDIAS')
        cursor.execute(
            'INSERT INTO guardias VALUES '
            '("napellido_3aapellido_3b", CURRENT_DATE + 1, "8:00 - 8:55", '
            '"1BACH-GL", "102", "S", NULL), '
            '("napellido_3aapellido_3b", CURRENT_DATE + 2, "8:00 - 8:55", '
            '"2ESO-D", "105", "N", NULL)')

        fecha_inicio = date.today()
        fecha_fin = date.today() + timedelta(days=3)
        result = BaseDatos.seleccionar_guardias_por_fechas(fecha_inicio,
                                                           fecha_fin)

        self.assertEqual(len(result), 2)
        self.assertTrue(isinstance(result[0], Guardia))
        self.assertTrue(isinstance(result[1], Guardia))

        cursor.close()
        conexion.rollback()

    def test_seleccionar_guardias_por_fechas_single_result(self):
        conexion.autocommit = False
        cursor = conexion.cursor()
        cursor.execute('DELETE FROM GUARDIAS')
        cursor.execute(
            'INSERT INTO guardias VALUES '
            '("ndeapellido_4aapellido_4b", CURRENT_DATE + 1, "8:00 - 8:55", '
            '"1BACH-CS", "102", "S", NULL)')

        fecha_inicio = date.today() + timedelta(days=1)
        fecha_fin = fecha_inicio
        result = BaseDatos.seleccionar_guardias_por_fechas(fecha_inicio,
                                                           fecha_fin)

        self.assertEqual(len(result), 1)
        self.assertTrue(isinstance(result[0], Guardia))

        cursor.close()
        conexion.rollback()

        conexion.autocommit = True

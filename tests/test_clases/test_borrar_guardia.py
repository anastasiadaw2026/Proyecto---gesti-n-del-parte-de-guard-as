import unittest
from datetime import date

from claves.conexion_bbdd import conexion
from lib.guardia import Guardia
from lib.hora import Hora
from lib.profesor import Profesor


class TestBorrarGuardia(unittest.TestCase):
    conexion = conexion
    cursor = conexion.cursor()

    def test_borrar_guardia_correcto(self):
        guardia = Guardia()
        guardia.id = Profesor('Nombre 2', 'Apellido_2a Apellido_2b')
        guardia.dia = date(2026, 5, 18)
        guardia.hora = Hora()
        guardia.hora.nombre = '8:55 - 9:50'
        guardia.curso.nombre = '1ESO-B'
        guardia.clase.nombre = "105"
        guardia.tarea = Guardia.NO_TAREA
        guardia.ficheros = ""

        self.conexion.autocommit = False
        guardia.insertar_guardia()
        filas_afectadas = guardia.borrar_guardia()
        self.assertEqual(1, filas_afectadas)

        self.cursor.execute(f"SELECT ficheros FROM guardias WHERE id = "
                            f"'{guardia.id.id}' and dia = "
                            f"'{guardia.dia}' and hora = '{guardia.hora}'")
        resultado = self.cursor.fetchone()
        self.assertIsNone(resultado)
        self.conexion.rollback()

    def test_borrar_guardia_inexistente(self):
        guardia = Guardia()
        guardia.id = Profesor('Nombre 2', 'Apellido_2a Apellido_2b')
        guardia.dia = date(2026, 5, 17)
        guardia.hora = Hora()
        guardia.hora.nombre = '8:55 - 9:50'

        self.conexion.autocommit = False
        filas_afectadas = guardia.borrar_guardia()
        self.assertEqual(0, filas_afectadas)
        self.conexion.rollback()

    def test_borrar_guardia_incorrecto_formato(self):
        guardia = Guardia()
        guardia.id = Profesor('Nombre 2', 'Apellido_2a Apellido_2b')
        guardia.dia = "invalid-date"
        guardia.hora.nombre = '11:15 - 12:10'

        with self.assertRaises(Exception):
            guardia.borrar_guardia()


if __name__ == '__main__':
    unittest.main()

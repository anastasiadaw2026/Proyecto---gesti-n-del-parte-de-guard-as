import unittest
from datetime import date

from claves.conexion_bbdd import conexion
from lib.guardia import Guardia
from lib.hora import Hora
from lib.profesor import Profesor


class TestInsertarGuardia(unittest.TestCase):
    conexion = conexion
    cursor = conexion.cursor()
    guardia = Guardia()
    guardia.id = Profesor('Nombre 1', 'Apellido_1a Apellido_1b')
    guardia.dia = date(2026, 6, 18)
    guardia.hora.nombre = '8:00 - 8:55'
    guardia.curso.nombre = '2ESO-A'
    guardia.clase.nombre = "105"
    guardia.tarea = Guardia.SI_TAREA
    guardia.ficheros = "archivo.pdf"

    def test_insertar_guardia_correcto(self):
        self.conexion.autocommit = False
        self.guardia.insertar_guardia()
        self.cursor.execute(f"SELECT * FROM guardias WHERE id = "
                            f"'{self.guardia.id.id}' and dia = "
                            f"'{self.guardia.dia}' and hora = '{self.guardia.hora}'")
        resultado = self.cursor.fetchone()

        self.assertIsNotNone(resultado)
        self.assertEqual(self.guardia.id.id, resultado[0])
        self.assertEqual(self.guardia.dia, resultado[1])
        self.assertEqual(self.guardia.hora.nombre, resultado[2])
        self.assertEqual(self.guardia.curso.nombre, resultado[3])
        self.assertEqual(self.guardia.clase.nombre, resultado[4])
        self.assertEqual(self.guardia.tarea, resultado[5])
        self.assertEqual(self.guardia.ficheros, resultado[6])

        self.conexion.rollback()

    def test_insertar_guardia_sin_tarea(self):
        self.conexion.autocommit = False
        self.guardia.tarea = Guardia.NO_TAREA
        self.guardia.insertar_guardia()
        self.cursor.execute(f"SELECT tarea FROM guardias WHERE id = "
                            f"'{self.guardia.id.id}' and dia = "
                            f"'{self.guardia.dia}' and hora = '{self.guardia.hora}'")
        resultado = self.cursor.fetchone()

        self.assertIsNotNone(resultado)
        self.assertEqual(self.guardia.tarea, resultado[0])

        self.conexion.rollback()

    def test_insertar_guardia_sin_ficheros(self):
        self.conexion.autocommit = False
        self.guardia.ficheros = ""
        self.guardia.insertar_guardia()
        self.cursor.execute(f"SELECT ficheros FROM guardias WHERE id = "
                            f"'{self.guardia.id.id}' and dia = "
                            f"'{self.guardia.dia}' and hora = '{self.guardia.hora}'")
        resultado = self.cursor.fetchone()

        self.assertIsNotNone(resultado)
        self.assertEqual(self.guardia.ficheros, resultado[0])

        self.conexion.rollback()

    def test_insertar_guardia_fecha_incorrecta(self):
        self.guardia.dia = "invalid-date"
        with self.assertRaises(Exception):
            self.guardia.insertar_guardia()
        self.guardia.dia = date(2026, 6, 18)

    conexion.autocommit = True


if __name__ == "__main__":
    unittest.main()

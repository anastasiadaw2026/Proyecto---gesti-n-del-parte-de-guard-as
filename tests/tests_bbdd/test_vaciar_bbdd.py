import unittest
from claves.conexion_bbdd import conexion
from recursos_externos.bbdd.base_datos import BaseDatos


class TestVaciarBBDD(unittest.TestCase):
    def test_vaciar_bbdd(self):
        cursor = conexion.cursor()
        conexion.autocommit = False


        cursor.execute("INSERT INTO AULAS VALUES ('AULA_TEST')")
        cursor.execute("INSERT INTO PROFESORES VALUES "
                       "('prof_test', 'Profesor_Test', 'Apellidos_Test', 'Clave_Test')")
        cursor.execute("INSERT INTO cursos (nombre) VALUES ('CURSO_TEST')")
        cursor.execute("INSERT INTO horas (nombre) VALUES ('HORA_TEST')")

        cursor.execute("SELECT COUNT(*) FROM AULAS")
        self.assertTrue(cursor.fetchone()[0] > 0)

        cursor.execute("SELECT COUNT(*) FROM PROFESORES")
        self.assertTrue(cursor.fetchone()[0] > 0)

        cursor.execute("SELECT COUNT(*) FROM cursos")
        self.assertTrue(cursor.fetchone()[0] > 0)

        cursor.execute("SELECT COUNT(*) FROM horas")
        self.assertTrue(cursor.fetchone()[0] > 0)

        BaseDatos.vaciar_bbdd()

        cursor.execute("SELECT COUNT(*) FROM AULAS")
        self.assertEqual(cursor.fetchone()[0], 0)

        cursor.execute("SELECT COUNT(*) FROM PROFESORES")
        self.assertEqual(cursor.fetchone()[0], 0)

        cursor.execute("SELECT COUNT(*) FROM cursos")
        self.assertEqual(cursor.fetchone()[0], 0)

        cursor.execute("SELECT COUNT(*) FROM horas")
        self.assertEqual(cursor.fetchone()[0], 0)


        conexion.rollback()
        conexion.autocommit = True


if __name__ == "__main__":
    unittest.main()

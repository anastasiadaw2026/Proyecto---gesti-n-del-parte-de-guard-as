import unittest
from claves.conexion_bbdd import conexion
from recursos_externos.bbdd.base_datos import BaseDatos


class TestSacarCursos(unittest.TestCase):
    def test_sacar_cursos(self):
        conexion = conexion
        conexion.autocommit = False

        try:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO cursos (nombre) VALUES ('Curso 1')")
            cursor.execute("INSERT INTO cursos (nombre) VALUES ('Curso 2')")

            cursos = BaseDatos.sacar_cursos()

            self.assertTrue(len(cursos) > 0)
            self.assertTrue(all(curso.nombre for curso in cursos))

        finally:
            # Revertir cambios
            conexion.rollback()
            conexion.autocommit = True


if __name__ == "__main__":
    unittest.main()

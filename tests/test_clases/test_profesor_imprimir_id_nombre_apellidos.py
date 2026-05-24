import unittest
import sys
import io
import bcrypt

from lib.profesor import Profesor


class TestProfesorImprimirIdNombreApellidos(unittest.TestCase):
    def _capturar(self, p):
        old = sys.stdout
        sys.stdout = io.StringIO()
        p.imprimir_id_nombre_apellidos()
        salida = sys.stdout.getvalue()
        sys.stdout = old
        return salida

    def test_imprime_id(self):
        p = Profesor('Ana', 'López')
        salida = self._capturar(p)
        assert p.id in salida, "La salida debe contener el id del profesor"

    def test_imprime_nombre(self):
        p = Profesor('Ana', 'López')
        salida = self._capturar(p)
        assert 'Ana' in salida

    def test_imprime_apellidos(self):
        p = Profesor('Ana', 'López')
        salida = self._capturar(p)
        assert 'López' in salida

    def test_id_aparece_antes_que_nombre(self):
        p = Profesor('Ana', 'López')
        salida = self._capturar(p)
        assert salida.index(p.id) < salida.index('Ana')

    def test_id_con_padding_37(self):
        p = Profesor('Ana', 'López')
        salida = self._capturar(p)
        parte_id = salida[:37]
        assert p.id in parte_id, "El id debe ocupar los primeros 37 caracteres"

    def test_termina_con_salto_de_linea(self):
        p = Profesor('Ana', 'López')
        salida = self._capturar(p)
        assert salida.endswith('\n'), "La salida debe terminar con salto de línea"

    def test_no_propaga_excepciones(self):
        p = Profesor('Ana', 'López')
        try:
            self._capturar(p)
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_profesores_distintos_salidas_distintas(self):
        p1 = Profesor('Ana', 'López')
        p2 = Profesor('Pedro', 'Ruiz')
        s1 = self._capturar(p1)
        s2 = self._capturar(p2)
        assert s1 != s2


if __name__ == '__main__':
    unittest.main()

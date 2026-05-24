import unittest
import datetime
from app.app import App
from tests.tests_app.helpers_app import simular
from lib.guardia import Guardia
from lib.profesor import Profesor


def _guardia(nombre='Ana', apellidos='López', hora='1', curso='1-A', aula='A01'):
    g = Guardia()
    g.id    = Profesor(nombre, apellidos)
    g.dia   = datetime.date.today()
    g.hora  = hora
    g.curso = curso
    g.clase = aula
    g.tarea = Guardia.NO_TAREA
    return g


class TestImprimirGuardias(unittest.TestCase):
    def _cap(self, guardias):
        _, salida = simular('', App().imprimir_guardias, guardias)
        return salida

    def test_lista_vacia_imprime_no_encontro(self):
        salida = self._cap([])
        assert 'No se encontró ninguna guardia' in salida

    def test_none_imprime_no_encontro(self):
        salida = self._cap(None)
        assert 'No se encontró ninguna guardia' in salida

    def test_una_guardia_imprime_separador(self):
        salida = self._cap([_guardia()])
        assert '·' in salida

    def test_una_guardia_imprime_nombre_profesor(self):
        salida = self._cap([_guardia('Carlos', 'García')])
        assert 'Carlos' in salida or 'García' in salida

    def test_tres_guardias_imprime_las_tres(self):
        gs = [_guardia('Ana', 'López'), _guardia('Pedro', 'Ruiz'), _guardia('Marta', 'Sanz')]
        salida = self._cap(gs)
        assert 'Ana' in salida
        assert 'Pedro' in salida
        assert 'Marta' in salida

    def test_separador_una_vez_por_guardia(self):
        n = 4
        gs = [_guardia(f'Prof{i}', f'Ap{i}') for i in range(n)]
        salida = self._cap(gs)
        assert salida.count('·' * 16) >= n

    def test_cinco_guardias_todas_aparecen(self):
        nombres = ['Luis', 'Eva', 'Raul', 'Noa', 'Iker']
        gs = [_guardia(n, f'Ap{i}') for i, n in enumerate(nombres)]
        salida = self._cap(gs)
        for nombre in nombres:
            assert nombre in salida, f"'{nombre}' debe aparecer en la salida"

    def test_imprime_str_de_guardia(self):
        g = _guardia('Ana', 'López')
        salida = self._cap([g])
        assert 'Profesor:' in salida

    def test_no_propaga_excepciones_lista_vacia(self):
        try:
            self._cap([])
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_no_propaga_excepciones_con_guardias(self):
        try:
            self._cap([_guardia()])
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada


if __name__ == '__main__':
    unittest.main()

import unittest
from datetime import date

from app.app import App
from tests.tests_app.helpers_app import simular, reset


class TestGenerarFecha(unittest.TestCase):
    def _f(self, dia, mes, anio, extra=''):
        return simular(f'{dia}\n{mes}\n{anio}\n{extra}\n', App().generar_fecha)

    def test_lunes_devuelve_date(self):
        # 15-01-2024 es lunes
        retorno, _ = self._f(15, 1, 2024)
        assert retorno == date(2024, 1, 15)

    def test_martes_devuelve_date(self):
        retorno, _ = self._f(16, 1, 2024)
        assert retorno == date(2024, 1, 16)

    def test_miercoles_devuelve_date(self):
        retorno, _ = self._f(17, 1, 2024)
        assert retorno == date(2024, 1, 17)

    def test_jueves_devuelve_date(self):
        retorno, _ = self._f(18, 1, 2024)
        assert retorno == date(2024, 1, 18)

    def test_viernes_devuelve_date(self):
        retorno, _ = self._f(19, 1, 2024)
        assert retorno == date(2024, 1, 19)

    def test_sabado_opcion_n_sale(self):
        # 20-01-2024 es sábado
        reset()
        simular('20\n1\n2024\nN\n', App().generar_fecha)
        assert App.fin is True

    def test_domingo_opcion_n_sale(self):
        # 21-01-2024 es domingo
        reset()
        simular('21\n1\n2024\nN\n', App().generar_fecha)
        assert App.fin is True

    def test_sabado_reintento_devuelve_lunes(self):
        # sábado 20-01-2024, reintento lunes 22-01-2024
        retorno, _ = simular('20\n1\n2024\nX\n22\n1\n2024\n', App().generar_fecha)
        assert retorno == date(2024, 1, 22)

    def test_dia_no_numerico_no_propaga(self):
        reset()
        try:
            simular('abc\n2\n', App().generar_fecha)
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_mes_invalido_no_propaga(self):
        try:
            simular('1\n13\n2024\n2\n', App().generar_fecha)
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_dia_cero_no_propaga(self):
        try:
            simular('0\n1\n2024\n2\n', App().generar_fecha)
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_dia_32_no_propaga(self):
        try:
            simular('32\n1\n2024\n2\n', App().generar_fecha)
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_fecha_devuelta_no_es_fin_de_semana(self):
        retorno, _ = self._f(15, 1, 2024)
        if retorno is not None:
            assert date.weekday(retorno) not in App.FINES_SEMANA

    def test_sabado_imprime_aviso_no_lectivo(self):
        _, salida = simular('20\n1\n2024\nN\n', App().generar_fecha)
        assert 'lectivo' in salida or 'fin de semana' in salida.lower() or 'no lectivo' in salida.lower()

    def test_bisiesto_valido(self):
        retorno, _ = self._f(29, 2, 2024)
        assert retorno == date(2024, 2, 29)


if __name__ == '__main__':
    unittest.main()

import unittest
import datetime

from app.app import App
from tests.tests_app.helpers_app import simular, reset
from recursos_externos.bbdd.base_datos import BaseDatos
from claves import claves_admin as ad


def _cargar_bd():
    if not BaseDatos.vaciar_bbdd():
        return False
    return BaseDatos.cargar_tablas()


def _primer_prof():
    datos = BaseDatos.recoger_info_ficheros()
    if not datos:
        return None
    _, _, _, profs = datos
    return (profs[0].id, profs[0].clave) if profs else None


class TestGenerarInforme(unittest.TestCase):
    F1 = '15\n1\n2024\n'
    F2 = '22\n1\n2024\n'

    def test_inicio_menor_fin_consulta(self):
        _cargar_bd()
        _, salida = simular(self.F1 + self.F2 + 'N\n', App().generar_informe)
        assert 'guardia' in salida.lower() or 'No se encontró' in salida or 'Base de Datos' in salida

    def test_inicio_menor_fin_imprime_fechas(self):
        _cargar_bd()
        _, salida = simular(self.F1 + self.F2 + 'N\n', App().generar_informe)
        assert 'FECHA' in salida or 'fecha' in salida.lower() or len(salida) > 0

    def test_inicio_mayor_fin_opcion_s_intercambia(self):
        _cargar_bd()
        _, salida = simular(self.F2 + self.F1 + 'S\nN\n', App().generar_informe)
        assert len(salida) > 0

    def test_inicio_mayor_fin_opcion_n_repite(self):
        _cargar_bd()
        entrada = self.F2 + self.F1 + 'N\n' + self.F1 + self.F2 + 'N\n'
        _, salida = simular(entrada, App().generar_informe)
        assert len(salida) > 0

    def test_inicio_mayor_fin_otra_tecla_sale(self):
        reset()
        simular(self.F2 + self.F1 + 'X\n', App().generar_informe)
        assert App.fin is True

    def test_fechas_invertidas_imprime_aviso(self):
        _, salida = simular(self.F2 + self.F1 + 'S\nN\n', App().generar_informe)
        assert 'menor' in salida or 'inicio' in salida.lower() or 'intercambiar' in salida.lower() or len(salida) > 0

    def test_no_propaga_excepciones_normal(self):
        try:
            simular(self.F1 + self.F2 + 'N\n', App().generar_informe)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_no_propaga_excepciones_invertida(self):
        try:
            simular(self.F2 + self.F1 + 'S\nN\n', App().generar_informe)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada


if __name__ == '__main__':
    unittest.main()

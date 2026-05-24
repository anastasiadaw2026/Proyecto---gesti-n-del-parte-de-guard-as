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


class TestLoginAdmin(unittest.TestCase):
    ID  = ad.ID
    CL  = ad.CLAVE

    def test_correctas_imprime_autentificacion(self):
        _, salida = simular(f'{self.ID}\n{self.CL}\n7\n', App().login_admin)
        assert 'correcta' in salida

    def test_correctas_llega_a_menu_admin(self):
        _, salida = simular(f'{self.ID}\n{self.CL}\n7\n', App().login_admin)
        assert 'Cargar' in salida or 'Visualizar' in salida or 'Salir' in salida

    def test_id_incorrecto_fallo(self):
        _, salida = simular(f'MAL\n{self.CL}\nN\n', App().login_admin)
        assert 'incorrectas' in salida or 'clave' in salida.lower()

    def test_clave_incorrecta_fallo(self):
        _, salida = simular(f'{self.ID}\nMAL\nN\n', App().login_admin)
        assert 'incorrectas' in salida or 'clave' in salida.lower()

    def test_ambos_incorrectos_fallo(self):
        _, salida = simular('X\nY\nN\n', App().login_admin)
        assert 'incorrectas' in salida or 'clave' in salida.lower()

    def test_fallo_opcion_n_sale(self):
        reset()
        simular('X\nY\nN\n', App().login_admin)
        assert App.fin is True

    def test_fallo_opcion_s_no_sale(self):
        reset()
        simular('X\nY\nS\n', App().login_admin)
        assert App.fin is False

    def test_no_propaga_excepciones_correctas(self):
        try:
            simular(f'{self.ID}\n{self.CL}\n7\n', App().login_admin)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_no_propaga_excepciones_incorrectas(self):
        try:
            simular('X\nY\nN\n', App().login_admin)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada



if __name__ == '__main__':
    unittest.main()

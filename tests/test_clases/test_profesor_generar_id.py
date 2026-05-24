import unittest
import sys
import io
import bcrypt

from lib.profesor import Profesor


class TestProfesorGenerarId(unittest.TestCase):
    def test_id_empieza_con_inicial_nombre(self):
        p = Profesor('Ana', 'López')
        assert p.id.startswith('a'), (
            "El id debe empezar con la inicial del nombre en minúsculas"
        )

    def test_id_contiene_apellidos_sin_espacios(self):
        p = Profesor('Ana', 'López')
        assert 'lópez' in p.id, "El id debe contener los apellidos en minúsculas"

    def test_id_apellidos_compuestos_sin_espacios(self):
        p = Profesor('Juan', 'de la Rosa')
        assert ' ' not in p.id, "El id no debe contener espacios"

    def test_id_nombre_compuesto_solo_primera_letra(self):
        p = Profesor('María José', 'García')
        assert p.id[0] == 'm', (
            "Solo la primera letra del nombre (en minúsculas) debe ir en el id"
        )

    def test_id_nombre_vacio_es_vacio(self):
        p = Profesor('', 'López')
        assert p.id == '', "Con nombre vacío, el id debe ser ''"

    def test_id_apellidos_vacios_es_vacio(self):
        p = Profesor('Ana', '')
        assert p.id == '', "Con apellidos vacíos, el id debe ser ''"

    def test_id_ambos_vacios_es_vacio(self):
        p = Profesor('', '')
        assert p.id == ''

    def test_id_solo_minusculas(self):
        p = Profesor('ANA', 'LOPEZ')
        assert p.id == p.id.lower(), "El id debe estar en minúsculas"

    def test_id_es_determinista(self):
        p1 = Profesor('Pedro', 'Ruiz')
        p2 = Profesor('Pedro', 'Ruiz')
        assert p1.id == p2.id

    def test_ids_distintos_para_nombres_distintos(self):
        p1 = Profesor('Ana', 'López')
        p2 = Profesor('Bea', 'Martín')
        assert p1.id != p2.id


if __name__ == '__main__':
    unittest.main()

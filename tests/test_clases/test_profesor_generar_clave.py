import unittest
import sys
import io
import bcrypt

from lib.profesor import Profesor


class TestProfesorGenerarClave(unittest.TestCase):
    def test_clave_empieza_con_nombre(self):
        p = Profesor('Ana', 'López')
        assert p.clave.startswith('ana'), (
            "La clave debe empezar con el nombre en minúsculas sin espacios"
        )

    def test_clave_termina_con_numero(self):
        p = Profesor('Ana', 'López')
        assert p.clave.endswith('8'), f"La clave debe terminar en 8, termina en: {p.clave}"

    def test_longitud_embebida_correcta(self):
        p = Profesor('Pedro', 'Ruiz')
        nombre_limpio = 'pedro'   # 5
        apellidos_limpio = 'ruiz' # 4  → total 9
        assert p.clave == 'pedro9', f"Esperado 'pedro9', obtenido '{p.clave}'"

    def test_nombre_con_espacios_se_elimina(self):
        p = Profesor('María José', 'García')
        assert ' ' not in p.clave, "Los espacios del nombre no deben estar en la clave"

    def test_clave_es_determinista(self):
        p1 = Profesor('Ana', 'López')
        p2 = Profesor('Ana', 'López')
        assert p1.clave == p2.clave

    def test_claves_distintas_para_nombres_distintos(self):
        p1 = Profesor('Ana', 'López')
        p2 = Profesor('Bea', 'Ruiz')
        assert p1.clave != p2.clave

    def test_clave_no_vacia(self):
        p = Profesor('Ana', 'López')
        assert p.clave != '' and p.clave is not None

    def test_clave_nombre_en_minusculas(self):
        p = Profesor('ANA', 'LOPEZ')
        assert p.clave.startswith('ana'), (
            "La parte del nombre en la clave debe estar en minúsculas"
        )

    def test_apellidos_compuestos_longitud_correcta(self):
        p = Profesor('Juan', 'de la Rosa')
        assert p.clave == 'juan12', f"Esperado 'juan12', obtenido '{p.clave}'"


if __name__ == '__main__':
    unittest.main()

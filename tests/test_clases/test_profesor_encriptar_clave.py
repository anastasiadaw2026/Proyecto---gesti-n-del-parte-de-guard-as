import unittest
import sys
import io
import bcrypt

from lib.profesor import Profesor


class TestProfesorEncriptarClave(unittest.TestCase):
    def test_encriptada_prefijo_bcrypt(self):
        p = Profesor('Ana', 'López')
        assert (p.clave_encriptada.startswith('$2b$') or
                p.clave_encriptada.startswith('$2a$')), (
            "El hash bcrypt debe empezar con '$2b$' o '$2a$'"
        )

    def test_encriptada_longitud_60(self):
        p = Profesor('Ana', 'López')
        assert len(p.clave_encriptada) == 60, (
            f"El hash bcrypt debe tener 60 caracteres, tiene {len(p.clave_encriptada)}"
        )

    def test_clave_plana_verifica_contra_hash(self):
        p = Profesor('Ana', 'López')
        resultado = bcrypt.checkpw(
            p.clave.encode('utf-8'),
            p.clave_encriptada.encode('utf-8')
        )
        assert resultado is True, (
            "La clave plana debe verificar correctamente contra el hash bcrypt"
        )

    def test_clave_incorrecta_no_verifica(self):
        p = Profesor('Ana', 'López')
        resultado = bcrypt.checkpw(
            b'clave_incorrecta',
            p.clave_encriptada.encode('utf-8')
        )
        assert resultado is False

    def test_hashes_distintos_por_sal(self):
        p1 = Profesor('Ana', 'López')
        p2 = Profesor('Ana', 'López')
        assert p1.clave_encriptada != p2.clave_encriptada, (
            "Cada instancia debe tener un hash único (sal aleatoria)"
        )

    def test_hash_es_str_no_bytes(self):
        p = Profesor('Ana', 'López')
        assert isinstance(p.clave_encriptada, str), (
            "clave_encriptada debe ser str, no bytes"
        )

    def test_hash_verifica_propia_clave_distintos_datos(self):
        p = Profesor('Pedro', 'Ruiz')
        resultado = bcrypt.checkpw(
            p.clave.encode('utf-8'),
            p.clave_encriptada.encode('utf-8')
        )
        assert resultado is True

    def test_clave_de_otro_no_verifica(self):
        p1 = Profesor('Ana', 'López')
        p2 = Profesor('Pedro', 'Ruiz')
        resultado = bcrypt.checkpw(
            p1.clave.encode('utf-8'),
            p2.clave_encriptada.encode('utf-8')
        )
        assert resultado is False


if __name__ == '__main__':
    unittest.main()

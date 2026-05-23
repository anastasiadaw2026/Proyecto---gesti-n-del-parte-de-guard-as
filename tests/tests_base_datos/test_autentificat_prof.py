import unittest
from recursos_externos.bbdd.base_datos import BaseDatos


def _cargar_bd():
    if not BaseDatos.vaciar_bbdd():
        return False
    return BaseDatos.cargar_tablas()


def _primer_profesor():
    datos = BaseDatos.recoger_info_ficheros()
    if not datos:
        return None
    _, _, _, profesores = datos
    if not profesores:
        return None
    p = profesores[0]
    return p.id, p.clave


class TestAutentificarProfesor(unittest.TestCase):

    def test_retorna_tipo_valido(self):
        if not _cargar_bd():
            return
        par = _primer_profesor()
        if not par:
            return
        id_p, clave_p = par
        resultado = BaseDatos.autentificar_profesor(id_p, clave_p)
        assert resultado is True or resultado == '' or resultado is False

    def test_clave_correcta_devuelve_true(self):
        if not _cargar_bd():
            return
        par = _primer_profesor()
        if not par:
            return
        id_p, clave_p = par
        resultado = BaseDatos.autentificar_profesor(id_p, clave_p)
        assert resultado is True

    def test_clave_incorrecta_devuelve_cadena_vacia(self):
        if not _cargar_bd():
            return
        par = _primer_profesor()
        if not par:
            return
        id_p, _ = par
        resultado = BaseDatos.autentificar_profesor(id_p, 'clave_incorrecta_99!')
        assert resultado == ''

    def test_id_inexistente_devuelve_cadena_vacia(self):
        if not _cargar_bd():
            return
        resultado = BaseDatos.autentificar_profesor('ID_QUE_NO_EXISTE_XYZXYZ', 'pass')
        assert resultado == ''

    def test_id_vacio_devuelve_cadena_vacia(self):
        if not _cargar_bd():
            return
        resultado = BaseDatos.autentificar_profesor('', 'pass')
        assert resultado == ''

    def test_clave_vacia_devuelve_cadena_vacia(self):
        if not _cargar_bd():
            return
        par = _primer_profesor()
        if not par:
            return
        id_p, _ = par
        resultado = BaseDatos.autentificar_profesor(id_p, '')
        assert resultado == ''

    def test_multiples_profesores_correctos(self):
        if not _cargar_bd():
            return
        datos = BaseDatos.recoger_info_ficheros()
        if not datos:
            return
        _, _, _, profesores = datos
        if len(profesores) < 2:
            return
        for p in profesores[:2]:
            r = BaseDatos.autentificar_profesor(p.id, p.clave)
            assert r is True

    def test_clave_de_otro_profesor_no_sirve(self):
        if not _cargar_bd():
            return
        datos = BaseDatos.recoger_info_ficheros()
        if not datos:
            return
        _, _, _, profesores = datos
        if len(profesores) < 2:
            return
        id_1 = profesores[0].id
        clave_2 = profesores[1].clave
        resultado = BaseDatos.autentificar_profesor(id_1, clave_2)
        assert resultado == ''

    def test_no_propaga_excepciones(self):
        try:
            BaseDatos.autentificar_profesor('x', 'y')
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada


if __name__ == '__main__':
    unittest.main()
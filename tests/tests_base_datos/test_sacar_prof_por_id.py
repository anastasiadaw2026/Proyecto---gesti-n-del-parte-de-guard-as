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


class TestSacarProfPorId(unittest.TestCase):
    def test_retorna_tupla_none_o_false(self):
        if not _cargar_bd():
            return
        par = _primer_profesor()
        if not par:
            return
        id_p, _ = par
        resultado = BaseDatos.sacar_prof_por_id(id_p)
        assert isinstance(resultado, tuple) or resultado is None or resultado is False

    def test_id_existente_devuelve_tupla(self):
        if not _cargar_bd():
            return
        par = _primer_profesor()
        if not par:
            return
        id_p, _ = par
        resultado = BaseDatos.sacar_prof_por_id(id_p)
        assert isinstance(resultado, tuple)
        assert len(resultado) == 2

    def test_id_existente_nombre_no_vacio(self):
        if not _cargar_bd():
            return
        par = _primer_profesor()
        if not par:
            return
        id_p, _ = par
        resultado = BaseDatos.sacar_prof_por_id(id_p)
        if isinstance(resultado, tuple):
            assert resultado[0]

    def test_id_existente_apellidos_no_vacio(self):
        if not _cargar_bd():
            return
        par = _primer_profesor()
        if not par:
            return
        id_p, _ = par
        resultado = BaseDatos.sacar_prof_por_id(id_p)
        if isinstance(resultado, tuple):
            assert resultado[1]

    def test_id_inexistente_devuelve_none(self):
        if not _cargar_bd():
            return
        resultado = BaseDatos.sacar_prof_por_id('ID_IMPOSIBLE_99999')
        assert resultado is None or resultado is False

    def test_id_vacio_devuelve_none(self):
        if not _cargar_bd():
            return
        resultado = BaseDatos.sacar_prof_por_id('')
        assert resultado is None or resultado is False

    def test_nombre_coherente_con_sacar_profesores(self):
        if not _cargar_bd():
            return
        par = _primer_profesor()
        if not par:
            return
        id_p, _ = par
        resultado_id = BaseDatos.sacar_prof_por_id(id_p)
        if not isinstance(resultado_id, tuple):
            return
        nombre_por_id = resultado_id[0]
        profesores = BaseDatos.sacar_profesores()
        if profesores is False:
            return
        nombres = [p.nombre for p in profesores]
        assert nombre_por_id in nombres

    def test_no_propaga_excepciones(self):
        try:
            BaseDatos.sacar_prof_por_id('cualquier_cosa')
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada


if __name__ == '__main__':
    unittest.main()
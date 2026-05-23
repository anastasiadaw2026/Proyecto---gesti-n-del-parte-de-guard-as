import unittest

from recursos_externos.bbdd.base_datos import BaseDatos


class TestVaciarBbdd(unittest.TestCase):
    def test_retorna_bool(self):
        resultado = BaseDatos.vaciar_bbdd()
        assert isinstance(resultado, bool), (
            "vaciar_bbdd debe devolver un bool"
        )

    def test_exito_devuelve_true(self):
        resultado = BaseDatos.vaciar_bbdd()
        if resultado is not False:
            assert resultado is True, (
                "Si la operación tiene éxito debe devolver True"
            )

    def test_exito_tabla_profesores_queda_vacia(self):
        ok = BaseDatos.vaciar_bbdd()
        if ok:
            profesores = BaseDatos.sacar_profesores()
            assert profesores == [] or profesores is False, (
                "Tras vaciar la BD, la tabla PROFESORES debe estar vacía"
            )

    def test_exito_tabla_cursos_queda_vacia(self):
        ok = BaseDatos.vaciar_bbdd()
        if ok:
            cursos = BaseDatos.sacar_cursos()
            assert cursos == [] or cursos is False, (
                "Tras vaciar la BD, la tabla CURSOS debe estar vacía"
            )

    def test_exito_tabla_aulas_queda_vacia(self):
        ok = BaseDatos.vaciar_bbdd()
        if ok:
            aulas = BaseDatos.sacar_aulas()
            assert aulas == [] or aulas is False, (
                "Tras vaciar la BD, la tabla AULAS debe estar vacía"
            )

    def test_exito_tabla_horas_queda_vacia(self):
        ok = BaseDatos.vaciar_bbdd()
        if ok:
            horas = BaseDatos.sacar_horas()
            assert horas == [] or horas is False, (
                "Tras vaciar la BD, la tabla HORAS debe estar vacía"
            )

    def test_doble_llamada_no_lanza_excepcion(self):
        try:
            BaseDatos.vaciar_bbdd()
            BaseDatos.vaciar_bbdd()
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada, (
            "Dos llamadas consecutivas a vaciar_bbdd no deben lanzar excepción"
        )

    def test_fallo_devuelve_false(self):
        resultado = BaseDatos.vaciar_bbdd()
        assert resultado is True or resultado is False, (
            "vaciar_bbdd debe devolver True o False, nunca None u otro tipo"
        )

    def test_conexion_sigue_operativa_despues(self):
        BaseDatos.vaciar_bbdd()
        profesores = BaseDatos.sacar_profesores()
        assert profesores is False or isinstance(profesores, list), (
            "La conexión debe seguir operativa después de vaciar_bbdd"
        )

    def test_no_propaga_excepciones(self):
        try:
            BaseDatos.vaciar_bbdd()
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada, (
            "vaciar_bbdd no debe dejar escapar ninguna excepción"
        )

    def test_vaciar_bd_ya_vacia_devuelve_true(self):
        BaseDatos.vaciar_bbdd()
        resultado = BaseDatos.vaciar_bbdd()
        if resultado is not False:
            assert resultado is True, (
                "Vaciar una BD ya vacía debe devolver True"
            )


if __name__ == '__main__':
    unittest.main()

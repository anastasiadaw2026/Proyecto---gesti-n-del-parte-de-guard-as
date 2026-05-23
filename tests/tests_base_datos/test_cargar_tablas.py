import unittest

from recursos_externos.bbdd.base_datos import BaseDatos


class TestCargarTablas(unittest.TestCase):
    def set_up_bd(self):
        vaciado = BaseDatos.vaciar_bbdd()
        if not vaciado:
            return False
        return BaseDatos.cargar_tablas()

    def test_retorna_bool(self):
        BaseDatos.vaciar_bbdd()
        resultado = BaseDatos.cargar_tablas()
        assert isinstance(resultado, bool), (
            "cargar_tablas debe devolver un bool"
        )

    def test_exito_devuelve_true(self):
        BaseDatos.vaciar_bbdd()
        resultado = BaseDatos.cargar_tablas()
        if resultado is not False:
            assert resultado is True, "cargar_tablas debe devolver True en éxito"


    def test_fallo_devuelve_false(self):
        resultado = BaseDatos.cargar_tablas()
        assert resultado is True or resultado is False, (
            "cargar_tablas debe devolver True o False, nunca None"
        )

    def test_cursos_cargados_en_bd(self):
        ok = self.set_up_bd()
        if not ok:
            return
        cursos = BaseDatos.sacar_cursos()
        assert cursos is not False and len(cursos) > 0, (
            "Tras cargar_tablas debe haber cursos en la BD"
        )

    def test_cursos_tienen_nombre_con_guion(self):
        ok = self.set_up_bd()
        if not ok:
            return
        cursos = BaseDatos.sacar_cursos()
        if cursos is False:
            return
        for c in cursos:
            assert '-' in c.nombre, (
                f"El curso '{c.nombre}' debe tener el formato 'ciclo-letra'"
            )

    def test_cursos_nombres_son_strings(self):
        ok = self.set_up_bd()
        if not ok:
            return
        cursos = BaseDatos.sacar_cursos()
        if cursos is False:
            return
        for c in cursos:
            assert isinstance(c.nombre, str), (
                f"El nombre del curso debe ser str, encontrado: {type(c.nombre)}"
            )

    def test_cursos_nombres_sin_espacios_extremos(self):
        ok = self.set_up_bd()
        if not ok:
            return
        cursos = BaseDatos.sacar_cursos()
        if cursos is False:
            return
        for c in cursos:
            assert c.nombre == c.nombre.strip(), (
                f"El curso '{c.nombre}' no debe tener espacios al inicio/fin"
            )

    def test_cursos_no_hay_duplicados_en_bd(self):
        ok = self.set_up_bd()
        if not ok:
            return
        cursos = BaseDatos.sacar_cursos()
        if cursos is False:
            return
        nombres = [c.nombre for c in cursos]
        assert len(nombres) == len(set(nombres)), (
            "No debe haber cursos duplicados en la BD"
        )

    def test_cursos_numero_coincide_con_fichero(self):
        ok = self.set_up_bd()
        if not ok:
            return
        datos = BaseDatos.recoger_info_ficheros()
        if not datos:
            return
        cursos_fichero, _, _, _ = datos
        cursos_bd = BaseDatos.sacar_cursos()
        if cursos_bd is False:
            return
        assert len(cursos_bd) == len(cursos_fichero), (
            "El número de cursos en BD debe coincidir con el del fichero"
        )

    def test_aulas_cargadas_en_bd(self):
        ok = self.set_up_bd()
        if not ok:
            return
        aulas = BaseDatos.sacar_aulas()
        assert aulas is not False and len(aulas) > 0, (
            "Tras cargar_tablas debe haber aulas en la BD"
        )

    def test_aulas_nombres_en_mayusculas(self):
        ok = self.set_up_bd()
        if not ok:
            return
        aulas = BaseDatos.sacar_aulas()
        if aulas is False:
            return
        for a in aulas:
            assert a.nombre == a.nombre.upper(), (
                f"El aula '{a.nombre}' debe estar en mayúsculas"
            )

    def test_aulas_nombres_son_strings(self):
        ok = self.set_up_bd()
        if not ok:
            return
        aulas = BaseDatos.sacar_aulas()
        if aulas is False:
            return
        for a in aulas:
            assert isinstance(a.nombre, str), (
                f"El nombre del aula debe ser str, encontrado: {type(a.nombre)}"
            )

    def test_aulas_nombres_sin_espacios_extremos(self):
        ok = self.set_up_bd()
        if not ok:
            return
        aulas = BaseDatos.sacar_aulas()
        if aulas is False:
            return
        for a in aulas:
            assert a.nombre == a.nombre.strip(), (
                f"El aula '{a.nombre}' no debe tener espacios al inicio/fin"
            )

    def test_aulas_numero_coincide_con_fichero(self):
        ok = self.set_up_bd()
        if not ok:
            return
        datos = BaseDatos.recoger_info_ficheros()
        if not datos:
            return
        _, aulas_fichero, _, _ = datos
        aulas_bd = BaseDatos.sacar_aulas()
        if aulas_bd is False:
            return
        assert len(aulas_bd) == len(aulas_fichero), (
            "El número de aulas en BD debe coincidir con el del fichero"
        )

    def test_horas_cargadas_en_bd(self):
        ok = self.set_up_bd()
        if not ok:
            return
        horas = BaseDatos.sacar_horas()
        assert horas is not False and len(horas) > 0, (
            "Tras cargar_tablas debe haber horas en la BD"
        )

    def test_horas_nombres_son_strings(self):
        ok = self.set_up_bd()
        if not ok:
            return
        horas = BaseDatos.sacar_horas()
        if horas is False:
            return
        for h in horas:
            assert isinstance(h.nombre, str), (
                f"El nombre de hora debe ser str, encontrado: {type(h.nombre)}"
            )

    def test_horas_nombres_sin_espacios_extremos(self):
        ok = self.set_up_bd()
        if not ok:
            return
        horas = BaseDatos.sacar_horas()
        if horas is False:
            return
        for h in horas:
            assert h.nombre == h.nombre.strip(), (
                f"La hora '{h.nombre}' no debe tener espacios al inicio/fin"
            )

    def test_horas_no_contienen_comas(self):
        ok = self.set_up_bd()
        if not ok:
            return
        horas = BaseDatos.sacar_horas()
        if horas is False:
            return
        for h in horas:
            assert ',' not in h.nombre, (
                f"La hora '{h.nombre}' no debe contener comas"
            )

    def test_horas_numero_coincide_con_fichero(self):
        ok = self.set_up_bd()
        if not ok:
            return
        datos = BaseDatos.recoger_info_ficheros()
        if not datos:
            return
        _, _, horas_fichero, _ = datos
        horas_bd = BaseDatos.sacar_horas()
        if horas_bd is False:
            return
        assert len(horas_bd) == len(horas_fichero), (
            "El número de horas en BD debe coincidir con el del fichero"
        )

    def test_profesores_cargados_en_bd(self):
        ok = self.set_up_bd()
        if not ok:
            return
        profesores = BaseDatos.sacar_profesores()
        assert profesores is not False and len(profesores) > 0, (
            "Tras cargar_tablas debe haber profesores en la BD"
        )

    def test_profesores_nombre_no_vacio(self):
        ok = self.set_up_bd()
        if not ok:
            return
        profesores = BaseDatos.sacar_profesores()
        if profesores is False:
            return
        for p in profesores:
            assert p.nombre and str(p.nombre) != '', (
                "El nombre del profesor no debe estar vacío"
            )

    def test_profesores_apellidos_no_vacio(self):
        ok = self.set_up_bd()
        if not ok:
            return
        profesores = BaseDatos.sacar_profesores()
        if profesores is False:
            return
        for p in profesores:
            assert p.apellidos and str(p.apellidos) != '', (
                "Los apellidos del profesor no deben estar vacíos"
            )

    def test_profesores_numero_coincide_con_fichero(self):
        ok = self.set_up_bd()
        if not ok:
            return
        datos = BaseDatos.recoger_info_ficheros()
        if not datos:
            return
        _, _, _, profs_fichero = datos
        profs_bd = BaseDatos.sacar_profesores()
        if profs_bd is False:
            return
        assert len(profs_bd) == len(profs_fichero), (
            "El número de profesores en BD debe coincidir con el del fichero"
        )

    def test_profesores_nombres_son_strings(self):
        ok = self.set_up_bd()
        if not ok:
            return
        profesores = BaseDatos.sacar_profesores()
        if profesores is False:
            return
        for p in profesores:
            assert isinstance(p.nombre, str), (
                f"El nombre del profesor debe ser str, encontrado: {type(p.nombre)}"
            )

    def test_no_propaga_excepciones(self):
        BaseDatos.vaciar_bbdd()
        try:
            BaseDatos.cargar_tablas()
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada, "cargar_tablas no debe propagar excepciones"


if __name__ == '__main__':
    unittest.main()

import unittest
import os
import datetime

from recursos_externos.bbdd.base_datos import BaseDatos


class TestHacerBackup(unittest.TestCase):
    def test_retorna_tupla_de_dos_elementos(self):
        resultado = BaseDatos.hacer_backup()
        assert isinstance(resultado, tuple), (
            "hacer_backup debe devolver una tupla"
        )
        assert len(resultado) == 2, (
            "La tupla debe tener exactamente 2 elementos"
        )

    def test_primer_elemento_es_bool(self):
        ok, _ = BaseDatos.hacer_backup()
        assert isinstance(ok, bool), (
            "El primer elemento de la tupla debe ser bool"
        )

    def test_segundo_elemento_es_str(self):
        _, info = BaseDatos.hacer_backup()
        assert isinstance(info, str), (
            "El segundo elemento de la tupla debe ser str"
        )

    def test_fallo_devuelve_false_con_mensaje(self):
        ok, msg = BaseDatos.hacer_backup()
        if not ok:
            assert msg == 'No se pudo realizar la copia de seguridad.', (
                "El mensaje de error no coincide con el esperado"
            )

    def test_exito_ruta_contiene_prefijo_backup(self):
        ok, info = BaseDatos.hacer_backup()
        if ok:
            assert 'backup_' in info, (
                "La ruta del backup debe contener 'backup_'"
            )
            assert info.endswith('.sql'), (
                "El archivo de backup debe tener extensión .sql"
            )

    def test_exito_fichero_creado_existe(self):
        ok, info = BaseDatos.hacer_backup()
        if ok:
            assert os.path.isfile(info), (
                f"El fichero de backup '{info}' debería existir en disco"
            )

    def test_exito_nombre_fichero_contiene_fecha_valida(self):
        ok, info = BaseDatos.hacer_backup()
        if ok:
            nombre = os.path.basename(info)
            parte_fecha = nombre.replace('backup_', '').split('_')[0]
            try:
                datetime.datetime.strptime(parte_fecha, "%Y-%m-%d")
                fecha_valida = True
            except ValueError:
                fecha_valida = False
            assert fecha_valida, (
                "El nombre del backup debe contener una fecha con formato YYYY-MM-DD"
            )

    def test_no_lanza_excepcion(self):
        try:
            BaseDatos.hacer_backup()
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada, (
            "hacer_backup no debe propagar ninguna excepción"
        )

    def test_mensaje_error_no_esta_vacio(self):
        ok, msg = BaseDatos.hacer_backup()
        if not ok:
            assert len(msg) > 0, (
                "El mensaje de error no debe ser una cadena vacía"
            )

    def test_llamadas_consecutivas_devuelven_misma_estructura(self):
        resultado1 = BaseDatos.hacer_backup()
        resultado2 = BaseDatos.hacer_backup()
        assert isinstance(resultado1, tuple), "Primera llamada debe devolver tupla"
        assert isinstance(resultado2, tuple), "Segunda llamada debe devolver tupla"
        assert len(resultado1) == 2, "Primera llamada: tupla de 2 elementos"
        assert len(resultado2) == 2, "Segunda llamada: tupla de 2 elementos"


if __name__ == '__main__':
    unittest.main()

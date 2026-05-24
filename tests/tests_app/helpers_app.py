"""
helpers_app.py  –  sin mock, sin patch
Utilidades compartidas por todos los ficheros de test de App.
"""
import sys
import io
from app.app import App


def simular(entrada: str, metodo, *args):
    """
    Redirige stdin y stdout, ejecuta metodo(*args) y devuelve
    (valor_retornado, texto_impreso).
    SystemExit y EOFError se capturan silenciosamente.
    """
    old_in, old_out = sys.stdin, sys.stdout
    sys.stdin  = io.StringIO(entrada)
    sys.stdout = io.StringIO()
    retorno = None
    try:
        retorno = metodo(*args)
    except SystemExit:
        pass
    except EOFError:
        pass
    except Exception:
        pass
    salida = sys.stdout.getvalue()
    sys.stdin, sys.stdout = old_in, old_out
    return retorno, salida


def reset():
    """Reinicia App.fin = False antes de cada test."""
    App.fin = False

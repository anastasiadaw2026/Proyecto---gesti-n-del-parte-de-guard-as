from lib.curso import Curso
from lib.hora import Hora
from lib.profesor import Profesor


class Guardia:
    NO_TAREA: str = "N"
    SI_TAREA: str = "S"

    def __init__(self):
        self.id: Profesor = Profesor()
        self.dia: str = '' #todo
        self.hora: Hora = Hora()
        self.curso: Curso = Curso()
        self.clase: int = 0
        self.tarea: str = Guardia.NO_TAREA
        self.ficheros: str = '' #todo
from colores import Colores


class Menus:
    class ConstantesMenu:
        UNO = '1'
        DOS = '2'
        TRES = '3'
        CUATRO = '4'
        CINCO = '5'
        SEIS = '6'
        SIETE = '7'
        SEGUIR = 'S'
        ACABAR = 'N'

    @staticmethod
    def imprimir_menu_inicio():
        print(f"{Colores.MAGENTA}¡Bienvenido a la página de gestión de las "
              f"guardias! {Colores.RESET}\n"
              f"Para empezar indique quién es introduciendo una de las "
              f"siguientes opciones:\n"
              f"{Menus.ConstantesMenu.UNO}. Administrador.\n"
              f"{Menus.ConstantesMenu.DOS}. Profesor.\n"
              f"{Menus.ConstantesMenu.TRES}. Lector (sin validar).\n"
              f"{Menus.ConstantesMenu.CUATRO}. Salir de la aplicación.")

    @staticmethod
    def imprimir_menu_visualizar_guardias():
        print(f"Elija una de las siguientes opciones:\n"
              f"{Menus.ConstantesMenu.UNO}. Visualizar el parte de guardias "
              f"semanas.\n"
              f"{Menus.ConstantesMenu.DOS}. Elegir otra semana.")

    @staticmethod
    def imprimir_menu_error():
        print(f'La opción introducida no corresponde a ninguna de las posibles.\n'
              f'Elija una de las siguientes opciones:\n'
              f'{Menus.ConstantesMenu.UNO}. Intentarlo de nuevo.\n'
              f'{Menus.ConstantesMenu.DOS}. Salir ')

    @staticmethod
    def imprimir_menu_inicial_prof():
        print(f"Elija una de las siguientes opciones:\n"
              f"{Menus.ConstantesMenu.UNO}. Visualizar el parte de guardias "
              f"semanal.\n"
              f"{Menus.ConstantesMenu.DOS}. Dar de baja una guardia.\n"
              f"{Menus.ConstantesMenu.TRES}. Dar de alta una guardia.\n"
              f"{Menus.ConstantesMenu.CUATRO}. Salir.")

    @staticmethod
    def imprimir_menu_lector_inicio():
        print(f"Ahora puede elegir una de las siguientes opciones:\n"
              f"{Menus.ConstantesMenu.UNO}. Visualizar el parte de guardias semanal.\n"
              f"{Menus.ConstantesMenu.DOS}. Salir.")

    @staticmethod
    def imprimir_elegir_semana():
        print(f'Estas son las guardias de esta semana.\n'
              f'Si desea elegir otra semana pulse '
              f'{Menus.ConstantesMenu.SEGUIR}, si no pulse '
              f'{Menus.ConstantesMenu.ACABAR} y '
              f'saldrás de la aplicación.')

    @staticmethod
    def imprimir_menu_inicial_admin():
        print(f"Elija una de las siguientes opciones:\n"
              f"{Menus.ConstantesMenu.UNO}. Cargar la Base de Datos.\n"
              f"{Menus.ConstantesMenu.DOS}. Visualizar el parte de guardias "
              f"semanal.\n"
              f"{Menus.ConstantesMenu.TRES}. Dar de baja una guardia.\n"
              f"{Menus.ConstantesMenu.CUATRO}. Dar de alta una guardia.\n"
              f"{Menus.ConstantesMenu.CINCO}. Ver informe de las guardias.\n"
              f"{Menus.ConstantesMenu.SEIS}. Ver el listado de usuarios.\n"
              f"{Menus.ConstantesMenu.SIETE}. Salir.")

    @staticmethod
    def imprimir_menu_backup():
        print(f'Antes de cargar una nueva base de datos, ¿desea hacer '
              f'la copia de seguridad de la base de datos en su '
              f'estado actual?\n'
              f'Si quiere generar el backup pulse '
              f'{Menus.ConstantesMenu.SEGUIR}, si no pulse '
              f'{Menus.ConstantesMenu.ACABAR}.')

    @staticmethod
    def imprimir_menu_cambiar_semana():
        print(f'Introduzca los datos del día a partir de las cual '
              f'quiere visualizar las guardias.\n'
              f'Aparecerán los datos de los siguientes '
              f'{Menus.ConstantesMenu.SIETE} días a partir de la fecha '
              f'introducida.')


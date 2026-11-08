# main.py
import logging

from persistencia.conexion import probar_conexion
from persistencia.crear_bd import crear_tablas
from persistencia.usuario_dao import UsuarioDAO
from menus.menu_usuario import solicitar_login, menu_privado

# el detalle técnico del error se guarda en un archivo; el usuario solo ve un mensaje seguro
logging.basicConfig(
    filename="ecotech.log",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(message)s",
)


def iniciar_sesion_y_menu():
    # primero el login; sin sesión no se muestra el menú
    while True:
        usuario_actual = solicitar_login()
        if usuario_actual is None:
            if input("Enter para reintentar o 0 para salir: ").strip() == "0":
                return
            continue

        opcion = menu_privado(usuario_actual)
        usuario_actual = None  # al cerrar sesión se pierde el acceso
        if opcion == "0":
            return
        print("Sesión cerrada. Ingrese nuevamente.")


def main():
    # main.py solo coordina: no contiene SQL ni credenciales
    if not probar_conexion():
        raise SystemExit("Revisa el archivo .env y que MariaDB/MySQL esté iniciado.")

    try:
        crear_tablas()
    except Exception:
        logging.exception("Error al preparar la base de datos")
        raise SystemExit("No fue posible preparar la base de datos.")

    try:
        if UsuarioDAO.contar() == 0:
            # sin cuentas nadie puede entrar: la semilla crea el empleado y la cuenta admin
            raise SystemExit("No hay cuentas de usuario. Ejecute primero: python src/semilla_bd.py")
        iniciar_sesion_y_menu()
    except (KeyboardInterrupt, EOFError):
        print()  # Ctrl+C o Ctrl+D: salida limpia, sin traceback

    print("Hasta luego.")


# ejecuta main() solo cuando este archivo se inicia directamente
if __name__ == "__main__":
    main()
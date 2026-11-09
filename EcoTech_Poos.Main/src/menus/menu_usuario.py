# menus/menu_usuario.py
# Login, creación de cuentas y menú principal según el rol de la sesión.
import logging
from getpass import getpass

from dominio.usuario import Usuario
from menus.demo_relaciones import demo_relaciones
from menus.entradas import (
    ejecutar_menu, manejar_errores, pedir_dato, solicitar_entero, solicitar_opcion,
)
from menus.menu_departamento import menu_departamento
from menus.menu_empleado import menu_empleado
from menus.menu_indicadores import menu_indicadores
from menus.menu_mi_cuenta import (
    editar_mis_datos, mostrar_mi_ficha, registrar_horas_propias, ver_mis_proyectos,
    ver_mis_registros,
)
from menus.menu_proyecto import menu_proyecto
from menus.menu_registro_tiempo import menu_registro_tiempo
from servicios.autenticacion import autenticar, crear_cuenta_empleado
from servicios.permisos import requiere_admin


# LOGIN
def solicitar_login():
    nombre = input("Usuario: ")
    clave = getpass("Contraseña: ")
    try:
        usuario = autenticar(nombre, clave)
    except (TypeError, ValueError):
        print("No se pudo validar el acceso.")
        return None
    except Exception:
        logging.exception("Error al iniciar sesión")
        print("No fue posible completar la operación.")
        return None

    if usuario is None:
        print("Usuario o contraseña incorrectos.")
    else:
        print("Sesión iniciada correctamente.")
    return usuario


# ADMINISTRACIÓN (solo administrador)
@manejar_errores("registrar usuario", "No se pudo crear esa cuenta.")
@requiere_admin
def solicitar_registro(sesion):
    # el formulario no ofrece elegir rol: el servicio asigna empleado
    empleado_id = solicitar_entero("ID del empleado que tendrá la cuenta")
    nombre = pedir_dato("Nuevo usuario: ", Usuario.normalizar_usuario)
    clave = pedir_dato("Contraseña: ", Usuario.validar_clave, leer=getpass)
    if clave != getpass("Repita la contraseña: "):
        print("Las contraseñas no coinciden. Vuelva al registro.")
        return None
    usuario_id = crear_cuenta_empleado(sesion, empleado_id, nombre, clave)
    print(f"Cuenta creada correctamente. ID: {usuario_id}")
    return usuario_id


@manejar_errores("abrir la administración")
@requiere_admin
def menu_administracion(sesion):
    ejecutar_menu("ADMINISTRACIÓN", {
        1: ("Empleados", menu_empleado),
        2: ("Departamentos", menu_departamento),
        3: ("Proyectos", menu_proyecto),
        4: ("Registro de tiempo (todos)", menu_registro_tiempo),
        5: ("Crear cuenta de usuario para un empleado", solicitar_registro),
        6: ("Demo de relaciones (sin base de datos)", demo_relaciones),
    }, sesion)


# MENÚ PRINCIPAL
def _opciones_del_rol(sesion):
    opciones = {
        1: ("Mi ficha", mostrar_mi_ficha),
        2: ("Editar mis datos", editar_mis_datos),
        3: ("Mis proyectos", ver_mis_proyectos),
        4: ("Mis registros de tiempo", ver_mis_registros),
        5: ("Registrar mis horas", registrar_horas_propias),
        6: ("Dólar (consultar e historial)", menu_indicadores),
    }
    if sesion["rol"] == "admin":
        opciones[7] = ("Administración", menu_administracion)
    return opciones


def menu_privado(sesion):
    """Devuelve "9" (cerrar sesión) o "0" (salir)."""
    if sesion is None:
        print("Debe iniciar sesión.")
        return "9"

    opciones = _opciones_del_rol(sesion)
    while True:
        print(f"\n===== ECOTECH ({sesion['nombre_usuario']} | {sesion['rol']}) =====")
        for numero, (texto, _) in opciones.items():
            print(f"{numero}. {texto}")
        print("9. Cerrar sesión")
        print("0. Salir")

        opcion = solicitar_opcion(9)
        if opcion in (0, 9):
            return str(opcion)
        if opcion in opciones:
            opciones[opcion][1](sesion)
        else:
            print("Opción no válida.")
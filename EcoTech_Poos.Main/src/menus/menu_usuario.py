# menus/menu_usuario.py
# Registro, login y opciones que solo se ven con la sesión iniciada.
import logging
from getpass import getpass

import requests

from dominio.usuario import Usuario
from menus.entradas import (
    manejar_errores, pedir_dato, solicitar_decimal, solicitar_entero, solicitar_opcion,
)
from menus.menu_empleado import menu_empleado
from menus.menu_departamento import menu_departamento
from menus.menu_proyecto import menu_proyecto
from menus.menu_registro_tiempo import menu_registro_tiempo
from menus.demo_relaciones import demo_relaciones
from servicios.autenticacion import autenticar, registrar_usuario
from servicios.indicadores import URL_DOLAR, clp_a_usd, extraer_primero, obtener_datos


@manejar_errores("registrar usuario", "No se pudo crear esa cuenta.")
def solicitar_registro():
    empleado_id = solicitar_entero("ID del empleado que tendrá la cuenta")
    nombre = pedir_dato("Nuevo usuario: ", Usuario.normalizar_usuario)
    clave = pedir_dato("Contraseña: ", Usuario.validar_clave, leer=getpass)
    if clave != getpass("Repita la contraseña: "):
        print("Las contraseñas no coinciden. Vuelva al registro.")
        return None
    usuario_id = registrar_usuario(empleado_id, nombre, clave)
    print(f"Cuenta creada correctamente. ID: {usuario_id}")
    return usuario_id


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


def mostrar_perfil(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión para ver el perfil.")
        return
    print(f"Usuario: {usuario_actual['nombre_usuario']}")
    print(f"Empleado: {usuario_actual['empleado_id']}")


def consultar_dolar(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión para consultar indicadores.")
        return
    try:
        datos = obtener_datos()
        fecha, valor = extraer_primero(datos)
    except requests.exceptions.RequestException:
        # falla la conexión, el tiempo de espera, el estado HTTP o el JSON
        print("No pudimos consultar el servicio. Reintente.")
        return
    except (ValueError, KeyError, TypeError):
        print("La respuesta no contiene un indicador válido.")
        return

    print(f"Dólar observado: {valor:.2f} CLP por USD")
    print(f"Fecha del registro: {fecha}")
    print(f"Origen: {URL_DOLAR}")

    monto = solicitar_decimal("Monto en CLP para estimar en dólares (vacío = omitir)",
                              opcional=True)
    if monto is not None:
        print(f"Estimación: {monto:,.0f} CLP = {clp_a_usd(monto, valor):,.2f} USD")
        print("(es una referencia, no una cotización bancaria)")




def menu_privado(usuario_actual):
    """Devuelve "9" (cerrar sesión) o "0" (salir)."""
    if usuario_actual is None:
        print("Debe iniciar sesión.")
        return "9"

    while True:
        print(f"\n===== ECOTECH (sesión: {usuario_actual['nombre_usuario']}) =====")
        print("1. Empleados")
        print("2. Departamentos")
        print("3. Proyectos")
        print("4. Registro de tiempo")
        print("5. Demo de relaciones (sin base de datos)")
        print("6. Crear cuenta de usuario para un empleado")
        print("7. Mi perfil")
        print("8. Dólar observado")
        print("9. Cerrar sesión")
        print("0. Salir")

        opcion = solicitar_opcion(9)
        if opcion in (0, 9):
            return str(opcion)
        if opcion == 1:
            menu_empleado()
        elif opcion == 2:
            menu_departamento()
        elif opcion == 3:
            menu_proyecto()
        elif opcion == 4:
            menu_registro_tiempo()
        elif opcion == 5:
            demo_relaciones()
        elif opcion == 6:
            solicitar_registro()
        elif opcion == 7:
            mostrar_perfil(usuario_actual)
        elif opcion == 8:
            consultar_dolar(usuario_actual)

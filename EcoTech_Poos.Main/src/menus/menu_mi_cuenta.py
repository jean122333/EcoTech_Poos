from menus.entradas import (
    manejar_errores, pedir_dato, solicitar_decimal, solicitar_entero, solicitar_fecha,
    solicitar_texto,
)
from menus.menu_empleado import imprimir_ficha
from dominio.empleado import Empleado
from servicios.mi_cuenta import (
    actualizar_mis_datos, mi_ficha, mis_proyectos, mis_registros, registrar_mis_horas,
)

# Opciones de datos propios, disponibles para admin y empleado.


_MSG_CORREO = "Ya existe un empleado con ese correo."


# FICHA
@manejar_errores("consultar mi ficha")
def mostrar_mi_ficha(sesion):
    print(f"Usuario: {sesion['nombre_usuario']} | Rol: {sesion['rol']}")
    imprimir_ficha(mi_ficha(sesion))


@manejar_errores("actualizar mis datos", _MSG_CORREO)
def editar_mis_datos(sesion):
    print("Solo puede cambiar su nombre y su correo.")
    nombre = pedir_dato("Nuevo nombre: ", Empleado.validar_nombre)
    correo = pedir_dato("Nuevo correo: ", Empleado.validar_correo)
    if actualizar_mis_datos(sesion, nombre, correo):
        print("Datos actualizados correctamente.")
    else:
        print("Empleado no encontrado.")


# PROYECTOS Y REGISTROS
@manejar_errores("listar mis proyectos")
def ver_mis_proyectos(sesion):
    proyectos = mis_proyectos(sesion)
    if not proyectos:
        print("No tiene proyectos asignados.")
    for proyecto in proyectos:
        print(" ", proyecto.mostrar_datos())


@manejar_errores("listar mis registros de tiempo")
def ver_mis_registros(sesion):
    registros = mis_registros(sesion)
    if not registros:
        print("No tiene registros de tiempo.")
    for registro in registros:
        print(" ", registro.mostrar_registro(), "|", registro.descripcion or "(sin descripción)")
    print("Total de horas:", sum(r.calcular_horas() for r in registros))


@manejar_errores("registrar mis horas")
def registrar_horas_propias(sesion):
    proyectos = mis_proyectos(sesion)
    if not proyectos:
        print("No tiene proyectos asignados.")
        return
    print("Sus proyectos:")
    for proyecto in proyectos:
        print(" ", proyecto.mostrar_datos())

    proyecto_id = solicitar_entero("ID del proyecto")
    fecha = solicitar_fecha("Fecha")
    horas = solicitar_decimal("Horas trabajadas (0-24)", minimo=0.01, maximo=24)
    descripcion = solicitar_texto("Descripción del trabajo", obligatorio=False)

    registro = registrar_mis_horas(sesion, fecha, horas, descripcion, proyecto_id)
    print("Horas registradas correctamente:", registro.mostrar_registro())
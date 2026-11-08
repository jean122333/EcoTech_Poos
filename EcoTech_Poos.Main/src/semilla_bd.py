# semilla_bd.py
# Carga datos de prueba (ficticios). Antes de insertar busca si el dato ya existe,
# así que se puede ejecutar varias veces sin duplicar.
# Uso: python src/semilla_bd.py
from getpass import getpass

from dominio.departamento import Departamento
from dominio.empleado import Empleado
from dominio.proyecto import Proyecto
from dominio.registroTiempo import RegistroTiempo
from dominio.usuario import Usuario
from persistencia.crear_bd import crear_tablas
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from persistencia.usuario_dao import UsuarioDAO
from servicios.autenticacion import registrar_usuario

CORREO_ADMIN = "admin@ecotech.example"
USUARIO_ADMIN = "admin"

DEPARTAMENTOS = [("Tecnología", "Marta Soto"), ("Administración", "Pedro Rojas")]
# (nombre, correo, salario, departamento)
EMPLEADOS = [
    ("Administrador EcoTech", CORREO_ADMIN, 1200000, "Tecnología"),
    ("Ana Torres", "ana@ecotech.example", 850000, "Tecnología"),
    ("Luis Pérez", "luis@ecotech.example", 920000, "Administración"),
]
# (nombre, fecha_inicio, descripcion, correos de los empleados asignados)
PROYECTOS = [("Sitio web", "2026-09-24", "Rediseño del sitio corporativo",
              ["ana@ecotech.example", "luis@ecotech.example"])]
# (correo, nombre del proyecto, fecha, horas, descripcion)
REGISTROS = [("ana@ecotech.example", "Sitio web", "2026-09-24", 8, "Maquetación"),
             ("luis@ecotech.example", "Sitio web", "2026-09-25", 6.5, "Revisión de contenidos")]


def cargar_departamentos():
    ids = {}
    for nombre, gerente in DEPARTAMENTOS:
        existente = DepartamentoDAO.buscar_por_nombre(nombre)
        if existente is not None:
            print(f"Ya existe: departamento {nombre}")
            ids[nombre] = existente.id_departamento
            continue
        depto = DepartamentoDAO.insertar(Departamento(nombre, gerente))
        ids[nombre] = depto.id_departamento
        print(f"Creado: departamento {nombre}")
    return ids


def cargar_empleados(ids_departamento):
    ids = {}
    for nombre, correo, salario, depto in EMPLEADOS:
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None:
            print(f"Ya existe: {correo}")
            ids[correo] = existente.id_empleado
            continue
        # el constructor valida nombre y correo: la semilla respeta las mismas reglas
        empleado = Empleado(nombre, correo, salario)
        empleado.departamento_id = ids_departamento[depto]
        EmpleadoDAO.insertar(empleado)
        ids[correo] = empleado.id_empleado
        print(f"Creado: {correo}")
    return ids


def cargar_proyectos(ids_empleado):
    ids = {}
    for nombre, fecha, descripcion, correos in PROYECTOS:
        proyecto = ProyectoDAO.buscar_por_nombre(nombre)
        if proyecto is None:
            proyecto = ProyectoDAO.insertar(Proyecto(nombre, fecha, descripcion))
            print(f"Creado: proyecto {nombre}")
        else:
            print(f"Ya existe: proyecto {nombre}")
        ids[nombre] = proyecto.id_proyecto
        for correo in correos:
            id_empleado = ids_empleado[correo]
            ya_asignado = False
            for p in ProyectoDAO.listar_por_empleado(id_empleado):
                if p.id_proyecto == proyecto.id_proyecto:
                    ya_asignado = True
            if not ya_asignado:
                ProyectoDAO.asignar_empleado(proyecto.id_proyecto, id_empleado)
                print(f"Asignado: {correo} -> {nombre}")
    return ids


def cargar_registros(ids_empleado, ids_proyecto):
    for correo, proyecto, fecha, horas, descripcion in REGISTROS:
        id_empleado = ids_empleado[correo]
        ya_cargado = False
        for r in RegistroTiempoDAO.listar_por_empleado(id_empleado):
            if r.fecha == fecha and r.descripcion == descripcion:
                ya_cargado = True
        if ya_cargado:
            print(f"Ya existe: registro de {correo} ({fecha})")
            continue
        RegistroTiempoDAO.insertar(RegistroTiempo(
            fecha, horas, descripcion,
            empleado_id=id_empleado, proyecto_id=ids_proyecto[proyecto],
        ))
        print(f"Creado: registro de {correo} ({fecha})")


def cargar_cuenta_admin(ids_empleado):
    # si la cuenta ya existe no se toca
    if UsuarioDAO.buscar_por_nombre(USUARIO_ADMIN) is not None:
        print(f"Ya existe: cuenta {USUARIO_ADMIN}")
        return
    while True:
        clave = getpass(f"Contraseña para la cuenta '{USUARIO_ADMIN}': ")
        try:
            Usuario.validar_clave(clave)
        except ValueError as error:
            print(f"{error} Intenta nuevamente.")
            continue
        if clave == getpass("Repita la contraseña: "):
            break
        print("Las contraseñas no coinciden.")
    usuario_id = registrar_usuario(ids_empleado[CORREO_ADMIN], USUARIO_ADMIN, clave)
    print(f"Creado: cuenta {USUARIO_ADMIN} (ID {usuario_id})")


def sembrar():
    crear_tablas()
    ids_departamento = cargar_departamentos()
    ids_empleado = cargar_empleados(ids_departamento)
    ids_proyecto = cargar_proyectos(ids_empleado)
    cargar_registros(ids_empleado, ids_proyecto)
    cargar_cuenta_admin(ids_empleado)
    print("Semilla lista.")


if __name__ == "__main__":
    sembrar()

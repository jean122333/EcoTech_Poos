# EcoTech – Modelo de clases y persistencia (POO)

Proyecto de Programación Orientada a Objetos (Unidad 2). Implementa en Python las
clases del diagrama UML (`Empleado`, `Departamento`, `Proyecto`, `RegistroTiempo`, `Usuario`)
con login, roles, consulta del dólar y menú de consola. Funciona con SQLite o MariaDB/MySQL,
según lo que se configure en el archivo `.env`.

## Estructura

```
EcoTech_Poos.Main/
├── requirements.txt
├── .env.example          # plantilla de configuración (se copia como .env)
├── docs/
│   ├── UML_unidad3.md    # cambios al UML (roles, Indicador, permisos)
│   └── USO_DE_IA.md      # documentación del uso de IA
└── src/
    ├── main.py           # login y coordinación
    ├── semilla_bd.py     # datos de prueba y cuentas admin / empleados
    ├── dominio/          # clases del UML (no conocen SQL)
    │   ├── empleado.py, departamento.py, proyecto.py, registroTiempo.py
    │   ├── usuario.py    # cuenta + rol (admin | empleado)
    │   └── indicador.py  # observación validada del dólar
    ├── servicios/        # reglas de acceso y consulta a la API
    │   ├── permisos.py                  # exigir_sesion, exigir_admin, @requiere_admin
    │   ├── autenticacion.py             # hash, registro y login (la sesión trae el rol)
    │   ├── mi_cuenta.py                 # datos propios (empleado_id sale de la sesión)
    │   ├── api_dolar.py                 # consulta HTTP y extracción del dato
    │   ├── deserializador_indicador.py  # diccionario -> Indicador
    │   └── indicadores.py               # consulta + guardado + respaldo + historial
    ├── menus/            # entrada de datos y menús de consola
    │   ├── entradas.py, menu_usuario.py, menu_mi_cuenta.py, menu_indicadores.py
    │   └── menu_empleado.py, menu_departamento.py, menu_proyecto.py,
    │       menu_registro_tiempo.py, demo_relaciones.py
    └── persistencia/     # acceso a la base de datos (todo el SQL)
        ├── conexion.py, base_dao.py, crear_bd.py
        └── empleado_dao.py, departamento_dao.py, proyecto_dao.py,
            registro_tiempo_dao.py, usuario_dao.py, indicador_dao.py
```

## Responsabilidades

- `dominio/`: clases del problema, con validaciones. No conocen SQLite ni MariaDB.
- `persistencia/`: conexión, creación de tablas y DAO. Aquí está todo el SQL.
- `main.py`: menú, validación de entradas y mensajes al usuario. No contiene SQL ni credenciales.
- `.env`: selecciona el motor y guarda la configuración local (no se sube al repositorio).

## Requisitos

- Python 3.10 o superior
- Para MariaDB: XAMPP (phpMyAdmin)

## Instalación y ejecución

1. Clonar el repositorio y entrar a la carpeta del proyecto:
```bash
git clone https://github.com/jean122333/EcoTech_Poos.Main.git
cd EcoTech_Poos.Main
```
2. Instalar las dependencias:
```bash
pip install -r requirements.txt
```
3. Crear el archivo `.env` a partir de la plantilla:
```bash
cp .env.example .env        # en git bush
```
4. Elegir el port en `.env`:

MariaDB (iniciar MySQL desde XAMPP antes de ejecutar):
```
DB_ENGINE=mariadb
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=ecotech
```

# Continuar con esto antes del paso 5
# PYTHONPATH=src python src/persistencia/crear_bd.py
# en la pc UNIversidad, revisar que puerto es 3307 o 3006

5. Cargar los datos de prueba y crear las cuentas "admin", "ana" y "luis" (pide una
   contraseña por cuenta; se puede ejecutar más de una vez sin duplicar ni cambiar cuentas):

```bash
python src/semilla_bd.py
```

6. Ejecutar el programa (pide usuario y contraseña antes de mostrar el menú):
```bash
python src/main.py
```

La base de datos (en MariaDB) y la tabla `empleado` se crean automáticamente si no existen.
Si se cambia de motor, los datos no se comparten: cada motor guarda los suyos.

## Menú (después del login)

```
Empleado y admin             Solo admin (opción 7, Administración)
1. Mi ficha                  1. Empleados          4. Registro de tiempo (todos)
2. Editar mis datos          2. Departamentos      5. Crear cuenta de usuario
3. Mis proyectos             3. Proyectos          6. Demo de relaciones
4. Mis registros de tiempo
5. Registrar mis horas       9. Cerrar sesión      0. Salir
6. Dólar (consultar e historial)
```

## Acceso remoto a MariaDB (phpMyAdmin)

El proyecto lee la conexión desde `.env`, por lo que usar un MariaDB en otro equipo o red no requiere cambiar el código.

1. En phpMyAdmin, pestaña **SQL**, ejecutar (cambiando la clave):

```sql
##CREATE DATABASE IF NOT EXISTS ecotech CHARACTER SET utf8mb4;
##CREATE USER IF NOT EXISTS 'ecotech_app'@'%' IDENTIFIED BY 'CLAVE_LARGA';
##GRANT ALL PRIVILEGES ON ecotech.* TO 'ecotech_app'@'%';
##FLUSH PRIVILEGES;
```
# Arreglo de diseño README 08/11/26 - Jean
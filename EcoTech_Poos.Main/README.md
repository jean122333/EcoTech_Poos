# EcoTech – Modelo de clases y persistencia (POO)

Proyecto de Programación Orientada a Objetos (Unidad 2). Implementa en Python las
clases del diagrama UML (`Empleado`, `Departamento`, `Proyecto`, `RegistroTiempo`)
y un CRUD de empleados con menú de consola. Funciona con SQLite o MariaDB/MySQL,
según lo que se configure en el archivo `.env`.

## Estructura

```
EcoTech_Poos.Main/
├── requirements.txt
├── .env.example          # plantilla de configuración (se copia como .env)
├── .gitignore
├── docs/
│   ├── UML_unidad3.md    # cambios al UML (Empleado y Usuario)
│   └── USO_DE_IA.md      # documentación del uso de IA
└── src/
    ├── main.py           # login y coordinación
    ├── semilla_bd.py     # datos de prueba y cuenta admin
    ├── dominio/          # clases del UML (no conocen SQL)
    │   ├── empleado.py
    │   ├── usuario.py
    │   ├── departamento.py
    │   ├── proyecto.py
    │   └── registroTiempo.py
    ├── servicios/        # autenticación y consulta a la API
    │   ├── autenticacion.py
    │   └── indicadores.py
    ├── menus/            # entrada de datos y menús de consola
    │   ├── entradas.py
    │   └── menu_usuario.py
    └── persistencia/     # acceso a la base de datos
        ├── conexion.py   # abre SQLite o MariaDB según DB_ENGINE
        ├── crear_bd.py   # crea las tablas según el motor
        ├── empleado_dao.py
        └── usuario_dao.py
```

## Responsabilidades

- `dominio/`: clases del problema, con validaciones. No conocen SQLite ni MariaDB.
- `persistencia/`: conexión, creación de tablas y DAO. Aquí está todo el SQL.
- `main.py`: menú, validación de entradas y mensajes al usuario. No contiene SQL ni credenciales.
- `.env`: selecciona el motor y guarda la configuración local (no se sube al repositorio).

## Requisitos

- Python 3.10 o superior
- Para MariaDB: XAMPP (MySQL/MariaDB y phpMyAdmin) o cualquier servidor compatible

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
cp .env.example .env        # en CMD de Windows: copy .env.example .env
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

5. Cargar los datos de prueba y crear la cuenta `admin` (pide una contraseña; se puede
   ejecutar más de una vez sin duplicar datos):
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
1. Empleados            5. Demo de relaciones
2. Departamentos        6. Crear cuenta de usuario para un empleado
3. Proyectos            7. Mi perfil
4. Registro de tiempo   8. Dólar observado (con estimación de CLP a USD)
9. Cerrar sesión        0. Salir
```

## Unidad 3

- **Validaciones:** `Empleado.validar_nombre` y `validar_correo` se usan en los setters, por lo
  que el constructor y la semilla cumplen las mismas reglas. `pedir_dato` repite solo el campo
  que falló. `MAX_CORREO` es 150 porque la columna `correo` es `VARCHAR(150)`.
- **Usuario:** un empleado puede tener una cuenta (`Empleado 1 ── 0..1 Usuario`). La tabla
  `usuario` guarda `password_hash` (bcrypt), no la contraseña. `empleado_id` es FK, `UNIQUE`
  y `NOT NULL`.
- **Login:** registrar una cuenta no inicia sesión. `autenticar` verifica la contraseña con
  `bcrypt.checkpw` y devuelve los datos de la sesión o `None`.
- **API y JSON:** `servicios/indicadores.py` consulta el dólar con `requests`, revisa el estado
  HTTP y valida estructura, unidad, valor y fecha antes de usar el dato.
- **IA:** ver `docs/USO_DE_IA.md`.

## Notas de diseño

- **Un DAO, dos motores:** `conexion.py` informa el motor y el marcador SQL (`?` en SQLite,
  `%s` en MariaDB); el dominio y `main.py` no cambian.
- **Consultas parametrizadas** en el DAO para evitar inyección SQL.
- **Identidad del objeto:** un `Empleado` nuevo comienza con `id=None`; la base de datos
  genera el id y el DAO lo recupera con `cursor.lastrowid`.
- **Manejo de errores:** las escrituras usan `try/except/finally` con `rollback` y cierre de
  conexión. El usuario ve un mensaje seguro; el detalle técnico queda en `ecotech.log`.
- **Resultados normales vs. excepciones:** buscar un id inexistente devuelve `None` y
  eliminar un id inexistente devuelve `False`; no son excepciones.
- **Credenciales fuera del código:** se leen desde `.env` con `python-dotenv`.
- **Relación "Consulta"** (Proyecto–Departamento, 1 a 1) del diagrama original:
  no se implementó por decisión del equipo.

## Acceso remoto a MariaDB (phpMyAdmin)

El proyecto lee la conexión desde `.env`, por lo que usar un MariaDB en otro equipo o red no requiere cambiar el código.

1. En phpMyAdmin, pestaña **SQL**, ejecutar (cambiando la clave):

```sql
##CREATE DATABASE IF NOT EXISTS ecotech CHARACTER SET utf8mb4;
##CREATE USER IF NOT EXISTS 'ecotech_app'@'%' IDENTIFIED BY 'CLAVE_LARGA';
##GRANT ALL PRIVILEGES ON ecotech.* TO 'ecotech_app'@'%';
##FLUSH PRIVILEGES;
```

2. En el `.env` de cada equipo:

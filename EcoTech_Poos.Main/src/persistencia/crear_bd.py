# persistencia/crear_bd.py
# Crea las tablas según el motor (SQLite o MariaDB) y migra bases de versiones anteriores.
from persistencia.conexion import abrir_conexion, obtener_motor

# TIPOS POR MOTOR
# Así cada CREATE TABLE se escribe una sola vez.
_TIPOS = {
    "sqlite": {
        "pk": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "int": "INTEGER",
        "texto_corto": "TEXT",
        "texto_medio": "TEXT",
        "texto_largo": "TEXT",
        "hash": "TEXT",
        "dinero": "REAL",
        "horas": "REAL",
        "fecha": "TEXT",
        "indicador": "REAL",
        "momento": "TEXT",
        "final": "",
    },
    "mysql": {
        "pk": "INT PRIMARY KEY AUTO_INCREMENT",
        "int": "INT",
        "texto_corto": "VARCHAR(100)",
        "texto_medio": "VARCHAR(150)",
        "texto_largo": "TEXT",
        "hash": "VARCHAR(255)",
        "dinero": "DECIMAL(10,2)",
        "horas": "DECIMAL(5,2)",
        "fecha": "DATE",
        "indicador": "DECIMAL(14,4)",
        "momento": "DATETIME",
        # InnoDB es el motor que soporta claves foráneas
        "final": " ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
    },
}

# TABLAS
# el orden importa: primero las tablas a las que otras hacen referencia
_TABLAS = [
    # Departamento 1 a muchos Empleado: la clave foránea queda en empleado
    """
    CREATE TABLE IF NOT EXISTS departamento (
        id_departamento {pk},
        nombre {texto_corto} NOT NULL UNIQUE,
        gerente {texto_corto} NOT NULL
    ){final}
    """,
    """
    CREATE TABLE IF NOT EXISTS empleado (
        id_empleado {pk},
        nombre {texto_corto} NOT NULL,
        correo {texto_medio} NOT NULL UNIQUE,
        salario {dinero} NOT NULL,
        departamento_id {int} NULL,
        FOREIGN KEY (departamento_id) REFERENCES departamento (id_departamento)
            ON DELETE SET NULL
    ){final}
    """,
    """
    CREATE TABLE IF NOT EXISTS proyecto (
        id_proyecto {pk},
        nombre {texto_corto} NOT NULL UNIQUE,
        fecha_inicio {fecha} NOT NULL,
        descripcion {texto_largo} NOT NULL
    ){final}
    """,
    # Empleado muchos a muchos Proyecto: tabla intermedia con clave primaria compuesta
    """
    CREATE TABLE IF NOT EXISTS empleado_proyecto (
        empleado_id {int} NOT NULL,
        proyecto_id {int} NOT NULL,
        PRIMARY KEY (empleado_id, proyecto_id),
        FOREIGN KEY (empleado_id) REFERENCES empleado (id_empleado) ON DELETE CASCADE,
        FOREIGN KEY (proyecto_id) REFERENCES proyecto (id_proyecto) ON DELETE CASCADE
    ){final}
    """,
    # Empleado 1 a muchos RegistroTiempo, Proyecto 1 a muchos RegistroTiempo
    """
    CREATE TABLE IF NOT EXISTS registro_tiempo (
        id_registro {pk},
        fecha {fecha} NOT NULL,
        horas_trabajadas {horas} NOT NULL,
        descripcion {texto_largo} NOT NULL,
        empleado_id {int} NOT NULL,
        proyecto_id {int} NULL,
        FOREIGN KEY (empleado_id) REFERENCES empleado (id_empleado) ON DELETE CASCADE,
        FOREIGN KEY (proyecto_id) REFERENCES proyecto (id_proyecto) ON DELETE SET NULL
    ){final}
    """,
    # Empleado 1 a 0..1 Usuario: empleado_id es FK, UNIQUE y NOT NULL
    # se guarda password_hash, no la contraseña; rol solo admite admin o empleado
    """
    CREATE TABLE IF NOT EXISTS usuario (
        id_usuario {pk},
        nombre_usuario {texto_corto} NOT NULL UNIQUE,
        password_hash {hash} NOT NULL,
        empleado_id {int} NOT NULL UNIQUE,
        rol {texto_corto} NOT NULL DEFAULT 'empleado' CHECK (rol IN ('admin', 'empleado')),
        FOREIGN KEY (empleado_id) REFERENCES empleado (id_empleado) ON DELETE CASCADE
    ){final}
    """,
    # Observaciones del dólar guardadas desde la API: una fila por fuente + indicador + fecha
    """
    CREATE TABLE IF NOT EXISTS indicador_api (
        id_indicador {pk},
        fuente {texto_corto} NOT NULL,
        codigo {texto_corto} NOT NULL,
        fecha {fecha} NOT NULL,
        valor {indicador} NOT NULL,
        unidad {texto_corto} NOT NULL,
        verificado_en {momento} NOT NULL,
        UNIQUE (fuente, codigo, fecha)
    ){final}
    """,
]


# AYUDAS DE MIGRACIÓN
def _tiene_columna(cursor, tabla, columna):
    if obtener_motor() == "sqlite":
        cursor.execute(f"PRAGMA table_info({tabla})")
        return any(fila[1] == columna for fila in cursor.fetchall())
    cursor.execute(f"SHOW COLUMNS FROM {tabla} LIKE '{columna}'")
    return cursor.fetchone() is not None


def _migrar_empleado(cursor):
    """Bases creadas con la versión anterior no tienen empleado.departamento_id."""
    if _tiene_columna(cursor, "empleado", "departamento_id"):
        return
    if obtener_motor() == "sqlite":
        cursor.execute(
            "ALTER TABLE empleado ADD COLUMN departamento_id INTEGER "
            "REFERENCES departamento (id_departamento) ON DELETE SET NULL"
        )
    else:
        cursor.execute(
            "ALTER TABLE empleado ADD COLUMN departamento_id INT NULL, "
            "ADD CONSTRAINT fk_empleado_departamento FOREIGN KEY (departamento_id) "
            "REFERENCES departamento (id_departamento) ON DELETE SET NULL"
        )


def _migrar_usuario(cursor, tipos):
    """Bases creadas antes de los roles no tienen usuario.rol."""
    if _tiene_columna(cursor, "usuario", "rol"):
        return
    cursor.execute(
        f"ALTER TABLE usuario ADD COLUMN rol {tipos['texto_corto']} "
        "NOT NULL DEFAULT 'empleado' CHECK (rol IN ('admin', 'empleado'))"
    )
    # la cuenta 'admin' que creó la semilla antes de existir los roles sigue siendo admin
    cursor.execute("UPDATE usuario SET rol = 'admin' WHERE nombre_usuario = 'admin'")


# CREACIÓN
def crear_tablas():
    conexion = None
    try:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        tipos = _TIPOS[obtener_motor()]

        # se desactivan las claves foráneas mientras se crean las tablas
        # (esta instrucción solo existe en MySQL/MariaDB)
        es_mysql = obtener_motor() == "mysql"
        if es_mysql:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        for plantilla in _TABLAS:
            cursor.execute(plantilla.format(**tipos))

        # se vuelven a activar
        if es_mysql:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

        _migrar_empleado(cursor)
        _migrar_usuario(cursor, tipos)
        conexion.commit()
    except Exception:
        if conexion:
            conexion.rollback()
        raise
    finally:
        if conexion:
            conexion.close()


if __name__ == "__main__":
    crear_tablas()
    print("Base de datos preparada correctamente.")
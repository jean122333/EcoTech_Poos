# Cambios al UML (Unidad 3)

Hay que actualizar `EcoTech_UML.pdf` con estos cambios. Las constantes pertenecen a la clase
y los métodos de validación son `@classmethod`.

```mermaid
classDiagram
    class Empleado {
        +MIN_NOMBRE: int = 2
        +MAX_NOMBRE: int = 100
        +MIN_CORREO: int = 6
        +MAX_CORREO: int = 150
        +validar_nombre(nombre: str) str
        +validar_correo(correo: str) str
    }
    class Usuario {
        +MIN_USUARIO: int = 3
        +MAX_USUARIO: int = 40
        +MIN_CLAVE: int = 6
        +id_usuario: int o None
        +nombre_usuario: str
        +password_hash: str
        +empleado_id: int
        +normalizar_usuario(nombre: str) str
        +validar_clave(clave: str) str
    }
    Empleado "1" -- "0..1" Usuario : tiene cuenta
```

Tabla nueva: `usuario(id_usuario PK, nombre_usuario UNIQUE, password_hash,
empleado_id FK UNIQUE NOT NULL)` que apunta a `empleado(id_empleado)`.
Las constantes `MIN_*` y `MAX_*` no son columnas de la base de datos.

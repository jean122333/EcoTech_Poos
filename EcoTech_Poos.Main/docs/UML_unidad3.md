# UML 

Las constantes pertenecen a la clase
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
        +ROLES: tuple = (admin, empleado)
        +id_usuario: int o None
        +nombre_usuario: str
        +password_hash: str
        +empleado_id: int
        +rol: str = empleado
        +normalizar_usuario(nombre: str) str
        +validar_clave(clave: str) str
        +validar_rol(rol: str) str
    }
    class Indicador {
        +fecha: str
        +valor: float
        +unidad: str = CLP/USD
        +fuente: str
        +codigo: str = dolar
        +verificado_en: str
        +validar_fecha(fecha: str) str
        +validar_valor(valor) float
        +clp_a_usd(monto_clp: float) float
    }
    class DeserializadorIndicador {
        +desde_api(datos: dict)$ Indicador
    }
    class IndicadorDAO {
        +guardar(indicador: Indicador)$
        +listar(codigo: str)$ list
        +ultimo(codigo: str)$ Indicador
    }
    Empleado "1" -- "0..1" Usuario : tiene cuenta
    DeserializadorIndicador ..> Indicador : crea
    IndicadorDAO ..> Indicador : guarda y lee
```

Tabla nueva: `usuario(id_usuario PK, nombre_usuario UNIQUE, password_hash,
empleado_id FK UNIQUE NOT NULL, rol CHECK admin|empleado)` que apunta a
`empleado(id_empleado)`.
Las constantes `MIN_*` y `MAX_*` no son columnas de la base de datos.

Tabla nueva: `indicador_api(id_indicador PK, fuente, codigo, fecha, valor, unidad,
verificado_en, UNIQUE(fuente, codigo, fecha))`.

Módulos de servicio (sin clase): `permisos` (`exigir_sesion`, `exigir_admin`, `requiere_admin`),
`mi_cuenta`, `api_dolar` (`obtener_datos`, `extraer_primero`) e `indicadores`
(`consultar_indicador`, `buscar_respaldo`, `obtener_historial`).

# Sugerencia de la IA en re-estructurar UML
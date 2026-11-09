# Uso de IA en el proyecto EcoTech (Unidad 3)

Registro del uso de IA según lo pedido en las clases 1 y 2: fuente, propuesta de la IA y
decisión propia. Herramienta usada: Claude (Anthropic).

## Fuente

Material de la Unidad 3: guía de refuerzo de validaciones (clase 2), diapositivas de
validaciones y semillas (clase 1), de HTTP, JSON. La API consultada es https://mindicador.cl/api/dolar.

## Qué propuso la IA

A partir del material anterior y del código de la Unidad 2, la IA generó una propuesta de
código que incluye:

| Parte | Archivos |
|---|---|
| Validaciones de nombre y correo en `Empleado` | `dominio/empleado.py` |
| Reintento por campo con `pedir_dato` | `menus/entradas.py`, `menus/menu_empleado.py` |
| Clase `Usuario` y tabla `usuario` | `dominio/usuario.py`, `persistencia/crear_bd.py` |
| Acceso a datos de usuarios | `persistencia/usuario_dao.py` |
| Hash, registro y login | `servicios/autenticacion.py`, `menus/menu_usuario.py`, `main.py` |
| Consulta a la API y lectura del JSON | `servicios/indicadores.py` |
| Semilla de datos y cuenta `admin` | `semilla_bd.py` |
| Documentación | `README.md`, `docs/UML_unidad3.md` |

La IA también corrigió que `crear_tablas` ejecutaba `SET FOREIGN_KEY_CHECKS`, instrucción que
no existe en SQLite, y la dejó solo para MariaDB.

## Qué se revisó y se decidió

- Se pidió bajar la propuesta al nivel de los PDFs (por ejemplo, se quitó una verificación
  con hash falso en el login y las constantes y listas de varios indicadores en la consulta
  a la API) y evitar el uso de `PYTHONPATH`, por lo que la semilla quedó en `src/`.
- Se eliminó  pruebas automáticas que venía en la propuesta.
- Se acortaron y reescribieron comentarios y docstrings de los archivos del proyecto; el
  código de los archivos de la Unidad 2 no se modificó.
- `MAX_CORREO` quedó en 150 (y no 254 como en la guía) para que coincida con la columna
  `correo` de la base de datos.

## Clases 5 y 6: roles, permisos y persistencia de la API

| Parte | Archivos |
|---|---|
| Rol en cuenta, DAO y sesión | `dominio/usuario.py`, `servicios/autenticacion.py` |
| Permisos y datos propios | `servicios/permisos.py` |
| Dólar: objeto, deserializador, DAO, respaldo e historial` |

## Mejora de seguridad con apoyo de IA / Auditoria

- **Propuesta de la IA:** mostrar el menú de administración solo al rol `admin`.
- **Problema detectado:** ocultar la opción no impide llamar a la función por otra ruta.
- **Decisión:** cada operación administrativa lleva `@requiere_admin` y comprueba el rol antes
  de usar el DAO; las cuentas nuevas siempre se crean con rol `empleado` y el formulario no
  permite elegir el rol.

- **Otras revisiones:** el `empleado_id` de los datos propios sale de la sesión (no se pide un ID);
  el guardado de indicadores usa consultas parametrizadas con clave única para no duplicar; los
  errores de la API se registran en `ecotech.log` y el usuario ve un mensaje general; se validó el
  estado HTTP (200) antes de leer el JSON y el valor y la fecha antes de crear el `Indicador`.
- **Ajuste propio:** la SQL de guardado se adaptó a los dos motores (`ON CONFLICT` en SQLite,
  `ON DUPLICATE KEY UPDATE` en MariaDB) y se agregó migración para bases sin la columna `rol`.
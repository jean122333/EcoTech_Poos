# Acceso remoto a MariaDB (XAMPP / phpMyAdmin)

El proyecto lee la conexión desde `.env`: usar un MariaDB de otro equipo no requiere cambiar el código.

## En el equipo que tiene MariaDB

1. Iniciar MySQL desde el panel de XAMPP.
2. Opción manual: en phpMyAdmin, pestaña **SQL**, ejecutar:

```sql
CREATE DATABASE IF NOT EXISTS ecotech CHARACTER SET utf8mb4;
CREATE USER IF NOT EXISTS 'ecotech_app'@'%' IDENTIFIED BY ' ';
GRANT ALL PRIVILEGES ON ecotech.* TO 'ecotech_app'@'%';
FLUSH PRIVILEGES;
```

4. Permitir conexiones externas: en `my.ini` (XAMPP) revisar que `bind-address` sea `0.0.0.0` o esté comentado, y reiniciar MySQL.
5. Abrir el puerto en el firewall de Windows (3306, o el que use el servidor):

```
netsh advfirewall firewall add rule name="MariaDB" dir=in action=allow protocol=TCP localport=3306
```

6. Si la otra PC está en otra red, el router debe redirigir el puerto 3306 hacia este equipo.

## En cada equipo que se conecta

`.env`:

```
DB_ENGINE=mariadb
DB_HOST=root
DB_PORT=3306
DB_PASSWORD=
DB_NAME=ecotech
```

Probar la conexión:

```
python src/diagnostico.py
```

## Errores comunes

| Código | Causa | Solución |
|---|---|---|
| 1045 | Usuario o clave incorrectos | Revisar `DB_USER` y `DB_PASSWORD` |
| 1130 | El usuario no permite conexión desde esa IP | Crear el usuario con `'%'` o con la IP del equipo |
| 1044 | Falta permiso sobre la base | Ejecutar el `GRANT` |
| 1049 | La base no existe | Ejecutar el `CREATE DATABASE` |
| 2003 | Servidor apagado, puerto mal o firewall | Revisar `DB_HOST`, `DB_PORT` y firewall |
| 2005 | Nombre del servidor no se resuelve | Revisar `DB_HOST` |

Si el puerto no es 3306 (en algunos PC de la universidad es 3307), cambiar `DB_PORT`.

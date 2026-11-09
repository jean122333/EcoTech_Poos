from menus.entradas import ejecutar_menu, manejar_errores, solicitar_decimal
from servicios.indicadores import consultar_indicador, obtener_historial
# Consulta del dólar e historial local (admin y empleado).

# OPERACIONES
@manejar_errores("consultar el dólar")
def consultar_dolar(sesion):
    resultado = consultar_indicador(sesion)
    print(resultado["mensaje"])
    dato = resultado["dato"]
    if dato is None:
        return  # sin respaldo no se inventa ningún dato

    print(f"Dólar: {dato.valor:.2f} CLP por USD")
    print(f"Fecha del dato: {dato.fecha}")
    print(f"Última verificación: {dato.verificado_en}")
    print(f"Origen: {resultado['origen']} ({dato.fuente})")

    monto = solicitar_decimal("Monto en CLP para estimar en dólares (vacío = omitir)", opcional=True)
    if monto is not None:
        print(f"Estimación: {monto:,.0f} CLP = {dato.clp_a_usd(monto):,.2f} USD")
        print("(es una referencia, no una cotización bancaria)")

    # Prueba Archivo Update en Github

@manejar_errores("ver el historial del dólar")
def ver_historial(sesion):
    historial = obtener_historial(sesion)
    if not historial:
        print("Aún no existe historial.")
        return

    print("Origen: BD local")
    for dato in historial:
        print(f"  {dato}")


# MENÚ
def menu_indicadores(sesion):
    ejecutar_menu("INDICADORES (DÓLAR)", {
        1: ("Consultar valor actualizado", consultar_dolar),
        2: ("Ver historial guardado", ver_historial),
    }, sesion)
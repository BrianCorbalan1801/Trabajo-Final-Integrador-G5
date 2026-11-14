from importlib import import_module

mod_magnitudes = import_module("02_magnitudes")
a_numero = mod_magnitudes.a_numero


def _hora_valida(hora_str):
    """Valida formato HH:MM:SS con rangos reales (00..23, 00..59, 00..59)."""
    partes = hora_str.split(":")
    if len(partes) != 3:
        return False
    try:
        h, m, s = int(partes[0]), int(partes[1]), int(partes[2])
    except ValueError:
        return False
    return (0 <= h <= 23) and (0 <= m <= 59) and (0 <= s <= 59)


def _fecha_valida(fecha_str):
    """Valida formato básico YYYY-MM-DD."""
    partes = fecha_str.split("-")
    if len(partes) != 3:
        return False
    try:
        anio, mes, dia = int(partes[0]), int(partes[1]), int(partes[2])
    except ValueError:
        return False
    return (anio > 0) and (1 <= mes <= 12) and (1 <= dia <= 31)


def analizar_linea(linea):
    """
    Analiza una línea de mediciones.log.
    Devuelve (medicion, motivo):
    - Si se ignora (vacía o comentario '#'): (None, None)
    - Si es válida: (dict_medicion, None)
    - Si se rechaza: (None, motivo_str)
    """
    limpia = linea.strip()
    if not limpia or limpia.startswith("#"):
        return (None, None)

    # split() sin argumentos separa por espacios Y tabulaciones
    campos = limpia.split()

    if len(campos) != 6:
        return (None, f"Cantidad de campos inválida ({len(campos)} en lugar de 6)")

    fecha, hora, equipo, canal, magnitud, valor_str = campos

    if not _fecha_valida(fecha):
        return (None, f"Fecha inválida: {fecha}")

    if not _hora_valida(hora):
        return (None, f"Hora imposible: {hora}")

    if canal not in ("CH1", "CH2"):
        return (None, f"Canal inválido: {canal}")

    if magnitud not in ("FREQ", "PKPK", "CYCRMS"):
        return (None, f"Magnitud inválida: {magnitud}")

    valor = a_numero(valor_str)
    if valor is None:
        return (None, f"Valor no numérico: {valor_str}")

    medicion = {
        "fecha": fecha,
        "hora": hora,
        "equipo": equipo,
        "canal": canal,
        "magnitud": magnitud,
        "valor": valor,
    }
    return (medicion, None)


def leer_log(ruta):
    """
    Recorre el archivo de log y devuelve un diccionario con:
    - 'series': diccionario agrupado por (equipo, canal, magnitud) -> lista de floats
    - 'rechazadas': lista de dicts con {'linea': nro, 'texto': contenido, 'motivo': razon}
    """
    series = {}
    rechazadas = []

    with open(ruta, "r", encoding="utf-8") as archivo:
        for num_linea, linea in enumerate(archivo, start=1):
            medicion, motivo = analizar_linea(linea)

            if medicion is None and motivo is None:
                # Línea ignorada (en blanco o comentario)
                continue

            if motivo is not None:
                rechazadas.append({
                    "linea": num_linea,
                    "texto": linea.rstrip("\r\n"),
                    "motivo": motivo,
                })
                continue

            clave = (medicion["equipo"], medicion["canal"], medicion["magnitud"])
            if clave not in series:
                series[clave] = []
            series[clave].append(medicion["valor"])

    return {
        "series": series,
        "rechazadas": rechazadas,
    }


if __name__ == "__main__":
    import os

    # 1. Línea normal con espacios
    med, mot = analizar_linea("2026-09-08 09:14:02 ADS3202 CH1 FREQ 1.000431E+03")
    assert mot is None
    assert med["valor"] == 1000.431
    assert med["canal"] == "CH1"

    # 2. Caso trampa de la consigna: línea válida separada por tabulaciones (\t)
    med_tab, mot_tab = analizar_linea("2026-09-08\t09:15:00\tADS3202\tCH1\tFREQ\t9.998000E+02")
    assert mot_tab is None
    assert med_tab["valor"] == 999.8

    # 3. Líneas ignoradas (vacía y comentario)
    assert analizar_linea("   \n") == (None, None)
    assert analizar_linea("# Comentario de sesion") == (None, None)

    # 4. Líneas rechazadas (hora imposible, canal inexistente, valor roto, pocos campos)
    assert analizar_linea("2026-09-08 25:61:00 ADS3202 CH1 FREQ 1.0E+03")[1] is not None
    assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH3 FREQ 1.0E+03")[1] is not None
    assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH1 VOLT 1.0E+03")[1] is not None
    assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH1 FREQ NaN")[1] is not None
    assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH1")[1] is not None

    # 5. Si mediciones.log está en la misma carpeta, probar lectura real
    if os.path.exists("mediciones.log"):
        resultado_log = leer_log("mediciones.log")
        assert ("ADS3202", "CH1", "FREQ") in resultado_log["series"]
        assert len(resultado_log["series"][("ADS3202", "CH1", "FREQ")]) > 0

    print("08_log.py: pruebas OK")

import math

con_unidad = __import__("02_magnitudes").con_unidad
resumen = __import__("09_estadistica").resumen


def armar_informe(idn, series, verificaciones):
    lineas = ["INFORME DEL BANCO DE MEDICIONES", ""]

    if idn:
        lineas.append(f"Equipo: {idn['fabricante']} {idn['modelo']}")
    else:
        lineas.append("Equipo: no identificado")

    lineas.append("")
    lineas.append("SERIES DEL LOG")
    for clave in sorted(series, key=str):
        if isinstance(clave, tuple):
            nombre = " ".join(clave)
        else:
            nombre = str(clave)
        valores = []
        descartados = 0
        for v in series[clave]:
            if math.isfinite(v):
                valores.append(v)
            else:
                descartados = descartados + 1
        r = resumen(valores)
        if r is None:
            lineas.append(f"{nombre}: sin datos")
        else:
            if "FREQ" in nombre:
                u = "Hz"
            else:
                u = "V"
            linea = (
                f"{nombre}: n={r['n']}, promedio={con_unidad(r['promedio'], u)}, "
                f"min={con_unidad(r['minimo'], u)}, max={con_unidad(r['maximo'], u)}"
            )
            if descartados > 0:
                linea = linea + f", descartados={descartados}"
            lineas.append(linea)

    lineas.append("")
    lineas.append("VERIFICACIÓN DE CANALES")
    for ver in verificaciones:
        if "motivo" in ver:
            lineas.append(f"{ver['canal']}: NO verificado ({ver['motivo']})")
        elif ver["coincide"]:
            lineas.append(f"{ver['canal']}: coincide con la teoría")
        else:
            lineas.append(f"{ver['canal']}: NO coincide con la teoría")

    return "\n".join(lineas)


# ---- pruebas ----
if __name__ == "__main__":
    idn = {"fabricante": "OWON", "modelo": "ADS3202", "serie": "1", "version": "2"}
    series = {
        ("ADS3202", "CH1", "FREQ"): [999.0, 1001.0, 1000.0],
        ("ADS3202", "CH2", "PKPK"): [],
    }
    verificaciones = [
        {"canal": "CH1", "coincide": True},
        {"canal": "CH2", "coincide": False},
        {"canal": "CH3", "coincide": False, "motivo": "Faltan datos"},
    ]
    lineas = armar_informe(idn, series, verificaciones).splitlines()

    assert "Equipo: OWON ADS3202" in lineas
    assert "ADS3202 CH1 FREQ: n=3, promedio=1 kHz, min=999 Hz, max=1.001 kHz" in lineas
    assert "ADS3202 CH2 PKPK: sin datos" in lineas
    assert "CH1: coincide con la teoría" in lineas
    assert "CH2: NO coincide con la teoría" in lineas
    assert "CH3: NO verificado (Faltan datos)" in lineas

    series_texto = {"CH1 FREQ": [999.0, 1001.0], "CH1 PKPK": [2.0]}
    lineas_texto = armar_informe(idn, series_texto, []).splitlines()
    assert "CH1 FREQ: n=2, promedio=1 kHz, min=999 Hz, max=1.001 kHz" in lineas_texto
    assert "CH1 PKPK: n=1, promedio=2 V, min=2 V, max=2 V" in lineas_texto

    series_nan = {"CH1 FREQ": [999.0, float("nan"), 1001.0, float("inf")]}
    lineas_nan = armar_informe(idn, series_nan, []).splitlines()
    assert (
        "CH1 FREQ: n=2, promedio=1 kHz, min=999 Hz, max=1.001 kHz, descartados=2"
        in lineas_nan
    )
    solo_nan = armar_informe(idn, {"CH1 FREQ": [float("nan")]}, []).splitlines()
    assert "CH1 FREQ: sin datos" in solo_nan

    vacio = armar_informe(None, {}, []).splitlines()
    assert "Equipo: no identificado" in vacio

    print("pruebas OK")

    Instrumento = __import__("05_cliente").Instrumento
    parsear_idn = __import__("01_identificacion").parsear_idn
    barrer = __import__("06_barrido").barrer
    verificar_canal = __import__("07_verificacion").verificar_canal
    leer_log = __import__("08_log").leer_log

    inst = Instrumento()
    idn = parsear_idn(inst.preguntar("*IDN?"))
    filas = barrer(inst, ["CH1", "CH2"])
    inst.cerrar()

    verificaciones = [verificar_canal(filas, "CH1"), verificar_canal(filas, "CH2")]
    resultado = leer_log("mediciones.log")
    if isinstance(resultado, dict):
        series = resultado["series"]
    else:
        series = resultado[0]
    print(armar_informe(idn, series, verificaciones))
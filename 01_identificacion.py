def parsear_idn(respuesta):
    if respuesta == "" or respuesta == "ERROR: comando desconocido":
        return None

    partes = respuesta.split(",")

    if len(partes) < 4:
        return None

    fabricante = partes[0].strip()
    modelo = partes[1].strip()
    serie = partes[2].strip()
    version = partes[3].strip()

    if fabricante == "" or modelo == "" or serie == "" or version == "":
        return None

    resultado = {
        "fabricante": fabricante,
        "modelo": modelo,
        "serie": serie,
        "version": version
    }
    return resultado

# Prueba Osciloscopio con los 4 datos
assert parsear_idn("OWON,ADS3202,25470803,V1.2.0") == {
    "fabricante": "OWON",
    "modelo": "ADS3202",
    "serie": "25470803",
    "version": "V1.2.0"
}

# Prueba Multímetro con 5 datos y espacios extra
assert parsear_idn(" OWON , XDM1041 , 25470803 , V4.4.0 , 3 ") == {
    "fabricante": "OWON",
    "modelo": "XDM1041",
    "serie": "25470803",
    "version": "V4.4.0"
}

# Casos raros (menos de 4 campos, cadena vacia, campos con espacio y comando desconocido)
assert parsear_idn("OWON,ADS3202,254") is None
assert parsear_idn("") is None
assert parsear_idn("OWON, , 254, V1.0") is None
assert parsear_idn("ERROR: comando desconocido") is None

print("01_identificacion.py: Pruebas OK")
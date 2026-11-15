def a_numero(texto):
    if texto == "":
        return None
    try:
        numero = float(texto.strip())
        return numero
    except ValueError:
        return None

def con_unidad(valor, unidad):
    if valor == 0:
        return "0 " + unidad

    signo = ""
    if valor < 0:
        signo = "-"
        valor = -valor

    factores = [1e9, 1e6, 1e3, 1, 1e-3, 1e-6, 1e-9, 1e-12]
    prefijos = ["G", "M", "k","", "m", "u", "n", "p"]

    for i in range(8):
        factor = factores[i]
        prefijo = prefijos[i]

        escalado = round(valor / factor, 3)

        # Que el resultado quede entre 1 y 999
        if (escalado >= 1.0 and escalado < 1000.0) or i == 7:
            
            if escalado == int(escalado):
                texto_num = str(int(escalado))
            else:
                texto_num = str(escalado)

            return signo + texto_num + " " + prefijo + unidad

# Prueba de a_numero
assert a_numero("1.000000E+03") == 1000.0
assert a_numero("-2.500000E-01") == -0.25
assert a_numero("ERROR: comando desconocido") is None
assert a_numero("") is None

# Prueba de con_unidad
assert con_unidad(1000.0, "Hz") == "1 kHz"
assert con_unidad(2500.0, "Hz") == "2.5 kHz"
assert con_unidad(2.0, "V") == "2 V"
assert con_unidad(0.707, "V") == "707 mV"
assert con_unidad(0.0005, "s") == "500 us"
assert con_unidad(0.0, "V") == "0 V"

assert con_unidad(999.9999, "Hz") == "1 kHz"
assert con_unidad(0.9999999, "V") == "1 V"

print("02_magnitudes.py: Pruebas OK")
import math


def a_numero(texto):
    """
    Convierte una cadena en notación científica o decimal a float.
    Devuelve None si no es un número válido o es NaN/Infinito.
    """
    if not isinstance(texto, str):
        return None
    limpio = texto.strip()
    if not limpio:
        return None
    try:
        valor = float(limpio)
        if math.isnan(valor) or math.isinf(valor):
            return None
        return valor
    except ValueError:
        return None


def con_unidad(valor, unidad):
    """
    Formatea un valor numérico con prefijos SI (p, n, u, m, '', k, M, G)
    de manera que la mantisa quede entre 1 y 999.
    """
    if valor == 0:
        return f"0 {unidad}"

    prefijos = [
        (-12, "p"),
        (-9, "n"),
        (-6, "u"),
        (-3, "m"),
        (0, ""),
        (3, "k"),
        (6, "M"),
        (9, "G"),
    ]

    signo = "-" if valor < 0 else ""
    magnitud = abs(valor)

    # Buscar el índice inicial adecuado
    idx = 0
    for i, (exp, _) in enumerate(prefijos):
        if magnitud >= (10 ** exp):
            idx = i
        else:
            break

    escalado = round(magnitud / (10 ** prefijos[idx][0]), 3)

    # Caso borde: si al redondear a 3 decimales llega a 1000, subir de prefijo
    if escalado >= 1000.0 and idx < len(prefijos) - 1:
        idx += 1
        escalado = round(magnitud / (10 ** prefijos[idx][0]), 3)

    # Formatear quitando ceros decimales innecesarios (ej: 1.000 -> "1", 2.500 -> "2.5")
    texto_num = f"{escalado:.3f}".rstrip("0").rstrip(".")
    prefijo = prefijos[idx][1]

    return f"{signo}{texto_num} {prefijo}{unidad}"


if __name__ == "__main__":
    # Pruebas de a_numero
    assert a_numero("1.000000E+03") == 1000.0
    assert a_numero("  -2.5e-03 \n") == -0.0025
    assert a_numero("ERROR") is None
    assert a_numero("") is None
    assert a_numero("NaN") is None

    # Pruebas de con_unidad (incluyendo todos los ejemplos de la consigna)
    assert con_unidad(1000.0, "Hz") == "1 kHz"
    assert con_unidad(2500.0, "Hz") == "2.5 kHz"
    assert con_unidad(2.0, "V") == "2 V"
    assert con_unidad(0.707, "V") == "707 mV"
    assert con_unidad(0.0005, "s") == "500 us"
    assert con_unidad(0.0, "V") == "0 V"

    # Caso trampa de redondeo mencionado en la consigna
    assert con_unidad(999.9999, "Hz") == "1 kHz"
    assert con_unidad(1e-12, "F") == "1 pF"
    assert con_unidad(2.4e9, "Hz") == "2.4 GHz"

    print("02_magnitudes.py: pruebas OK")

import math


def vrms_teorico(vpp):
    """
    Calcula el Vrms teórico de una señal senoidal a partir de su Vpp:
    Vp = vpp / 2, Vrms = Vp / sqrt(2).
    Devuelve None si vpp no es un número positivo válido.
    """
    if vpp is None or isinstance(vpp, bool) or not isinstance(vpp, (int, float)):
        return None
    if math.isnan(vpp) or math.isinf(vpp) or vpp <= 0:
        return None
    return (vpp / 2.0) / math.sqrt(2.0)


def coincide(medido, teorico, tolerancia=0.02):
    """
    Verifica si el valor medido cae dentro de la tolerancia relativa respecto al teórico.
    error = |medido - teorico| / |teorico|
    """
    if medido is None or teorico is None or teorico == 0:
        return False
    error_relativo = abs(medido - teorico) / abs(teorico)
    return error_relativo <= tolerancia


def verificar_canal(filas, canal):
    """
    Busca PKPK y CYCRMS de un canal en el resultado de barrer()
    y verifica si el Vrms medido coincide con el teórico senoidal.
    """
    vpp_medido = None
    vrms_medido = None

    for fila in filas:
        if fila.get("canal") == canal:
            if fila.get("magnitud") == "PKPK":
                vpp_medido = fila.get("valor")
            elif fila.get("magnitud") == "CYCRMS":
                vrms_medido = fila.get("valor")

    teorico = vrms_teorico(vpp_medido)
    ok = coincide(vrms_medido, teorico)

    return {
        "canal": canal,
        "vpp": vpp_medido,
        "vrms_medido": vrms_medido,
        "vrms_teorico": teorico,
        "coincide": ok,
    }


if __name__ == "__main__":
    # 1. Pruebas de vrms_teorico
    assert abs(vrms_teorico(2.0) - 0.70710678) < 1e-6
    assert vrms_teorico(0) is None
    assert vrms_teorico(-5.0) is None
    assert vrms_teorico(None) is None

    # 2. Pruebas de coincide (con "temblor" típico de laboratorio dentro del 2%)
    assert coincide(0.710, 0.7071) is True
    assert coincide(0.750, 0.7071) is False

    # 3. Prueba de verificar_canal con señal senoidal real (debe coincidir)
    barrido_senoidal = [
        {"canal": "CH1", "magnitud": "FREQ", "unidad": "Hz", "crudo": "1.00E+03", "valor": 1000.0},
        {"canal": "CH1", "magnitud": "PKPK", "unidad": "V", "crudo": "2.01E+00", "valor": 2.01},
        {"canal": "CH1", "magnitud": "CYCRMS", "unidad": "V", "crudo": "7.09E-01", "valor": 0.709},
    ]
    res_ok = verificar_canal(barrido_senoidal, "CH1")
    assert res_ok["coincide"] is True

    # 4. Prueba negativa de la consigna: señal cuadrada (Vpp = 2 V, Vrms = 1 V -> NO es senoide)
    barrido_cuadrada = [
        {"canal": "CH1", "magnitud": "PKPK", "unidad": "V", "crudo": "2.00E+00", "valor": 2.0},
        {"canal": "CH1", "magnitud": "CYCRMS", "unidad": "V", "crudo": "1.00E+00", "valor": 1.0},
    ]
    res_cuadrada = verificar_canal(barrido_cuadrada, "CH1")
    assert res_cuadrada["coincide"] is False

    # 5. Canal inexistente o sin mediciones
    res_vacio = verificar_canal(barrido_senoidal, "CH2")
    assert res_vacio["coincide"] is False

    print("07_verificacion.py: pruebas OK")

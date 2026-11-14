from importlib import import_module

mod_magnitudes = import_module("02_magnitudes")
a_numero = mod_magnitudes.a_numero


def barrer(instrumento, canales):
    """
    Consulta FREQuency?, PKPK? y CYCRms? para cada canal indicado.
    Devuelve una lista de diccionarios con:
    canal, magnitud, unidad, crudo y valor (float o None si hubo error).
    """
    magnitudes = [
        ("FREQ", "FREQuency?", "Hz"),
        ("PKPK", "PKPK?", "V"),
        ("CYCRMS", "CYCRms?", "V"),
    ]

    resultados = []
    for canal in canales:
        for nombre_mag, sufijo_scpi, unidad in magnitudes:
            comando = f":MEASUrement:{canal}:{sufijo_scpi}"
            crudo = instrumento.preguntar(comando)
            valor = a_numero(crudo)

            resultados.append({
                "canal": canal,
                "magnitud": nombre_mag,
                "unidad": unidad,
                "crudo": crudo,
                "valor": valor,
            })

    return resultados


if __name__ == "__main__":
    # Clase mock (de mentira) para probar sin levantar instrumento_virtual.py
    class InstrumentoFalso:
        def __init__(self, respuestas):
            self.respuestas = respuestas

        def preguntar(self, comando):
            return self.respuestas.get(comando, "ERROR: comando desconocido")

    datos_simulados = {
        ":MEASUrement:CH1:FREQuency?": "1.000000E+03",
        ":MEASUrement:CH1:PKPK?": "2.000000E+00",
        ":MEASUrement:CH1:CYCRms?": "7.071000E-01",
        ":MEASUrement:CH2:FREQuency?": "2.500000E+03",
        ":MEASUrement:CH2:PKPK?": "8.000000E-01",
        ":MEASUrement:CH2:CYCRms?": "ERROR: sin senal",
    }

    inst_falso = InstrumentoFalso(datos_simulados)
    filas = barrer(inst_falso, ["CH1", "CH2"])

    # 2 canales x 3 magnitudes = 6 mediciones
    assert len(filas) == 6

    # Verificar primera medición (CH1 FREQ)
    assert filas[0] == {
        "canal": "CH1",
        "magnitud": "FREQ",
        "unidad": "Hz",
        "crudo": "1.000000E+03",
        "valor": 1000.0,
    }

    # Verificar caso de error del equipo: valor debe ser None pero crudo se conserva
    assert filas[5]["canal"] == "CH2"
    assert filas[5]["magnitud"] == "CYCRMS"
    assert filas[5]["crudo"] == "ERROR: sin senal"
    assert filas[5]["valor"] is None

    print("06_barrido.py: pruebas OK")

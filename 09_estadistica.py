import math


def resumen(valores):
    if not valores:
        return None
    n = len(valores)
    minimo = valores[0]
    maximo = valores[0]
    total = 0.0
    for v in valores:
        total = total + v
        if v < minimo:
            minimo = v
        if v > maximo:
            maximo = v
    promedio = total / n
    desvio = 0.0
    if n > 1:
        suma = 0.0
        for v in valores:
            suma = suma + (v - promedio) ** 2
        desvio = math.sqrt(suma / (n - 1))
    return {
        "n": n,
        "minimo": minimo,
        "maximo": maximo,
        "promedio": promedio,
        "desvio": desvio,
    }


def fuera_de_rango(valores, minimo, maximo):
    posiciones = []
    for i in range(len(valores)):
        if valores[i] < minimo or valores[i] > maximo:
            posiciones.append(i)
    return posiciones


# ////////////// pruebas //////////////
if __name__ == "__main__":
    r = resumen([2.0, 4.0])
    assert r["n"] == 2
    assert r["promedio"] == 3.0
    assert abs(r["desvio"] - math.sqrt(2)) < 1e-9

    r = resumen([-75.0, -52.3, -80.1])
    assert r["minimo"] == -80.1
    assert r["maximo"] == -52.3

    assert resumen([]) is None
    assert resumen([5.0])["desvio"] == 0.0

    assert fuera_de_rango([1.0, 5.0, 10.0, 15.0], 5.0, 10.0) == [0, 3]
    assert fuera_de_rango([5.0, 10.0], 5.0, 10.0) == []
    assert fuera_de_rango([], 0.0, 1.0) == []

    print("pruebas OK")
CANALES_VALIDOS = ("CH1", "CH2")


def comandos_de_canal(canal, display, acoplamiento, sonda, escala):
    if canal not in CANALES_VALIDOS:
        return None
    return [
        f":{canal}:DISPlay {display}",
        f":{canal}:COUPling {acoplamiento}",
        f":{canal}:PROBe {sonda}",
        f":{canal}:SCALe {escala}",
    ]


# /////////////// pruebas ///////////////
if __name__ == "__main__":
    validar = __import__("03_comandos").validar

    cmds = comandos_de_canal("CH1", "ON", "DC", "10X", "1v")
    assert cmds == [
        ":CH1:DISPlay ON",
        ":CH1:COUPling DC",
        ":CH1:PROBe 10X",
        ":CH1:SCALe 1v",
    ]

    cmds2 = comandos_de_canal(
        canal="CH2", display="OFF", acoplamiento="AC", sonda="1X", escala="500mv"
    )
    assert cmds2 == comandos_de_canal("CH2", "OFF", "AC", "1X", "500mv")
    assert cmds2 == [
        ":CH2:DISPlay OFF",
        ":CH2:COUPling AC",
        ":CH2:PROBe 1X",
        ":CH2:SCALe 500mv",
    ]

    for c in cmds + cmds2:
        assert validar(c) is None, f"validar rechazo {c!r}"

    assert len(cmds) == 4
    assert all(not c.endswith("?") for c in cmds)

    assert comandos_de_canal("CH3", "ON", "DC", "10X", "1v") is None
    assert comandos_de_canal("ch1", "ON", "DC", "10X", "1v") is None
    assert comandos_de_canal("", "ON", "DC", "10X", "1v") is None
    assert comandos_de_canal(None, "ON", "DC", "10X", "1v") is None
    assert comandos_de_canal(1, "ON", "DC", "10X", "1v") is None

    mala = comandos_de_canal("CH1", "ON", "DC", "10X", "1 v")
    assert validar(mala[3]) is not None

    print("pruebas OK")
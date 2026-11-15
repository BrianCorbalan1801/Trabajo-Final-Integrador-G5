def es_consulta(comando):
    comando_limpio = comando.strip()
    if comando_limpio.endswith("?"):
        return True
    else:
        return False

def validar(comando):
    cmd = comando.strip()

    # 1 No puede estar vacío
    if cmd == "":
        return "No puede estar vacio"

    # 2 Empieza con : o con *
    if cmd[0] != ":" and cmd[0] != "*":
        return "Empieza con : o *"

    # 3 No hay dos espacios seguidos
    if "  " in cmd:
        return "No hay dos espacios seguidos"

    # 4 Hay a lo sumo un ?
    cantidad_preguntas = cmd.count("?")
    if cantidad_preguntas > 1:
        return "Hay a lo sumo un ?"

    # 5 El signo ? va al final
    if cantidad_preguntas == 1 and not cmd.endswith("?"):
        return "El signo ? va al final"

    partes = cmd.split(" ")

    # 6 Una orden lleva un solo argumento
    if len(partes) > 2:
        return "Una orden lleva un solo argumento"

    # 7 Una consulta no lleva argumento
    if es_consulta(cmd) and len(partes) > 1:
        return "Una consulta no lleva argumento"

    # Si el comando esta bien formado devuelve un None
    return None

# Prueba de es_consulta
assert es_consulta(":MEASUrement:CH1:FREQuency?") is True
assert es_consulta(":CH1:DISPlay ON") is False

# Prueba de comandos válidos
assert validar(":CH1:DISPlay ON") is None
assert validar("*IDN?") is None

# Prueba de las reglas
assert validar("") == "No puede estar vacio"
assert validar("CH1:DISPlay ON") == "Empieza con : o *"
assert validar(":CH1:DISPlay  ON") == "No hay dos espacios seguidos"
assert validar(":CH1:DISPlay??") == "Hay a lo sumo un ?"
assert validar(":CH1:DIS?Play") == "El signo ? va al final"
assert validar(":CH1:SCALe 1 v") == "Una orden lleva un solo argumento"
assert validar(":CH1:DISPlay ON?") == "Una consulta no lleva argumento"

print("03_comandos.py: Pruebas OK")
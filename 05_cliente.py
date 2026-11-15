import socket


class Instrumento:
    def __init__(self, direccion="127.0.0.1", puerto=5555):
        self.sock = socket.socket()
        self.sock.connect((direccion, puerto))

    def enviar(self, comando):
        self.sock.sendall((comando + "\n").encode())

    def preguntar(self, comando):
        self.enviar(comando)
        respuesta = ""
        while not respuesta.endswith("\n"):
            datos = self.sock.recv(1024).decode()
            if datos == "":
                break
            respuesta = respuesta + datos
        return respuesta.strip()

    def cerrar(self):
        self.sock.close()


# /////////// pruebas ///////////
if __name__ == "__main__":
    parsear_idn = __import__("01_identificacion").parsear_idn
    try:
        inst = Instrumento()
    except ConnectionRefusedError:
        print("Prendé primero el instrumento virtual: python3 instrumento_virtual.py")
        raise SystemExit(1)

    respuesta = inst.preguntar("*IDN?")
    assert respuesta == "OWON,ADS3202,25470803,V1.2.0"
    assert parsear_idn(respuesta)["modelo"] == "ADS3202"

    inst.enviar(":CH1:DISPlay ON")
    assert inst.preguntar("*IDN?") == "OWON,ADS3202,25470803,V1.2.0"

    assert inst.preguntar(":NO:EXISTE?").startswith("ERROR")

    inst.cerrar()
    try:
        inst.preguntar("*IDN?")
        assert False, "tenia que fallar con la conexion cerrada"
    except OSError:
        pass

    print("pruebas OK")
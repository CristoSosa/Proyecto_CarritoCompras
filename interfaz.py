import msvcrt


def leer_contrasena(mensaje):
    print(mensaje, end="", flush=True)
    contrasena = ""

    while True:
        tecla = msvcrt.getch()

        if tecla in (b"\r", b"\n"):
            print()
            return contrasena

        if tecla == b"\x08":
            if contrasena:
                contrasena = contrasena[:-1]
                print("\b \b", end="", flush=True)
            continue

        if tecla in (b"\x00", b"\xe0"):
            msvcrt.getch()
            continue

        try:
            caracter = tecla.decode("utf-8")
        except UnicodeDecodeError:
            continue

        contrasena += caracter
        print("*", end="", flush=True)

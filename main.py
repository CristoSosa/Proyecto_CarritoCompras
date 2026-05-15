from base_datos import BaseDatos
from interfaz import InterfazConsola


def main():
    interfaz = InterfazConsola(BaseDatos())
    try:
        interfaz.iniciar()
    finally:
        interfaz.cerrar()


if __name__ == "__main__":
    main()

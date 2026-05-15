import sqlite3
from pathlib import Path


class BaseDatos:
    def __init__(self, nombre_archivo="DataBaseMercado.db"):
        self.ruta = Path(__file__).resolve().parent / nombre_archivo

    def conectar(self):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        return conexion, cursor

    def cerrar(self, conexion):
        conexion.close()

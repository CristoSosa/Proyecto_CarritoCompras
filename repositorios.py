class RepositorioUsuarios:
    def __init__(self, conexion):
        self.conexion = conexion

    def crear(self, nombre, contrasena, correo, numero):
        cursor = self.conexion.cursor()
        cursor.execute(
            """
            INSERT INTO USUARIOS (NOMBRE, CONTRASENA, CORREO, NUMERO)
            VALUES (?, ?, ?, ?)
            """,
            (nombre, contrasena, correo, numero),
        )

    def buscar_por_correo(self, correo):
        cursor = self.conexion.cursor()
        cursor.execute(
            """
            SELECT ID, NOMBRE, CONTRASENA, CORREO, NUMERO
            FROM USUARIOS
            WHERE CORREO = ?
            """,
            (correo,),
        )
        return cursor.fetchone()


class RepositorioEmpleados:
    def __init__(self, conexion):
        self.conexion = conexion

    def crear(self, nombre, contrasena, correo, numero, nomina=0.0):
        cursor = self.conexion.cursor()
        cursor.execute(
            """
            INSERT INTO EMPLEADOS (NOMBRE, CONTRASENA, CORREO, NUMERO, NOMINA)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nombre, contrasena, correo, numero, nomina),
        )

    def buscar_por_correo(self, correo):
        cursor = self.conexion.cursor()
        cursor.execute(
            """
            SELECT ID, NOMBRE, CONTRASENA, CORREO, NUMERO, NOMINA
            FROM EMPLEADOS
            WHERE CORREO = ?
            """,
            (correo,),
        )
        return cursor.fetchone()

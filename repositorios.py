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


class RepositorioCategorias:
    def __init__(self, conexion):
        self.conexion = conexion

    def listar(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM CATEGORIA")
        return cursor.fetchall()

    def listar_id_nombre(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT ID, NOMBRE FROM CATEGORIA")
        return cursor.fetchall()

    def crear(self, nombre, descripcion):
        cursor = self.conexion.cursor()
        cursor.execute(
            "INSERT INTO CATEGORIA VALUES (?, ?, ?)",
            (None, nombre, descripcion),
        )

    def eliminar(self, categoria_id):
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM CATEGORIA WHERE ID = ?", (categoria_id,))


class RepositorioProductos:
    def __init__(self, conexion):
        self.conexion = conexion

    def listar(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM PRODUCTOS")
        return cursor.fetchall()

    def listar_por_categoria(self, categoria_id):
        cursor = self.conexion.cursor()
        cursor.execute(
            """
            SELECT ID, NOMBRE_ARTICULO, PRECIO, CANTIDAD
            FROM PRODUCTOS
            WHERE CATEGORIA_ID = ?
            """,
            (categoria_id,),
        )
        return cursor.fetchall()

    def crear(self, nombre, precio, cantidad, categoria_id):
        cursor = self.conexion.cursor()
        cursor.execute(
            "INSERT INTO PRODUCTOS VALUES (?, ?, ?, ?, ?)",
            (None, nombre, precio, cantidad, categoria_id),
        )

    def eliminar(self, producto_id):
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM PRODUCTOS WHERE ID = ?", (producto_id,))

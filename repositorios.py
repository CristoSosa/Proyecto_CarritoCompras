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

    def actualizar(self, categoria_id, nombre, descripcion):
        cursor = self.conexion.cursor()
        cursor.execute(
            "UPDATE CATEGORIA SET NOMBRE=?, DESCRIPCION=? WHERE ID=?",
            (nombre, descripcion, categoria_id)
        )

    def buscar_por_id(self, categoria_id):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM CATEGORIA WHERE ID = ?", (categoria_id,))
        return cursor.fetchone()


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
    
    def actualizar(self, producto_id, nombre, precio, cantidad, categoria_id):
        cursor = self.conexion.cursor()
        cursor.execute(
            "UPDATE PRODUCTOS SET NOMBRE_ARTICULO=?, PRECIO=?, CANTIDAD=?, CATEGORIA_ID=? WHERE ID=?",
            (nombre, precio, cantidad, categoria_id, producto_id)
        )

    def buscar_por_id(self, producto_id):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM PRODUCTOS WHERE ID = ?", (producto_id,))
        return cursor.fetchone()



    def actualizar_cantidad(self, producto_id, cantidad):
        cursor = self.conexion.cursor()
        cursor.execute(
            "UPDATE PRODUCTOS SET CANTIDAD = ? WHERE ID = ?",
            (cantidad, producto_id),
        )


class RepositorioCarrito:
    def __init__(self, conexion):
        self.conexion = conexion

    def agregar(self, usuario_id, producto_id, cantidad):
        cursor = self.conexion.cursor()
        cursor.execute(
            "INSERT INTO Carrito_Compras VALUES (?, ?, ?, ?)",
            (None, usuario_id, producto_id, cantidad),
        )

    def listar_por_usuario(self, usuario_id):
        cursor = self.conexion.cursor()
        cursor.execute(
            """
            SELECT Carrito_Compras.ID, PRODUCTOS.NOMBRE_ARTICULO, PRODUCTOS.PRECIO, Carrito_Compras.CANTIDAD, CATEGORIA.NOMBRE, Carrito_Compras.PRODUCTO_ID
            FROM Carrito_Compras
            INNER JOIN PRODUCTOS ON Carrito_Compras.PRODUCTO_ID = PRODUCTOS.ID
            INNER JOIN CATEGORIA ON PRODUCTOS.CATEGORIA_ID = CATEGORIA.ID
            WHERE Carrito_Compras.USER_ID = ?
            """,
            (usuario_id,),
        )
        return cursor.fetchall()

    def eliminar_articulo(self, usuario_id, articulo_id):
        cursor = self.conexion.cursor()
        cursor.execute(
            "DELETE FROM Carrito_Compras WHERE USER_ID = ? AND ID = ?",
            (usuario_id, articulo_id),
        )

    def vaciar(self, usuario_id):
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM Carrito_Compras WHERE USER_ID = ?", (usuario_id,))


class RepositorioVentas:
    def __init__(self, conexion):
        self.conexion = conexion

    def crear(self, usuario_id, producto_id, total):
        cursor = self.conexion.cursor()
        cursor.execute(
            "INSERT INTO VENTAS VALUES (?, ?, ?, ?)",
            (None, usuario_id, producto_id, total),
        )

    def listar_todas(self):
        cursor = self.conexion.cursor()
        cursor.execute(
            """
            SELECT VENTAS.ID, USUARIOS.NOMBRE, PRODUCTOS.NOMBRE_ARTICULO, VENTAS.TOTAL FROM VENTAS
            INNER JOIN USUARIOS ON VENTAS.USUARIO_ID = USUARIOS.ID
            INNER JOIN PRODUCTOS ON VENTAS.PRODUCTO_ID = PRODUCTOS.ID
            """
        )
        return cursor.fetchall()

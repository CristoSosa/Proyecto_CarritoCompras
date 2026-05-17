import bcrypt

from repositorios import (
    RepositorioCarrito,
    RepositorioCategorias,
    RepositorioEmpleados,
    RepositorioProductos,
    RepositorioUsuarios,
    RepositorioVentas,
)


class ServicioAutenticacion:
    def __init__(self, conexion):
        self.conexion = conexion
        self.repositorio_usuarios = RepositorioUsuarios(conexion)
        self.repositorio_empleados = RepositorioEmpleados(conexion)

    def registrar_usuario(self, nombre, contrasena, correo, numero):
        if self.correo_registrado(correo):
            return False
        
        contrasena_encriptada = self._encriptar_contrasena(contrasena)
        self.repositorio_usuarios.crear(nombre, contrasena_encriptada, correo, numero)
        self.conexion.commit()
        return True

    def registrar_empleado(self, nombre, contrasena, correo, numero):
        if self.correo_registrado(correo):
            return False
        
        contrasena_encriptada = self._encriptar_contrasena(contrasena)
        self.repositorio_empleados.crear(nombre, contrasena_encriptada, correo, numero)
        self.conexion.commit()
        return True

    def iniciar_sesion(self, correo, contrasena):
        usuario = self.repositorio_usuarios.buscar_por_correo(correo)
        if usuario and self._contrasena_correcta(contrasena, usuario[2]):
            return "usuario", (usuario[1],), (usuario[0],)

        empleado = self.repositorio_empleados.buscar_por_correo(correo)
        if empleado and self._contrasena_correcta(contrasena, empleado[2]):
            return "empleado", (empleado[1],), (empleado[0],)

        return None, None, None

    def _encriptar_contrasena(self, contrasena):
        return bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt())

    def _contrasena_correcta(self, contrasena, contrasena_guardada):
        if isinstance(contrasena_guardada, str):
            contrasena_guardada = contrasena_guardada.encode("utf-8")

        return bcrypt.checkpw(contrasena.encode("utf-8"), contrasena_guardada)
    
    def correo_registrado(self, correo):
        usuario = self.repositorio_usuarios.buscar_por_correo(correo)
        empleado = self.repositorio_empleados.buscar_por_correo(correo)
        return usuario is not None or empleado is not None
    
    def correo_valido(self, correo):
        correo = correo.strip().lower()
        if correo.count("@") != 1:
            return False
        
        posicion_arroba = correo.find("@")
        posicion_punto = correo.rfind(".")

        if posicion_arroba == 0:
            return False
        if posicion_punto == -1:
            return False
        if posicion_punto < posicion_arroba:
            return False
        if posicion_punto == len(correo) - 1:
            return False

        dominios_permitidos = ["gmail.com", "hotmail.com", "outlook.com", "culiacan.tecnm.mx"]
        dominio = correo[posicion_arroba + 1:]

        if dominio not in dominios_permitidos :
            return False
        
        return True

    def numero_valido(self, numero):
        numero = numero.strip()

        if len(numero) != 10:
            return False
        
        if not numero.isdigit():
            return False
        
        return True

class ServicioInventario:
    def __init__(self, conexion):
        self.conexion = conexion
        self.repositorio_productos = RepositorioProductos(conexion)
        self.repositorio_categorias = RepositorioCategorias(conexion)

    def listar_productos(self):
        return self.repositorio_productos.listar()

    def eliminar_producto(self, producto_id):
        self.repositorio_productos.eliminar(producto_id)
        self.conexion.commit()

    def agregar_producto(self, nombre, precio, cantidad, categoria_id):
        self.repositorio_productos.crear(nombre, precio, cantidad, categoria_id)
        self.conexion.commit()

    def listar_categorias(self):
        return self.repositorio_categorias.listar()

    def listar_categorias_id_nombre(self):
        return self.repositorio_categorias.listar_id_nombre()

    def eliminar_categoria(self, categoria_id):
        self.repositorio_categorias.eliminar(categoria_id)
        self.conexion.commit()

    def agregar_categoria(self, nombre, descripcion):
        self.repositorio_categorias.crear(nombre, descripcion)
        self.conexion.commit()
    
    def actualizar_producto(self, producto_id, nombre, precio, cantidad, categoria_id):
        self.repositorio_productos.actualizar(producto_id, nombre, precio, cantidad, categoria_id)
        self.conexion.commit()

    def actualizar_categoria(self, categoria_id, nombre, descripcion):
        self.repositorio_categorias.actualizar(categoria_id, nombre, descripcion)
        self.conexion.commit()

    def obtener_producto(self, producto_id):
        return self.repositorio_productos.buscar_por_id(producto_id)

    def obtener_categoria(self, categoria_id):
        return self.repositorio_categorias.buscar_por_id(categoria_id)




class ServicioCompras:
    def __init__(self, conexion):
        self.conexion = conexion
        self.repositorio_categorias = RepositorioCategorias(conexion)
        self.repositorio_productos = RepositorioProductos(conexion)
        self.repositorio_carrito = RepositorioCarrito(conexion)

    def listar_categorias_id_nombre(self):
        return self.repositorio_categorias.listar_id_nombre()

    def listar_productos_por_categoria(self, categoria_id):
        return self.repositorio_productos.listar_por_categoria(categoria_id)

    def agregar_al_carrito(self, usuario_id, producto_id, unidades, nueva_cantidad):
        self.repositorio_carrito.agregar(usuario_id, producto_id, unidades)
        self.repositorio_productos.actualizar_cantidad(producto_id, nueva_cantidad)
        self.conexion.commit()

    def listar_carrito(self, usuario_id):
        return self.repositorio_carrito.listar_por_usuario(usuario_id)

    def eliminar_articulo_carrito(self, usuario_id, articulo_id):
        self.repositorio_carrito.eliminar_articulo(usuario_id, articulo_id)
        self.conexion.commit()


class ServicioVentas:
    def __init__(self, conexion):
        self.conexion = conexion
        self.repositorio_carrito = RepositorioCarrito(conexion)
        self.repositorio_ventas = RepositorioVentas(conexion)

    def registrar_venta(self, usuario_id, producto_id, total):
        self.repositorio_carrito.vaciar(usuario_id)
        self.repositorio_ventas.crear(usuario_id, producto_id, total)
        self.conexion.commit()

    def listar_todas(self):
        return self.repositorio_ventas.listar_todas()

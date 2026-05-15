import bcrypt

from repositorios import RepositorioEmpleados, RepositorioUsuarios


class ServicioAutenticacion:
    def __init__(self, conexion):
        self.conexion = conexion
        self.repositorio_usuarios = RepositorioUsuarios(conexion)
        self.repositorio_empleados = RepositorioEmpleados(conexion)

    def registrar_usuario(self, nombre, contrasena, correo, numero):
        contrasena_encriptada = self._encriptar_contrasena(contrasena)
        self.repositorio_usuarios.crear(nombre, contrasena_encriptada, correo, numero)
        self.conexion.commit()

    def registrar_empleado(self, nombre, contrasena, correo, numero):
        contrasena_encriptada = self._encriptar_contrasena(contrasena)
        self.repositorio_empleados.crear(nombre, contrasena_encriptada, correo, numero)
        self.conexion.commit()

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

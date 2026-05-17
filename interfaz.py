import msvcrt

from servicios import (
    ServicioAutenticacion,
    ServicioCompras,
    ServicioInventario,
    ServicioVentas,
)

from ticket import generar_ticket


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

def leer_contrasena_valida(mensaje):
    password = leer_contrasena(mensaje)

    if es_cancelacion(password):
        return None

    while not contrasena_valida(password):
        print("\nLa contraseña debe tener al menos una mayúscula y un número.\n")
        password = leer_contrasena(mensaje)
        if es_cancelacion(password):
            return None

    return password

def contrasena_valida(password):
    if password.strip() == "":
        return False
    
    contiene_mayuscula = False
    contiene_numero = False

    for caracter in password:
        if caracter.isupper():
            contiene_mayuscula = True
        if caracter.isdigit():
            contiene_numero = True
    
    return contiene_mayuscula and contiene_numero

def es_cancelacion(valor):
    return valor.strip().lower() == "cancelar"

def leer_entero(mensaje):  
    while True:
        valor = input(mensaje)
        if valor.strip().isdigit():
            return int(valor)
        print("Entrada inválida. Por favor ingrese un número entero.")

def leer_entero_valido(mensaje, ids_validos):
    while True:
        valor = leer_entero(mensaje)
        if valor in ids_validos:
            return valor
        print("ID inválido. Por favor ingrese un ID de la lista.")


class InterfazConsola:
    def __init__(self, base_datos):
        self.base_datos = base_datos
        self.conexion, self.cursorDB = self.base_datos.conectar()

    def iniciar(self):
        self.menu()

    def cerrar(self):
        self.base_datos.cerrar(self.conexion)

    def registrar_usuario(self):
        self.registrar_cuenta("usuario")

    def registrar_empleado(self):
        self.registrar_cuenta("empleado")

    def registrar_cuenta(self, tipo):
        if tipo == "usuario":
            print("[-------¡Holaaaa!, Bienvenid@ nuevo usuario a nuestra app MercadoVentas-------]")
        elif tipo == "empleado":
            print("[-------¡Holaaaa!, Bienvenid@ nuevo empleado a nuestra app MercadoVentas-------]")
        else:
            print("Tipo de cuenta inválido.")
            self.menu()
            return

        nombre = input("\nIngrese su nombre completo o escriba 'cancelar': ")
        if es_cancelacion(nombre):
            print("Registro cancelado.")
            self.menu()
            return
        
        servicio_autenticacion = ServicioAutenticacion(self.conexion)
        numero = input("Ingrese su número de teléfono o escriba 'cancelar': ").strip()
        if es_cancelacion(numero):
            print("Registro cancelado.")
            self.menu()
            return
        
        while not servicio_autenticacion.numero_valido(numero):
            print("Número inválido. Ingrese un numero de 10 dígitos.")
            numero = input("Ingrese su número de teléfono o escriba 'cancelar': ").strip()

            if es_cancelacion(numero):
                print("Registro cancelado.")
                self.menu()
                return
            
        correo = input("Ingrese su correo electrónico o escriba 'cancelar': ").strip().lower()
        if es_cancelacion(correo):
            print("Registro cancelado.")
            self.menu()
            return
        
        while not servicio_autenticacion.correo_valido(correo) or servicio_autenticacion.correo_registrado(correo):
            if not servicio_autenticacion.correo_valido(correo):
                print("Correo inválido. Intente con gmail, hotmail, outlook o culiacan.tecnm.mx")
            elif servicio_autenticacion.correo_registrado(correo):
                print("Ese correo ya está registrado. Inténtelo de nuevo.")
            correo = input("Ingrese su correo electrónico o escriba 'cancelar': ").strip().lower()
            if es_cancelacion(correo):
                print("Registro cancelado.")
                self.menu()
                return

        password = leer_contrasena_valida("Ingrese una contraseña (¡Recuérdala siempre! ;D) o escriba 'cancelar': ")
        if password is None:
            print("Registro cancelado.")
            self.menu()
            return
        
        password_confirmacion = leer_contrasena("Confirma tu contraseña o escriba 'cancelar': ")
        if es_cancelacion(password_confirmacion):
            print("Registro cancelado.")
            self.menu()
            return
        
        while password != password_confirmacion:
            print("\n¡Uups!, parece que las contraseñas no coinciden, vuelve a intentarlo\n")
            password = leer_contrasena_valida("Ingrese una contraseña (¡Recuérdala siempre! ;D) o escriba 'cancelar': ")
            if password is None:
                print("Registro cancelado.")
                self.menu()
                return
            password_confirmacion = leer_contrasena("Confirma tu contraseña o escriba 'cancelar': ")
            if es_cancelacion(password_confirmacion):
                print("Registro cancelado.")
                self.menu()
                return

        print("\n[---------- Confirmación de cuenta ----------]")
        print("Tipo de cuenta:", tipo)
        print("Nombre:", nombre)
        print("Correo:", correo)
        print("Teléfono:", numero)
        print("----------------------------------------------")

        confirmacion_cuenta = input("\n¿Desea crear esta cuenta?\n 1.- Sí\n 2.- No, cancelar\nEscriba su respuesta: ")
        if confirmacion_cuenta != "1":
            print("Registro cancelado.")
            self.menu()
            return

        if tipo == "usuario":
            servicio_autenticacion.registrar_usuario(nombre, password, correo, numero)
            print("Usuario registrado exitosamente.")
        elif tipo == "empleado":
            servicio_autenticacion.registrar_empleado(nombre, password, correo, numero)
            print("Empleado registrado exitosamente.")
        self.iniciar_sesion()

    def iniciar_sesion(self):
        servicio_autenticacion = ServicioAutenticacion(self.conexion)

        while True:
            print("\n[-------¡Holaaaa!, Bienvenid@ a nuestra app MercadoVentas-------]\n")

            correo = input("Ingrese su correo o escriba 'cancelar': ").strip().lower()
            if es_cancelacion(correo):
                print("Inicio de sesión cancelado.")
                self.menu()
                return

            password = leer_contrasena("Ingrese su contraseña o escriba 'cancelar': ")
            if es_cancelacion(password):
                print("Inicio de sesión cancelado.")
                self.menu()
                return

            tipo_usuario, nombre, usuario_id = servicio_autenticacion.iniciar_sesion(correo, password)

            if tipo_usuario == "usuario":
                self.interfaz_usuario(nombre, usuario_id)
                return

            if tipo_usuario == "empleado":
                self.interfaz_empleado(nombre, usuario_id)
                return

            print("Lo siento, los datos proporcionados no coinciden. Favor de intentarlo denuevo")

    def interfaz_usuario(self, nombre, usuario_id):
        print("\n¡Hola de nuevo", nombre[0], "!\n ¿Qué desea hacer hoy?\n 1.- Comprar producto\n 2.- Mostrar Carrito\n 3.- Salir al menú")
        opcion = input("\nEscriba su respuesta: ")

        if opcion == "1":
            self.compra(nombre, usuario_id)
        elif opcion == "2":
            self.venta(nombre, usuario_id)
        elif opcion == "3":
            print("\nSaliendo al menú...")
            self.menu()
        else:
            print("\nOpción inválida. Por favor vuelva a intentarlo")
            self.interfaz_usuario(nombre, usuario_id)

    def interfaz_empleado(self, nombre, usuario_id):
        print("\n¡Hola de nuevo", nombre[0],"!\n¿Qué desea hacer hoy?\n 1.- Gestión de inventarios\n 2.- Ver categorías\n 3.- Registro de ventas\n 4.- Salir al menú")
        opcion = input("Escriba su respuesta: ")

        if opcion == "1":
            self.inventario(nombre, usuario_id)
        elif opcion == "2":
            self.categorias(nombre, usuario_id)
        elif opcion == "3":
            self.mostrar_todas_ventas(nombre, usuario_id)
        elif opcion == "4":
            print("\nSaliendo al menú...")
            self.menu()
        else:
            print("\nOpción inválida crrrrrack, vuelve a intentarlo")

    def inventario(self, nombre, usuario_id):
        try:
            servicio_inventario = ServicioInventario(self.conexion)
            print("\n[-----------Inventario de Productos-----------]\n")
            productos = servicio_inventario.listar_productos()

            for producto in productos:
                print("ID:", producto[0])
                print("Nombre:", producto[1])
                print("Precio:", producto[2])
                print("Cantidad:", producto[3])
                print("Categoría:", producto[4])
                print("----------------------------------------------")

            opcion = input("\n 1.- Eliminar producto\n 2.- Añadir producto\n 3.- Editar producto\n 4.- Volver\n")

            if opcion == "1":
                ids_validos = [p[0] for p in productos]
                producto_id = leer_entero_valido("\nIngrese el ID del producto a eliminar:\n", ids_validos)
                servicio_inventario.eliminar_producto(producto_id)
                print("\nProducto eliminado con éxito\n")
                self.inventario(nombre, usuario_id)
            elif opcion == "2":
                producto_nombre = input("\nIngrese el nombre del producto a añadir:\n")
                precio = input("\nIngrese su precio:\n")
                unidades = input("\nIngrese la cantidad a añadir:\n")
                print("\nIngrese el ID de la categoría a la que pertenece  (ID):\n")
                categorias = servicio_inventario.listar_categorias_id_nombre()

                for categoria in categorias:
                    print("ID:", categoria[0], " NOMBRE: ", categoria[1])

                ids_validos = [c[0] for c in categorias]
                categoria_id = leer_entero_valido("\n", ids_validos)
                servicio_inventario.agregar_producto(producto_nombre, precio, unidades, categoria_id)
                print("\nProducto añadido con éxito\n")
                self.inventario(nombre, usuario_id)
            elif opcion == "3":
                ids_validos = [p[0] for p in productos]
                producto_id = leer_entero_valido("\nIngrese el ID del producto a editar:\n", ids_validos)
                actual = servicio_inventario.obtener_producto(producto_id)
                nuevo_nombre = input(f"\nNuevo nombre (actual: {actual[1]}, Enter para mantener):\n")

                if nuevo_nombre.strip() == "":
                    nuevo_nombre = actual[1]
                nuevo_precio = input(f"\nNuevo precio (actual: {actual[2]}, Enter para mantener):\n")

                if nuevo_precio.strip() == "":
                    nuevo_precio = actual[2]
                nueva_cantidad = input(f"\nNueva cantidad (actual: {actual[3]}, Enter para mantener):\n")
                
                if nueva_cantidad.strip() == "":
                    nueva_cantidad = actual[3]
                categorias = servicio_inventario.listar_categorias_id_nombre()

                for categoria in categorias:
                    print("ID:", categoria[0], " NOMBRE: ", categoria[1])

                ids_cat = [c[0] for c in categorias]
                nueva_categoria = leer_entero_valido(f"\nNuevo ID de categoría (actual: {actual[4]}):\n", ids_cat)
                servicio_inventario.actualizar_producto(producto_id, nuevo_nombre, nuevo_precio, nueva_cantidad, nueva_categoria)
                print("\nProducto actualizado con éxito\n")
                self.inventario(nombre, usuario_id)
            elif opcion == "4":
                self.interfaz_empleado(nombre, usuario_id)


            else:
                print("\nOpción inválida crrrrrack, vuelve a intentarlo")
                self.inventario(nombre, usuario_id)
        except Exception as e:
            print("Error: Conexión incorrecta con la data beis", e)

    def categorias(self, nombre, usuario_id):
        try:
            servicio_inventario = ServicioInventario(self.conexion)
            print("[-----------------Categorías-----------------]")
            categorias = servicio_inventario.listar_categorias()

            for categoria in categorias:
                print("ID:", categoria[0])
                print("Nombre:", categoria[1])
                print("Descripción:", categoria[2])
                print("----------------------------------------------")

            opcion = input("\n 1.- Eliminar categoría\n 2.- Añadir categoría\n 3.- Editar categoría\n 4.- Volver\n")

            if opcion == "1":
                ids_validos = [c[0] for c in categorias]
                categoria_id = leer_entero_valido("\nIngrese el ID de la categoría a eliminar:\n ", ids_validos)
                servicio_inventario.eliminar_categoria(categoria_id)
                print("Categoría eliminada con éxito")
                self.categorias(nombre, usuario_id)
            elif opcion == "2":
                categoria_nombre = input("\nIngrese el nombre de la categoría a añadir:\n")
                descripcion = input("\nIngrese su Descripción: \n")
                servicio_inventario.agregar_categoria(categoria_nombre, descripcion)
                print("\nCategoría añadida con éxito añadido con éxito\n")
                self.categorias(nombre, usuario_id)

            elif opcion == "3":
                ids_validos = [c[0] for c in categorias]
                categoria_id = leer_entero_valido("\nIngrese el ID de la categoría a editar:\n", ids_validos)
                actual = servicio_inventario.obtener_categoria(categoria_id)
                nuevo_nombre = input(f"\nNuevo nombre (actual: {actual[1]}, Enter para mantener):\n")

                if nuevo_nombre.strip() == "":
                    nuevo_nombre = actual[1]
                nueva_descripcion = input(f"\nNueva descripción (actual: {actual[2]}, Enter para mantener):\n")

                if nueva_descripcion.strip() == "":
                    nueva_descripcion = actual[2]
                servicio_inventario.actualizar_categoria(categoria_id, nuevo_nombre, nueva_descripcion)
                print("\nCategoría actualizada con éxito\n")
                self.categorias(nombre, usuario_id)
            elif opcion == "4":
                self.interfaz_empleado(nombre, usuario_id)



        except Exception as e:
            print("Error en la databeis:", e)

    def compra(self, nombre, usuario_id):
        try:
            servicio_compras = ServicioCompras(self.conexion)
            print("\n¿Qué te interesa hoy? He aquí nuestras secciones:\n")
            categorias = servicio_compras.listar_categorias_id_nombre()
            print("[------------CATEGORÍAS------------]")

            for categoria in categorias:
                print("______________________________________")
                print(f"ID: {categoria[0]} [", categoria[1], "]")
                print("______________________________________")

            opcion = input("\nSelecciona la categoría que más te interese: ")
            productos = servicio_compras.listar_productos_por_categoria(opcion)
            print("[-------------------------------PRODUCTOS------------------------------]")

            for producto in productos:
                print("________________________________________________________________________")
                print(f"ID: {producto[0]} [", producto[1], " ", producto[2], " ", producto[3], "]")
                print("________________________________________________________________________")

            ids_validos = [p[0] for p in productos]
            producto_id = leer_entero_valido("\nSeleccione el producto a comprar (SU ID): \n", ids_validos)
            opcion_carrito = input("\n¿Añadir al carrito?: \n 1.- Si\n 2.- No\n")

            if opcion_carrito == "1":
                unidades = leer_entero("\n¿Cuántas unidades?:\n")
                for producto in productos:
                    if producto[0] == producto_id:
                        cantidad_disponible = producto[3]
                        if unidades <= cantidad_disponible:
                            nueva_cantidad = cantidad_disponible - unidades
                            servicio_compras.agregar_al_carrito(usuario_id[0], producto_id, unidades, nueva_cantidad)
                            print("Se ha añadido al carrito.")
                        else:
                            print("\nLo siento, no hay suficiente stock para esa cantidad.\n")
                        break
            else:
                print("Operación cancelada.")
                self.compra(nombre, usuario_id)

            opcion_carrito = input("Desea seguir comprando? \n 1.- Si\n 2.- No\n")
            if opcion_carrito == "1":
                self.compra(nombre, usuario_id)
            elif opcion_carrito == "2":
                self.interfaz_usuario(nombre, usuario_id)
        except Exception as e:
            print("Error:", e)

    def venta(self, nombre, usuario_id):
        try:
            servicio_compras = ServicioCompras(self.conexion)
            servicio_ventas = ServicioVentas(self.conexion)
            print("\n[------------------Carrito de ", nombre[0], "-------------------]")
            cosas_carrito = servicio_compras.listar_carrito(usuario_id[0])

            "Condicion para verificar si el carrito está vacío"
            if not cosas_carrito:
                print("\nTu carrito está vacío. Regresando al menú principal...\n")
                self.interfaz_usuario(nombre, usuario_id)
                return
            
            "Mejorar la presentación del carrito"
            print("%-5s | %-20s | %-12s | %-10s | %-20s" % ("ID", "Producto", "Precio", "Cantidad", "Categoría"))
            print("-" * 80)
            
            for cosa in cosas_carrito:
                print("%-5s | %-20s | %-12s | %-10s | %-20s" % (cosa[0], cosa[1], str(cosa[2]), cosa[3],  cosa[4]))

            print("\nElige una opción: \n 1.- Proceder al pago\n 2.- Eliminar artículo\n 3.- Regresar\n")
            opcion = input("Escriba su respuesta: ")

            "Mejorar logica del carrito"
            if opcion == "1":
                print("-" * 80)
                print("%-20s | %-10s | %-10s | %-20s | %-10s" % ("Producto", "Categoría", "Cantidad", "Precio unitario", "Subtotal"))
                print("-" * 80)
                total = 0
                for cosa in cosas_carrito:
                    nombre_producto = cosa[1]
                    precio_unidad = cosa[2]
                    cantidad = cosa[3]
                    subtotal = precio_unidad * cantidad
                    total += subtotal
                    
                    print("%-20s | %-10s | %-10s | %-20s | %-10s" % (nombre_producto, cosa[4], str(precio_unidad), cantidad, str(subtotal)))
                print("-" * 80)
                print("Total a pagar: $", str(total))
                print("\n¿Desea proceder al pago?\n 1.- Si \n 2.- No, eliminar artículo\n")
                opcion = input("Escriba su respuesta: ")
                    
                if opcion == "1":
                    while True:
                        try:
                            pago = float(input("\nIngrese el monto a pagar: $"))
                            if pago < total:
                                print("\nMonto insuficiente. Por favor ingrese al menos $", total)
                            else:
                                break
                        except ValueError:
                            print("\nEntrada inválida. Por favor ingrese un número válido.")
                    cambio = pago - total
                    print("\n" + "-" * 25)
                    print("  RESUMEN DE PAGO")
                    print("-" * 25)
                    print("  Total:   $" + str(total))
                    print("  Pago:    $" + str(pago))
                    print("  Cambio:  $" + str(round(cambio, 2)))
                    print("-" * 25)
                    articulos_ticket = []
                    for cosa in cosas_carrito:
                        subtotal = cosa[2] * cosa[3]
                        servicio_ventas.registrar_venta(usuario_id[0], cosa[0], subtotal)
                        articulos_ticket.append((cosa[1], cosa[4], cosa[2], cosa[3], subtotal))
                        
                    archivo_ticket = generar_ticket(nombre[0], articulos_ticket, total, pago, cambio)
                    print("\nCompra realizada con éxito.")
                    print("\nTicket generado: " + archivo_ticket)
                    self.interfaz_usuario(nombre, usuario_id)
                else:
                    self.venta(nombre, usuario_id)         
            elif opcion == "2":
                ids_validos = [c[0] for c in cosas_carrito]
                articulo_id = leer_entero_valido("\nIngrese el ID del artículo a eliminar: ", ids_validos)
                servicio_compras.eliminar_articulo_carrito(usuario_id[0], articulo_id)
                print("\nArtículo eliminado del carrito correctamente.")
                self.venta(nombre, usuario_id)
            elif opcion == "3":
                self.interfaz_usuario(nombre, usuario_id)
            else:
                print("\nOpción inválida crrrrrack, vuelve a intentarlo")
                self.venta(nombre, usuario_id)
        except Exception as e:
            print("Error:", e)

    def menu(self):
        try:
            print("\n[-------¡Holaaaa!, Bienvenid@ a nuestra app MercadoVentas-------]\n")
            print(" 1.- Iniciar sesión\n 2.- Crear una cuenta\n 3.- Salir")
            opcion = input("Escriba su respuesta: ")

            if opcion == "1":
                self.iniciar_sesion()
            elif opcion == "2":
                print("\n¿Crear cuenta en el portal de empleados o en el de usuarios?\n 1.- Empleado \n 2.- Usuario")
                opcion_cuenta = input("Escriba su respuesta: ")

                if opcion_cuenta == "1":
                    self.registrar_empleado()
                elif opcion_cuenta == "2":
                    self.registrar_usuario()
                else:
                    print("\nOpción inválida, por favor vuelva a intentarlo")
                    self.menu()
            elif opcion == "3":
                print("\n¡Gracias por usar MercadoVentas. Vuelva pronto!\n")
                return
            else:
                print("\nOpción inválida, por favor vuelva a intentarlo")
                self.menu()
        except Exception as e:
            print("Error:", e)

    def mostrar_todas_ventas(self, nombre, usuario_id):
        try:
            servicio_ventas = ServicioVentas(self.conexion)
            ventas = servicio_ventas.listar_todas()

            for venta in ventas:
                print("[------------------ Todas las Ventas ------------------]")
                for venta in ventas:
                    print("ID:", venta[0])
                    print("Usuario:", venta[1])
                    print("Producto:", venta[2])
                    print("Total:", venta[3])
                    print("---------------------------------------------------------")
        except Exception as e:
            print("Error en la base de datos:", e)

        self.interfaz_empleado(nombre, usuario_id)

        

import bcrypt
import sys

from base_datos import BaseDatos
from interfaz import leer_contrasena
from repositorios import (
    RepositorioCategorias,
    RepositorioEmpleados,
    RepositorioProductos,
    RepositorioUsuarios,
)

base_datos = BaseDatos()

def register_user(cursorDB, conexion):
    print("[-------¡Holaaaa!, Bienvenid@ nuevo usuario a nuestra app MercadoVentas-------]") 
    name = input("\nIngrese su nombre completo: ")
    password = leer_contrasena("Ingrese una contraseña (¡Recuérdala siempre! ;D): ")
    passwordC = leer_contrasena("Confirma tu contraseña: ")
    while password != passwordC:
        print("\n¡Uups!, parece que las contraseñas no coinciden, vuelve a intentarlo\n")
        password = leer_contrasena("Ingrese una contraseña (¡Recuérdala siempre! ;D): ")
        passwordC = leer_contrasena("Confirma tu contraseña: ")
    pwd = password.encode('utf-8')
    encrypt1 = bcrypt.gensalt()
    contraEncriptada = bcrypt.hashpw(pwd, encrypt1)     
    mail = input("Ingrese su correo electrónico: ")
    numeroT = input("Ingrese su número de teléfono: ")
    repositorio_usuarios = RepositorioUsuarios(conexion)
    repositorio_usuarios.crear(name, contraEncriptada, mail, numeroT)
    conexion.commit()
    print("Usuario registrado exitosamente.")
    login()

def register_admin(cursorDB, conexion):
    print("[-------¡Holaaaa!, Bienvenid@ nuevo empleado a nuestra app MercadoVentas-------]")
    name = input("\nIngrese su nombre completo: ")
    password = leer_contrasena("Ingrese una contraseña (¡Recuérdala siempre! ;D): ")
    passwordC = leer_contrasena("Confirma tu contraseña: ") 
    while password != passwordC:
        print("\n¡Uups!, parece que las contraseñas no coinciden, vuelve a intentarlo\n")
        password = leer_contrasena("Ingrese una contraseña (¡Recuérdala siempre! ;D): ")
        passwordC = leer_contrasena("Confirma tu contraseña: ")    
    pwd = password.encode('utf-8')
    encrypt2 = bcrypt.gensalt()
    contraEncriptada = bcrypt.hashpw(pwd, encrypt2)    
    mail = input("Ingrese su correo electrónico: ")
    numeroT = input("Ingrese su número de teléfono: ")
    repositorio_empleados = RepositorioEmpleados(conexion)
    repositorio_empleados.crear(name, contraEncriptada, mail, numeroT)
    conexion.commit()
    print("Empleado registrado exitosamente.")
    login()

def login():
    print("\n[-------¡Holaaaa!, Bienvenid@ a nuestra app MercadoVentas-------]\n")
    mail = input("Ingrese su correo: ")
    conexion, cursorDB = base_datos.conectar()
    password = leer_contrasena("Ingrese su contraseña: ")
    repositorio_usuarios = RepositorioUsuarios(conexion)
    repositorio_empleados = RepositorioEmpleados(conexion)
    user = repositorio_usuarios.buscar_por_correo(mail) 
    if user:
        stored_password = user[2]
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            name = (user[1],)
            userID = (user[0],)
            InterfazU(name, userID, cursorDB, conexion)
            return
    empleado = repositorio_empleados.buscar_por_correo(mail)
    if empleado:
        stored_password = empleado[2]
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            name = (empleado[1],)
            userID = (empleado[0],)
            Interfaz(name, userID, cursorDB, conexion)
            return
    print("Lo siento, los datos proporcionados no coinciden, favor de intentarlo denuevo")
    base_datos.cerrar(conexion)
    login()

def InterfazU(name, userID, cursorDB, conexion):
    print("\n¡Hola de nuevo ", name[0], "!\n ¿Qué desea hacer hoy?\n 1.- Comprar producto\n 2.- Mostrar Carrito\n 3.- Salir al menú")
    opcion: str = input("Escriba su respuesta: ")
    if opcion == "1":
        compra(name, userID, cursorDB, conexion)
    elif opcion == "2":
        venta(name, userID, cursorDB, conexion)
    elif opcion == "3":
        print("\nSaliendo al menú...")
        menu()
    else:
        print("\nOpción inválida crrrrrack, vuelve a intentarlo")
        InterfazU(name, userID, cursorDB, conexion)

def Interfaz(name, userID, cursorDB, conexion):
    print("\n¡Hola de nuevo ", name[0],"!\n¿Qué desea hacer hoy?\n 1.- Gestión de inventarios\n 2.- Ver categorías\n 3.- Registro de ventas\n 4.- Salir al menú")
    opcion: str = input("Escriba su respuesta: ")
    if opcion == "1":
        Inventario(name, cursorDB, userID, conexion)
    elif opcion == "2":
        Categorias(name, userID,cursorDB, conexion)
    elif opcion == "3":
        mostrar_todas_ventas(name, userID, cursorDB, conexion)
    elif opcion == "4":
        print("\nSaliendo al menú...")
        menu()
    else:
        print("\nOpción inválida crrrrrack, vuelve a intentarlo")

def Inventario(name, cursorDB, userID, conexion):
    try:
        repositorio_productos = RepositorioProductos(conexion)
        repositorio_categorias = RepositorioCategorias(conexion)
        print("\n[-----------Inventario de Productos-----------]\n")
        productos = repositorio_productos.listar()
        for producto in productos:
            print("ID:", producto[0])
            print("Nombre:", producto[1])
            print("Precio:", producto[2])
            print("Cantidad:", producto[3])
            print("Categoría:", producto[4])
            print("----------------------------------------------")
        opcion:str = input("\n 1.- Eliminar producto\n 2.- Añadir producto\n 3.- Volver\n")
        if opcion == "1":
            select:str = input("\nIngrese el ID del producto a eliminar:\n")
            repositorio_productos.eliminar(select)
            conexion.commit()
            print("\nProducto eliminado con éxito\n")
            Inventario(name, cursorDB, userID, conexion)
        elif opcion == "2":
            nombre:str = input("\nIngrese el nombre del producto a añadir:\n")
            precio:str = input("\nIngrese su precio:\n")
            unidades:str = input("\nIngrese la cantidad a añadir:\n")
            print("\nIngrese el ID de la categoría a la que pertenece  (ID):\n")
            categorias = repositorio_categorias.listar_id_nombre()
            for categoria in categorias:
                print("ID:", categoria[0], " NOMBRE: ", categoria[1])
            id_categoria:int = int(input("\n"))
            repositorio_productos.crear(nombre, precio, unidades, id_categoria)
            conexion.commit()
            print("\nProducto añadido con éxito\n")
            Inventario(name, cursorDB, userID, conexion)
        elif opcion == "3":
            Interfaz(name, userID, cursorDB, conexion)
        else:
            print("\nOpción inválida crrrrrack, vuelve a intentarlo")
            Inventario(name, cursorDB, userID, conexion)
    except Exception as e:
        print("Error: Conexión incorrecta con la data beis", e)

def Categorias(name, userID, cursorDB, conexion):
    try:
        repositorio_categorias = RepositorioCategorias(conexion)
        print("[-----------------Categorías-----------------]")
        categorias = repositorio_categorias.listar()
        for categoria in categorias:
            print("ID:", categoria[0])
            print("Nombre:", categoria[1])
            print("Descripción:", categoria[2])
            print("----------------------------------------------")
        opcion = input("\n 1.- Eliminar categoría\n 2.- Añadir categoría\n 3.- Volver\n")
        if opcion == "1":
            select = input("\nIngrese el ID de la categoría a eliminar:\n ")
            repositorio_categorias.eliminar(select)
            conexion.commit()
            print("Categoría eliminada con éxito")
            Categorias(name, userID, cursorDB, conexion) 
        elif opcion == "2":
            nombre = input("\nIngrese el nombre de la categoría a añadir:\n")
            descripcion = input("\nIngrese su Descripción: \n")
            repositorio_categorias.crear(nombre, descripcion)
            conexion.commit()
            print("\nCategoría añadida con éxito añadido con éxito\n")
            Categorias(name, userID, cursorDB, conexion)  
        elif opcion == "3":
            Interfaz(name, userID, cursorDB, conexion,)  
            print("\nOpción inválida crrrrrack, vuelve a intentarlo")
    except Exception as e:
        print("Error en la databeis:", e)

def compra(name, userID, cursorDB, conexion):
    try:
        repositorio_categorias = RepositorioCategorias(conexion)
        repositorio_productos = RepositorioProductos(conexion)
        print("\n¿Qué te interesa hoy? He aquí nuestras secciones:\n")
        categorias = repositorio_categorias.listar_id_nombre()
        print("[------------CATEGORÍAS------------]")
        for categoria in categorias:
            print("______________________________________")
            print(f"ID: {categoria[0]} [",categoria[1],"]")
            print("______________________________________")
        opcion = input("\nSelecciona la categoría que más te interese: ")
        productos = repositorio_productos.listar_por_categoria(opcion)
        print("[-------------------------------PRODUCTOS------------------------------]")
        for producto in productos:  
            print("________________________________________________________________________")
            print(f"ID: {producto[0]} [",producto[1]," ",producto[2]," ",producto[3],"]")
            print("________________________________________________________________________")
        opcion2:int = int(input("\nSeleccione el producto a comprar (SU ID): \n"))
        opcion3 = input("\n¿Añadir al carrito?: \n 1.- Si\n 2.- No\n")
        if opcion3 == "1":
            unidades = int(input("\n¿Cuántas unidades?:\n"))
            for producto in productos:
                 if producto[0] == opcion2:
                        cantidad_disponible = producto[3]
                        if unidades <= cantidad_disponible:
                            nueva_cantidad = cantidad_disponible - unidades
                            cursorDB.execute("INSERT INTO Carrito_Compras VALUES (?,?,?,?)", [None, userID[0], opcion2, unidades])
                            cursorDB.execute("UPDATE PRODUCTOS SET CANTIDAD = ? WHERE ID = ?", (nueva_cantidad, opcion2))
                            conexion.commit()
                            print("Se ha añadido al carrito.")
                        else:
                            print("\nLo siento, no hay suficiente stock para esa cantidad.\n")
                        break
        else:
            print("Operación cancelada.")
            compra(name, userID, cursorDB, conexion)
        opcion3 = input("Desea seguir comprando? \n 1.- Si\n 2.- No\n")
        if opcion3 == "1":
            compra(name, userID, cursorDB, conexion)
        elif opcion3 == "2":
            InterfazU(name, userID, cursorDB, conexion)
    except Exception as e:
        print("Error:", e)
        
def venta(name, userID, cursorDB, conexion):
    try:
        print("[---------Carrito de ", name[0],"----------]")
        cursorDB.execute("""
            SELECT Carrito_Compras.ID, PRODUCTOS.NOMBRE_ARTICULO, PRODUCTOS.PRECIO, Carrito_Compras.CANTIDAD, CATEGORIA.NOMBRE
            FROM Carrito_Compras
            INNER JOIN PRODUCTOS ON Carrito_Compras.PRODUCTO_ID = PRODUCTOS.ID
            INNER JOIN CATEGORIA ON PRODUCTOS.CATEGORIA_ID = CATEGORIA.ID
            WHERE Carrito_Compras.USER_ID = ?
            """, (userID[0],)) 
        cosas_carrito = cursorDB.fetchall()
        for cosa in cosas_carrito:
            print("ID: ", cosa[0], "Producto:", cosa[1], "Categoría:", cosa[4])
        opcion:str = input("\n 1.- Proceder al pago\n 2.- Eliminar artículo\n 3.- Regresar\n")
        if opcion == "1":
            total = 0
            for cosa in cosas_carrito:
                nombre_producto = cosa[1]
                precio_unidad = cosa[2]
                cantidad = cosa[3]
                subtotal = precio_unidad * cantidad
                total += subtotal
                print("Producto:", nombre_producto, "Categoría:", cosa[3], "Cantidad:", cantidad, "Precio unitario:", precio_unidad, "Subtotal:", subtotal)
        elif opcion == "2":
            id_articulo = input("\nIngrese el ID del artículo a eliminar: ")
            cursorDB.execute("DELETE FROM Carrito_Compras WHERE USER_ID = ? AND ID = ?", (userID[0], id_articulo))
            conexion.commit()
            print("\nArtículo eliminado del carrito correctamente.")
            venta(name, userID, cursorDB, conexion)
        elif opcion == "3":
            InterfazU(name, userID, cursorDB, conexion)
        else:
            print("\nOpción inválida crrrrrack, vuelve a intentarlo")
            venta(name, userID, cursorDB, conexion)
        print("\nTotal a pagar:", total)
        opcion:str = input("\n¿Desea continuar?\n 1.- Si \n 2.- Regresar\n")
        if opcion == "1":
            cursorDB.execute("DELETE FROM Carrito_Compras WHERE USER_ID = ?", (userID))
            cursorDB.execute("INSERT INTO VENTAS VALUES (?,?,?,?)", (None, userID[0], cosa[0], subtotal))
            conexion.commit()
            print("\nCompra realizada con éxito. Pronto llegará a tu casa porque sé dónde vives guap@\n")
            InterfazU(name, userID, cursorDB, conexion)
    except Exception as e:
        print("Error:", e)

def menu():
    try:
        print("\n[-------¡Holaaaa!, Bienvenid@ a nuestra app MercadoVentas-------]\n")
        print(" 1.- Iniciar sesión\n 2.- Crear una cuenta\n 3.- Salir")
        opcion: str = input("Escriba su respuesta: ")
        if opcion == "1":
            login()
        elif opcion == "2":
            print("\n¿Crear cuenta en el portal de empleados o en el de usuarios?\n 1.- Empleado \n 2.- Usuario")
            opcion1:str = input("Escriba su respuesta: ")
            if opcion1 == "1":
                register_admin(cursorDB, conexion)
            elif opcion1 == "2":
                register_user(cursorDB, conexion)
            else:
                print("\nOpción inválida crrrrrack, vuelve a intentarlo")
                menu()
        elif opcion == "3":
            sys.exit()
        else:
           print("\nOpción inválida crrrrrack, vuelve a intentarlo")
           menu() 
    except Exception as e:
        print("Error:", e)

def mostrar_todas_ventas(name, userID, cursorDB, conexion):
    try:
        cursorDB.execute("""
            SELECT VENTAS.ID, USUARIOS.NOMBRE, PRODUCTOS.NOMBRE_ARTICULO, VENTAS.TOTAL FROM VENTAS
            INNER JOIN USUARIOS ON VENTAS.USUARIO_ID = USUARIOS.ID
            INNER JOIN PRODUCTOS ON VENTAS.PRODUCTO_ID = PRODUCTOS.ID
        """)
        ventas = cursorDB.fetchall()

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
    Interfaz(name, userID, cursorDB, conexion)
conexion, cursorDB = base_datos.conectar()
menu()
base_datos.cerrar(conexion)

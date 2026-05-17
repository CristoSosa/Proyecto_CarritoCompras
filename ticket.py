from datetime import datetime
import os


def generar_ticket(nombre_cliente, articulos, total, pago, cambio):
    """
    Genera un ticket de compra en formato TXT.
    
    articulos: lista de tuplas (nombre_producto, categoria, precio_unidad, cantidad, subtotal)
    """
    fecha = datetime.now()
    fecha_texto = fecha.strftime("%d/%m/%Y %H:%M:%S")
    carpeta = "tickets"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    nombre_limpio = nombre_cliente.replace(" ", "_")
    nombre_archivo = os.path.join(carpeta, nombre_limpio + "_" + fecha.strftime("%d-%m-%Y_%H-%M") + ".txt")

    lineas = []
    lineas.append("=" * 50)
    lineas.append("                  MERCADOVENTAS")
    lineas.append("               TICKET DE COMPRA")
    lineas.append("=" * 50)
    lineas.append("Cliente: " + nombre_cliente)
    lineas.append("Fecha:   " + fecha_texto)
    lineas.append("-" * 50)
    lineas.append("%-20s %5s %10s %10s" % ("Producto", "Cant", "Precio", "Subtotal"))
    lineas.append("-" * 50)

    for articulo in articulos:
        nombre = articulo[0]
        cantidad = articulo[3]
        precio = articulo[2]
        subtotal = articulo[4]
        lineas.append("%-20s %5s %10s %10s" % (nombre, str(cantidad), "$" + str(precio), "$" + str(subtotal)))

    lineas.append("-" * 50)
    lineas.append("%37s %10s" % ("TOTAL:", "$" + str(total)))
    lineas.append("%37s %10s" % ("Pago:", "$" + str(pago)))
    lineas.append("%37s %10s" % ("CAMBIO:", "$" + str(round(cambio, 2))))
    lineas.append("=" * 50)
    lineas.append("Gracias por su compra!")
    lineas.append("Vuelva pronto")
    lineas.append("=" * 50)

    contenido = "\n".join(lineas)

    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)

    return nombre_archivo

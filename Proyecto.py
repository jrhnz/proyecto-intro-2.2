import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="6666",
    database="prueba"
)

cursor = conexion.cursor()

cursor.execute("SELECT id, nombre FROM categorias")
categorias = {row[0]: row[1] for row in cursor.fetchall()}

def obtener_positivo(mensaje, tipo="float"):
    while True:
        try:
            valor = float(input(mensaje)) if tipo == "float" else int(input(mensaje))
            if valor < 0:
                print("No puede ser negativo")
                continue
            return valor
        except ValueError:
            print("Ingrese un valor válido")

def seleccionar_categoria():
    print("\n--- CATEGORÍAS DISPONIBLES ---")
    for clave, nombre in categorias.items():
        print(f"{clave}. {nombre}")
    
    while True:
        opcion = input("Seleccione una categoría: ")
        try:
            opcion_int = int(opcion)
            if opcion_int in categorias:
                return opcion_int
            print("Categoría no válida. Intente de nuevo")
        except ValueError:
            print("Ingrese un número válido")

def mostrar_producto(producto):
    print(f"ID: {producto[0]} | Nombre: {producto[1]} | Categoría: {producto[4]}")
    print(f"Precio: ${producto[2]:.2f} | Cantidad: {producto[3]} unidades")
    print("-" * 60)

ejecutar = True
intentos_fallidos = 0

while ejecutar:
    print("\n--- MENÚ ---")
    print("1. Registrar producto")
    print("2. Mostrar inventario")
    print("3. Buscar producto")
    print("4. Productos agotados")
    print("5. Resumen general")
    print("6. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        nombre = input("Ingrese el nombre del producto: ")
        precio = obtener_positivo("Ingrese el precio: ", "float")
        cantidad = obtener_positivo("Ingrese la cantidad: ", "int")
        categoria_id = seleccionar_categoria()

        cursor.execute("""
            INSERT INTO productos (nombre, precio, cantidad, categoria_id)
            VALUES (%s, %s, %s, %s)
        """, (nombre, precio, cantidad, categoria_id))

        conexion.commit()
        print("Producto registrado correctamente")
        input("Presione enter para regresar al menu")
        
    elif opcion == "2":
        cursor.execute("""
            SELECT p.id, p.nombre, p.precio, p.cantidad, c.nombre
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
        """)
        productos = cursor.fetchall()

        if len(productos) == 0:
            print("No hay productos registrados")
        else:
            print("\n--- INVENTARIO COMPLETO ---")
            print(f"Total de productos: {len(productos)}")
            print("=" * 60)
            for producto in productos:
                mostrar_producto(producto)
        input("Presione enter para regresar al menu")

    elif opcion == "3":
        buscar = input("Ingrese el nombre del producto: ")
        cursor.execute("""
            SELECT p.id, p.nombre, p.precio, p.cantidad, c.nombre
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.nombre = %s
        """, (buscar,))
        producto = cursor.fetchone()

        if producto:
            print("\nProducto encontrado:")
            mostrar_producto(producto)
        else:
            print("Producto no encontrado")
        input("Presione enter para regresar al menu")

    elif opcion == "4":
        cursor.execute("""
            SELECT p.id, p.nombre, p.precio, p.cantidad, c.nombre
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.cantidad = 0
        """)
        productos = cursor.fetchall()

        if len(productos) == 0:
            print("No hay productos agotados")
        else:
            print("\n--- PRODUCTOS AGOTADOS ---")
            for producto in productos:
                mostrar_producto(producto)
        input("Presione enter para regresar al menu")

    elif opcion == "5":
        cursor.execute("""
            SELECT p.id, p.nombre, p.precio, p.cantidad, c.nombre
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
        """)
        productos = cursor.fetchall()
        total_productos = len(productos)
        valor_total = sum(p[2] * p[3] for p in productos)

        print("\n--- RESUMEN GENERAL ---")
        print(f"Cantidad de productos registrados: {total_productos}")
        print(f"Valor total del inventario: ${valor_total:.2f}")
        input("Presione enter para regresar al menu")

    elif opcion == "6":
        print("Saliendo del programa...")
        conexion.close()
        ejecutar = False
    else:
        intentos_fallidos += 1
        intentos_restantes = 3 - intentos_fallidos
        if intentos_fallidos < 3:
            print(f"Opción no válida. Intentos restantes: {intentos_restantes}")
        else:
            print("Ha agotado sus 3 intentos. El programa se cerrará.")
            conexion.close()
            ejecutar = False
        input("Presione enter para regresar al menu")
        
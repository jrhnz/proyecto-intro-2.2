import mysql.connector
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="6666",
    database="prueba"
)

cursor = conexion.cursor()

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

        precio = float(input("Ingrese el precio: "))

        while precio < 0:
            print("El precio no puede ser negativo")
            precio = float(input("Ingrese nuevamente el precio: "))

        cantidad = int(input("Ingrese la cantidad: "))

        while cantidad < 0:
            print("La cantidad no puede ser negativa")
            cantidad = int(input("Ingrese nuevamente la cantidad: "))
        cursor.execute("""

        INSERT INTO productos (nombre, precio, cantidad)
        VALUES (%s, %s, %s)

        """, (nombre, precio, cantidad))

        conexion.commit()

        print("Producto registrado correctamente")
        input("Presione enter para regresar al menu")
        
    elif opcion == "2":

        cursor.execute("SELECT * FROM productos")

        productos = cursor.fetchall()

        if len(productos) == 0:
            print("No hay productos registrados")
            input("Presione enter para regresar al menu")

        else:

            print("\n--- INVENTARIO COMPLETO ---")
            print("Total de productos: ", len(productos))
            print("=" * 50)
            for producto in productos:

                print(f"ID: {producto[0]}")
                print(f"Nombre: {producto[1]}")
                print(f"Precio: ${producto[2]:.2f}")
                print(f"Cantidad: {producto[3]} unidades")
                print("-" * 50)
            input("Presione enter para regresar al menu")
                
    elif opcion == "3":

        buscar = input("Ingrese el nombre del producto: ")

        cursor.execute("""

        SELECT * FROM productos
        WHERE nombre = %s

        """, (buscar,))

        producto = cursor.fetchone()

        if producto:

            print("\nProducto encontrado")

            print("ID:", producto[0])
            print("Nombre:", producto[1])
            print("Precio:", producto[2])
            print("Cantidad:", producto[3])
            input("Presione enter para regresar al menu")

        else:
            print("Producto no encontrado")
            input("Presione enter para regresar al menu")
            
    elif opcion == "4":

        cursor.execute("""

        SELECT * FROM productos
        WHERE cantidad = 0

        """)

        productos = cursor.fetchall()

        if len(productos) == 0:
            print("No hay productos agotados")
            input("Presione enter para regresar al menu")
        else:
            print("\n--- PRODUCTOS AGOTADOS ---")
            for producto in productos:
                print("ID:", producto[0])
                print("Nombre:", producto[1])
                print("Precio:", producto[2])
                print("----------------------")
            input("Presione enter para regresar al menu")
                
    elif opcion == "5":
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        total_productos = len(productos)
        valor_total = 0
        for producto in productos:
            precio = producto[2]
            cantidad = producto[3]
            valor_total += precio * cantidad
        print("\n--- RESUMEN GENERAL ---")
        print("Cantidad de productos registrados:", total_productos)
        print("Valor total del inventario:", valor_total)
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
            input("Presione enter para regresar al menu")
        else:
            print("Ha agotado sus 3 intentos. El programa se cerrará.")
            conexion.close()
            ejecutar = False

import mysql.connector
 
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="6666",
    database="prueba"
)
cursor = conexion.cursor()
 
 
def obtener_positivo(mensaje, tipo="float"):
    """Solicita un número no negativo del tipo indicado."""
    while True:
        try:
            valor = float(input(mensaje)) if tipo == "float" else int(input(mensaje))
            if valor < 0:
                print("El valor no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print("Ingrese un valor válido.")
 
 
def mostrar_producto(p):
    """Imprime un producto con formato.
    Columnas esperadas: id, nombre, precio, cantidad
    """
    print(f"ID: {p[0]} | Nombre: {p[1]}")
    print(f"Precio: Q{p[2]:.2f} | Cantidad: {p[3]} unidades")
    print("-" * 60)
 
 
QUERY_INVENTARIO = """
    SELECT p.id, p.nombre, p.precio, i.cantidad
    FROM   productos  p
    LEFT JOIN inventario i ON p.id = i.producto_id
"""
 
intentos_fallidos = 0
 
while True:
    print("\n========== MENÚ ==========")
    print("1. Registrar producto")
    print("2. Mostrar inventario")
    print("3. Buscar producto")
    print("4. Productos agotados")
    print("5. Resumen general")
    print("6. Salir")
    opcion = input("Seleccione una opción: ").strip()
 
    if opcion == "1":
        nombre   = input("Nombre del producto: ").strip()
        precio   = obtener_positivo("Precio: ", "float")
        cantidad = obtener_positivo("Cantidad: ", "int")
 
        cursor.execute(
            "INSERT INTO productos (nombre, precio) VALUES (%s, %s)",
            (nombre, precio)
        )
        producto_id = cursor.lastrowid
 
        cursor.execute(
            "INSERT INTO inventario (producto_id, cantidad) VALUES (%s, %s)",
            (producto_id, cantidad)
        )
        conexion.commit()
        print("Producto registrado correctamente.")
        intentos_fallidos = 0
 
    elif opcion == "2":
        cursor.execute(QUERY_INVENTARIO)
        productos = cursor.fetchall()
        if not productos:
            print("No hay productos registrados.")
        else:
            print(f"\n--- INVENTARIO COMPLETO  ({len(productos)} producto(s)) ---")
            print("=" * 60)
            for p in productos:
                mostrar_producto(p)
        intentos_fallidos = 0
 
    elif opcion == "3":
        buscar = input("Nombre del producto: ").strip()
        cursor.execute(QUERY_INVENTARIO + " WHERE p.nombre LIKE %s", (f"%{buscar}%",))
        resultados = cursor.fetchall()
        if resultados:
            print(f"\n{len(resultados)} resultado(s) encontrado(s):")
            for p in resultados:
                mostrar_producto(p)
        else:
            print("No se encontró ningún producto con ese nombre.")
        intentos_fallidos = 0
 
    elif opcion == "4":
        cursor.execute(QUERY_INVENTARIO + " WHERE i.cantidad = 0")
        productos = cursor.fetchall()
        if not productos:
            print("No hay productos agotados.")
        else:
            print(f"\n--- PRODUCTOS AGOTADOS ({len(productos)}) ---")
            for p in productos:
                mostrar_producto(p)
        intentos_fallidos = 0
 
    elif opcion == "5":
        cursor.execute(QUERY_INVENTARIO)
        productos = cursor.fetchall()
 
        total_productos = len(productos)
        valor_total     = sum(p[2] * p[3] for p in productos)
        total_unidades  = sum(p[3] for p in productos)
        agotados        = sum(1 for p in productos if p[3] == 0)
 
        print("\n--- RESUMEN GENERAL ---")
        print(f"  Productos registrados : {total_productos}")
        print(f"  Unidades en inventario: {total_unidades}")
        print(f"  Productos agotados    : {agotados}")
        print(f"  Valor total inventario: Q{valor_total:.2f}")
        intentos_fallidos = 0
 
    elif opcion == "6":
        print("Cerrando el programa.")
        cursor.close()
        conexion.close()
        break
 
    else:
        intentos_fallidos += 1
        restantes = 3 - intentos_fallidos
        if restantes > 0:
            print(f"Opción no válida. Intentos restantes: {restantes}.")
        else:
            print("Ha agotado sus 3 intentos. El programa se cerrará.")
            cursor.close()
            conexion.close()
            break
 
    input("\nPresione Enter para volver al menú")

usuarios = {
    "username": "jmarquezco@unal.edu.co",
    "password": "juaneselmejor"
}

def iniciar_sesion():
    print("\n=== INICIO DE SESIÓN ===")
    usuario = input("Ingrese el Usuario: ")
    contraseña = input("Ingrese la Contraseña: ")

    if usuario == usuarios["username"] and contraseña == usuarios["password"]:
        mostrar_menu_opciones()
    else:
        print("❌ Contraseña y/o usuario incorrecto, vuelve a intentar")
        iniciar_sesion()  

def mostrar_menu_opciones():
    while True:
        print("\n=== MENÚ DE OPCIONES ===")
        print("1. Opción uno")
        print("2. Opción dos")
        print("3. Opción tres")
        print("4. Opción cuatro")
        print("5. Opción cinco")
        print("6. Opción seis")
        print("7. Cerrar sesión")
        opcion = input("Elija una opción (1-7): ")

        match opcion:
            case "1":
                print("✔ Has seleccionado la primera opción")
            case "2":
                print("✔ Has seleccionado la segunda opción")
            case "3":
                print("✔ Has seleccionado la tercera opción")
            case "4":
                print("✔ Has seleccionado la cuarta opción")
            case "5":
                print("✔ Has seleccionado la quinta opción")
            case "6":
                print("✔ Has seleccionado la sexta opción")
            case "7":
                print("👋 Cerrando sesión..."); iniciar_sesion()
                break
            case _:
                print("❌ Opción incorrecta, intenta de nuevo")

iniciar_sesion()

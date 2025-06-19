usuarios= {
    "username": "juaneselmejor",
    "password": "Holacomoesta"
}

def iniciar_sesion():
 print("===Inicio de sesion===")
 print("Ingrese el Usuario: ")
 usuario = input(str)
 print("Ingrese la contraseña")
 contraseña = input(str)

 if usuario == "juaneselmejor" and contraseña == "Holacomoesta":
     print("===Menu de opciones===")
     print("1.")
     print("2.")
     print("3.")
     print("4.")
     print("5.")
     print("6.")
     print("Elija una de las opciones anteriores")
     opcion = input(int)
     match opcion:
        case "1": print("Haz seleccionado la primera opcion")
        case "2": print("Haz seleccionado la segunda opcion")
        case "3": print("Haz seleccionado la tercera opcion")
        case "4": print("Haz seleccionado la cuarta opcion")
        case "5": print("Haz seleccionado la quinta opcion")
        case "6": print("Haz seleccionado la sexta opcion")
        case _ : print("Opcion incorrecta")
 else: print("Contraseña y/o usuario incorrecto ")
 
iniciar_sesion()
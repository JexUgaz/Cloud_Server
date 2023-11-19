import inquirer

def AgregarUsuario():
    print("Ha selecionado la opción de: Agregar Usuario")
    # Capturar datos del usuario
    nombre = input("Ingrese el nombre del usuario: ")
    correo = input("Ingrese su correo: ")
    codigo_pucp = input("Ingrese su codigo PUCP: ")
    contraseña = input("Ingrese su contraseña: ")

def showMenuAdministrador():
    opciones = [
        inquirer.List("opcion",
                      message="Bienvenido Administrador, escoja la opción que desea hacer: ",
                      choices=[
                          ("Usuarios", "Usuarios"),
                          ("Imagenes", "Imagenes"),
                          ("Slices", "Slices"),
                          ("Alertas", "Alertas"),
                          ("Monitoreo - Listar recursos", "Monitoreo- Listar recursos"),
                          ("Salir", "Salir"),
                      ])
    ]
    respuestas = inquirer.prompt(opciones)
    seleccion = respuestas["opcion"]
    
    if seleccion == "Salir":
        print("Saliendo del programa.")
    else:
        print("Ha seleccionado " + seleccion)


def AdministradorUsuarios():
    opciones = [
        inquirer.List("opcion",
                      choices=[
                          ("Listar Usuario", "Listar Usuario"),
                          ("Agregar Usuario", "Agregar Usuario"),
                          ("Eliminar Usuario", "Eliminar Usuario"),
                          ("Volver", "Volver"),
                      ])
    ]
    respuestas = inquirer.prompt(opciones)
    seleccion = respuestas["opcion"]
    
    if seleccion == "Salir":
        print("Saliendo del programa.")
    else:
        print("Ha seleccionado " + seleccion)



def AdministradorImagenes():
    opciones = [
        inquirer.List("opcion",
                      choices=[
                          ("Listar imagenes", "Listar imagenes"),
                          ("Agregar imagenes", "Agregar imagenes"),
                          ("Eliminar imagenes", "Eliminar imagenes"),
                          ("Volver", "Volver"),
                      ])
    ]
    respuestas = inquirer.prompt(opciones)
    seleccion = respuestas["opcion"]
    
    if seleccion == "Salir":
        print("Saliendo del programa.")
    else:
        print("Ha seleccionado " + seleccion)


def AdministradorSlices():
    opciones = [
        inquirer.List("opcion",
                      choices=[
                          ("Listar slices", "Listar slices"),
                          ("Eliminar slices", "Eliminar slices"),
                          ("Volver", "Volver"),
                      ])
    ]
    respuestas = inquirer.prompt(opciones)
    seleccion = respuestas["opcion"]
    
    if seleccion == "Salir":
        print("Saliendo del programa.")
    else:
        print("Ha seleccionado " + seleccion)

def AdministradorAlertas():
    opciones = [
        inquirer.List("opcion",
                    message="Bienvenido Administrador, escoja el servidor del que quiera ver su alerta: ",
                    choices=[
                        ("Worker 1", "Worker 1"),
                        ("Worker 2", "Worker 2"),
                        ("Worker 3", "Worker 3"),
                        ("Volver", "Volver"),
                    ])
    ]
    respuestas = inquirer.prompt(opciones)
    seleccion = respuestas["opcion"]
    
    if seleccion == "Salir":
        print("Saliendo del programa.")
    else:
        print("Ha seleccionado " + seleccion)




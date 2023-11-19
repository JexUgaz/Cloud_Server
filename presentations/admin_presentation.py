import inquirer
from config.helpers import clearScreen, printWaiting, setBarra, setListOptionsShell
from entities.UserEntity import UserEntity

def AgregarUsuario():
    print("Ha selecionado la opción de: Agregar Usuario")
    # Capturar datos del usuario
    nombre = input("Ingrese el nombre del usuario: ")
    correo = input("Ingrese su correo: ")
    codigo_pucp = input("Ingrese su codigo PUCP: ")
    contraseña = input("Ingrese su contraseña: ")

def showMenuAdministrador(user:UserEntity):
    salir=False
    while not salir:
        clearScreen()
        setBarra(text=f"Bienvenido Administrador, {user.nombre}!",enter=True)
        choices=[
            "Usuarios",
            "Imagenes",
            "Slices",
            "Alertas",
            "Monitoreo - Listar recursos",
            "Cerrar Sesión"
        ]
        seleccion = setListOptionsShell(
            message="Seleccione una opción: ",
            choices=choices
        ) 
        
        if seleccion == choices[len(choices)-1]:
            salir=True
        elif seleccion==choices[0]:
            AdministradorUsuarios()
        elif seleccion==choices[1]:
            AdministradorImagenes()
        elif seleccion==choices[2]:
            AdministradorSlices()
        elif seleccion==choices[3]:
            AdministradorAlertas()
        elif seleccion==choices[4]:
            printWaiting(f"Selección: {seleccion}")

def AdministradorUsuarios():
    while True:
        clearScreen()
        setBarra(text="Opciones sobre los usuarios",enter=True)
        choices=[
                "Listar Usuario",
                "Agregar Usuario",
                "Eliminar Usuario",
                "Volver"
        ]
        seleccion=setListOptionsShell(
            message="Opción",
            choices=choices
        )
        
        if seleccion == choices[len(choices)-1]:
            break



def AdministradorImagenes():
    while True:
        clearScreen()
        setBarra(text="Opciones sobre las imágenes",enter=True)
        choices=[
                "Listar imagenes",
                "Agregar imagenes",
                "Eliminar imagenes",
                "Volver"
        ]
        seleccion=setListOptionsShell(
            message="Opción",
            choices=choices
        )
        if seleccion == choices[len(choices)-1]:
            break

def AdministradorSlices():
    while True:
        clearScreen()   
        setBarra(text="Opciones sobre los slices",enter=True)
        choices=[
                "Listar slices",
                "Eliminar slices",
                "Volver"
        ]
        seleccion=setListOptionsShell(
            message="Opción",
            choices=choices
        )
        if seleccion == choices[len(choices)-1]:
            break

def AdministradorAlertas():
    while True:
        clearScreen()   
        setBarra(text="Seleccione el servidor para ver sus alertas: ",enter=True)
        choices=[
                "Worker 1",
                "Worker 2",
                "Worker 3",
                "Volver"
        ]
        seleccion=setListOptionsShell(
            message="Opción",
            choices=choices
        )
        if seleccion == choices[len(choices)-1]:
            break




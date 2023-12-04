import inquirer
import tabulate
from config.helpers import clearScreen, printWaiting, setBarra, setListOptionsShell, setTitle
from entities.UserEntity import UserEntity
from services.admin_services import get_all_users

def AgregarUsuario():
    print("Ha selecionado la opción de: Agregar Usuario")
    # Capturar datos del usuario
    nombre = input("Ingrese el nombre del usuario: ")
    correo = input("Ingrese su correo: ")
    codigo_pucp = input("Ingrese su codigo PUCP: ")
    contraseña = input("Ingrese su contraseña: ")

def showMenuAdministrador(user:UserEntity):
    while True:
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
            break
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
                "Listar Usuarios",
                "Agregar Usuario",
                "Bloquear Usuario",
                "Volver"
        ]
        seleccion=setListOptionsShell(
            message="Opción",
            choices=choices
        )
        
        if seleccion == choices[len(choices)-1]:
            break
        elif seleccion==choices[0]:
            clearScreen()
            setTitle("Lista de Usuarios")
            usuarios=get_all_users()
            listas_usuarios = [usuario.to_list() for usuario in usuarios]
            headers=["id","nombre","email"]
            printWaiting(tabulate.tabulate(listas_usuarios, headers, tablefmt="fancy_grid"))


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




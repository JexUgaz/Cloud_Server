import msvcrt
import tabulate
from prettytable import PrettyTable
from config.helpers import clearScreen, printWaiting, setBarra, setListOptionsShell, setTitle
from entities.UserEntity import UserEntity
from services.admin_services import get_all_users, get_monitoreo_recursos
from services.connection_functions import monitorear_asignacion_recursos

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
            "Monitoreo - Asignacion de recursos",
            "Monitoreo - Uso de recursos",
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
            monitorear_asignacion_recursos()
            print("\nPresione una tecla para continuar...")
            msvcrt.getch()
        elif seleccion==choices[5]:
            monitorear_uso_recursos()
        elif seleccion==choices[6]:
            printWaiting(f"Selección: {seleccion}")

def monitorear_uso_recursos():
    memoria_workers,uso_sistema_workers=get_monitoreo_recursos()
    clearScreen()
    setBarra(text="TABLA DE MONITOREO DE RECURSOS",enter=True)
    # Tabla consolidada para la memoria de cada worker
    tabla_memoria_consolidada = PrettyTable()
    tabla_memoria_consolidada.field_names = ["Worker", "Memoria Total (KB)", "Memoria Usada (KB)", "Memoria Libre (KB)"]

    # Tabla consolidada para el uso del sistema de cada worker
    tabla_uso_sistema_consolidado = PrettyTable()
    tabla_uso_sistema_consolidado.field_names = ["Worker", "Porcentaje Sistema Usado", "Porcentaje Sistema No Usado", "Cores Usados", "Tiempo de Espera"]
    
    for memoria in memoria_workers:
        tabla_memoria_consolidada.add_row(memoria)
    for uso_sistema in uso_sistema_workers:
        tabla_uso_sistema_consolidado.add_row(uso_sistema)
    print(tabla_memoria_consolidada)
    printWaiting(tabla_uso_sistema_consolidado)

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




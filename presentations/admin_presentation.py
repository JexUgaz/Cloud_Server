import tabulate
from config.globals import RolesGlobal
from presentations.user_presentation import showMenuUser
from prettytable import PrettyTable
from config.helpers import clearScreen, printWaiting, setBarra, setListOptionsShell, setTitle
from entities.UserEntity import UserEntity
from services.admin_services import get_all_images, get_all_slices, get_all_users, get_monitoreo_recursos, set_new_user,get_all_subredes,set_new_subredes
from services.connection_functions import monitorear_asignacion_recursos

_usuario_global=None

def showMenuAdministrador(user:UserEntity):
    global _usuario_global
    _usuario_global=user
    while True:
        clearScreen()
        setBarra(text=f"Bienvenido Administrador, {user.nombre}!",enter=True)
        choices=[
            "Ingresar como usuario",
            "Usuarios",
            "Imagenes",
            "Slices",
            "Alertas",
            "Monitoreo - Asignacion de recursos",
            "Monitoreo - Uso de recursos",
            "Subredes",
            "Cerrar Sesión"
        ]
        seleccion = setListOptionsShell(
            message="Seleccione una opción: ",
            choices=choices
        ) 
        
        if seleccion == choices[len(choices)-1]:
            break
        elif seleccion==choices[1]:
            AdministradorUsuarios()
        elif seleccion==choices[2]:
            AdministradorImagenes()
        elif seleccion==choices[3]:
            AdministradorSlices()
        elif seleccion==choices[4]:
            AdministradorAlertas()
        elif seleccion==choices[5]:
            monitorear_asignacion_recursos()
            printWaiting("\nPresione una tecla para continuar...")
        elif seleccion==choices[6]:
            monitorear_uso_recursos()
        elif seleccion==choices[7]:
            AdministradorSubredes()
        elif seleccion==choices[0]:
            showMenuUser(user=user)

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

def AdministradorSubredes():
    while True:
        clearScreen()
        setBarra(text="Opciones sobre las subredes",enter=True)
        choices=[
                "Añadir Subredes",
                "Listar Subredes",
                "Volver"
        ]
        seleccion=setListOptionsShell(
            message="Opción",
            choices=choices
        )

        if seleccion == choices[len(choices)-1]:
            break
        elif seleccion==choices[0]:
            anadirSubredesAdmin()
        elif seleccion==choices[1]:
            listarSubredesAdmin()

def anadirSubredesAdmin():
    result=input("¿Seguro de que quiere añadir más subredes? (Y/N): ")
    if result.lower()=="y":
        clearScreen()
        setTitle("Añadiendo nuevas subredes")
        set_new_subredes()
        printWaiting("Se añadieron más subredes exitosamente!")

def listarSubredesAdmin():
    clearScreen()
    setTitle("Todas las subredes")
    subredes=get_all_subredes()
    listas_subredes = [[subred[0],subred[1],subred[2]] for subred in subredes]
    headers=["ID","Dirección","Activo"]
    printWaiting(tabulate.tabulate(listas_subredes, headers, tablefmt="fancy_grid"))
    
def AdministradorUsuarios():
    while True:
        clearScreen()
        setBarra(text="Opciones sobre los usuarios",enter=True)
        choices=[
                "Listar Usuarios",
                "Agregar Usuario",
                "Volver"
        ]
        seleccion=setListOptionsShell(
            message="Opción",
            choices=choices
        )
        
        if seleccion == choices[len(choices)-1]:
            break
        elif seleccion==choices[0]:
            listarUsuariosAdmin()
        elif seleccion==choices[1]:
            addUsuariosAdmin()

def addUsuariosAdmin():
    clearScreen()
    setTitle("Agregar Usuarios")
    nombre=input("Ingrese el nombre del nuevo usuario: ")
    if(len(nombre)==0):
        printWaiting("Incorrecto!")
        return
    
    email= input("Ingrese el email del nuevo usuario: ")
    if(len(email)==0):
        printWaiting("Incorrecto!")
        return
    set_new_user(name=nombre,email=email,rol=RolesGlobal.usuario)
    printWaiting("")

def listarUsuariosAdmin():
    clearScreen()
    usuarios=get_all_users()
    clearScreen()
    setTitle("Lista de Usuarios")
    listas_usuarios = [usuario.to_list() for usuario in usuarios]
    headers=["ID","Nombre","Email"]
    printWaiting(tabulate.tabulate(listas_usuarios, headers, tablefmt="fancy_grid"))

def AdministradorImagenes():
    clearScreen()
    images=get_all_images()
    clearScreen()
    setTitle("Lista de Todas las Imágenes")
    listas_images = [image.to_list() for image in images]
    headers=["ID","Nombre","Propietario"]
    printWaiting(tabulate.tabulate(listas_images, headers, tablefmt="fancy_grid"))


def AdministradorSlices():
    clearScreen()
    slices=get_all_slices()
    clearScreen()
    setTitle("Lista de Todos los Slices")
    listas_slices = [[slice["id_vlan"],slice["nombre"],slice["n_nodos"],slice["topologia"],slice["creador"],slice["dir_red"],slice["fecha_creacion"]] for slice in slices]
    headers=["Vlan","Nombre","N° VMs","Topologia","Creador","Red","Fecha de creación"]
    printWaiting(tabulate.tabulate(listas_slices, headers, tablefmt="fancy_grid"))

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



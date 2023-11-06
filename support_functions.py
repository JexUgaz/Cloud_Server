import tabulate,requests,getpass
from entities.SliceEntity import Slice
from entities.VirtualMachineEntity import VirtualMachine
from graphs import GraphHelper
from helpers import *

listTopologias=["Arbol","Anillo","Lineal","Bus","Cancelar"]


def crearSlice():
    clearScreen()
    setTitle(title="CREAR SLICE")
    nombreSlice=input("Indique el nombre de su slice: ")

    if nombreSlice=="":
        printWaiting("Debe ingresar un nombre...CREACIÓN CANCELADA")
        return
    print("")
    setBarra(text="Cantidad de VMs",enter=True)
    print("OJO: Solo puede crear entre 2 a 5 VMs")
    try:
        cantidad= int(input("Indique la cantidad de VMs en el slice, ('0' para Cancelar): "))
        if(cantidad==0):
            printWaiting("Cancelado!")
        else:    
            if(cantidad>=2 and cantidad<=5):
                print("")
                topologiaSelected,listVM=listarTopologias(cant_vm=cantidad)
                clearScreen()
                slice=Slice(id_vlan=None,nombre=nombreSlice,vms=listVM,nombre_dhcp='',topologia=topologiaSelected,infraestructura=None,fecha_creacion=None,usuario_id=None,subred=None)
                detallesCreacionExitosa(slice)
            else:
                printWaiting("Cantidad de VMs inválida.")
    except ValueError:
        printWaiting("Por favor, ingrese un número válido.")

def detallesCreacionExitosa(slice:Slice):
    setTitle(title="Creación Exitosa")
    print()
    setBarra(text="Slice",enter=True)
    print(f"Nombre: {slice.nombre}")
    print(f"N° Vms: {len(slice.vms)}")
    print(f"Topología: {slice.topologia}\n")
    i=1
    for vm in slice.vms:
        setBarra(text=f"VM #{i}")
        print(f"Nombre: {vm.nombre}")
        print(f"Imagen: {vm.imagen}")
        print(f"RAM: {vm.sizeRam}MB")
        i=i+1
    filename=""
    if slice.topologia == listTopologias[0]:
        filename=GraphHelper.drawArbol(slice.vms)
    elif slice.topologia==listTopologias[1]:
        filename=GraphHelper.drawAnillo(slice.vms)
    printWaiting("")
    try:
        os.remove(filename)
    except Exception as e:
        return

def listarTopologias(cant_vm):
    setBarra(text=f"Topologías para {cant_vm} VMs",enter=True)
    topologiaSelected=setListOptionsShell(
        message="Seleccione la topología",
        choices=listTopologias
    )
    if(listTopologias[-1]!=topologiaSelected):
        """ubicaciones=[]
        idUser=1 # ID del usuario, se guarda al loguearse
        n_Vms=4 #N° de VMs a crear (por defecto), debe ingresar el usuario
        size_ram= [100,100,100,100] #100Mbytes,100Mbytes,100Mbytes,100Mbytes RAM de cada VMs (Debe ingresar)
        idTopologia=1 # ID de la Topolía (por defecto: Arbol, por ahora)
        """
        listVM=[]
        for i in range(cant_vm):
            print()
            salir,virtualMachine=setDetailsVM(i)
            if salir:
                break
            listVM.append(virtualMachine)
        return topologiaSelected,listVM
    else:
        printWaiting("CREACIÓN CANCELADA...")
        return None,None

def setDetailsVM(i):
    setBarra(text=f"Especifique a detalles la VM #{i + 1}",enter=True)
    nombreVM=input("Indique el nombre de la VM: ")

    if nombreVM=="":
        printWaiting("Debe ingresar un nombre...CREACIÓN CANCELADA")
        return
    print("")
    images=["cirros-image.img", "ubuntu-iso-20.04.iso","Cancelar"]
    imagenSelected=setListOptionsShell(
        message="Indique la imagen: ",
        choices=images
    )
    if(images[-1]==imagenSelected):
        return True,None
    
    print()
    print("OJO: La memoria RAM debe estar entre 100 a 200 (MB).")
    try:
        memoria=float(input("Indique la memoria RAM de la VM: "))
        if (memoria>=100 and memoria<=200):
            print(f"Se creará la VM #{i+1} con la imagen {imagenSelected} y memoria RAM de {memoria}MB")
            return False,VirtualMachine(id=None,nombre=nombreVM,sizeRam=memoria,fechaCreacion=None,dirMac=None,portVNC=None,zonaID=None,imagen=imagenSelected)
        else:
            printWaiting("Valor fuera del rango establecido...CREACIÓN CANCELADA")
    except ValueError:
        printWaiting("Valor inválido...CREACIÓN CANCELADA")           
    return True,None




def listarImagenes():
    imagenesNombres = ["cirros-image.img", "ubuntu-iso-20.04.iso"]
    imagen_data = []
    for i, imagen in enumerate(imagenesNombres, start=1):
        imagen_data.append([i, imagen])

    headers = ["N°", "Nombre de la imagen"]
    table = tabulate.tabulate(imagen_data, headers, tablefmt="fancy_grid")
    while True:
        clearScreen()
        setBarra(text="Lista de Imagenes",enter=True)
        print(table)
        
        choices=["Volver","Borrar una Imagen"]
        selection=setListOptionsShell(
            message="Seleccione: ",
            choices=choices
        )
        if selection==choices[1]:
            while True:
                clearScreen()
                print(table)
                try:
                    indice=int(input("Indique el índice de la imagen que desea seleccionar (1-" + str(len(imagen_data)) + "), '0' para Cancelar: "))
                    if indice==0:
                        break
                    if 1 <= indice and indice <= len(imagen_data):
                        printWaiting(f"Ha seleccionado la imagen para borrar: {imagenesNombres[indice-1]}")
                        break 
                    else:
                        printWaiting("Por favor, ingrese un número válido dentro del rango.")
                    
                except ValueError:
                    printWaiting("Por favor, ingrese un número válido.")
        else:
            break

def imagenes():
    while True:
        clearScreen()
        setBarra(text="Imágenes",enter=True)
        choices=["Agregar imagen","Listar imágenes","Volver"]
        seleccion = setListOptionsShell(
            message="Seleccione entre las opciones ",
            choices=choices
        ) 
        
        if seleccion == choices[0]:
            agregarImagen()
        elif seleccion == choices[1]:
            listarImagenes()
        else:
            break

def agregarImagen():
    clearScreen()
    setBarra(text="Agregar Imagen",enter=True)
    filename = input("Seleccionar archivo: ")
    printWaiting("Imagen agregada correctamente")

def menu(api):
    clearScreen()
    if(api=="Openstack"):
        printWaiting("En Construcción...")
        return 
        
    choices=["Ver mis slices","Crear nuevo slice","Editar slice","Imágenes","Volver"]

    while True:
        clearScreen()
        setBarra(text=f"API: {api}",enter=True)
        seleccion = setListOptionsShell(
            message="¿Qué desea realizar el día de hoy? ",
            choices=choices
        )
        
        if seleccion == choices[0]:
            listarSliceUsuario()
        elif seleccion == choices[1]:
            crearSlice()
        elif seleccion == choices[3]:
            imagenes()
        elif seleccion == choices[2]:
            clearScreen()
            printWaiting("En Construcción...")
        elif seleccion == choices[4]:
            break
"""def setApiNewSlice(ubicaciones,idUser,n_Vms,size_ram,idTopologia):
    url = 'http://localhost:5001/setNewSlice'
    data = {
        'idUser':idUser,
        'n_Vms': n_Vms,
        'ubicaciones': ubicaciones,
        'size_ram':size_ram,
        'idTopologia':idTopologia
    }
    response = requests.post(url, data=data)

    # Verificar la respuesta
    if response.status_code == 200:
        print("Solicitud exitosa")
        print(response.json())
    else:
        print(f"Error en la solicitud: {response.status_code}")
        print(response.text)"""

def listarSliceUsuario():
    listasAlumnos = [['1', 'Tarea', "21/10/2023", 2, 1],
                     ['2', 'Laboratorio', "23/05/2023", 7, 8],
                     ['3', 'Examen', "11/12/2023", 7, 8]]

    headers = ["N°", "Nombre", "Fecha", "Número VMs", "Número Enlaces"]
    
    choices=["Ver más detalles de un slice","Borrar un slice","Volver"]

    while True:
        clearScreen()
        setBarra(text="Sus Slices",enter=True)
        print(tabulate.tabulate(listasAlumnos, headers, tablefmt="fancy_grid"))

        seleccion = setListOptionsShell(
            message="Seleccione una opción: ",
            choices=choices
        ) 
        if seleccion==choices[0]:
            try:
                numero=int(input("Indique el índice del slice a detallar (1-" + str(len(listasAlumnos)) + "): "))
                if 1 <= numero and numero <= len(listasAlumnos):
                    clearScreen()
                    setBarra(text=f"Los detalles del slice {numero}", enter=True)
                    printWaiting(tabulate.tabulate([listasAlumnos[numero-1]], headers, tablefmt="fancy_grid"))  
                else:
                    printWaiting("Por favor, ingrese un número válido dentro del rango.")
            except ValueError:
                    printWaiting("Por favor, ingrese un índice válido.")                 
        elif seleccion==choices[1]:
            try:
                numero=int(input("Indique el índice del slice a borrar (1-" + str(len(listasAlumnos)) + "): "))
                if 1 <= numero and numero <= len(listasAlumnos):
                    printWaiting("Se ha borrado el slice: " + str(numero))
                else:
                    printWaiting("Por favor, ingrese un número válido dentro del rango.")
            except ValueError:
                printWaiting("Por favor, ingrese un índice válido.") 
        else:
            break 

def autenticar_usuario(user, password):
    usuarios_regitrados={"Niurka":"123456","Jex":"654321"}
    if user in usuarios_regitrados:
        if usuarios_regitrados[user]==password:
            return True,user
        
    return False,None

def main_function():
    clearScreen()
    setBarra(text="Bienvenido a cloud help")
    print("Inicie sesión para comenzar\n")

    usuario = input('Ingrese su usuario: ')
    contrasena =  getpass.getpass('Ingrese su contraseña:')
    is_autenthicated,user=autenticar_usuario(usuario,contrasena)
    if not is_autenthicated:
        printWaiting("Autenticación fallida")
        return False
    
    salir=False
    while not salir:
        clearScreen()
        setBarra(text=f"Bienvenido, {user}!",enter=True)
        seleccion = setListOptionsShell(
            message="Seleccione la plataforma",
            choices=["Linux","Openstack","Cerrar Sesión"]
        ) 
        
        if seleccion == "Cerrar Sesión":
            print("Cerrando sesión...")
            salir=True
        else:
            menu(api=seleccion)
    return False


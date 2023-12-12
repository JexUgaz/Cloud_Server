import tabulate
from config.globals import RolesGlobal
from config.helpers import *
from entities.SliceEntity import SliceEntity
from entities.UserEntity import UserEntity
from entities.VirtualMachineEntity import VirtualMachine
from config.graphs import GraphHelper
from services.connection_functions import add_new_image, add_new_slice, delete_image, delete_slice, get_all_images_user, get_all_topologias, get_all_vm_slice, get_slices_user
listTopologias=["Arbol","Anillo","Cancelar"]

_usuario_global=None

def showMenuUser(user:UserEntity):
    global _usuario_global
    _usuario_global=user
    choices=[]
    if user.roles_id==RolesGlobal.usuario:
        choices=["Linux","Openstack","Cerrar Sesión"]
    if user.roles_id==RolesGlobal.administrador:
        choices=["Linux","Openstack","Salir"]
    while True:
        clearScreen()
        setBarra(text=f"Bienvenido, {user.nombre}!",enter=True)
        seleccion = setListOptionsShell(
            message="Seleccione la plataforma",
            choices=choices
        ) 
        if seleccion == choices[len(choices)-1]:
            break
        else:
            menuUsuario(api=seleccion)


def menuUsuario(api):
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

def agregarImagen():
    clearScreen()
    setBarra(text="Agregar Imagen",enter=True)
    nombre = input("Nombre de la imagen: ")
    
    if(len(nombre)==0):
        printWaiting("Incorrecto!")
        return
    
    link = input("Indique URL de descarga: ")

    if(len(link)==0 or not es_URI(link)):
        printWaiting("Incorrecto!")
        return

    add_new_image(link=link,nombre=nombre,idUser=_usuario_global.id)
    printWaiting("")


def listarImagenes():
    clearScreen()
    while True:
        imagenesNombres = get_all_images_user(idUser=_usuario_global.id)
        clearScreen()
        listas_images = [[index+1,imagen.nombre, imagen.path.split("/")[-1]] for index,imagen in enumerate(imagenesNombres)]

        headers = ["N°", "Nombre","Archivo"]
        table = tabulate.tabulate(listas_images, headers, tablefmt="fancy_grid")
        setBarra(text="Lista de Imagenes",enter=True)
        if(len(listas_images)==0):
            printWaiting("Tiene 0 imágenes, porfavor añada una")
            break
        else:
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
                        indice=int(input("Indique el índice de la imagen que desea seleccionar (1-" + str(len(listas_images)) + "), '0' para Cancelar: "))
                        if indice==0:
                            break
                        if 1 <= indice and indice <= len(listas_images):
                            delete_image(idImage=imagenesNombres[indice-1].id)
                            printWaiting("")
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
        choices=["Ver mis imágenes","Agregar imagen","Volver"]
        seleccion = setListOptionsShell(
            message="Seleccione entre las opciones ",
            choices=choices
        ) 
        
        if seleccion == choices[1]:
            agregarImagen()
        elif seleccion == choices[0]:
            listarImagenes()
        else:
            break

def crearSlice():
    imagenes=get_all_images_user(idUser=_usuario_global.id)
    clearScreen()
    if len(imagenes)==0:
        printWaiting("No posee imágenes para crear un Slice\nPorfavor, agregue una imagen primero.")
        return
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
                if topologiaSelected is None or listVM is None:
                    printWaiting("Inválido")
                    return
                clearScreen()
                slice=SliceEntity(id_vlan=None,nombre=nombreSlice,vms=listVM,nombre_dhcp='',topologia=topologiaSelected,infraestructura=None,fecha_creacion=None,usuario_id=_usuario_global.id,subred=None)
                detallesCreacionExitosa(slice)
            else:
                printWaiting("Cantidad de VMs inválida.")
    except ValueError:
        printWaiting("Por favor, ingrese un número válido.")

def detallesCreacionExitosa(slice:SliceEntity):
    setTitle(title="Creación Exitosa")
    print()
    setBarra(text="Slice",enter=True)
    print(f"Nombre: {slice.nombre}")
    print(f"N° Vms: {len(slice.vms)}")
    print(f"Topología: {slice.topologia.nombre}\n")
    i=1
    for vm in slice.vms:
        setBarra(text=f"VM #{i}")
        print(f"Nombre: {vm.nombre}")
        print(f"Imagen: {vm.imagen.nombre}")
        print(f"RAM: {vm.sizeRam}MB")
        i=i+1
    filename=""
    if slice.topologia == listTopologias[0]:
        filename=GraphHelper.drawArbol(slice.vms)
    elif slice.topologia==listTopologias[1]:
        filename=GraphHelper.drawAnillo(slice.vms)
    
    add_new_slice(slice=slice)
    printWaiting("")
    try:
        os.remove(filename)
    except Exception as e:
        return

def listarTopologias(cant_vm):
    setBarra(text=f"Topologías para {cant_vm} VMs",enter=True)
    topologias =get_all_topologias()
    
    listTopologias=[topologia.nombre for topologia in topologias]
    listTopologias.append("Cancelar")
    topologiaSelected=setListOptionsShell(
        message="Seleccione la topología",
        choices=listTopologias
    )
    if(listTopologias[-1]!=topologiaSelected):
        listVM=[]
        for i in range(cant_vm):
            print()
            salir,virtualMachine=setDetailsVM(i)
            if salir:
                return None,None
            listVM.append(virtualMachine)
        topologia = [topologia for topologia in topologias if topologia.nombre == topologiaSelected]

        return topologia[0],listVM
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
    images=get_all_images_user(idUser=_usuario_global.id)
    imagenSelected=setListOptionsShell(
        message="Indique la imagen: ",
        choices=[image.nombre for image in images]
    )
    if(images[-1]==imagenSelected):
        return True,None
    
    print()
    print("OJO: La memoria RAM debe estar entre 100 a 200 (MB).")
    try:
        memoria=float(input("Indique la memoria RAM de la VM: "))
        if (memoria>=100 and memoria<=200):
            print(f"Se creará la VM #{i+1} con la imagen {imagenSelected} y memoria RAM de {memoria}MB")
            imagenFinal = [image for image in images if image.nombre == imagenSelected]
            return False,VirtualMachine(id=None,nombre=nombreVM,sizeRam=memoria,fechaCreacion=None,dirMac=None,portVNC=None,zonaID=None,imagen=imagenFinal[0])
        else:
            printWaiting("Valor fuera del rango establecido...CREACIÓN CANCELADA")
    except ValueError:
        printWaiting("Valor inválido...CREACIÓN CANCELADA")           
    return True,None

def listarSliceUsuario():
    headers=["N°","Nombre","N° VMs","Topologia","Red","Fecha de creación"]
    choices=["Ver más detalles de un slice","Borrar un slice","Volver"]

    while True:
        clearScreen()
        slices = get_slices_user(_usuario_global.id)
        listas_slices = [[index+1,slice["nombre"],slice["n_nodos"],slice["topologia"],slice["dir_red"],slice["fecha_creacion"]] for index,slice in enumerate(slices)]
        clearScreen()
        setTitle(title="Sus Slices")
        if(len(listas_slices)==0):
            printWaiting("No tiene slices creados...")
            break
        else:
            print(tabulate.tabulate(listas_slices, headers, tablefmt="fancy_grid"))

            seleccion = setListOptionsShell(
                message="Seleccione una opción: ",
                choices=choices
            ) 
            if seleccion==choices[0]:
                try:
                    numero=int(input("Indique el índice del slice a detallar (1-" + str(len(listas_slices)) + "): "))
                    if 1 <= numero and numero <= len(listas_slices):
                        verDetallesSlice(numero=numero,slice=listas_slices[numero-1],id_vlan=slices[numero-1]["id_vlan"])
                    else:
                        printWaiting("Por favor, ingrese un número válido dentro del rango.")
                except ValueError:
                        printWaiting("Por favor, ingrese un índice válido.")                 
            elif seleccion==choices[1]:
                try:
                    numero=int(input("Indique el índice del slice a borrar (1-" + str(len(listas_slices)) + "): "))
                    if 1 <= numero and numero <= len(listas_slices):
                        clearScreen()
                        delete_slice(idSlice=slices[numero-1]["id_vlan"])
                        printWaiting("")
                    else:
                        printWaiting("Por favor, ingrese un número válido dentro del rango.")
                except ValueError:
                    printWaiting("Por favor, ingrese un índice válido.") 
            else:
                break

def verDetallesSlice(numero,slice,id_vlan):
    clearScreen()
    vms=get_all_vm_slice(id_vlan=id_vlan)
    clearScreen()
    setBarra(text=f"Los detalles del slice N° {numero}", enter=True)
    headers=["Nombre","N° VMs","Topologia","Red","Fecha de creación"]
    print(tabulate.tabulate([[slice[1],slice[2],slice[3],slice[4],slice[5]]], headers, tablefmt="fancy_grid"))  
    print()
    setBarra(text=f"Máquinas Virtuales del slice N° {numero}", enter=True)
    list_vms=[[vm.nombre,vm.dirMac,vm.portVNC,vm.sizeRam,vm.fechaCreacion] for vm in vms]
    headers=["Nombre","MAC","Puerto VNC","RAM","Fecha de creación"]
    printWaiting(tabulate.tabulate(list_vms, headers, tablefmt="fancy_grid"))  
    

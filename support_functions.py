import inquirer,tabulate,requests,getpass

def crearSlice():
    opciones = [
        inquirer.List("opcion",
                      message="Seleccione la forma de despliegue  ",
                      choices=[
                          ("Predeterminado", "Predeterminado"),
                          ("Volver", "Volver"),
                      ])
    ]
    respuestas = inquirer.prompt(opciones)
    seleccion = respuestas["opcion"]
    
    if seleccion == "Predeterminado":
        topologiaYaPuesta()
    else:
        print("Ha seleccionado " + seleccion)

def imagenes():
    opciones = [
        inquirer.List("opcion",
                      message="Seleccione entre las opciones ",
                      choices=[
                          ("Agregar imagen", "Agregar imagen"),
                          ("Listar imagenes", "Listar imagenes"),
                          ("Volver", "Volver"),
                      ])
    ]
    respuestas = inquirer.prompt(opciones)
    seleccion = respuestas["opcion"]
    
    if seleccion == "Agregar imagen":
        agregarImagen()
    elif seleccion == "Listar imagenes":
        listarImagenes()
    else:
        menu()

def agregarImagen():
    filename = input("Seleccionar archivo: ")
    print("Imagen agregada correctamente")
    menu()

def listarImagenes():
    imagenesNombres = ["cirros-image.img", "ubuntu-iso-20.04.iso"]
    imagen_data = []
    for i, imagen in enumerate(imagenesNombres, start=1):
        imagen_data.append([i, imagen])

    headers = ["N°", "Nombre de la imagen"]
    table = tabulate.tabulate(imagen_data, headers, tablefmt="fancy_grid")
    print(table)

    while True:
        try:
            print("Indique el número de la imagen que desea seleccionar (1-" + str(len(imagen_data)) + "): ")
            numero = int(input())
            if 1 <= numero <= len(imagen_data):
                print("Ha seleccionado la imagen para borrar: " + imagen_data[numero - 1][1])
                break  # Sale del bucle si el número es válido
            else:
                print("Por favor, ingrese un número válido dentro del rango.")
        except ValueError:
            print("Por favor, ingrese un número válido.")

def elegirImagen():
    opciones = [
        inquirer.List("opcion",
                      message="Seleccione la imagen de su maquina virtual ",
                      choices=[
                          ("cirros-image.img", "cirros-image.img"),
                          ("ubuntu-iso-20.04.iso", "ubuntu-iso-20.04.iso"),
                          ("Volver", "Volver"),
                      ])
    ]
    respuestas = inquirer.prompt(opciones)
    seleccion = respuestas["opcion"]
    
    if seleccion == "Volver":
        menu()
    else:
        print("Ha seleccionado " + seleccion)

def zonasDeDisponibilidad():
    opciones = [
        inquirer.List("opcion",
                      message="Seleccione la zona de disponibilidad ",
                      choices=[
                          ("Worker 1", "Worker 1"),
                          ("Worker 2", "Worker 2"),
                          ("Worker 3", "Worker 3"),
                          ("Volver", "Volver"),
                      ])
    ]
    respuestas = inquirer.prompt(opciones)
    seleccion = respuestas["opcion"]
    
    if seleccion == "Volver":
        print("Saliendo del programa.")
    elif seleccion=="Worker 1":
        return str(0)
    elif seleccion=="Worker 2":
        return str(1)
    elif seleccion=="Worker 3":
        return str(2)
    else:
        print("Ha seleccionado " + seleccion)
    menu()

def menu():
    opciones = [
        inquirer.List("opcion",
                      message="¿Qué desea realizar el día de hoy? ",
                      choices=[
                          ("Ver mis slices", "Ver mis slices"),
                          ("Crear nuevo slice", "Crear nuevo slice"),
                          ("Editar slice", "Editar slice"),
                          ("Imágenes", "Imágenes"),
                          ("Volver", "Volver"),
                      ])
    ]
    
    respuestas = inquirer.prompt(opciones)
    seleccion = respuestas["opcion"]
    
    if seleccion == "Ver mis slices":
        listarSliceUsuario()
    elif seleccion == "Crear nuevo slice":
        crearSlice()
    elif seleccion == "Imágenes":
        imagenes()
    elif seleccion == "Editar slice":
        personalizarTopología()
    elif seleccion == "Volver":
        return

def setApiNewSlice(ubicaciones,idUser,n_Vms,size_ram,idTopologia):
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
        print(response.text)
        
def topologiaYaPuesta():
    print("Escogiendo cualquier opcion de topología se creará 4 VM's por defecto")    
    #------INICIAMOS A OBTENER LA DATA PARA CREAR EL SLICE---------#

    ubicaciones=[]
    idUser=1 # ID del usuario, se guarda al loguearse
    n_Vms=4 #N° de VMs a crear (por defecto), debe ingresar el usuario
    size_ram= [100,100,100,100] #100Mbytes,100Mbytes,100Mbytes,100Mbytes RAM de cada VMs (Debe ingresar)
    idTopologia=1 # ID de la Topolía (por defecto: Arbol, por ahora)

    for i in range(n_Vms):
        print("Elija la zona de disponibilidad para la VM #" + str(i + 1))
        ubicaciones.append(zonasDeDisponibilidad())

    for i in range(n_Vms):
        print("Elija la imagen para la VM #" + str(i + 1))
        elegirImagen()
    
    
    print("Se a realizado la creacion de sus VM's en la zona de disponibilidad que eligio")

    opciones = [
        inquirer.List("opcion",
                      message="Elige el tipo de topología ",
                      choices=[
                          ("Arbol", "Arbol"),
                          ("Malla", "Malla"),
                          ("Anillo", "Anillo"),
                          ("Lineal", "Lineal"),
                          ("Bus", "Bus"),
                          ("Salir", "Salir"),
                      ])
    ] 
    respuestas = inquirer.prompt(opciones)
    seleccion = respuestas["opcion"]
    
    if seleccion == "Salir":
        print("Saliendo del programa.")
    else:
        print("Ha seleccionado la topología tipo " + seleccion)

        setApiNewSlice(
            ubicaciones=ubicaciones,
            idUser=idUser,
            n_Vms=n_Vms,
            size_ram=size_ram,
            idTopologia=idTopologia
        ) #FUNCION QUE CONTACTA A LA API, Y CREE UN SLICE
    
    menu()

def personalizarTopología():
    ListasSlices = [['1', 'Tarea', "21/10/2023", 2, 1],
                     ['2', 'Laboratorio', "23/05/2023", 7, 8],
                     ['3', 'Examen', "11/12/2023", 7, 8]]
    headers = ["N°", "Nombre", "Fecha", "Número VMs", "Número Enlaces"]
    table = tabulate.tabulate(ListasSlices, headers, tablefmt="fancy_grid")
    print(table)

    while True:
        try:
            print("Indique el número de slice que quiere editar (1-" + str(len(ListasSlices)) + "): ")
            numero = int(input())
            if 1 <= numero <= len(ListasSlices):
                print("Se ha editado el slice: " + str(numero))

                opciones = [
                    inquirer.List("opcion",
                                  message="Para personalizar su topología elija entre ",
                                  choices=[
                                      ("Añada maquina virtual (VM)", "Añada maquina virtual (VM)"),
                                      ("Añadir Enlace", "Añadir Enlace"),
                                      ("Salir", "Salir"),
                                  ])
                ] 
                respuestas = inquirer.prompt(opciones)
                seleccion = respuestas["opcion"]
                
                if seleccion == "Añada maquina virtual (VM)":
                    print("Cantidad de VM a emplear: ")
                    cantidad = int(input())  # Convertir la entrada a un número entero

                    for i in range(cantidad):
                        print("Elija la zona de disponibilidad para la VM #" + str(i + 1))
                        zonasDeDisponibilidad()
                    
                
                else:
                    print("Ha seleccionado la topología tipo " + seleccion)

                break  # Sale del bucle
            else:
                print("Por favor, ingrese un número válido dentro del rango.")
        except ValueError:
            print("Por favor, ingrese un número válido.")

def listarSlicesAdmin():
    ListasAlumnos = [['1', 'Tarea', "21/10/2023", 2, 1],
                     ['2', 'Laboratorio', "23/05/2023", 7, 8],
                     ['3', 'Examen', "11/12/2023", 7, 8]]

    headers = ["N°", "Nombre", "Fecha", "Número VMs", "Número Enlaces"]
    table = tabulate.tabulate(ListasAlumnos, headers, tablefmt="fancy_grid")
    print(table)

    opciones = [
        inquirer.List("opcion",
                      message="¿Desea borrar alguno de sus slices? ",
                      choices=[
                          ("Sí", "Si"),
                          ("No", "No"),
                          ("Salir", "Salir"),
                      ])
    ] 
    respuestas = inquirer.prompt(opciones)
    seleccion = respuestas["opcion"]
    
    if seleccion == "Si":
        while True:
            try:
                print("Indique el número de slice a borrar (1-" + str(len(ListasAlumnos)) + "): ")
                numero = int(input())
                if 1 <= numero <= len(ListasAlumnos):
                    print("Se ha borrado el slice: " + str(numero))
                    break  
                else:
                    print("Por favor, ingrese un número válido dentro del rango.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
    elif seleccion == "No":
        menu()

def listarSliceUsuario():
    ListasAlumnos = [['1', 'Tarea', "21/10/2023", 2, 1],
                     ['2', 'Laboratorio', "23/05/2023", 7, 8],
                     ['3', 'Examen', "11/12/2023", 7, 8]]

    headers = ["N°", "Nombre", "Fecha", "Número VMs", "Número Enlaces"]
    
    # Utiliza la función tabulate desde el módulo tabulate
    table = tabulate.tabulate(ListasAlumnos, headers, tablefmt="fancy_grid")
    print(table)
    opciones = [
        inquirer.List("opcion",
                      message="¿Desea borrar alguno de sus slices? ",
                      choices=[
                          ("Sí", "Si"),
                          ("No", "No"),
                          ("Salir", "Salir"),
                      ])
    ] 
    respuestas = inquirer.prompt(opciones)
    seleccion = respuestas["opcion"]
    
    if seleccion == "Si":
        while True:
            try:
                print("Indique el número de slice a borrar (1-" + str(len(ListasAlumnos)) + "): ")
                numero = int(input())
                if 1 <= numero <= len(ListasAlumnos):
                    print("Se ha borrado el slice: " + str(numero))
                    menu()
                    break  
                else:
                    print("Por favor, ingrese un número válido dentro del rango.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
    elif seleccion == "No":
        menu()

def autenticar_usuario(user, password):
    usuarios_regitrados={"niurka":"123456","jex":"654321"}
    if user in usuarios_regitrados:
        if usuarios_regitrados[user]==password:
            return True
        
    return False

def main_function():
    print("Bienvenido a cloud help")
    print("Inicie sesión para comenzar ")
    print("")

    usuario = input('Ingrese su usuario: ')
    contrasena =  getpass.getpass('Ingrese su contraseña:')
    is_autenthicated=autenticar_usuario(usuario,contrasena)
    if not is_autenthicated:
        print("Autenticación fallida")
        return None
    
    opciones = [
        inquirer.List("opcion",
                      message="Seleccione la plataforma ",
                      choices=[
                          ("Linux", "Linux"),
                          ("OpenStack", "OpenStack"),
                          ("Salir", "Salir"),
                      ])
    ]
    respuestas = inquirer.prompt(opciones)
    seleccion = respuestas["opcion"]
    
    if seleccion == "Salir":
        print("Saliendo del programa.")
    else:
        print("Ha seleccionado " + seleccion)
        menu()
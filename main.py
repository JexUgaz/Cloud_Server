import getpass
from config.globals import RolesGlobal
from config.helpers import clearScreen, printWaiting, setBarra
from services.connection_functions import autenticar_usuario, get_usuario_credentials
from presentations.admin_presentation import showMenuAdministrador
from presentations.user_presentation import showMenuUser

def main_function():
    clearScreen()
    setBarra(text="Bienvenido a cloud help")
    print("Inicie sesión para comenzar\n")

    usuario = input('Ingrese su usuario: ')
    contrasena =  getpass.getpass('Ingrese su contraseña:')
    is_autenthicated,user_token=autenticar_usuario(usuario,contrasena)
    if not is_autenthicated:
        printWaiting("Autenticación fallida")
        return False
    user=get_usuario_credentials(usuario,contrasena)
    print(f'Is Autenticado: {is_autenthicated}')
    print(f'User: {user}')
    print(f'Token: {user_token}')
    input('presiona enter...')

    if user.roles_id==RolesGlobal.usuario:
        showMenuUser(user=user)
    elif user.roles_id==RolesGlobal.administrador:
        showMenuAdministrador(user=user)
    return False

if __name__ == "__main__":
    salir=False
    while not salir:
        salir=main_function()


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

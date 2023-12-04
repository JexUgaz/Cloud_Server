import json
import requests
from entities.UserEntity import UserEntity
from services.constantes_env import SERVER_API_ENDPOINT
prefix_admin='/admin'

def get_all_users():
    url = SERVER_API_ENDPOINT + prefix_admin+'/listUser'
    try:
        r = requests.get(url=url)
        response_data = json.loads(r.text)
        usuarios_json = response_data.get('usuarios', [])
        
        # Convertir la lista de objetos JSON a objetos UserEntity
        usuarios = [UserEntity.convertToUser(usuario) for usuario in usuarios_json]
        
        return usuarios
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud: ", e)
    return []
import json
import threading
import requests
from config.helpers import cancel_loading_done, loading_animation
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

def get_monitoreo_recursos():
    animation_thread = threading.Thread(target=loading_animation)
    animation_thread.start()
    
    url = SERVER_API_ENDPOINT + prefix_admin+'/getMonitoreoRecursos'
    try:
        r = requests.get(url=url)
        response_data = json.loads(r.text)
        memoria_workers = response_data.get('memoria_workers', [])
        uso_sistema_workers = response_data.get('uso_sistema_workers', [])
        cancel_loading_done()  
        animation_thread.join()
        
        return memoria_workers,uso_sistema_workers
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud: ", e)
    return [],[]
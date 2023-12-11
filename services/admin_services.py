import json
import threading
import requests
from config.helpers import MensajeResultados, cancel_loading_done, loading_animation
from entities.ImageEntity import ImagenEntity
from entities.UserEntity import UserEntity
from services.constantes_env import SERVER_API_ENDPOINT
prefix_admin='/admin'

def get_all_users():
    animation_thread = threading.Thread(target=loading_animation)
    animation_thread.start()
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
    finally:
        cancel_loading_done()  
        animation_thread.join() 
    return []

def get_all_images():
    animation_thread = threading.Thread(target=loading_animation)
    animation_thread.start()
    url = SERVER_API_ENDPOINT + prefix_admin+'/listImages'
    try:
        r = requests.get(url=url)
        response_data = json.loads(r.text)
        images_json = response_data.get('images', [])
        
        # Convertir la lista de objetos JSON a objetos UserEntity
        images = [ImagenEntity.convertToImagen(image) for image in images_json]
        
        return images
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud: ", e)
    finally:
        cancel_loading_done()  
        animation_thread.join() 
    return []

def set_new_user(name,rol,email):
    animation_thread = threading.Thread(target=loading_animation)
    animation_thread.start()
    
    url = SERVER_API_ENDPOINT + prefix_admin + '/setNewUser'
    data = {
        "name": name,
        "rol": rol,
        "email": email
    }

    try:
        r = requests.post(url=url, data=data, stream=True)
        response_data = json.loads(r.text)

        result = response_data.get('result')
        msg = response_data.get('msg') 

        if MensajeResultados.success == result:
            print(f'\nListo! {msg}')
        else:
            print(f'\nUps! {msg}')
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud: ", e)
    except Exception as e:
        print("Error no manejado: ", e)
    finally:
        cancel_loading_done()  
        animation_thread.join() 

def get_monitoreo_recursos():
    animation_thread = threading.Thread(target=loading_animation)
    animation_thread.start()
    
    url = SERVER_API_ENDPOINT + prefix_admin+'/getMonitoreoRecursos'
    try:
        r = requests.get(url=url)
        response_data = json.loads(r.text)
        memoria_workers = response_data.get('memoria_workers', [])
        uso_sistema_workers = response_data.get('uso_sistema_workers', [])
        
        return memoria_workers,uso_sistema_workers
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud: ", e)
    finally:
        cancel_loading_done()  
        animation_thread.join()
    return [],[]
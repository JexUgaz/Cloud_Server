import json
import threading
import requests
from config.helpers import MensajeResultados, cancel_loading_done, loading_animation
from entities.ImageEntity import ImagenEntity
from entities.UserEntity import UserEntity
from openstack_sdk import password_authentication_with_unscoped_authorization
from services.constantes_env import DOMAIN_NAME, KEYSTONE_ENDPOINT, SERVER_API_ENDPOINT

prefix_user='/user'
def autenticar_usuario(username, password):
    r = password_authentication_with_unscoped_authorization(KEYSTONE_ENDPOINT, DOMAIN_NAME, username, password)
    if r is not None:
        if r.status_code == 201:
            user_token = r.headers['X-Subject-Token']
            return True, user_token
    return False, None

def get_usuario_credentials(username, password):
    url = SERVER_API_ENDPOINT + prefix_user+'/authenticationUser'    
    data = \
        {
           "name":username,
           "pswrd":password
        }
    try:
        r = requests.post(url=url, data=data)
        response_data = json.loads(r.text)
        user_data = response_data.get('user')
        return UserEntity.convertToUser(user_data)
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud: ",e)
    return None

def add_new_image(link, idUser, nombre):
    animation_thread = threading.Thread(target=loading_animation)
    animation_thread.start()
    
    url = SERVER_API_ENDPOINT + prefix_user + '/setNewImage'
    data = {
        "link": link,
        "idUser": idUser,
        "nombre": nombre
    }

    try:
        r = requests.post(url=url, data=data, stream=True)
        response_data = json.loads(r.text)

        result = response_data.get('result')
        msg = response_data.get('msg')

        cancel_loading_done()  
        animation_thread.join()  

        if MensajeResultados.success == result:
            print(f'\nListo! {msg}')
        else:
            print(f'\nUps! {msg}')
    except requests.exceptions.RequestException as e:
        cancel_loading_done()      
        animation_thread.join()  # Espera a que el hilo de animación termine
        print("Error en la solicitud: ", e)
    except Exception as e:
        cancel_loading_done()        
        animation_thread.join()  # Espera a que el hilo de animación termine
        print("Error no manejado: ", e)
        
def get_all_images_user(idUser):
    url = SERVER_API_ENDPOINT + prefix_user+'/getImagesByUser?idUser='+idUser
    try:
        r = requests.get(url=url)
        response_data = json.loads(r.text)
        imagenes_json = response_data.get('imagenes', [])
        
        # Convertir la lista de objetos JSON a objetos UserEntity
        imagenes = [ImagenEntity.convertToImagen(image) for image in imagenes_json]
        
        return imagenes
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud: ", e)
    return []

def delete_image(idImage):
    url = SERVER_API_ENDPOINT + prefix_user+f'/deleteImage?idImage={idImage}'
    try:
        r = requests.get(url=url)
        response_data = json.loads(r.text)
        result = response_data.get('result')
        msg = response_data.get('msg')

        if MensajeResultados.success == result:
            print(f'\nListo! {msg}')
        else:
            print(f'\nUps! {msg}')
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud: ", e)
    return []
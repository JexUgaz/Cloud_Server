import json
import requests
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
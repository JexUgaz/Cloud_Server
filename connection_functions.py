import json
import os

import requests
from entities.UserEntity import UserEntity
from openstack_sdk import password_authentication_with_unscoped_authorization
from dotenv import load_dotenv

load_dotenv()
# ACCESS NODE IP
ACCESS_NODE_IP = os.getenv("ACCESS_NODE_IP") # ------------------ DONE
# API SERVER PORT
SERVER_API_PORT=os.getenv("SERVER_API_PORT")
# OPENSTACK SERVICE PORTS
KEYSTONE_PORT = os.getenv("KEYSTONE_PORT") # ------------------ DONE
NEUTRON_PORT = os.getenv("NEUTRON_PORT") # ------------------ DONE
NOVA_PORT = os.getenv("NOVA_PORT") # ------------------ DONE
GLANCE_PORT = os.getenv("GLANCE_PORT") # ------------------ DONE
# OPENSTACK ENDPOINTS
KEYSTONE_ENDPOINT = 'http://' + ACCESS_NODE_IP + ':' + KEYSTONE_PORT + '/v3' # ------------------ DONE
NEUTRON_ENDPOINT = 'http://' + ACCESS_NODE_IP + ':' + NEUTRON_PORT + '/v2.0' # ------------------ DONE
NOVA_ENDPOINT = 'http://' + ACCESS_NODE_IP + ':' + NOVA_PORT + '/v2.1' # ------------------ DONE
GLANCE_ENDPOINT = 'http://' + ACCESS_NODE_IP + ':' + GLANCE_PORT # ------------------ DONE
DOMAIN_NAME = os.getenv("DOMAIN_NAME") # ------------------ DONE
# API SERVER ENDPOINT
SERVER_API_ENDPOINT = 'http://' + ACCESS_NODE_IP + ':' + SERVER_API_PORT # ------------------ DONE

def autenticar_usuario(username, password):
    r = password_authentication_with_unscoped_authorization(KEYSTONE_ENDPOINT, DOMAIN_NAME, username, password)
    if r is not None:
        if r.status_code == 201:
            user_token = r.headers['X-Subject-Token']
            return True, user_token
    return False, None

def get_usuario_credentials(username, password):
    url = SERVER_API_ENDPOINT + '/authenticationUser'    
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
import json
import threading
import requests
from entities.SliceEntity import SliceEntity
from entities.TopologiaEntity import TopologiaEntity
from entities.VirtualMachineEntity import VirtualMachine
from prettytable import PrettyTable
from config.helpers import MensajeResultados, cancel_loading_done, loading_animation
from entities.ImageEntity import ImagenEntity
from entities.UserEntity import UserEntity
from openstack_sdk import password_authentication_with_unscoped_authorization,password_authentication_with_scoped_authorization,monitorear_asignacion_servidores
from services.constantes_env import DOMAIN_NAME, KEYSTONE_ENDPOINT, NOVA_ENDPOINT,SERVER_API_ENDPOINT,ADMIN_USERNAME,ADMIN_PASSWORD,ADMIN_PROJECT_NAME, ADMIN_USER_ID, ADMIN_USER_PASSWORD, DOMAIN_ID, ADMIN_PROJECT_ID

prefix_user='/user'
def autenticar_usuario(username, password):
    r = password_authentication_with_unscoped_authorization(KEYSTONE_ENDPOINT, DOMAIN_ID, username, password)
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

class _MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ImagenEntity):
            return obj.__dict__  # Si es un objeto ImagenEntity, conviértelo a un diccionario
        return super().default(obj)


def add_new_slice(slice: SliceEntity):
    animation_thread = threading.Thread(target=loading_animation)
    animation_thread.start()

    url = SERVER_API_ENDPOINT + prefix_user + '/setNewSlice'

    try:
        data = {
            'id_vlan': slice.id_vlan,
            'nombre': slice.nombre,
            'vms': json.dumps([vm.__dict__ for vm in slice.vms],cls=_MyEncoder),  # Convierte la lista de objetos a una lista de diccionarios
            'nombre_dhcp': slice.nombre_dhcp,
            'topologia': json.dumps(slice.topologia.__dict__),  # Convierte el objeto a un diccionario
            'infraestructura': slice.infraestructura,
            'fecha_creacion': slice.fecha_creacion,
            'usuario_id': slice.usuario_id,
            'subred': slice.subred,
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        r = requests.post(url=url, data=data, stream=True, headers=headers)
        response_data = json.loads(r.text)

        result = response_data.get('result')
        msg = response_data.get('msg')

        cancel_loading_done()
        animation_thread.join()

        if MensajeResultados.success == result:
            print(f'\nListo! {msg}')
            idSlice = response_data.get('idSlice')
            ports = response_data.get('ports')
            print(f"Vlan asignado: {idSlice}")
            print(f"Puertos VNC: {ports}")
        else:
            print(f'\nUps! {msg}')
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud: ", e)
    except Exception as e:
        print("Error no manejado: ", e)
    finally:
        cancel_loading_done()
        animation_thread.join()  # Espera a que el hilo de animación termine

        
def get_all_images_user(idUser):
    url = SERVER_API_ENDPOINT + prefix_user+'/getImagesByUser?idUser='+idUser
    try:
        animation_thread = threading.Thread(target=loading_animation)
        animation_thread.start()
        r = requests.get(url=url)
        response_data = json.loads(r.text)
        imagenes_json = response_data.get('imagenes', [])
        
        # Convertir la lista de objetos JSON a objetos UserEntity
        imagenes = [ImagenEntity.convertToImagen(image) for image in imagenes_json]
        
        return imagenes
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud: ", e)
    finally:
        cancel_loading_done()  
        animation_thread.join()  
    return []


        
def get_all_vm_slice(id_vlan):
    url = SERVER_API_ENDPOINT + prefix_user+'/getAllVMs?idSlice='+id_vlan
    try:
        animation_thread = threading.Thread(target=loading_animation)
        animation_thread.start()
        r = requests.get(url=url)
        response_data = json.loads(r.text)
        vms_json = response_data.get('vms', [])
        
        # Convertir la lista de objetos JSON a objetos UserEntity
        vms = [VirtualMachine(id=vm["id"],nombre=vm["nombre"],sizeRam=vm["sizeRam"],fechaCreacion=vm["fechaCreacion"],dirMac=vm["dirMac"],portVNC=vm["portVNC"],zonaID=vm["zonaID"],imagen=None) for vm in vms_json]
        
        return vms
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud: ", e)
    finally:
        cancel_loading_done()  
        animation_thread.join()  
    return []


def get_all_topologias():
    url = SERVER_API_ENDPOINT + prefix_user+'/getAllTopologias'
    try:
        animation_thread = threading.Thread(target=loading_animation)
        animation_thread.start()
        r = requests.get(url=url)
        response_data = json.loads(r.text)
        topologias_json = response_data.get('topologias', [])
        
        # Convertir la lista de objetos JSON a objetos UserEntity
        topologias = [TopologiaEntity.convertToTopologia(topologia) for topologia in topologias_json]

        return topologias
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud: ", e)
    finally:
        cancel_loading_done()  
        animation_thread.join()  
    return []

def delete_image(idImage):
    url = SERVER_API_ENDPOINT + prefix_user+f'/deleteImage?idImage={idImage}'
    try:
        animation_thread = threading.Thread(target=loading_animation)
        animation_thread.start()
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
    finally:
        cancel_loading_done()  
        animation_thread.join() 
    return []

def delete_slice(idSlice):
    url = SERVER_API_ENDPOINT + prefix_user+f'/deleteSlice?idSlice={idSlice}'
    try:
        animation_thread = threading.Thread(target=loading_animation)
        animation_thread.start()
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
    finally:
        cancel_loading_done()  
        animation_thread.join()


def monitorear_asignacion_recursos():
    #is_autenthicated,user,user_token=autenticar_usuario(ADMIN_USERNAME,ADMIN_PASSWORD)
    #r11 = password_authentication_with_scoped_authorization(KEYSTONE_ENDPOINT, DOMAIN_NAME, ADMIN_USERNAME, ADMIN_PASSWORD, 'default', ADMIN_PROJECT_NAME)
    r1 = password_authentication_with_scoped_authorization(KEYSTONE_ENDPOINT, ADMIN_USER_ID, ADMIN_USER_PASSWORD, DOMAIN_ID, ADMIN_PROJECT_ID)
    user_token = r1.headers['X-Subject-Token']
    #print(r1.status_code)
    #'''
    m=monitorear_asignacion_servidores(NOVA_ENDPOINT,user_token)

    print(m.status_code)
    if m.status_code == 200:
        hyp_list=m.json()['hypervisors']
        data=[]
        for hyp in hyp_list:
            data.append({
                'hypervisor_hostname': hyp['hypervisor_hostname'],
                'vcpus': hyp['vcpus'],
                'memory_mb': hyp['memory_mb'],
                'local_gb': hyp['local_gb'],
                'vcpus_used': hyp['vcpus_used'],
                'memory_mb_used': hyp['memory_mb_used'],
                'local_gb_used': hyp['local_gb_used'],
            })


        #import json
        #datos_json = json.dumps(datos)
        
        
        #print(datos_json['hypervisors'])
        #print(datos_json)
        #
        #print(json.dumps(datos))
        #user_token = m.headers['X-Subject-Token']
        #return True, username, user_token
    #'''
    
    table = PrettyTable()
    table.field_names = data[0].keys()
    print ()
    for row in data:
        table.add_row(row.values())
    
    print(table)

def get_slices_user(idUser):
    animation_thread = threading.Thread(target=loading_animation)
    animation_thread.start()
    url = SERVER_API_ENDPOINT + prefix_user+'/getSlicesByUser?idUser='+idUser
    try:
        r = requests.get(url=url)
        response_data = json.loads(r.text)
        slices_json = response_data.get('slices', [])
        
        return slices_json
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud: ", e)
    finally:
        cancel_loading_done()  
        animation_thread.join() 
    return []



'''
def crear_instancia(nombre_instancia, imagen_id, flavor_id,network_list=[]):
    token = password_authentication_with_scoped_authorization(KEYSTONE_ENDPOINT, DOMAIN_NAME, ADMIN_USERNAME, ADMIN_PASSWORD, 'default', "ins")

    r= create_instance(NOVA_ENDPOINT, token, nombre_instancia, flavor_id, imagen_id, network_list)

    if r.status_code == 202:
        print("creacion de instancia exitosa")
        print(r.json())
    else:
        print(f"Error en la solicitud: {r.status_code}")
        print(r.text)
'''
from dotenv import load_dotenv
from openstack_sdk import password_authentication_with_scoped_authorization, assign_role_to_user_on_project, create_project, list_projects, create_network, create_subnet, create_port, get_server_console, create_server, list_flavors, list_images, token_authentication_with_scoped_authorization
import os

load_dotenv()
# ACCESS NODE IP
ACCESS_NODE_IP = os.getenv("ACCESS_NODE_IP") # ------------------ DONE
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
# OPENSTACK CREDENTIALS
ADMIN_USER_PASSWORD = os.getenv("ADMIN_USER_PASSWORD") # ------------------ DONE
ADMIN_USER_ID = os.getenv("ADMIN_USER_ID") # ------------------ DONE
DOMAIN_ID = os.getenv("DOMAIN_ID") # ------------------ DONE
ADMIN_PROJECT_ID = os.getenv("ADMIN_PROJECT_ID") # ------------------ DONE
# ROLES
ADMIN_ROLE_ID = os.getenv("ADMIN_ROLE_ID") # ------------------ DONE
# COMPUTE API VERSION
COMPUTE_API_VERSION = os.getenv("COMPUTE_API_VERSION") # ------------------ DONE
# CONSOLE ACCESS
TARGET_PORT = os.getenv("TARGET_PORT") # ------------------ DONE
TARGET_HOST = os.getenv("TARGET_HOST") # ------------------ DONE

def get_token_for_admin():
    r = password_authentication_with_scoped_authorization(KEYSTONE_ENDPOINT, ADMIN_USER_ID, ADMIN_USER_PASSWORD, DOMAIN_ID, ADMIN_PROJECT_ID)
    if r.status_code == 201:
        return r.headers['X-Subject-Token']
    else:
        return None

def get_token_for_admin_in_project(project_id):
    admin_token = get_token_for_admin()
    resp = token_authentication_with_scoped_authorization(KEYSTONE_ENDPOINT, admin_token, DOMAIN_ID, project_id)
    #print('token project')
    #print(resp.status_code)
    if resp.status_code == 201:
        token_for_project = resp.headers['X-Subject-Token']
        return token_for_project
    else:
        return None

def get_flavors():
    admin_token = get_token_for_admin()
    r = list_flavors(NOVA_ENDPOINT, admin_token)
    if r.status_code == 200:
        flavors = []
        flavor_list = r.json()['flavors']
        for f in flavor_list:
            flavors.append({
                'id' : f['id'],
                'name' : f['name'],
                'ram' : f['ram'],
                'disk' : f['disk'],
                'vcpus' : f['vcpus']
            })
        return flavors
    else:
        return None

def get_images():
    admin_token = get_token_for_admin()
    r = list_images(NOVA_ENDPOINT, admin_token, 300)
    if r.status_code == 200:
        images = []
        image_list = r.json()['images']
        for i in image_list:
            #image_object = Image(i['id'], i['name'])
            images.append({
                'id' : i['id'],
                'name' : i['name']
            })
        return images
    else:
        return None

# NETWORK SECTION
def build_network(token_for_project, network_name):
    r = create_network(NEUTRON_ENDPOINT, token_for_project, network_name)
    if r.status_code == 201:
        network_created = r.json()['network']
        network_object = {'id':network_created['id'],'name':network_created['name']}
        return network_object
    else:
        return None

def build_subnet(token_for_project, network_name, network_id, cidr):
    subnet_name = 'subnet_' + network_name
    r = create_subnet(NEUTRON_ENDPOINT, token_for_project, network_id, subnet_name, '4', cidr)
    if r.status_code == 201:
        subnet_created = r.json()['subnet']
        subnet_object = {'id':subnet_created['id'], 'name':subnet_created['name'], 'network_id':subnet_created['network_id']}
        return subnet_object
    else:
        return None

def build_port(token_for_project, port_name, network_id, project_id):
    resp1 = create_port(NEUTRON_ENDPOINT, token_for_project, port_name, network_id, project_id)
    if resp1.status_code == 201:
        port_created = resp1.json()['port']
        port_object = {'id':port_created['id'], 'name':port_created['name'], 'network_id':port_created['network_id'], 'project_id':port_created['project_id']}
        return port_object
    else:
        return None

def get_console_url_per_instance(instance_id):
    admin_token = get_token_for_admin()
    r = get_server_console(NOVA_ENDPOINT, admin_token, instance_id, COMPUTE_API_VERSION)
    if r.status_code == 200:
        remote_url = r.json()['remote_console']['url']
        # REPLACE
        remote_url = remote_url.replace('controller:6080',TARGET_HOST + ':' + TARGET_PORT)
        return remote_url
    else:
        return None

def create_topology(vm_list, type_topology, topology_name, topology_description, user_id):
    num_vms = len(vm_list)
    vms = []
    for vm in vm_list:
        vms.append({
            'name':vm.name,
            'image':vm.image,
            'flavor':vm.flavor,
            'networks':[]
        })
    
    # OBTENER TOKEN
    admin_token = get_token_for_admin()

    # CREAR PROJECT
    r1 = create_project(KEYSTONE_ENDPOINT, admin_token, DOMAIN_ID, topology_name, topology_description)
    if r1.status_code != 201:
        return None
    t = r1.json()['project']
    topology_id = t['id']

    # ASIGNAR ROLE ADMIN AL USUARIO ADMIN
    r2 = assign_role_to_user_on_project(KEYSTONE_ENDPOINT, admin_token, topology_id, ADMIN_USER_ID, ADMIN_ROLE_ID)
    r3 = assign_role_to_user_on_project(KEYSTONE_ENDPOINT, admin_token, topology_id, user_id, ADMIN_ROLE_ID)

    if r2.status_code != 204:
        return None
    if r3.status_code != 204:
        return None
    
    token_for_project = get_token_for_admin_in_project(topology_id)

    if type_topology == 'Anillo':
        for i in range(num_vms):
            network_name = 'red ' + str(i+1)
            cidr = '10.0.0.0/30'
            net = build_network(token_for_project, network_name)
            network_id = net['id']
            sub = build_subnet(token_for_project, network_name, network_id, cidr)
            port_obj_1 = build_port(token_for_project, network_name, network_id, topology_id)
            port_obj_2 = build_port(token_for_project, network_name, network_id, topology_id)
            vms[i]['networks'].append({"port": port_obj_1['id']})
            if i==(num_vms-1):
                vms[0]['networks'].append({"port": port_obj_2['id']})
            else:
                vms[i+1]['networks'].append({"port": port_obj_2['id']})

    if type_topology == 'Lineal':
        for i in range(num_vms-1):
            network_name = 'red ' + str(i+1)
            cidr = '10.0.0.0/30'
            net = build_network(token_for_project, network_name)
            network_id = net['id']
            sub = build_subnet(token_for_project, network_name, network_id, cidr)
            port_obj_1 = build_port(token_for_project, network_name, network_id, topology_id)
            port_obj_2 = build_port(token_for_project, network_name, network_id, topology_id)
            vms[i]['networks'].append({"port": port_obj_1['id']})
            vms[i+1]['networks'].append({"port": port_obj_2['id']})

    if type_topology == 'Bus':
        network_name = 'red bus'
        cidr = '10.0.0.0/24'
        net = build_network(token_for_project, network_name)
        network_id = net['id']
        sub = build_subnet(token_for_project, network_name, network_id, cidr)
        for i in range(num_vms-1):
            port_obj_1 = build_port(token_for_project, network_name, network_id, topology_id)
            vms[i]['networks'].append({"port": port_obj_1['id']})

    if type_topology == 'Malla':
        pass
    
    if type_topology == 'Anillo Doble':
        for i in range(num_vms):
            network_name = 'red ' + str(i+1)
            network_name_red = 'red red' + str(i+1)
            cidr = '10.0.0.0/30'
            cidr_red = '20.0.0.0/30'
            net = build_network(token_for_project, network_name)
            net_red = build_network(token_for_project, network_name_red)
            network_id = net['id']
            network_red_id = net_red['id']
            
            sub = build_subnet(token_for_project, network_name, network_id, cidr)
            sub_red = build_subnet(token_for_project, network_name_red, network_red_id, cidr_red)
            
            port_obj_1 = build_port(token_for_project, network_name, network_id, topology_id)
            port_obj_2 = build_port(token_for_project, network_name, network_id, topology_id)
            
            port_obj_3 = build_port(token_for_project, network_name_red, network_red_id, topology_id)
            port_obj_4 = build_port(token_for_project, network_name_red, network_red_id, topology_id)

            vms[i]['networks'].append({"port": port_obj_1['id']})
            vms[i]['networks'].append({"port": port_obj_3['id']})
            if i==(num_vms-1):
                vms[0]['networks'].append({"port": port_obj_2['id']})
                vms[0]['networks'].append({"port": port_obj_4['id']})
            else:
                vms[i+1]['networks'].append({"port": port_obj_2['id']})
                vms[i+1]['networks'].append({"port": port_obj_4['id']})
    
    for instance in vms:
        r6 = create_server(NOVA_ENDPOINT, token_for_project, instance['name'], instance['flavor'], instance['image'], instance['networks'])
        if r6.status_code != 202:
            return None
        print('INSTANCIA CREADA CORRECTAMENTE')
from services.support_functions import build_port, get_token_for_admin, get_token_for_admin_in_project
from openstack_sdk import create_server

project_id = 'bccef51db1a549799aa755b32037e4f0'
#admin_token = get_token_for_admin()
token_for_project = get_token_for_admin_in_project(project_id)
#port_name = 'internet'
#network_id = 'db12c22a-e0f6-402a-a6fb-e10137a6adcf'

#p1 = build_port(token_for_project, port_name, network_id, project_id)
#port_id = p1['id']
#port_id = '76bf11ff-c5a1-43c8-a3c8-40f34de24af9'

vm = {
    "name": "computo1",
    "image": "fb75d039-fcca-4550-97f2-a7349a865386",
    "flavor": "a1850913-5c6b-4561-8c45-340ae4b614dd",
    "networks": []
}
ACCESS_NODE_IP = '10.20.10.113'
NOVA_PORT = '8774'
NOVA_ENDPOINT = 'http://' + ACCESS_NODE_IP + ':' + NOVA_PORT + '/v2.1'
r6 = create_server(NOVA_ENDPOINT, token_for_project, vm['name'], vm['flavor'], vm['image'], vm['networks'])
print(r6.status_code)
#if r6.status_code != 202:


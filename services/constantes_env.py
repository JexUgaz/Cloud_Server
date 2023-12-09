import os
from dotenv import load_dotenv

# Obtén la ruta al directorio padre (un nivel arriba)
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')

load_dotenv(dotenv_path)

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

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD= os.getenv("ADMIN_PASSWORD")
ADMIN_PROJECT_NAME= os.getenv("ADMIN_PROJECT_NAME")
# API SERVER ENDPOINT
SERVER_API_ENDPOINT = 'http://' + ACCESS_NODE_IP + ':' + SERVER_API_PORT # ------------------ DONE

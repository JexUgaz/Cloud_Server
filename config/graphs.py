import os
import platform
import subprocess
import tempfile
import networkx as nx
import matplotlib.pyplot as plt

from entities.VirtualMachineEntity import VirtualMachine

class GraphHelper:
    G = nx.Graph()  # crear un grafo
    
    @staticmethod
    def _showImage(title):
        fig, ax = plt.subplots(figsize=(8, 5))
        layout = nx.spring_layout(GraphHelper.G)  # Layout spring

        # Dibujar nodos como círculos con texto dentro
        node_colors = 'white'
        node_edge_colors = 'black'
        node_size = 800

        nx.draw_networkx_nodes(GraphHelper.G, layout, ax=ax, node_shape='o', node_color=node_colors, edgecolors=node_edge_colors, node_size=node_size)
        nx.draw_networkx_edges(GraphHelper.G, layout, ax=ax)

        # Colocar etiquetas en el centro de los círculos
        node_labels = {node: node for node in GraphHelper.G.nodes()}
        nx.draw_networkx_labels(GraphHelper.G, layout, labels=node_labels, ax=ax, font_size=10, verticalalignment='center', horizontalalignment='center')

        ax.set_title(f"Topología {title}")
        # Genera un nombre de archivo aleatorio
        temp_dir = tempfile.gettempdir()
        filename = os.path.join(temp_dir, next(tempfile._get_candidate_names()) + ".png")
        plt.savefig(filename)

        if platform.system() == "Windows":
            # Abrir el archivo PNG con el visor de imágenes predeterminado
            os.startfile(filename)  
        else:
            # Intenta abrir el archivo PNG con el visor de imágenes predeterminado en sistemas basados en Unix/Linux
            try:
                subprocess.Popen(["xdg-open", filename])
            except OSError as e:
                print(f"No se pudo abrir el visor de imágenes: {e}")
        GraphHelper.G.clear()
        return filename
    
    @staticmethod
    def drawAnillo(vms:list[VirtualMachine]):
        router_name = "Router"
        GraphHelper.G.add_node(router_name)
        num_vms=len(vms)
        vms = [f"VM{i + 1}" for i in range(num_vms)]

        for vm in vms:
            GraphHelper.G.add_node(vm)
            GraphHelper.G.add_edge(vm,router_name)

        for vm1, vm2 in zip(vms, vms[1:] + [vms[0]]):
            GraphHelper.G.add_edge(vm1, vm2)
        return GraphHelper._showImage("Anillo")


    @staticmethod
    def drawArbol(vms:list[VirtualMachine]):
        GraphHelper.G.add_node("Router")  # Nodo raíz
        switches = []
        num_vms=len(vms)

        for i in range((num_vms - 1) // 2 + 1):
            switch_name = f"Switch{i+1}"
            GraphHelper.G.add_node(switch_name)
            switches.append(switch_name)

        for switch in switches:
            GraphHelper.G.add_edge("Router", switch)

        for i in range(1, num_vms + 1):
            vm_name = vms[i-1].nombre
            switch_index = (i - 1) // 2
            switch_name = switches[switch_index]
            GraphHelper.G.add_node(vm_name)
            GraphHelper.G.add_edge(switch_name, vm_name)
        return GraphHelper._showImage("Arbol")







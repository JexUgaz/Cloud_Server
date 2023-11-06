import itertools
import networkx as nx
import matplotlib.pyplot as plt
G = nx.Graph()  # crear un grafo
num_vms=4
router_name = "Router"
G.add_node(router_name)


vms = [f"VM{i + 1}" for i in range(num_vms)]

for vm in vms:
   G.add_node(vm)

for vm1, vm2 in zip(vms, vms[1:] + [vms[0]]):
    G.add_edge(vm1, vm2)

for vm in vms:
    G.add_edge(vm,router_name)

fig, ax = plt.subplots(figsize=(8, 5))
layout = nx.spring_layout(G)  # Layout spring

# Dibujar nodos como círculos con texto dentro
node_colors = 'white'
node_edge_colors = 'black'
node_size = 800

nx.draw_networkx_nodes(G, layout, ax=ax, node_shape='o', node_color=node_colors, edgecolors=node_edge_colors, node_size=node_size)
nx.draw_networkx_edges(G, layout, ax=ax)

# Colocar etiquetas en el centro de los círculos
node_labels = {node: node for node in G.nodes()}
nx.draw_networkx_labels(G, layout, labels=node_labels, ax=ax, font_size=10, verticalalignment='center', horizontalalignment='center')

ax.set_title("Network Diagram")

plt.show()
################################
# IMPORTAR GRAFO
# G2 = nx.read_graphml("red.graphml")
#  EXPORTAR GRAFO
# G2 = nx.write_graphml("red.graphml")
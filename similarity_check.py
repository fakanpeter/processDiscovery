import xml.etree.ElementTree as ET

import networkx as nx
import matplotlib.pyplot as plt

from networkx.algorithms.similarity import graph_edit_distance

def convert_bpmn_to_graph(bpmn_path):
    tree = ET.parse(bpmn_path)
    root = tree.getroot()
    namespace = {'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL'}
    g = nx.Graph()

    for element in root.findall(".//*", namespace):
        tag_name = element.tag.split('}')[-1]
        if tag_name in {"task", "exclusiveGateway", "parallelGateway"}:
            node_id = element.get('id')
            node_name = element.get('name')
            if node_name == "":
                node_name = tag_name
            g.add_node(node_id, name=node_name, type=tag_name)
        elif tag_name == "sequenceFlow":
            source = element.get('sourceRef')
            target = element.get('targetRef')
            g.add_edge(source, target)


    return g

G_own = convert_bpmn_to_graph("models/discovered_model_szig_final_100_v3.bpmn")
G_idom = convert_bpmn_to_graph("models/discovered_model_szig_final_100_v2.bpmn")

# Gráf vizualizálása
plt.figure(figsize=(8,6))
pos = nx.spring_layout(G_own)
nx.draw(G_own, pos, with_labels=False, node_size=300, node_color="lightblue", font_size=1)
labels = nx.get_node_attributes(G_own, 'name')
nx.draw_networkx_labels(G_own, pos, labels=labels, font_size=8)
plt.title("Sajat log")
plt.show()

plt.figure(figsize=(8,6))
pos = nx.spring_layout(G_idom)
nx.draw(G_idom, pos, with_labels=False, node_size=300, node_color="lightblue", font_size=1)
labels = nx.get_node_attributes(G_idom, 'name')
nx.draw_networkx_labels(G_idom, pos, labels=labels, font_size=8)
plt.title("Idom log")
plt.show()

edit_distance = graph_edit_distance(G_own,G_idom, timeout = 300)
print(edit_distance)

#OPTIMIZE
# 130 v1 v2
# 201 idom v2
# 218 gepjaremu v2
# 120 v2  v2govonmly
# 201 v2govonly idom

#PLAIN 5 min
#200 gov_only idom
#201 v2 idom
#130 v1 v2
#216 v2 gepjarmu
#118 v2 govonly
#177 szig_teljes szig_happy_path
#208 idom_v2 szig_final_main
#325 idom_v2 gepjarmu_final_v2

#PLAIN UNDIRECTED 5MIN IDOM V2
#197
#195

#PLAIN UNDIRECTED 10MIN
#175 szig_teljes szig_happy_path

#PLAIN DIRECTED 7.5h
#173 szig_teljes szig_happy_path

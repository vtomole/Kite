import networkx as nx
from lexer import tokenize
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_node(1)
G.add_node(2)
G.add_edge(1, 2)
nx.draw(G)
plt.show()

tokenize("""/ quantum ripple-carry adder from Cuccaro et al, quant-ph/0410184
OPENQASM 2.0;
include "qelib1.inc";

qreg cin[1];
qreg a[4];
""")

print(nx.is_directed_acyclic_graph(G))

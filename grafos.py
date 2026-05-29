import networkx as nx
import matplotlib.pyplot as plt
from heapq import heapify, heappop, heappush

grafo = {
    "A": {"B": 3, "C": 3},
    "B": {"A": 3, "D": 3.5, "E": 2.8},
    "C": {"A": 3, "E": 2.8, "F": 3.5},
    "D": {"B": 3.5, "E": 3.1, "G": 10},
    "E": {"B": 2.8, "C": 2.8, "D": 3.1, "G": 7},
    "F": {"G": 2.5, "C": 3.5},
    "G": {"F": 2.5, "E": 7, "D": 10},
}   

class Grafo: 
    def __init__(self, grafo: dict = {}):
        self.grafo = grafo 

    def add_borda(self, nó1, nó2, peso):
        if nó1 not in self.grafo:
            self.grafo[nó1] = {}
        self.grafo[nó1][nó2] = peso 

    def menor_distancia(self, fonte: str ):    
        distancias = {nó: float("inf") for nó in self.grafo}
        distancias[fonte] = 0

        pq = [(0, fonte)]
        heapify(pq)

        visited = set()

        while pq:
            distancia_atual, nó_atual = heappop(pq)
            if nó_atual in visited:
                continue
            visited.add(nó_atual)
            
            for vizinhos, peso in self.grafo[nó_atual].items():
                tentativa_distancia = distancia_atual + peso
                if tentativa_distancia < distancias[vizinhos]:
                    distancias[vizinhos] = tentativa_distancia
                    heappush(pq, (tentativa_distancia, vizinhos))
    
        predecessores = {nó: None for nó in self.grafo}

        for nó, distancia in distancias.items():
            for vizinhos, peso in self.grafo[nó].items():
                if distancias[vizinhos] == distancia + peso:
                    predecessores[vizinhos] = nó

        return distancias, predecessores
    
    def caminho_maisCurto(self, fonte: str, alvo: str):
        _, predecessores = self.menor_distancia(fonte)

        caminho = []
        nó_atual = alvo

        while nó_atual:
            caminho.append(nó_atual)
            nó_atual = predecessores[nó_atual]

        caminho.reverse()
        return caminho
    


G_nx = nx.Graph()

for no_principal, dicionario_vizinhos in grafo.items():
    for vizinho, peso in dicionario_vizinhos.items():
        G_nx.add_edge(no_principal, vizinho, weight=peso)


G_custom = Grafo(grafo)
origem = "A"
destino = "G"
caminho = G_custom.caminho_maisCurto(origem, destino)

print(f"Caminho mais curto de {origem} até {destino}: {caminho}")

plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(8, 6))
pos = nx.spring_layout(G_nx, seed=42) 


arestas_caminho = list(zip(caminho, caminho[1:]))
cores_arestas = []
largura_arestas = []

for u, v in G_nx.edges():
    if (u, v) in arestas_caminho or (v, u) in arestas_caminho:
        cores_arestas.append("#FF3333")    
        largura_arestas.append(4.0)    
    else:
        cores_arestas.append("#555555")   
        largura_arestas.append(1.5)


nx.draw_networkx_nodes(G_nx, pos, node_color="#00FF00", node_size=700, ax=ax)

nx.draw_networkx_labels(G_nx, pos, font_size=12, font_color="black", font_weight="bold", ax=ax)

nx.draw_networkx_edges(G_nx, pos, edgelist=G_nx.edges(), edge_color=cores_arestas, width=largura_arestas, ax=ax)

labels_pesos = nx.get_edge_attributes(G_nx, "weight")
nx.draw_networkx_edge_labels(G_nx, pos, edge_labels=labels_pesos, font_size=10, font_color="white", bbox=dict(facecolor='black', edgecolor='none', alpha=0.7))

plt.title(f"Grafo - Caminho mais curto de {origem} até {destino}", color="white", fontsize=14)
plt.axis("off")
plt.show()







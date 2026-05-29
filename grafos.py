import networkx as nx
import matplotlib.pyplot as plt
from heapq import heapify, heappop, heappush

plt.style.use('dark_background')

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
        self.grafo = grafo #Dicionario para a lista de adjacencias

    def add_borda(self, no1, no2, peso): #Método para adicionar conexão entre dois nós
        if no1 not in self.grafo: #Verifica se o nó ja foi adicionado
            self.grafo[no1] = {} #Cria o node
        self.grafo[no1][no2] = peso #Se não, adiciona a conexão

    def menor_distancia(self, fonte: str ):    
        #Passa o valor de todos os nós como infinito
        distancias = {nó: float("inf") for nó in self.grafo}
        distancias[fonte] = 0 # Seta o valor pra 0
        
        #Fila de prioridade
        pq = [(0, fonte)]
        heapify(pq)
        #Um set pra nós ja visitados
        visited = set()
        #Enquanto a fila de prioridade não esta vazia
        while pq:
            distancia_atual, no_atual = heappop(pq) # pega o nó com a menor distancia
            if no_atual in visited:
                continue #Se ele ja foi visitado continua
            visited.add(no_atual) #Se não adiciona o nó ao set
            
            for vizinhos, peso in self.grafo[no_atual].items(): 
                #Calcula a distancia do nó atual para o vizinho
                tentativa_distancia = distancia_atual + peso
                if tentativa_distancia < distancias[vizinhos]:
                    distancias[vizinhos] = tentativa_distancia
                    heappush(pq, (tentativa_distancia, vizinhos)) #Adiciona os elementos a fila com a prioridade associada.
    
        predecessores = {no: None for no in self.grafo} #Dicionario de predecessores

        for no, distancia in distancias.items(): 
            #Quando o código é executado, o dicionário predecessoress contém o 
            # pai imediato de cada nó envolvido no caminho mais curto para a origem.
            for vizinhos, peso in self.grafo[no].items():
                if distancias[vizinhos] == distancia + peso:
                    predecessores[vizinhos] = no

        return distancias, predecessores
    
    def menor_caminho(self, fonte: str, alvo: str):
        #Gera o dicionario de predecessores
        _, predecessores = self.menor_distancia(fonte)

        caminho = []
        no_atual = alvo
        # Retroceder a partir do nó alvo usando predecessores
        while no_atual:
            caminho.append(no_atual)
            no_atual = predecessores[no_atual]
        # Reverte o caminho, pois o algoritmo traz o caminho de trás pra frente
        caminho.reverse()
        return caminho
    


G_nx = nx.Graph()

for no_principal, dicionario_vizinhos in grafo.items():
    for vizinho, peso in dicionario_vizinhos.items():
        G_nx.add_edge(no_principal, vizinho, weight=peso)

# Criar o grafo no NetworkX
G_custom = Grafo(grafo)
origem = "A"
destino = "G"
caminho = G_custom.menor_caminho(origem, destino)

print(f"Caminho mais curto de {origem} até {destino}: {caminho}")


# Configura e desenha o gráfico
fig, ax = plt.subplots(figsize=(8, 6))
pos = nx.spring_layout(G_nx, seed=42) 

# Configura o destaque do caminho mais curto
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

# Desenha os nós
nx.draw_networkx_nodes(G_nx, pos, node_color="#00FF00", node_size=700, ax=ax)
# Desenha as letras
nx.draw_networkx_labels(G_nx, pos, font_size=12, font_color="black", font_weight="bold", ax=ax)
# Desenha as linhas
nx.draw_networkx_edges(G_nx, pos, edgelist=G_nx.edges(), edge_color=cores_arestas, width=largura_arestas, ax=ax)
# Desenha os números
labels_pesos = nx.get_edge_attributes(G_nx, "weight")
# O 'bbox' cria uma caixinha preta atrás do número para ele não sumir na linha
nx.draw_networkx_edge_labels(G_nx, pos, edge_labels=labels_pesos, font_size=10, font_color="white", bbox=dict(facecolor='black', edgecolor='none', alpha=0.7))

plt.title(f"Grafo - Caminho mais curto de {origem} até {destino}", color="white", fontsize=14)
plt.axis("off")
plt.show()
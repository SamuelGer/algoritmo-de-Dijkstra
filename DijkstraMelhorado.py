import networkx as nx
import matplotlib.pyplot as plt
from heapq import heappop, heappush

# 1. Ativar o modo de fundo escuro global do Matplotlib
plt.style.use('dark_background')

# O seu dicionário de dados original
dados_grafo = {
    "A": {"B": 3, "C": 3},
    "B": {"A": 3, "D": 3.5, "E": 2.8},
    "C": {"A": 3, "E": 2.8, "F": 3.5},
    "D": {"B": 3.5, "E": 3.1, "G": 10},
    "E": {"B": 2.8, "C": 2.8, "D": 3.1, "G": 7},
    "F": {"G": 2.5, "C": 3.5},
    "G": {"F": 2.5, "E": 7, "D": 10},
}   

class GrafoOtimizado: 
    def __init__(self, grafo: dict = None):
        # Evita o problema de argumento mutável padrão do Python
        self.grafo = grafo if grafo is not None else {}

    def add_borda(self, nó1, nó2, peso):
        if nó1 not in self.grafo:
            self.grafo[nó1] = {}
        self.grafo[nó1][nó2] = peso 

    def caminho_mais_curto(self, fonte: str, alvo: str):    
        #Calcula o caminho mais curto de forma 100% iterativa (sem recursão).
        # Ideal para performance e escalabilidade em grafos maiores.
        
        # Inicializa distâncias com infinito e predecessores vazios
        distancias = {nó: float("inf") for nó in self.grafo}
        predecessores = {nó: None for nó in self.grafo}
        
        distancias[fonte] = 0
        pq = [(0, fonte)] # Fila de prioridades guardando: (distancia, nó)
        visited = set()

        while pq:
            distancia_atual, nó_atual = heappop(pq)
            # Otimização crucial: se chegamos ao alvo, paramos o algoritmo mais cedo
            if nó_atual == alvo:
                break
                
            if nó_atual in visited:
                continue
            visited.add(nó_atual)
            
            for vizinho, peso in self.grafo[nó_atual].items(): 
                # pega cada nó vizinho ligado diretamente ao seu nó atual e o custo
                if vizinho in visited:
                    continue
                #Soma simples da distancia ja percorrida + o peso/custo ate o próximo nó    
                distancia_candidata = distancia_atual + peso

                if distancia_candidata < distancias[vizinho]:
                    distancias[vizinho] = distancia_candidata
                    # Guarda o "pai" do nó de forma iterativa no momento da descoberta
                    predecessores[vizinho] = nó_atual
                    heappush(pq, (distancia_candidata, vizinho))
    
        # Reconstrução do caminho de trás para frente usando um laço while (iterativo)
        caminho = []
        nó_passo = alvo
        while nó_passo is not None:
            caminho.append(nó_passo)
            nó_passo = predecessores[nó_passo]
        
        caminho.reverse()
        
        # Validação caso o nó de destino seja completamente inacessível
        if caminho[0] != fonte:
            return [], float("inf")
            
        return caminho, distancias[alvo]


# Definir os pontos de busca
origem = "A"
destino = "G"

# Instanciar e rodar o nosso algoritmo iterativo baseado na sua estrutura
G_custom = GrafoOtimizado(dados_grafo)
caminho, distancia_total = G_custom.caminho_mais_curto(origem, destino)
#Resultado do dijkstra
print(f"Caminho mais curto de {origem} até {destino}: {caminho}")
print(f"Distância total: {distancia_total}\n")

# Alimentar e gerar o Objeto do NetworkX ANTES de qualquer desenho
G_nx = nx.Graph()
for nó_principal, dicionario_vizinhos in dados_grafo.items():
    for vizinho, peso in dicionario_vizinhos.items():
        G_nx.add_edge(nó_principal, vizinho, weight=peso)

# Preparar a plotagem do gráfico com o Matplotlib (Estilo Dark)
fig, ax = plt.subplots(figsize=(9, 7))
pos = nx.spring_layout(G_nx, seed=42) # Mantém os nós na mesma posição a cada execução

# Mapeia e colorir as arestas baseando-se no caminho que encontramos
arestas_caminho_visto = list(zip(caminho, caminho[1:]))
cores_arestas = []
largura_arestas = []

for u, v in G_nx.edges():
    # Verifica se a aresta atual faz parte do caminho calculado (em qualquer sentido)
    if (u, v) in arestas_caminho_visto or (v, u) in arestas_caminho_visto:
        cores_arestas.append("#FF3333") 
        largura_arestas.append(4.0)
    else:
        cores_arestas.append("#444444") 
        largura_arestas.append(1.5)

# Renderização Visual no painel do Matplotlib
# Desenha os círculos dos nós
nx.draw_networkx_nodes(G_nx, pos, node_color="#00FF00", node_size=800, ax=ax)

# Desenha as letras textuais internas dos nós
nx.draw_networkx_labels(G_nx, pos, font_size=12, font_color="black", font_weight="bold", ax=ax)

# Desenha as linhas das conexões (arestas)
nx.draw_networkx_edges(G_nx, pos, edgelist=G_nx.edges(), edge_color=cores_arestas, width=largura_arestas, ax=ax)

# Desenha os números de peso em cima das linhas com uma caixinha preta de fundo para não embolar
labels_pesos = nx.get_edge_attributes(G_nx, "weight")
nx.draw_networkx_edge_labels(
    G_nx, pos, edge_labels=labels_pesos, font_size=10, font_color="#FFFFFF",
    bbox=dict(facecolor='#000000', edgecolor='none', alpha=0.7)
)

# Título e finalização da janela
plt.title(f"Grafo - Menor Caminho de {origem} até {destino} (Tema Escuro)", color="white", fontsize=14, pad=20)
plt.axis("off") # Oculta as coordenadas dos eixos X e Y cartesianos
plt.show()
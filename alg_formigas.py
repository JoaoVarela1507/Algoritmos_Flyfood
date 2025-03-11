import numpy as np
import math
import matplotlib.pyplot as plt
import random

class Formiga:
    def __init__(self, aco, grafo):
        self.aco = aco
        self.grafo = grafo
        
        self.custo_total = 0.0
        self.tabu = []  
        self.delta_feromonio = np.zeros((grafo.rank, grafo.rank))
        self.nos_permitidos = list(range(grafo.rank))  
    
    def seleciona_proximo(self):
        no_atual = self.tabu[-1] if self.tabu else 0  
        probabilidades = []
        
        for i in self.nos_permitidos:
            numerador = (self.grafo.matriz_feromonio[no_atual][i] ** self.aco.alpha) * \
                       ((1.0 / self.grafo.matriz_custos[no_atual][i]) ** self.aco.beta)
            probabilidades.append(numerador)
        
        soma = sum(probabilidades)
        if soma == 0:
            return random.choice(self.nos_permitidos)
        
        probabilidades = [p / soma for p in probabilidades]
        
        r = random.random()
        acumulado = 0
        for i, prob in zip(self.nos_permitidos, probabilidades):
            acumulado += prob
            if r <= acumulado:
                return i
        
        return self.nos_permitidos[0]
    
    def atualiza_delta_feromonio(self):
        self.delta_feromonio = np.zeros((self.grafo.rank, self.grafo.rank))
        
        for i in range(len(self.tabu) - 1):
            atual = self.tabu[i]
            proximo = self.tabu[i + 1]
            
            if self.aco.estrategia == 1:
                self.delta_feromonio[atual][proximo] = self.aco.Q
                self.delta_feromonio[proximo][atual] = self.aco.Q  
            
            elif self.aco.estrategia == 2:
                distancia = self.grafo.matriz_custos[atual][proximo]
                self.delta_feromonio[atual][proximo] = self.aco.Q / distancia
                self.delta_feromonio[proximo][atual] = self.aco.Q / distancia  
            
            else:
                self.delta_feromonio[atual][proximo] = self.aco.Q / self.custo_total
                self.delta_feromonio[proximo][atual] = self.aco.Q / self.custo_total  


class Grafo:
    def __init__(self, matriz_custos, rank):
        self.matriz_custos = matriz_custos
        self.rank = rank
        self.matriz_feromonio = [[0.1 for _ in range(rank)] for _ in range(rank)]


class ACO:
    def __init__(self, quantidade_formigas, geracoes, alpha, beta, rho, Q, estrategia):
        self.quantidade_formigas = quantidade_formigas
        self.geracoes = geracoes
        self.alpha = alpha  
        self.beta = beta    
        self.rho = rho      
        self.Q = Q          
        self.estrategia = estrategia  
    
    def atualiza_feromonio(self, grafo, formigas):
        for i in range(grafo.rank):
            for j in range(grafo.rank):
                grafo.matriz_feromonio[i][j] *= (1 - self.rho)
                
                for formiga in formigas:
                    grafo.matriz_feromonio[i][j] += formiga.delta_feromonio[i][j]
    
    def resolver(self, grafo):
        melhor_custo = float('inf')
        melhor_solucao = []
        
        for geracao in range(self.geracoes):
            formigas = []
            
            for _ in range(self.quantidade_formigas):
                formiga = Formiga(self, grafo)
                
                no_inicial = random.randint(0, grafo.rank - 1)
                formiga.tabu.append(no_inicial)
                formiga.nos_permitidos.remove(no_inicial)
                
                while formiga.nos_permitidos:
                    proximo = formiga.seleciona_proximo()
                    formiga.custo_total += grafo.matriz_custos[formiga.tabu[-1]][proximo]
                    formiga.tabu.append(proximo)
                    formiga.nos_permitidos.remove(proximo)
                
                formiga.custo_total += grafo.matriz_custos[formiga.tabu[-1]][formiga.tabu[0]]
                
                if formiga.custo_total < melhor_custo:
                    melhor_custo = formiga.custo_total
                    melhor_solucao = formiga.tabu.copy()
                
                formiga.atualiza_delta_feromonio()
                formigas.append(formiga)
            
            self.atualiza_feromonio(grafo, formigas)
            
            print(f"Geração {geracao+1}/{self.geracoes}, Melhor custo: {melhor_custo}")
        
        return melhor_solucao, melhor_custo


def distancia(cidade1, cidade2):
    return math.sqrt((cidade1[0] - cidade2[0])**2 + (cidade1[1] - cidade2[1])**2)


def principal():
    cidades = [
        (0, 0),    
        (1, 5),    
        (5, 2),    
        (9, 8),    
        (4, 12),   
        (12, 6),   
        (8, 1),    
        (3, 6)     
    ]
    
    num_cidades = len(cidades)
    matriz_custos = [[0 for _ in range(num_cidades)] for _ in range(num_cidades)]
    
    for i in range(num_cidades):
        for j in range(num_cidades):
            if i != j:
                matriz_custos[i][j] = distancia(cidades[i], cidades[j])
            else:
                matriz_custos[i][j] = 0.001  
    
    aco = ACO(
        quantidade_formigas=10,
        geracoes=100,
        alpha=1.0,     
        beta=2.0,      
        rho=0.5,       
        Q=100,         
        estrategia=2   
    )
    
    grafo = Grafo(matriz_custos, num_cidades)
    
    melhor_solucao, melhor_custo = aco.resolver(grafo)
    
    print(f"Melhor custo: {melhor_custo}")
    print(f"Melhor rota: {melhor_solucao}")
    
    plt.figure(figsize=(10, 6))
    
    x = [cidades[i][0] for i in range(num_cidades)]
    y = [cidades[i][1] for i in range(num_cidades)]
    plt.scatter(x, y, s=100, color='blue')
    
    for i in range(num_cidades):
        plt.text(x[i], y[i], f' {i}', fontsize=12)
    
    for i in range(len(melhor_solucao)):
        j = (i + 1) % len(melhor_solucao)
        cidade1 = cidades[melhor_solucao[i]]
        cidade2 = cidades[melhor_solucao[j]]
        plt.plot([cidade1[0], cidade2[0]], [cidade1[1], cidade2[1]], 'r-')
    
    plt.title(f'Problema do Caixeiro Viajante - Custo: {melhor_custo:.2f}')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    principal()

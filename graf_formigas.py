import matplotlib.pyplot as plt
import numpy as np
from alg_formigas import *
import random
from ler_arquivo_tsp import ler_arquivo_tsp

# cidades = ler_arquivo_tsp("tsp/berlin52.tsp")
cidades = ler_arquivo_tsp("tsp/bier127.tsp")

def principal():
    
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
    
    evolucao_custo = []
    
    def resolver_com_evolucao(aco, grafo):
        melhor_custo = float('inf')
        melhor_solucao = []
        
        for geracao in range(aco.geracoes):
            formigas = []
            
            for _ in range(aco.quantidade_formigas):
                formiga = Formiga(aco, grafo)
                
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
            
            aco.atualiza_feromonio(grafo, formigas)
            evolucao_custo.append(melhor_custo)
            
            print(f"Geração {geracao+1}/{aco.geracoes}, Melhor custo: {melhor_custo}")
        
        return melhor_solucao, melhor_custo
    
    melhor_solucao, melhor_custo = resolver_com_evolucao(aco, grafo)
    
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
    
    plt.title(f'Rota Otimizada - Custo: {melhor_custo:.2f}')
    plt.grid(True)
    plt.show()
    
    plt.figure(figsize=(10, 6))
    plt.plot(evolucao_custo, marker='o', linestyle='-', color='b')
    plt.title('Evolução do Custo ao Longo das Gerações')
    plt.xlabel('Geração')
    plt.ylabel('Melhor Custo')
    plt.grid(True)
    plt.show()
    
    plt.figure(figsize=(10, 6))
    plt.imshow(grafo.matriz_feromonio, cmap='hot', interpolation='nearest')
    plt.colorbar(label='Intensidade do Feromônio')
    plt.title('Matriz de Feromônios')
    plt.show()
    
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, s=100, color='blue')
    for i in range(num_cidades):
        plt.text(x[i], y[i], f' {i}', fontsize=12)
    plt.title('Distribuição das Cidades')
    plt.grid(True)
    plt.show()
    
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, s=100, color='blue')
    for i in range(num_cidades):
        plt.text(x[i], y[i], f' {i}', fontsize=12)
    
    for i in range(len(melhor_solucao)):
        j = (i + 1) % len(melhor_solucao)
        cidade1 = cidades[melhor_solucao[i]]
        cidade2 = cidades[melhor_solucao[j]]
        espessura = grafo.matriz_feromonio[melhor_solucao[i]][melhor_solucao[j]] * 10
        plt.plot([cidade1[0], cidade2[0]], [cidade1[1], cidade2[1]], 'r-', linewidth=espessura)
    
    plt.title('Rota Otimizada com Destaque para Arestas Mais Utilizadas')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    principal()
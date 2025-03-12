import random
import math
import numpy as np
import matplotlib.pyplot as plt
import time
from ler_arquivo_tsp import ler_arquivo_tsp

def calcular_distancia(ponto1, ponto2):
    return math.sqrt((ponto1[0] - ponto2[0])**2 + (ponto1[1] - ponto2[1])**2)

def calcular_percurso_total(percurso, cidades):
    distancia_total = 0
    for i in range(len(percurso) - 1):
        cidade_atual = cidades[percurso[i]]
        proxima_cidade = cidades[percurso[i + 1]]
        distancia_total += calcular_distancia(cidade_atual, proxima_cidade)
    distancia_total += calcular_distancia(cidades[percurso[-1]], cidades[percurso[0]])
    return distancia_total

def resolver_caixeiro_viajante_guloso(cidades, cidade_inicial=0):
    inicio = time.time()
    
    n = len(cidades)
    percurso = [cidade_inicial]
    cidades_nao_visitadas = set(range(n))
    cidades_nao_visitadas.remove(cidade_inicial)
    
    etapas = []
    etapas.append(list(percurso))  
    
    while cidades_nao_visitadas:
        cidade_atual = percurso[-1]
        
        cidade_mais_proxima = None
        menor_distancia = float('inf')
        
        for proxima_cidade in cidades_nao_visitadas:
            dist = calcular_distancia(cidades[cidade_atual], cidades[proxima_cidade])
            if dist < menor_distancia:
                menor_distancia = dist
                cidade_mais_proxima = proxima_cidade
        
        percurso.append(cidade_mais_proxima)
        cidades_nao_visitadas.remove(cidade_mais_proxima)
        
        etapas.append(list(percurso))
    
    fim = time.time()
    tempo_execucao = fim - inicio
    
    distancia_total = calcular_percurso_total(percurso, cidades)
    
    print(f"Tempo de execução: {tempo_execucao:.6f} segundos")
    
    return percurso, distancia_total, etapas

def plotar_cidades(cidades, titulo="Distribuição das Cidades"):
    x = [cidade[0] for cidade in cidades]
    y = [cidade[1] for cidade in cidades]
    
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, s=100, c='blue', edgecolor='black')

    for i, (x_i, y_i) in enumerate(zip(x, y)):
        plt.annotate(f"Cidade {i}", (x_i, y_i), 
                     xytext=(5, 5), textcoords='offset points')
    
    plt.title(titulo)
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.grid(True)
    plt.show()

def plotar_percurso(cidades, percurso, titulo="Percurso Encontrado pelo Algoritmo Guloso"):

    percurso_completo = list(percurso) + [percurso[0]]
    
    x = [cidades[i][0] for i in percurso_completo]
    y = [cidades[i][1] for i in percurso_completo]
    
    plt.figure(figsize=(10, 6))
    
    plt.scatter([cidade[0] for cidade in cidades], 
                [cidade[1] for cidade in cidades], 
                s=100, c='blue', edgecolor='black', zorder=2)
    
    plt.plot(x, y, 'r-', linewidth=1.5, zorder=1)
    
    plt.scatter(x[0], y[0], s=150, c='green', edgecolor='black', zorder=3)
    
    for i, cidade in enumerate(cidades):
        plt.annotate(f"Cidade {i}", cidade, 
                     xytext=(5, 5), textcoords='offset points')
    
    for i in range(len(percurso_completo) - 1):
        meio_x = (x[i] + x[i+1]) / 2
        meio_y = (y[i] + y[i+1]) / 2
        
        # Calcula direção
        dx = x[i+1] - x[i]
        dy = y[i+1] - y[i]
        

        plt.arrow(meio_x - dx/8, meio_y - dy/8, dx/20, dy/20, 
                 head_width=2, head_length=2, fc='black', ec='black', zorder=4)
    
    plt.title(f"{titulo}\nDistância Total: {calcular_percurso_total(percurso, cidades):.2f}")
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.grid(True)
    plt.show()

def visualizar_construcao_percurso(cidades, etapas, intervalo=0.5):
    plt.figure(figsize=(12, 8))
    

    x_cidades = [cidade[0] for cidade in cidades]
    y_cidades = [cidade[1] for cidade in cidades]
    plt.scatter(x_cidades, y_cidades, s=100, c='blue', edgecolor='black')
    

    for i, cidade in enumerate(cidades):
        plt.annotate(f"Cidade {i}", cidade, xytext=(5, 5), textcoords='offset points')
    
    plt.title("Construção do Percurso - Algoritmo Guloso")
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.grid(True)
    

    for etapa_idx, percurso_atual in enumerate(etapas):
        if etapa_idx > 0:  

            idx1 = percurso_atual[-2]  
            idx2 = percurso_atual[-1]  
            
            x = [cidades[idx1][0], cidades[idx2][0]]
            y = [cidades[idx1][1], cidades[idx2][1]]
            
            plt.plot(x, y, 'r-', linewidth=1.5)
            
 
            plt.scatter([cidades[idx2][0]], [cidades[idx2][1]], s=150, 
                       c='red', edgecolor='black', zorder=3)
            
  
            meio_x = (x[0] + x[1]) / 2
            meio_y = (y[0] + y[1]) / 2
            dx = x[1] - x[0]
            dy = y[1] - y[0]
            plt.arrow(meio_x - dx/8, meio_y - dy/8, dx/20, dy/20, 
                     head_width=2, head_length=2, fc='black', ec='black')
            

            plt.title(f"Construção do Percurso - Algoritmo Guloso\n"
                     f"Etapa {etapa_idx}/{len(etapas)-1}: Adicionada Cidade {idx2}")
            
            plt.pause(intervalo)  
    
    cidade_inicial = etapas[0][0]
    cidade_final = etapas[-1][-1]
    
    x = [cidades[cidade_final][0], cidades[cidade_inicial][0]]
    y = [cidades[cidade_final][1], cidades[cidade_inicial][1]]
    
    plt.plot(x, y, color='r', linestyle='--', linewidth=1.5)  
    
    meio_x = (x[0] + x[1]) / 2
    meio_y = (y[0] + y[1]) / 2
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    plt.arrow(meio_x - dx/8, meio_y - dy/8, dx/20, dy/20, 
             head_width=2, head_length=2, fc='black', ec='black')
    
    plt.title(f"Percurso Completo - Algoritmo Guloso\n"
             f"Distância Total: {calcular_percurso_total(etapas[-1], cidades):.2f}")
    
    plt.show()

def main():
 
    cidade = ler_arquivo_tsp("tsp/berlin52.tsp")
    # cidade = ler_arquivo_tsp("tsp/bier127.tsp")

    plotar_cidades(cidade, titulo="Distribuição das Cidades")
    
    print("\nResolvendo com algoritmo guloso...")
    percurso, distancia, etapas = resolver_caixeiro_viajante_guloso(cidade)
    
    print(f"Percurso encontrado: {percurso}")
    print(f"Distância total: {distancia:.2f} unidades")
    
    plotar_percurso(cidade, percurso, titulo="Percurso Encontrado pelo Algoritmo Guloso")
    
    visualizar_construcao_percurso(cidade, etapas, intervalo=0.8)

if __name__ == "__main__":
    main()
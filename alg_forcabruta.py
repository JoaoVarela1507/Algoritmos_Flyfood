import random
import math
import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations
import time

def calcular_distancia(ponto1, ponto2):
    """
    Calcula a distância euclidiana entre dois pontos.
    
    Args:
        ponto1 (tuple): Coordenadas (x, y) do primeiro ponto
        ponto2 (tuple): Coordenadas (x, y) do segundo ponto
    
    Returns:
        float: Distância entre os pontos
    """
    return math.sqrt((ponto1[0] - ponto2[0])**2 + (ponto1[1] - ponto2[1])**2)

def calcular_percurso_total(percurso, cidades):
    """
    Calcula a distância total percorrida em um percurso.
    
    Args:
        percurso (list): Lista de índices das cidades no percurso
        cidades (list): Lista de coordenadas das cidades
    
    Returns:
        float: Distância total do percurso
    """
    distancia_total = 0
    for i in range(len(percurso) - 1):
        cidade_atual = cidades[percurso[i]]
        proxima_cidade = cidades[percurso[i + 1]]
        distancia_total += calcular_distancia(cidade_atual, proxima_cidade)
    
    # Adiciona a distância de volta à cidade inicial para completar o ciclo
    distancia_total += calcular_distancia(cidades[percurso[-1]], cidades[percurso[0]])
    
    return distancia_total

def gerar_cidades_aleatorias(n, min_coord=0, max_coord=100):
    """
    Gera n cidades com coordenadas aleatórias.
    
    Args:
        n (int): Número de cidades
        min_coord (float): Valor mínimo para coordenadas
        max_coord (float): Valor máximo para coordenadas
    
    Returns:
        list: Lista de tuplas (x, y) representando as coordenadas das cidades
    """
    return [(random.uniform(min_coord, max_coord), 
             random.uniform(min_coord, max_coord)) 
            for _ in range(n)]

def resolver_caixeiro_viajante_forca_bruta(cidades):
    """
    Resolve o problema do caixeiro viajante usando força bruta.
    
    Args:
        cidades (list): Lista de coordenadas (x, y) das cidades
    
    Returns:
        tuple: Melhor percurso e distância total mínima
    """
    indices_cidades = list(range(len(cidades)))
    
    menor_distancia = float('inf')
    melhor_percurso = None
    total_permutacoes = math.factorial(len(cidades))
    permutacoes_verificadas = 0
    
    print(f"Calculando {total_permutacoes} permutações possíveis...")
    inicio = time.time()
    
    for permutacao in permutations(indices_cidades):
        distancia = calcular_percurso_total(permutacao, cidades)
        
        if distancia < menor_distancia:
            menor_distancia = distancia
            melhor_percurso = permutacao
        
        permutacoes_verificadas += 1
        if permutacoes_verificadas % 10000 == 0:
            tempo_decorrido = time.time() - inicio
            print(f"Progresso: {permutacoes_verificadas}/{total_permutacoes} permutações verificadas "
                  f"({(permutacoes_verificadas/total_permutacoes)*100:.2f}%), "
                  f"Tempo: {tempo_decorrido:.2f}s")
    
    fim = time.time()
    print(f"Tempo total de execução: {fim - inicio:.2f} segundos")
    
    return melhor_percurso, menor_distancia

def plotar_cidades(cidades, titulo="Distribuição das Cidades"):
    """
    Plota as cidades em um gráfico de dispersão.
    
    Args:
        cidades (list): Lista de coordenadas (x, y) das cidades
        titulo (str): Título do gráfico
    """
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

def plotar_percurso(cidades, percurso, titulo="Melhor Percurso Encontrado"):
    """
    Plota o percurso encontrado.
    
    Args:
        cidades (list): Lista de coordenadas (x, y) das cidades
        percurso (list): Lista de índices das cidades no percurso
        titulo (str): Título do gráfico
    """
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
        
        dx = x[i+1] - x[i]
        dy = y[i+1] - y[i]
        
        plt.arrow(meio_x - dx/8, meio_y - dy/8, dx/20, dy/20, 
                  head_width=2, head_length=2, fc='black', ec='black', zorder=4)
    
    plt.title(f"{titulo}\nDistância Total: {calcular_percurso_total(percurso, cidades):.2f}")
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.grid(True)
    plt.show()

def comparar_tempos_execucao():
    """
    Compara o tempo de execução do algoritmo para diferentes números de cidades.
    Plota um gráfico de tempo de execução vs. número de cidades.
    """
    num_cidades = list(range(3, 11))
    tempos_execucao = []
    
    for n in num_cidades:
        cidades = gerar_cidades_aleatorias(n)
        
        inicio = time.time()
        resolver_caixeiro_viajante_forca_bruta(cidades)
        fim = time.time()
        
        tempo = fim - inicio
        tempos_execucao.append(tempo)
        print(f"Tempo para {n} cidades: {tempo:.4f} segundos")
    
    base_n = 3
    base_tempo = tempos_execucao[0]
    tempos_teoricos = [base_tempo * math.factorial(n) / math.factorial(base_n) for n in num_cidades]
    
    plt.figure(figsize=(12, 6))
    plt.plot(num_cidades, tempos_execucao, 'bo-', label='Tempo Real')
    plt.plot(num_cidades, tempos_teoricos, 'r--', label='Crescimento Teórico O(n!)')
    
    plt.yscale('log')
    plt.title('Tempo de Execução vs. Número de Cidades')
    plt.xlabel('Número de Cidades')
    plt.ylabel('Tempo (segundos) - Escala Logarítmica')
    plt.grid(True)
    plt.legend()
    plt.show()

def main():
    random.seed(42)
    
    num_cidades = 8
    
    cidades = gerar_cidades_aleatorias(num_cidades, 0, 100)
    
    plotar_cidades(cidades)
    
    percurso, distancia = resolver_caixeiro_viajante_forca_bruta(cidades)
    
    print(f"\nMelhor percurso encontrado: {percurso}")
    print(f"Distância total: {distancia:.2f} unidades")
    
    plotar_percurso(cidades, percurso)
    
    resposta = input("\nDeseja fazer uma comparação de tempos de execução? (s/n): ")
    if resposta.lower() == 's':
        comparar_tempos_execucao()

if __name__ == "__main__":
    main()

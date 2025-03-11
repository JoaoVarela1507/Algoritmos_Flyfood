import random
import math
import numpy as np
import matplotlib.pyplot as plt
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

def resolver_caixeiro_viajante_guloso(cidades, cidade_inicial=0):
    """
    Resolve o problema do caixeiro viajante usando algoritmo guloso
    (sempre escolhe a cidade mais próxima ainda não visitada).
    
    Args:
        cidades (list): Lista de coordenadas (x, y) das cidades
        cidade_inicial (int): Índice da cidade de início
    
    Returns:
        tuple: Percurso construído e distância total
    """
    inicio = time.time()
    
    n = len(cidades)
    percurso = [cidade_inicial]
    cidades_nao_visitadas = set(range(n))
    cidades_nao_visitadas.remove(cidade_inicial)
    
    # Para visualização: salvar etapas do processo
    etapas = []
    etapas.append(list(percurso))  # Estado inicial
    
    # Enquanto houver cidades não visitadas
    while cidades_nao_visitadas:
        cidade_atual = percurso[-1]
        
        # Encontrar a cidade mais próxima não visitada
        cidade_mais_proxima = None
        menor_distancia = float('inf')
        
        for proxima_cidade in cidades_nao_visitadas:
            dist = calcular_distancia(cidades[cidade_atual], cidades[proxima_cidade])
            if dist < menor_distancia:
                menor_distancia = dist
                cidade_mais_proxima = proxima_cidade
        
        # Adicionar a cidade mais próxima ao percurso
        percurso.append(cidade_mais_proxima)
        cidades_nao_visitadas.remove(cidade_mais_proxima)
        
        # Salvar esta etapa para visualização
        etapas.append(list(percurso))
    
    fim = time.time()
    tempo_execucao = fim - inicio
    
    # Calcular a distância total
    distancia_total = calcular_percurso_total(percurso, cidades)
    
    print(f"Tempo de execução: {tempo_execucao:.6f} segundos")
    
    return percurso, distancia_total, etapas

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
    
    # Adiciona rótulos às cidades
    for i, (x_i, y_i) in enumerate(zip(x, y)):
        plt.annotate(f"Cidade {i}", (x_i, y_i), 
                     xytext=(5, 5), textcoords='offset points')
    
    plt.title(titulo)
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.grid(True)
    plt.show()

def plotar_percurso(cidades, percurso, titulo="Percurso Encontrado pelo Algoritmo Guloso"):
    """
    Plota o percurso encontrado.
    
    Args:
        cidades (list): Lista de coordenadas (x, y) das cidades
        percurso (list): Lista de índices das cidades no percurso
        titulo (str): Título do gráfico
    """
    # Adiciona o primeiro ponto ao final para fechar o ciclo
    percurso_completo = list(percurso) + [percurso[0]]
    
    # Extrai as coordenadas x e y
    x = [cidades[i][0] for i in percurso_completo]
    y = [cidades[i][1] for i in percurso_completo]
    
    plt.figure(figsize=(10, 6))
    
    # Plota as cidades
    plt.scatter([cidade[0] for cidade in cidades], 
                [cidade[1] for cidade in cidades], 
                s=100, c='blue', edgecolor='black', zorder=2)
    
    # Plota o percurso
    plt.plot(x, y, 'r-', linewidth=1.5, zorder=1)
    
    # Destaca a cidade inicial/final
    plt.scatter(x[0], y[0], s=150, c='green', edgecolor='black', zorder=3)
    
    # Adiciona rótulos às cidades
    for i, cidade in enumerate(cidades):
        plt.annotate(f"Cidade {i}", cidade, 
                     xytext=(5, 5), textcoords='offset points')
    
    # Adiciona setas para indicar direção
    for i in range(len(percurso_completo) - 1):
        # Calcula posição da seta (meio do caminho)
        meio_x = (x[i] + x[i+1]) / 2
        meio_y = (y[i] + y[i+1]) / 2
        
        # Calcula direção
        dx = x[i+1] - x[i]
        dy = y[i+1] - y[i]
        
        # Adiciona pequena seta
        plt.arrow(meio_x - dx/8, meio_y - dy/8, dx/20, dy/20, 
                 head_width=2, head_length=2, fc='black', ec='black', zorder=4)
    
    plt.title(f"{titulo}\nDistância Total: {calcular_percurso_total(percurso, cidades):.2f}")
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.grid(True)
    plt.show()

def visualizar_construcao_percurso(cidades, etapas, intervalo=0.5):
    """
    Cria uma visualização animada da construção do percurso pelo algoritmo guloso.
    
    Args:
        cidades (list): Lista de coordenadas das cidades
        etapas (list): Lista de listas, onde cada uma representa o percurso em uma etapa
        intervalo (float): Tempo de espera entre cada etapa da animação
    """
    plt.figure(figsize=(12, 8))
    
    # Plotar todas as cidades
    x_cidades = [cidade[0] for cidade in cidades]
    y_cidades = [cidade[1] for cidade in cidades]
    plt.scatter(x_cidades, y_cidades, s=100, c='blue', edgecolor='black')
    
    # Adicionar rótulos
    for i, cidade in enumerate(cidades):
        plt.annotate(f"Cidade {i}", cidade, xytext=(5, 5), textcoords='offset points')
    
    plt.title("Construção do Percurso - Algoritmo Guloso")
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.grid(True)
    
    # Para cada etapa do percurso
    for etapa_idx, percurso_atual in enumerate(etapas):
        if etapa_idx > 0:  # Se não for a primeira etapa
            # Plotar o novo segmento adicionado
            idx1 = percurso_atual[-2]  # Penúltima cidade
            idx2 = percurso_atual[-1]  # Última cidade adicionada
            
            x = [cidades[idx1][0], cidades[idx2][0]]
            y = [cidades[idx1][1], cidades[idx2][1]]
            
            plt.plot(x, y, 'r-', linewidth=1.5)
            
            # Destacar a última cidade adicionada
            plt.scatter([cidades[idx2][0]], [cidades[idx2][1]], s=150, 
                       c='red', edgecolor='black', zorder=3)
            
            # Adicionar seta
            meio_x = (x[0] + x[1]) / 2
            meio_y = (y[0] + y[1]) / 2
            dx = x[1] - x[0]
            dy = y[1] - y[0]
            plt.arrow(meio_x - dx/8, meio_y - dy/8, dx/20, dy/20, 
                     head_width=2, head_length=2, fc='black', ec='black')
            
            # Atualizar o título com o progresso
            plt.title(f"Construção do Percurso - Algoritmo Guloso\n"
                     f"Etapa {etapa_idx}/{len(etapas)-1}: Adicionada Cidade {idx2}")
            
            plt.pause(intervalo)  # Pausa para visualização
    
    # Fechar o ciclo (voltar para a cidade inicial)
    cidade_inicial = etapas[0][0]
    cidade_final = etapas[-1][-1]
    
    x = [cidades[cidade_final][0], cidades[cidade_inicial][0]]
    y = [cidades[cidade_final][1], cidades[cidade_inicial][1]]
    
    plt.plot(x, y, color='r', linestyle='--', linewidth=1.5)  
    
    # Adicionar seta
    meio_x = (x[0] + x[1]) / 2
    meio_y = (y[0] + y[1]) / 2
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    plt.arrow(meio_x - dx/8, meio_y - dy/8, dx/20, dy/20, 
             head_width=2, head_length=2, fc='black', ec='black')
    
    plt.title(f"Percurso Completo - Algoritmo Guloso\n"
             f"Distância Total: {calcular_percurso_total(etapas[-1], cidades):.2f}")
    
    plt.show()

def comparar_com_forca_bruta(cidades):
    """
    Compara o algoritmo guloso com o algoritmo de força bruta.
    
    Args:
        cidades (list): Lista de coordenadas das cidades
        
    Returns:
        tuple: (percurso_guloso, dist_guloso, percurso_forca_bruta, dist_forca_bruta)
    """
    from itertools import permutations
    
    # Algoritmo guloso
    print("Executando algoritmo guloso...")
    inicio_guloso = time.time()
    percurso_guloso, dist_guloso, _ = resolver_caixeiro_viajante_guloso(cidades)
    tempo_guloso = time.time() - inicio_guloso
    
    # Algoritmo de força bruta
    print("Executando algoritmo de força bruta...")
    inicio_fb = time.time()
    
    indices_cidades = list(range(len(cidades)))
    menor_distancia = float('inf')
    melhor_percurso = None
    
    for perm in permutations(indices_cidades):
        dist = calcular_percurso_total(perm, cidades)
        if dist < menor_distancia:
            menor_distancia = dist
            melhor_percurso = perm
    
    tempo_fb = time.time() - inicio_fb
    
    # Resultados
    print("\nComparação de resultados:")
    print(f"Algoritmo Guloso:")
    print(f"  Percurso: {percurso_guloso}")
    print(f"  Distância: {dist_guloso:.2f}")
    print(f"  Tempo de execução: {tempo_guloso:.6f} segundos")
    
    print(f"\nAlgoritmo de Força Bruta:")
    print(f"  Percurso: {melhor_percurso}")
    print(f"  Distância: {menor_distancia:.2f}")
    print(f"  Tempo de execução: {tempo_fb:.6f} segundos")
    
    # Mostrar ganho/perda de qualidade
    diferenca_percentual = ((dist_guloso - menor_distancia) / menor_distancia) * 100
    
    if diferenca_percentual > 0:
        print(f"\nO algoritmo guloso produziu um percurso {diferenca_percentual:.2f}% pior que o ótimo.")
    else:
        print("\nO algoritmo guloso encontrou o percurso ótimo!")
    
    print(f"O algoritmo guloso foi {tempo_fb/tempo_guloso:.2f}x mais rápido.")
    
    return percurso_guloso, dist_guloso, melhor_percurso, menor_distancia

def main():
    # Configuração para reprodutibilidade
    random.seed(42)
    
    # Número de cidades
    num_cidades = int(input("Digite o número de cidades (recomendado: entre 5 e 12): "))
    
    # Limitamos o número máximo de cidades para força bruta
    if num_cidades > 10:
        print("Aviso: Para mais de 10 cidades, a comparação com força bruta pode levar muito tempo.")
        if input("Continuar? (s/n): ").lower() != 's':
            num_cidades = 10
            print(f"Número de cidades ajustado para {num_cidades}")
    
    # Gerar cidades aleatórias
    cidades = gerar_cidades_aleatorias(num_cidades, 0, 100)
    
    # Plotar distribuição das cidades
    plotar_cidades(cidades)
    
    # Resolver usando algoritmo guloso
    print("\nResolvendo com algoritmo guloso...")
    percurso, distancia, etapas = resolver_caixeiro_viajante_guloso(cidades)
    
    # Exibir resultados
    print(f"Percurso encontrado: {percurso}")
    print(f"Distância total: {distancia:.2f} unidades")
    
    # Plotar o percurso
    plotar_percurso(cidades, percurso)
    
    # Perguntar se o usuário quer ver a construção do percurso
    if input("\nDeseja visualizar a construção passo a passo do percurso? (s/n): ").lower() == 's':
        visualizar_construcao_percurso(cidades, etapas, intervalo=0.8)
    
    # Perguntar se o usuário quer comparar com força bruta
    if num_cidades <= 10:
        if input("\nDeseja comparar com o algoritmo de força bruta? (s/n): ").lower() == 's':
            percurso_guloso, dist_guloso, percurso_fb, dist_fb = comparar_com_forca_bruta(cidades)
            
            # Plotar os dois percursos para comparação
            plt.figure(figsize=(12, 10))
            
            # Subplot para o algoritmo guloso
            plt.subplot(2, 1, 1)
            percurso_completo = list(percurso_guloso) + [percurso_guloso[0]]
            x = [cidades[i][0] for i in percurso_completo]
            y = [cidades[i][1] for i in percurso_completo]
            
            plt.scatter([cidade[0] for cidade in cidades], 
                        [cidade[1] for cidade in cidades], 
                        s=100, c='blue', edgecolor='black')
            plt.plot(x, y, 'r-', linewidth=1.5)
            plt.scatter(x[0], y[0], s=150, c='green', edgecolor='black')
            
            # Adicionar rótulos
            for i, cidade in enumerate(cidades):
                plt.annotate(f"{i}", cidade, xytext=(5, 5), textcoords='offset points')
            
            plt.title(f"Algoritmo Guloso - Distância: {dist_guloso:.2f}")
            plt.grid(True)
            
            # Subplot para força bruta
            plt.subplot(2, 1, 2)
            percurso_completo = list(percurso_fb) + [percurso_fb[0]]
            x = [cidades[i][0] for i in percurso_completo]
            y = [cidades[i][1] for i in percurso_completo]
            
            plt.scatter([cidade[0] for cidade in cidades], 
                        [cidade[1] for cidade in cidades], 
                        s=100, c='blue', edgecolor='black')
            plt.plot(x, y, 'g-', linewidth=1.5)
            plt.scatter(x[0], y[0], s=150, c='green', edgecolor='black')
            
            # Adicionar rótulos
            for i, cidade in enumerate(cidades):
                plt.annotate(f"{i}", cidade, xytext=(5, 5), textcoords='offset points')
            
            plt.title(f"Força Bruta (Ótimo) - Distância: {dist_fb:.2f}")
            plt.grid(True)
            
            plt.tight_layout()
            plt.show()

if __name__ == "__main__":
    main()
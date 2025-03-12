import random
import math
import numpy as np
import matplotlib.pyplot as plt
from ler_arquivo_tsp import ler_arquivo_tsp

def gerar_populacao_inicial(numero_cidades, numero_individuos):
    populacao = []
    for _ in range(numero_individuos):
        individuo = list(range(numero_cidades))
        random.shuffle(individuo)
        populacao.append(individuo)
    return populacao

def calcular_dois_pontos(ponto1, ponto2):
    diff_x = ponto1[0] - ponto2[0]
    diff_y = ponto1[1] - ponto2[1]
    dist_pontos = math.sqrt(diff_x**2 + diff_y**2)
    return dist_pontos

def calcular_todas_distancias(lista_cidades):
    distancia_rotas = [[0 for _ in range(len(lista_cidades))] for _ in range(len(lista_cidades))]
    for i, cidade in enumerate(lista_cidades):
        for j, outra_cidade in enumerate(lista_cidades):
            if i != j:
                distancia = calcular_dois_pontos(cidade, outra_cidade)
                distancia_rotas[i][j] = distancia
    return distancia_rotas

def escala_apt(lista):
    valor_minimo = min(lista)
    valor_maximo = max(lista)
    lista_escalada = []
    
    if valor_maximo == valor_minimo:
        return [1 for _ in lista]
    
    for valor in lista:
        valor_escalado = (valor - valor_minimo + 1) / (valor_maximo - valor_minimo + 1)
        lista_escalada.append(valor_escalado)
    
    return lista_escalada

def torneio(aptidao):
    pai1 = random.randint(0, len(aptidao) - 1)
    pai2 = random.randint(0, len(aptidao) - 1)
    
    if aptidao[pai1] > aptidao[pai2]:
        return pai1
    else:
        return pai2

def mutacao_genes(lista_populacao, taxa_mutacao):
    for i, elemento in enumerate(lista_populacao):
        if random.random() <= taxa_mutacao:
            a = random.randint(0, len(elemento) - 1)
            b = random.randint(0, len(elemento) - 1)
            
            while a == b:
                b = random.randint(0, len(elemento) - 1)
            
            lista_populacao[i][a], lista_populacao[i][b] = lista_populacao[i][b], lista_populacao[i][a]
    
    return lista_populacao

def aptidao(lista_populacao, matriz_distancias):
    lista_aptidao = []
    
    for rota in lista_populacao:
        distancia_total = 0
        for i in range(len(rota) - 1):
            cidade_atual = rota[i]
            proxima_cidade = rota[i + 1]
            distancia_total += matriz_distancias[cidade_atual][proxima_cidade]
        
        distancia_total += matriz_distancias[rota[-1]][rota[0]]
        
        lista_aptidao.append(1 / (distancia_total + 0.00001))
    
    return lista_aptidao

def selecao_pais(lista_populacao, aptidao, sel_func):
    lista_pais = []
    
    for i in range(0, len(lista_populacao) // 2):
        idx_pai1_selecionado = sel_func(aptidao)
        
        aptidao_sem_pai1 = aptidao.copy()
        aptidao_sem_pai1[idx_pai1_selecionado] = 0
        
        idx_pai2_selecionado = sel_func(aptidao_sem_pai1)
        
        lista_pais.append([
            lista_populacao[idx_pai1_selecionado],
            lista_populacao[idx_pai2_selecionado]
        ])
    
    return lista_pais

def PMX(pai1, pai2):
    tamanho = len(pai1)
    filho = [-1] * tamanho
    
    punto_corte1 = random.randint(0, tamanho - 2)
    punto_corte2 = random.randint(punto_corte1 + 1, tamanho - 1)
    
    for i in range(punto_corte1, punto_corte2 + 1):
        filho[i] = pai2[i]
        
    for i in range(tamanho):
        if i >= punto_corte1 and i <= punto_corte2:
            continue
            
        item = pai1[i]
        while item in filho[punto_corte1:punto_corte2 + 1]:
            idx = pai2.index(item)
            item = pai1[idx]
        
        filho[i] = item
    
    return filho

def cruzamento_dois_pais(pai1, pai2, taxa_cruzamento):
    if random.random() < taxa_cruzamento:
        return PMX(pai1, pai2), PMX(pai2, pai1)
    else:
        return pai1.copy(), pai2.copy()

def cruzamento_todos_pais(lista_pais, taxa_cruzamento):
    lista_filho = []
    
    for par in lista_pais:
        filho1, filho2 = cruzamento_dois_pais(par[0], par[1], taxa_cruzamento)
        lista_filho.append(filho1)
        lista_filho.append(filho2)
    
    return lista_filho

def calcular_distancia_rota(rota, matriz_distancias):
    distancia_total = 0
    for i in range(len(rota) - 1):
        distancia_total += matriz_distancias[rota[i]][rota[i + 1]]
    distancia_total += matriz_distancias[rota[-1]][rota[0]]
    return distancia_total

def evolucao(lista_cidades, numero_individuo, numero_geracoes, taxa_cruzamento, taxa_mutacao, sel_func=torneio):
    matriz_distancias = calcular_todas_distancias(lista_cidades)
    
    populacao = gerar_populacao_inicial(len(lista_cidades), numero_individuo)
    
    menor_caminho = float('inf')
    melhor_rota = None
    evolucao_custo = []  
    evolucao_aptidao = []  
    evolucao_diversidade = []  
    
    for geracao in range(numero_geracoes):
        lista_aptidao = aptidao(populacao, matriz_distancias)
        lista_aptidao_escalada = escala_apt(lista_aptidao)
        
        melhor_idx = lista_aptidao.index(max(lista_aptidao))
        melhor_individuo = populacao[melhor_idx]
        distancia_atual = calcular_distancia_rota(melhor_individuo, matriz_distancias)
        
        if distancia_atual < menor_caminho:
            menor_caminho = distancia_atual
            melhor_rota = melhor_individuo.copy()
        
        evolucao_custo.append(menor_caminho)  
        evolucao_aptidao.append(np.mean(lista_aptidao))  
        evolucao_diversidade.append(len(set(map(tuple, populacao)))) 
        
        if geracao % 10 == 0 or geracao == numero_geracoes - 1:
            print(f"Geração {geracao}: Menor caminho = {menor_caminho:.2f}")
        
        pares = selecao_pais(populacao, lista_aptidao_escalada, sel_func)
        
        filhos = cruzamento_todos_pais(pares, taxa_cruzamento)
        
        filhos_mutados = mutacao_genes(filhos, taxa_mutacao)
        
        populacao = filhos_mutados
        
        if melhor_rota is not None:
            populacao[0] = melhor_rota.copy()
    
    print(f"Menor caminho encontrado: {menor_caminho:.2f}")
    
    melhor_caminho_cidades = [lista_cidades[idx] for idx in melhor_rota]
    
    return menor_caminho, melhor_caminho_cidades, melhor_rota, evolucao_custo, evolucao_aptidao, evolucao_diversidade

def visualizar_rota(cidades, melhor_rota, titulo="ALGORITMO GENÉTICO"):
    plt.figure(figsize=(10, 6))
    
    x = [cidade[0] for cidade in cidades]
    y = [cidade[1] for cidade in cidades]
    
    plt.scatter(x, y, c='blue', s=100)
    
    for i, (x_i, y_i) in enumerate(cidades):
        plt.text(x_i, y_i, f' {i}', fontsize=12)
    
    rota_x = [cidades[idx][0] for idx in melhor_rota]
    rota_y = [cidades[idx][1] for idx in melhor_rota]
    
    rota_x.append(cidades[melhor_rota[0]][0])
    rota_y.append(cidades[melhor_rota[0]][1])
    
    plt.plot(rota_x, rota_y, 'r-', linewidth=2)
    
    plt.title(titulo)
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.grid(True)
    plt.show()

def visualizar_evolucao_custo(evolucao_custo):
    plt.figure(figsize=(10, 6))
    plt.plot(evolucao_custo, marker='o', linestyle='-', color='b')
    plt.title('Evolução do Custo ao Longo das Gerações')
    plt.xlabel('Geração')
    plt.ylabel('Menor Custo')
    plt.grid(True)
    plt.show()

def visualizar_aptidao_media(evolucao_aptidao):
    plt.figure(figsize=(10, 6))
    plt.plot(evolucao_aptidao, marker='o', linestyle='-', color='g')
    plt.title('Evolução da Aptidão Média da População')
    plt.xlabel('Geração')
    plt.ylabel('Aptidão Média')
    plt.grid(True)
    plt.show()

def visualizar_diversidade(evolucao_diversidade):
    plt.figure(figsize=(10, 6))
    plt.plot(evolucao_diversidade, marker='o', linestyle='-', color='m')
    plt.title('Evolução da Diversidade da População')
    plt.xlabel('Geração')
    plt.ylabel('Número de Rotas Únicas')
    plt.grid(True)
    plt.show()

def visualizar_matriz_distancias(matriz_distancias):
    plt.figure(figsize=(10, 6))
    plt.imshow(matriz_distancias, cmap='viridis', interpolation='nearest')
    plt.colorbar(label='Distância')
    plt.title('Matriz de Distâncias')
    plt.show()

if __name__ == "__main__":
    random.seed(42)
    
    # cidade = ler_arquivo_tsp("tsp/berlin52.tsp")
    cidade = ler_arquivo_tsp("tsp/bier127.tsp")
    
    numero_individuos = 100
    numero_geracoes = 200
    taxa_cruzamento = 0.8
    taxa_mutacao = 0.1
    
    menor_distancia, melhor_caminho_cidades, melhor_rota, evolucao_custo, evolucao_aptidao, evolucao_diversidade = evolucao(
        cidade, 
        numero_individuos, 
        numero_geracoes, 
        taxa_cruzamento, 
        taxa_mutacao
    )
    
    print(f"Distância total do melhor caminho: {menor_distancia:.2f}")
    print(f"Melhor rota (índices): {melhor_rota}")
    
    
    visualizar_rota(cidade, melhor_rota)
    visualizar_evolucao_custo(evolucao_custo)
    visualizar_aptidao_media(evolucao_aptidao)
    visualizar_diversidade(evolucao_diversidade)
    visualizar_matriz_distancias(calcular_todas_distancias(cidade))
def ler_arquivo_tsp(caminho_arquivo):
    cidades = []
    with open(caminho_arquivo, 'r') as arquivo:
        ler_coordenadas = False
        for linha in arquivo:
            if linha.strip() == "NODE_COORD_SECTION":
                ler_coordenadas = True
                continue
            if linha.strip() == "EOF":
                break
            if ler_coordenadas:
                partes = linha.strip().split()
                if len(partes) == 3: 
                    cidades.append((float(partes[1]), float(partes[2])))
    return cidades
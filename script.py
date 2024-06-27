import os
import fnmatch as fn
import pandas as pd

def caminhos(root, nome):
    # Monta o caminho completo do arquivo da zona (onde estão os resultados da simulação)
    caminhoDoArquivo = os.path.join(root, nome)

    # Cria uma sub-lista com cada parte do caminho até o arquivo
    partesDoCaminho = caminhoDoArquivo.split(os.sep)
    # Extrai somente o número da zona do arquivo
    zona = nome.replace("Zon", '').replace("TUP.txt", '').replace("CONS.txt", '')
    # Extrai somente o número da iteração
    iteracao = partesDoCaminho[-3].replace("ite_", '')
    # Extrai a simulação
    simulacao = partesDoCaminho[-4]

    return caminhoDoArquivo, zona, iteracao, simulacao

# Caminho da pasta raiz que você deseja iterar
diretorioRaiz = ''

# Lista para armazenar linhas do CSV
csvTUP = []
csvCONS = []

# Itera sobre os diretórios e arquivos dentro do diretório raiz e subdiretórios
for root, dirs, files in os.walk(diretorioRaiz):
    # Verifica se o diretório atual corresponde ao padrão '*/simDomus'
    if fn.fnmatch(root, '*/simDomus'):
        # Itera sobre os arquivos encontrados dentro do diretório atual
        for nome in files:
            # Verifica se o nome do arquivo corresponde ao padrão 'Zon*TUP.txt'
            if fn.fnmatch(nome, 'Zon*TUP.txt'):
                # Obter os caminhos e outras informações
                caminhoDoArquivo, zona, iteracao, simulacao = caminhos(root, nome)

                # Abre o arquivo para leitura com encoding ISO-8859-1
                with open(caminhoDoArquivo, "r", encoding="ISO-8859-1") as arquivo:
                    # Lê todas as linhas do arquivo e armazena em uma lista
                    linhas = arquivo.readlines()

                    # Acessa a quarta linha do arquivo (onde estão os valores da simulação)
                    valores = linhas[3].split()

                    temperaturaInterna = valores[0]
                    temperaturaExterna = valores[1]
                    umidadeInterna = valores[2]
                    umidadeExterna = valores[3]
                    mes = valores[4]
                    dia = valores[5]
                    hora = valores[6]
                    
                    # Constrói a linha do CSV sem o caractere de nova linha
                    linhaCSV = f"{simulacao},{iteracao},{zona},{temperaturaInterna},{temperaturaExterna},{umidadeInterna},{umidadeExterna},{mes},{dia},{hora}"
                    csvTUP.append(linhaCSV)
            elif fn.fnmatch(nome, 'Zon*CONS.txt'):
                # Obter os caminhos e outras informações
                caminhoDoArquivo, zona, iteracao, simulacao = caminhos(root, nome)

                # Abre o arquivo para leitura com encoding ISO-8859-1
                with open(caminhoDoArquivo, "r", encoding="ISO-8859-1") as arquivo:
                    # Lê todas as linhas do arquivo e armazena em uma lista
                    linhas = arquivo.readlines()

                    # Acessa a quarta linha do arquivo (onde estão os valores da simulação)
                    valores = linhas[3].split()

                    iluminacao = valores[1]
                    equipamentos = valores[3]
                    geracaoDeVapor = valores[5]
                    aquecimento = valores[7]
                    resfriamento = valores[9]
                    demandaMedia = valores[11]
                    demandaMaxima = valores[13]

                    # Constrói a linha do CSV sem o caractere de nova linha
                    linhaCSV = f"{simulacao},{iteracao},{zona},{iluminacao},{equipamentos},{geracaoDeVapor},{aquecimento},{resfriamento},{demandaMedia},{demandaMaxima},{mes},{dia},{hora}"
                    csvCONS.append(linhaCSV)

# Escreve todas as linhas no arquivo CSV de TUP de uma vez
with open('csvTUP.csv', 'w') as arquivo_csv:
    arquivo_csv.write('Simulação,Iteração,Zona,Temperatura Interna,Temperatura Externa,Umidade Interna,Umidade Externa,Mês,Dia,Hora\n')
    for linha in csvTUP:
        arquivo_csv.write(f"{linha}\n")

# Escreve todas as linhas no arquivo CSV de CONS de uma vez
with open('csvCONS.csv', 'w') as arquivo_csv:
    arquivo_csv.write('Simulação,Iteração,Zona,Iluminação,Equipamentos,Geração de vapor,Aquecimento,Resfriamento,Demanda média,Demanda máxima,Mês,Dia,Hora\n')
    for linha in csvCONS:
        arquivo_csv.write(f"{linha}\n")

# Ler o arquivo CSV corretamente com Pandas
csvTUP = pd.read_csv('csvTUP.csv', sep=',', index_col=False)

# Ordena as 3 colunas - Simulação,Iteração,Zona - em ordem crescente
tupOrdenado = csvTUP.sort_values(by=['Simulação', 'Iteração', 'Zona'], ascending=[True, True, True])

# Salvar o CSV em um arquivo Excel
tupOrdenado.to_excel('tabelaTUP.xlsx', index=False)

# Ler o arquivo CSV corretamente com Pandas
csvCONS = pd.read_csv('csvCONS.csv', sep=',', index_col=False)

# Ordena as 3 colunas - Simulação,Iteração,Zona - em ordem crescente
consOrdenado = csvCONS.sort_values(by=['Simulação', 'Iteração', 'Zona'], ascending=[True, True, True])

# Salvar o CSV em um arquivo Excel
consOrdenado.to_excel('tabelaCONS.xlsx', index=False)

# Deletar os arquivos CSV após a criação dos arquivos Excel
os.remove('csvTUP.csv')
os.remove('csvCONS.csv')

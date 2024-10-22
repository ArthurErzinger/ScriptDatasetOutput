'''
Script escrito em python para a organização de outputs de co-simulações com o software DOMUS em formatos de tabela.

Como usar:

-Baixar o pandas (pip install pandas)
-Baixar o openpyxl (pip install openpyxl)
-Copie o caminho da pasta da sua simulação
-Cole dentro das aspas de "diretorioRaiz" no inicio do código
Desenvolvido por Arthur e Micael.

PUCPR.
'''

import platform
import os
import fnmatch as fn
import pandas as pd
import re

def caminhoTUPCONS(root, nome):
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

def caminhoCHTC(root,nome):
    caminhoDoArquivo = os.path.join(root, nome)
    partesDoCaminho = caminhoDoArquivo.split(os.sep)
    iteracao = partesDoCaminho[-3].replace("ite_", '')

    return caminhoDoArquivo

def identificarTipoZona(zona):
    # Identificar se é cobertura ou fachada e extrair o número associado
    tipo = ""
    numero_tipo = ""
    
    if "cobertura" in zona.lower():
        tipo = "Cobertura"
        # Extrair o número logo após a palavra "cobertura"
        inicio = zona.lower().find("cobertura") + len("cobertura")
        for char in zona[inicio:]:
            if char.isdigit():
                numero_tipo += char
            else:
                break
    elif "fachada" in zona.lower():
        tipo = "Fachada"
        # Extrair o número logo após a palavra "fachada"
        inicio = zona.lower().find("fachada") + len("fachada")
        for char in zona[inicio:]:
            if char.isdigit():
                numero_tipo += char
            else:
                break
    else:
        tipo = "Desconhecido"
        numero_tipo = "N/A"
    
    # Encontrar a posição da palavra "Zona" e extrair o número da zona
    pos_zona = zona.find("Zona")
    if pos_zona != -1:
        zona_num = ""
        for char in zona[pos_zona + 4:]:
            if char.isdigit():
                zona_num += char
            else:
                break
    else:
        zona_num = "Zona não encontrada"
    
    return tipo, int(numero_tipo), zona_num


diretorioRaiz = r''

if (platform.system() == "Windows"):
    diretorioRaiz = diretorioRaiz.replace('\\', '\\\\')


# Lista para armazenar linhas do CSV
csvTUP = []
csvCONS = []
csvCHTC_TA = []

# Itera sobre os diretórios e arquivos dentro do diretório raiz e subdiretórios
for root, dirs, files in os.walk(diretorioRaiz):
    # Verifica se o diretório atual corresponde ao padrão '*/simDomus'
    if fn.fnmatch(root, '*/simDomus'):
        # Itera sobre os arquivos encontrados dentro do diretório atual
        for nome in files:
            # Verifica se o nome do arquivo corresponde ao padrão 'Zon*TUP.txt'
            if fn.fnmatch(nome, 'Zon*TUP.txt'):
                # Obter os caminhoTUPCONS e outras informações
                caminhoDoArquivo, zona, iteracao, simulacao = caminhoTUPCONS(root, nome)

                # Abre o arquivo para leitura com encoding UTF-8
                with open(caminhoDoArquivo, "r", encoding="UTF-8", errors="ignore") as arquivo:
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
                # Obter os caminhoTUPCONS e outras informações
                caminhoDoArquivo, zona, iteracao, simulacao = caminhoTUPCONS(root, nome)
                # Abre o arquivo para leitura com encoding UTF-8
                with open(caminhoDoArquivo, "r", encoding="UTF-8", errors="ignore") as arquivo:
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
                    linhaCSV = f"{simulacao},{iteracao},{zona},{iluminacao},{equipamentos},{geracaoDeVapor},{aquecimento},{resfriamento},{demandaMedia},{demandaMaxima}"
                    csvCONS.append(linhaCSV)
    elif fn.fnmatch(root, '*/simCFX'):
        for nome in files:
            if fn.fnmatch(nome, 'CHTC_TA.txt'):
                caminhoDoArquivo = caminhoCHTC(root, nome)
                with open(caminhoDoArquivo, "r", encoding="UTF-8", errors="ignore") as arquivo:
                    linhas = arquivo.readlines()

                    #Arquivos CHTC_TA vão da linha 01 até a 41
                    for i in range(1,41):
                        linhaFormatada = linhas[i].split()

                        tipo, numeroTipo, zona = identificarTipoZona(linhaFormatada[0])

                        CHTC = linhaFormatada[1]
                        Ta = linhaFormatada[2]
                        CHT = linhaFormatada[3]
                        Cp = linhaFormatada[4]

                        linhaCSV = f"{zona},{tipo},{numeroTipo},{CHTC},{Ta},{CHT},{Cp}"
                        csvCHTC_TA.append(linhaCSV)


# Escreve todas as linhas no arquivo CSV de TUP de uma vez
with open('csvTUP.csv', 'w') as arquivo_csv:
    arquivo_csv.write('simulacao,iteracao,zona,temperatura_interna,temperatura_Externa,umidade_interna,umidade_externa,mes,dia,hora\n')
    for linha in csvTUP:
        arquivo_csv.write(f"{linha}\n")

# Escreve todas as linhas no arquivo CSV de CONS de uma vez
with open('csvCONS.csv', 'w') as arquivo_csv:
    arquivo_csv.write('simulacao,iteracao,zona,iluminacao,equipamentos,geracao_de_vapor,aquecimento,resfriamento,demanda_media,demanda_maxima\n')
    for linha in csvCONS:
        arquivo_csv.write(f"{linha}\n")

with open('csvCHTC_TA.csv', 'w') as arquivo_csv:
    arquivo_csv.write('Zona,Tipo,Numeração,CHTC,Ta,CHT,Cp\n')
    for linha in csvCHTC_TA:
        arquivo_csv.write(f"{linha}\n")



# Ler o arquivo CSV corretamente com Pandas
csvTUP = pd.read_csv('csvTUP.csv', sep=',', index_col=False)

# Ordena as 3 colunas - Simulação,Iteração,Zona - em ordem crescente
tupOrdenado = csvTUP.sort_values(by=['simulacao', 'iteracao', 'zona'], ascending=[True, True, True])

# Salvar o CSV em um arquivo Excel
tupOrdenado.to_excel('tabelaTUP.xlsx', index=False)

# Ler o arquivo CSV corretamente com Pandas
csvCONS = pd.read_csv('csvCONS.csv', sep=',', index_col=False)

# Ordena as 3 colunas - Simulação,Iteração,Zona - em ordem crescente
consOrdenado = csvCONS.sort_values(by=['simulacao', 'iteracao', 'zona'], ascending=[True, True, True])

# Salvar o CSV em um arquivo Excel
consOrdenado.to_excel('tabelaCONS.xlsx', index=False)

csvCHTC_TA = pd.read_csv('csvCHTC_TA.csv', sep=',', index_col=False)

CHTC_TA_Ordenado = csvCHTC_TA.sort_values(by=['Zona', 'Numeração'], ascending=[True, True])

CHTC_TA_Ordenado.to_excel('tabelaCHTC.xlsx', index=False)


# Deletar os arquivos CSV após a criação dos arquivos Excel
os.remove('csvTUP.csv')
os.remove('csvCONS.csv')
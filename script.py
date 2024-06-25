import os
import fnmatch as fn
import pandas as pd

# Caminho da pasta raiz que você deseja iterar
diretorioRaiz = ''

# Lista para armazenar linhas do CSV
linhas_csv = []

# Itera sobre os diretórios e arquivos dentro do diretório raiz e subdiretórios
for root, dirs, files in os.walk(diretorioRaiz):
    # Verifica se o diretório atual corresponde ao padrão '*/simDomus'
    if fn.fnmatch(root, '*/simDomus'):
        # Itera sobre os arquivos encontrados dentro do diretório atual
        for nome in files:
            # Verifica se o nome do arquivo corresponde ao padrão 'Zon*TUP.txt'
            if fn.fnmatch(nome, 'Zon*TUP.txt'):
                # Monta o caminho completo do arquivo da zona (onde estão os resultados da simulação)
                caminhoDoArquivo = os.path.join(root, nome)

                # Cria uma sub-lista com cada parte do caminho até o arquivo
                partesDoCaminho = caminhoDoArquivo.split(os.sep)
                # Extrai somente o número da zona do arquivo
                zona = nome.replace("Zon", '').replace("TUP.txt", '')
                # Extrai somente o número da iteração
                iteracao = partesDoCaminho[-3].replace("ite_", '')
                # Extrai a simulação
                simulacao = partesDoCaminho[-4]


                # Abre o arquivo para leitura com encoding ISO-8859-1
                with open(caminhoDoArquivo, "r", encoding="ISO-8859-1") as arquivo:
                    # Lê todas as linhas do arquivo e armazena em uma lista
                    linhas = arquivo.readlines()

                    # Acessa a quarta linha do arquivo (onde estão os valores da simulação)
                    valores = linhas[3].split('\t')

                    temperaturaInterna = valores[0]
                    temperaturaExterna = valores[1]
                    umidadeInterna = valores[2]
                    umidadeExterna = valores[3]
                    mes = valores[4]
                    dia = valores[5]
                    hora = valores[6]
                    
                    # Constrói a linha do CSV sem o caractere de nova linha
                    linha_csv = f"{simulacao},{iteracao},{zona},{temperaturaInterna},{temperaturaExterna},{umidadeInterna},{umidadeExterna},{mes},{dia},{hora}"
                    linhas_csv.append(linha_csv)

# Escreve todas as linhas no arquivo CSV de uma vez
with open('dadosCSV.csv', 'w') as arquivo_csv:
    arquivo_csv.write('Simulação,Iteração,Zona,Temperatura Interna,Temperatura Externa,Umidade Interna,Umidade Externa,Mês,Dia,Hora\n')
    for linha in linhas_csv:
        arquivo_csv.write(f"{linha}\n")

# Ler o arquivo CSV corretamente com Pandas
csv = pd.read_csv('dadosCSV.csv', sep=',', index_col=False)


# Ordena as 3 colunas - Simulação,Iteração,Zona - em ordem crescente
csvOrdenado = csv.sort_values(by=['Simulação', 'Iteração','Zona'], ascending=[True, True,True])


# Salvar o CSV em um arquivo Excel
csvOrdenado.to_excel('dadosExcel.xlsx', index=False)
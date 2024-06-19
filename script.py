import os
import fnmatch as fn



# Caminho da pasta raiz que você deseja iterar
diretorioRaiz = '/home/arthur/arthur/ScriptDatasetOutput'

'''
os.walk(root_path) gera um iterador que produz uma tupla de três valores (dirpath, dirnames, filenames) para cada diretório encontrado em root_path.
    - root: Caminho do diretório atual.
    - dirs: Lista dos nomes das subpastas no diretório atual.
    - files: Lista dos nomes dos arquivos no diretório atual.
'''

# Itera sobre os diretórios e arquivos dentro do diretório raiz e subdiretórios
for root, dirs, files in os.walk(diretorioRaiz):
    # Verifica se o diretório atual corresponde ao padrão '*/simDomus'
    if fn.fnmatch(root, '*/simDomus'):
        # Itera sobre os arquivos encontrados dentro do diretório atual
        for nome in files:
            # Verifica se o nome do arquivo corresponde ao padrão 'Zon*TUP.txt'
            if fn.fnmatch(nome, 'Zon*TUP.txt'):  # or fn.fnmatch(nome, 'Zon*CONS.txt'):
                # Monta o caminho completo do arquivo
                caminhoDoArquivo = os.path.join(root, nome)
                #print(f"O arquivo é o {caminhoDoArquivo}")

                partesDoCaminho = caminhoDoArquivo.split(os.sep)
                zona = nome.replace("Zon", '').replace("TUP.txt", '')
                iteracao = partesDoCaminho[-3]
                simulacao = partesDoCaminho[-4]


                # Abre o arquivo para leitura com encoding ISO-8859-1 (encoding UTF-8 dava erro). Abrindo com o 'with' eu garanto que o arquivo será fechado logo após o bloco.
                with open(caminhoDoArquivo, "r", encoding="ISO-8859-1") as arquivo:
                    # Lê todas as linhas do arquivo e armazena em uma lista
                    linhas = arquivo.readlines()

                    # Acessa a quarta linha do arquivo (onde estão os valores da simulação), o método .split('\t) divide a string no caractere especificado e guarda as substrings em um array chamado valores
                    valores = linhas[3].split('\t')

                    temperaturaInterna = valores[0]
                    temperaturaExterna = valores[1]
                    umidadeInterna = valores[2]
                    umidadeExterna = valores[3]
                    mes = valores[4]
                    dia = valores[5]
                    hora = valores[6]

                    print(f'A temperatura interna da zona {zona} na iteração {iteracao} da simulação {simulacao} é {temperaturaInterna}')

                    
                
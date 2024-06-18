import os
import fnmatch as fn

# Caminho da pasta raiz que você deseja iterar
diretorio_raiz = ''

'''
    os.walk(root_path) gera um iterador que produz uma tupla de três valores (dirpath, dirnames, filenames) para cada diretório encontrado em root_path.
        -dirpath: Caminho do diretório atual.
        -dirnames: Lista dos nomes das subpastas no diretório atual.
        -filenames: Lista dos nomes dos arquivos no diretório atual.
'''

for root, dirs, files in os.walk(diretorio_raiz):
    if fn.fnmatch(root, '*/simDomus'):
        for nome in files:
            if fn.fnmatch(nome, 'Zon*TUP.txt'):
                #Código
                pass
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 07:47:36 2015

@author: ricardo

Programa para simular autômatos finitos.
Arquivo de entrada tem nas linhas
1. Estado inicial
2. Conjunto de estados separados por espaços
3. Conjunto de estados finais
4. 

"""

import sys

def main():
    # Checa os parâmetros
    if (len(sys.argv) != 2):
        print("Uso: " + sys.argv[0] + " <regras_do_automato>")
        sys.exit();
    #variáveis        
    estados = []
    estados_finais = []
    alfabeto_entrada = []
    transicoes = []
    
    #Lê arquivo de entrada
    with open(sys.argv[1],"r") as leitura:
        
        pass
    
    
main()
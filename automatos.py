# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 07:47:36 2015

@author: ricardo

Programa para simular autômatos finitos.
Arquivo de entrada tem nas linhas
1. Conjunto de estados separados por espaços
2. Estado inicial
3. Conjunto de estados finais separados por espaços
4. Alfabeto separados por espaços
5. Transição de estados separados por ; na forma: ESTADO,SIMBOLO NOVO_ESTADO
"""

import sys, json

DEBUG = True

class Automato:
    def __init__(self, estados, estado_inicial, alfabeto, transicoes):
        self.estados = map(lambda x: str(x), estados)
        self.estado_inicial = str(estado_inicial)
        self.alfabeto = map(lambda x: str(x), alfabeto)
        # coloca transicões como um dicionário (ESTADO, ENTRADA) -> ESTADO
        if not self.automato_pilha:
            self.transicoes = dict(map(lambda x: (tuple(map(lambda y: str(y), x[0])), str(x[1])), transicoes))
        else:
            self.transicoes = dict(map(lambda x: (tuple(map(lambda y: str(y), x[0])), str(x[1])), transicoes))
        self.alfabeto = map(lambda x: str(x), alfabeto)
        if DEBUG:
            if not self.automato_pilha:
                print "Autômato Finito lido:"
            else:
                print "Autômato de Pilha Estruturado lido:"
            print "    Q  =", str(json.dumps(self.estados)).replace('"', '')
            print "    q0 =", self.estado_inicial
            print "    F  =", str(json.dumps(self.estados_finais)).replace('"', '')
            if self.automato_pilha:
                print "    Γ  =", str(json.dumps(self.alfabeto_pilha)).replace('"', '')
            print "    Σ  =", str(json.dumps(self.alfabeto)).replace('"', '')
            print "    δ  ="
            for t in self.transicoes:
                print "         " + str(json.dumps(t).replace('"', '')) + " -> " + self.transicoes[t] 
  
    def ler_simbolo(self, s, conf):
        if self.transicoes.has_key((conf.estado, s)):
            conf.estado = self.transicoes[(conf.estado, s)]
        else:
            # Transição não presente! Rejeita a cadeia
            conf.rejeitada = True
        return conf
    def estado_aceitacao(self, conf):
        return (not conf.rejeitada) and self.estados_finais.count(conf.estado) > 0

    def iniciar_conf(self):
        """ Função para iniciar o Autômato, retornando a Configuração Inicial"""
        return Configuracao(self.estado_inicial)
       
def main():
    # Checa os parâmetros
    if (len(sys.argv) != 3):
        print("Uso: " + sys.argv[0] + " <regras_do_automato> <cadeias>")
        sys.exit()
    
    # Lê arquivo de entrada
    with open(sys.argv[1],"r") as leitura:
        dados = json.load(leitura)
    # Instancia autômatos
    automatos = dict()
    estados_finais = []
    for maq in dados["maquinas"]:
        estados_finais.append(dados["maquinas"][maq]["estados_finais"])
        automatos[maq] = Automato(dados["maquinas"][maq]["estados"], dados["maquinas"][maq]["estado_inicial"]\
            ,dados["maquinas"][maq]["alfabeto"], dados["maquinas"][maq]["transicoes"])
main()

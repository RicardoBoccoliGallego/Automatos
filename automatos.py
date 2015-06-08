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

class Configuracao:
    """Classe para guardar a configuração atual"""
    def __init__(self, estado):
        self.estado = estado
        self.rejeitada = False
        self.aceita = False
        self.pilha = []
    
    def print_init_conf (self):
        print 'Configuração Inicial: '
        print '     Estado  = ' + self.estado
        print '     pilha  = ' + str(json.dumps(self.pilha)).replace('"', '')

    def print_conf (self, entrada):
        print 'Configuração: '
        print '     Entrada = ' + entrada
        print '     Estado  = ' + self.estado

class Automato:
    def __init__(self, estados, estado_inicial, estados_finais, alfabeto, transicoes, alfabeto_pilha):
        self.estados = map(lambda x: str(x), estados)
        self.estado_inicial = str(estado_inicial)
        self.estados_finais = map(lambda x: str(x), estados_finais)
        self.alfabeto_pilha = map(lambda x: str(x), alfabeto_pilha)
        self.automato_pilha = len(alfabeto_pilha) > 0
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
    # Instancia autômato
    automato = Automato(dados["estados"], dados["estado_inicial"], dados["estados_finais"], dados["alfabeto_entrada"],\
        dados["transicoes"], dados["alfabeto_pilha"] if "alfabeto_pilha" in dados else [])

    with open(sys.argv[2],"r") as leitura:
        for linha in leitura:
            
            # Pega a configuração inicial
            conf = automato.iniciar_conf()
            for s in linha.split()[0]:
                # Lê um símbolo do autômato e atualiza a configuração
                conf = automato.ler_simbolo(s, conf)
                conf.print_conf(s)
                if conf.rejeitada:
                   break
            print "Cadeia '" + linha.split()[0] + "'", 
            if automato.estado_aceitacao(conf):
                print "aceita no estado", conf.estado
            else:
                print "rejeitada"
main()

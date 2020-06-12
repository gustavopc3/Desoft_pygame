# -*- coding: utf-8 -*-
"""
Created on Fri May 22 21:06:30 2020

@author: rafae
"""


""""
Jogo pygame
Authors: Gustavo Pinheiro
         Maria Eduarda Mourão
         Rafaela Zyingier
"""
import pygame
import sys
import os
"""Rotina principal do jogo"""
def main():
    #Inicializa as rotinas do jogo
    pygame.init()
    
    #Muda o nome no título do pygame
    pygame.display.set_caption("Octopy")

    #Cria superfície para o jogo
    superficie = pygame.display.set_mode([600, 600]) #Define o tamanho
    arquivo = os.path.join('imagens', 'jogo_pygame')
    #Para colocar nossa imagem:
    try:
        peixinho = pygame.image.load("peixinho.png").convert_alpha() #Convert_alpha: Desfaz o corte gerado de imagem ao converter a imagem para o padrão de tela mantendo as áreas diferentes.
    except pygame.error:
        print("Erro ao tentar ler imagem")
        sys.exit()

    surf.blit(peixinho, pos_peixinho) #desenha o peixinho na tela
    
    #Cria nossa superfície de fundo:
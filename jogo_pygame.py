""""
Jogo pygame
Authors: Gustavo Pinheiro
         Maria Eduarda Mourão
         Rafaela Zyingier
"""
import pygame
import sys
"""Rotina principal do jogo"""
def main():
    #Inicializa as rotinas do jogo
    pygame.init()
    
    #Muda o nome no título do pygame
    pygame.display.set_caption("Octopy")

    #Cria superfície para o jogo
    superficie = pygame.display.set_mode([600, 600]) #Define o tamanho

    arquivo = 

    #Para colocar nossa imagem:
    try:
        img = pygame.image.load(" ").convert_alpha() #Convert_alpha: Desfaz o corte gerado de imagem ao converter a imagem para o padrão de tela mantendo as áreas diferentes.
    except pygame.error:
        print("Erro ao tentar ler imagem")
        sys.exit()

    #Cria nossa superfície de fundo:
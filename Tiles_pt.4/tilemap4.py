import pygame as pg
from settings4 import *

# Cria uma classe MAP
class Map:
    # Inicializa a classe com o nome do arquivo
    def __init__(self, filename):
        self.data = []
        with open(filename, "rt") as f:
            for line in f:
                #Para ajustar a brecha da camera e o fim do mapa no lado direito, por conta da leitura do mapa que conta os "/n"a cada linha.
                self.data.append(line.strip())
        
        # Para sabermos o tamanho do mapa
        self.tilewidth = len(self.data[0]) # Comprimento (número de colunas)
        self.tileheight = len(self.data) # Altura (número de linhas)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

# Para que a "câmera" acompanhe o movimento do jogador quando o mapa excede os limites da superfície do jogo.
class Camera:
    def __init__(self, widht, height):
        self.camera = pg.Rect(0, 0, widht, height)
        self.width = widht
        self.height = height

    def apply(self, entity):
        #A função move realiza um movimento do retângulo da camera para a direção do player
        return entity.rect.move(self.camera.topleft)
    #Faz o update da posição da câmera para o a direção contrária ao movimento do jogador (por isso negativo)
    def update(self, target):
        x = -target.rect.x + int(WIDTH/2)
        y = -target.rect.y + int(HEIGHT/2)

        #Limita o movimento da câmera para a extremidade do mapa
        x = min(0, x) #Lado esquerdo
        y = min(0, y) #Topo
        x = max(-(self.width - WIDTH), x) #Lado direito
        y = max(-(self.height - HEIGHT), y) #Fundo
        self.camera = pg.Rect(x, y, self.width, self.height)




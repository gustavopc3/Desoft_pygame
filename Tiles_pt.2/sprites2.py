import pygame as pg
from settings2 import *

# Criando o jogador
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y): #O x e y representam o ponto inicial do jogador
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE)) # Um quadrado
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x # Guarda a coordenada x do jogador
        self.y = y # Guarda a coordernada y do jogador

    # Para mover o jogador
    def move(self, dx=0, dy=0): # dx e dy (quanto x e y devem mudar)
        # Para o jogador não poder passar pela parede
        if not self.collide_with_walls(dx, dy):
            # Na horizontal
            self.x += dx
            # Na vertical 
            self.y += dy

    # Analisa se o espaço está vazio para o jogador poder se movimentar
    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False


    # UPDATE
    def update(self):
        # Faz o update da posição do jogador
        # Na horizontal
        self.rect.x = self.x * TILESIZE
        # Na vertical 
        self.rect.y = self.y * TILESIZE

# Criando uma parede
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y): # x e y definem a posição inicial da parede
        # Adiciona a parede ao grupo de sprites
        self.groups = game.all_sprites, game.walls
        # Inicializa o sprite
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # Cria a superfície da parede (de cada quadrado, não da parede por inteiro)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # Preenche a superfície com uma cor
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        # Cria as variaveis x e y para a parede
        self.x = x
        self.y = y
        # Faz as posições se transformarem nos tiles
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


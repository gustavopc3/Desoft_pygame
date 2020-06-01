import pygame as pg
from settings4 import *

# Criando o jogador
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y): #O x e y representam o ponto inicial do jogador
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE)) # Um quadrado
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE # Guarda a coordenada x do jogador
        self.y = y * TILESIZE # Guarda a coordernada y do jogador

    def get_keys(self):
        self.vx, self.vy = 0, 0
        # Para movimentar o jogador de acordo com a sua velocidade (e não pelos tiles)
        # OBS: Os if's (em vez de elif's) possibilitam o movimento na diagonal.
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        # Porém, o movimento na diagonal é mais rápido, e precisa de uma adaptação
        if self.vx !=0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    # Para mover o jogador
    def move(self, dx=0, dy=0): # dx e dy (quanto x e y devem mudar)
        # Para o jogador não poder passar pela parede
        if not self.collide_with_walls(dx, dy):
            # Na horizontal
            self.x += dx
            # Na vertical 
            self.y += dy

    # Analisa se o espaço está vazio para o jogador poder se movimentar
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y



    # UPDATE
    def update(self):
        # Faz o update da posição do jogador
        self.get_keys()
        # Na horizontal
        self.x += self.vx * self.game.dt # O self.game.dt faz parte do Main, e é o delta t dos frames.
        # Na vertical 
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

        # Para fazer com que o jogador colida com as paredes quando utilizamos uma PLAYER_SPEED
   

# Criando uma parede (fixa)
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
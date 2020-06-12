import pygame as pg
from settings9 import *
vec = pg.math.Vector2 #Vetores podem ser usados para várias coisas dentro do pygame

# Criamos uma função unica de colisão com as paredes que podem ser aplicadas a vários sprites (e não mais dentro da Class Player)
# Analisa se o espaço está vazio para o jogador poder se movimentar
def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.rect.width
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right
            sprite.vel.x = 0
            sprite.rect.x = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, sprite.game.walls, False)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom
            sprite.vel.y = 0
            sprite.rect.y = sprite.pos.y

# Criando o jogador
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y): #O x e y representam o ponto inicial do jogador
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img # Imagem do jogador
        self.rect = self.image.get_rect()
        # Velocidade em função dos vetores
        self.vel = vec(0, 0)
        # Posição em função dos vetores
        self.pos = vec(x, y) * TILESIZE
        # Rotação do jogador (não funciona pro Octopy)
        self.rot = 0


    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        # Para movimentar o jogador de acordo com a sua velocidade (e não pelos tiles)
        # OBS: Os if's (em vez de elif's) possibilitam o movimento na diagonal.
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        # Porém, o movimento na diagonal é mais rápido, e precisa de uma adaptação
        if self.vel.x !=0 and self.vel.y != 0:
            self.vel *= 0.7071

    # Analisa se o espaço está vazio para o jogador poder se movimentar
    # UPDATE
    def update(self):
        # Faz o update da posição do jogador
        self.get_keys()
        #Quando usamos vetores (e por isso o self.pos)
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.rect.y = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')

        # Para fazer com que o jogador colida com as paredes quando utilizamos uma PLAYER_SPEED

# Criando os polvos   
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y): # x e y definem a posição inicial da parede
        # Adiciona os polvos ao grupo de sprites
        self.groups = game.all_sprites, game.mobs
        # Inicializa o sprite
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # Define a imagem do polvo
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        #Define uma rotação para o mob
        self.rot = 0
    #Faz o update da posição do mob para que ele sempre esteja de frente para o peixinho
    def update(self):
        # (vetores player.pos - mob.pos, função do ângulo angle_to() )
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(-1,0)) # Coloquei -1 no vetor x por peixe ficar de frente (tava ao contrario)
        # Rotaciona a imagem pelo vetor de rotação
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        #Faz o update do centro da imagem para permanecer na direção
        self.rect.center = self.pos



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
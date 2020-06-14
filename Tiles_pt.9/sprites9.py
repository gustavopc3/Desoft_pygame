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
            #if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.rect.width
            if sprite.vel.x < 0:
            #if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right
            sprite.vel.x = 0
            sprite.rect.x = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, sprite.game.walls, False)
        if hits:
            if sprite.vel.y > 0:
            #if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height
            if sprite.vel.y < 0:
            #if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom
            sprite.vel.y = 0
            sprite.rect.y = sprite.pos.y

# Criando o jogador
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y): #O x e y representam o ponto inicial do jogador
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.peixinho_images_esquerda[0]
        #self.image = peixinho_images_esquerda[0]
        #self.image.set_colorkey(PRETO) # Imagem do jogador
        self.rect = self.image.get_rect()
        # Velocidade em função dos vetores
        self.vel = vec(0, 0)
        # Posição em função dos vetores
        self.pos = vec(x, y) * TILESIZE
        # Rotação do jogador (não funciona pro Octopy)
        self.rot = 0
        self.frame_esquerda=0
        self.frame_direita=0
        self.frame_tapa = 0
        self.frame_rate = 300
        self.last_update = pg.time.get_ticks()
        self.tapa = False
        self.health = PLAYER_HEALTH


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
        now = pg.time.get_ticks()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.rect.y = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        #if self.health <= 0:
            #self.kill()
        keys = pg.key.get_pressed()

        # UPDATE da mudança de imagens do peixinho

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            if now - self.last_update > self.frame_rate:
                self.last_update=now
                self.frame_esquerda +=1
                if self.frame_esquerda == 6:
                    self.frame_esquerda =0
                else:
                    self.image = self.game.peixinho_images_esquerda[self.frame_esquerda] 
                    self.image.set_colorkey(BLACK)
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            if now - self.last_update > self.frame_rate:
                self.last_update=now
                self.frame_direita +=1
                if self.frame_direita == 6:
                    self.frame_direita =0
                else:
                    self.image = self.game.peixinho_images_direita[self.frame_direita] 
                    self.image.set_colorkey(BLACK)

        if keys[pg.K_SPACE] or self.tapa == True:
                self.tapa = True
                if now - self.last_update > self.frame_rate:
                    self.last_update=now
                    self.frame_tapa +=1
                    if self.frame_tapa == 4 :
                        self.frame_tapa = 0
                        self.tapa = False
                    else:
                        self.image = self.game.peixinho_images_tapa[self.frame_tapa] 
                        self.image.set_colorkey(BLACK)

        # Para fazer com que o jogador colida com as paredes quando utilizamos uma PLAYER_SPEED
    # Para criar uma barra de vidas que fica acima do sprite
    #def draw_health(self):
        #if self.health >= 75:
            #col = GREEN
        #elif self.health >=50:
            #col = YELLOW
        #elif self.health >=25:
            #col = RED
        #width = int(self.rect.width * self.health / PLAYER_HEALTH)
        #self.health_bar = pg.Rect(0, 0, width, 7)
        #if self.health < PLAYER_HEALTH:
            #pg.draw.rect(self.image, col, self.health_bar)

class Bullet(pg.sprite.Sprite):
    #Posição que vai aparecer e em qual direção ela vai se mover
    def __init__(self, game, player, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.player = player
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()
        self.rot = 0
    
    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        #if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            #self.kill()
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        #self.rect.x = self.pos.x
        #if collide_with_walls(self, self.game.walls, 'x'):
            #self.kill()
        #self.rect.y = self.pos.y
        #if collide_with_walls(self, self.game.walls, 'y'):
            #self.kill()
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))


# Criando os polvos   
class Mob(pg.sprite.Sprite):
    def __init__(self, game, player, x, y): # x e y definem a posição inicial da parede
        # Adiciona os polvos ao grupo de sprites
        self.groups = game.all_sprites, game.mobs
        # Inicializa o sprite
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.player = player
        # Define a imagem do polvo
        self.image = game.octopy_images[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        #Define uma rotação para o mob
        #self.rot = 0
        # Parte nova
        self.frame=0
        self.frame_rate = 200
        self.last_update = pg.time.get_ticks()
        self.last_update1 = pg.time.get_ticks()
        self.health = MOB_HEALTH
    #Faz o update da posição do mob para que ele sempre esteja de frente para o peixinho
    def update(self):
        # (vetores player.pos - mob.pos, função do ângulo angle_to() )
        #self.rot = (self.game.player.pos - self.pos).angle_to(vec(-1,0)) # Coloquei -1 no vetor x por peixe ficar de frente (tava ao contrario)
        # Rotaciona a imagem pelo vetor de rotação
        #self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        #Faz o update do centro da imagem para permanecer na direção
        self.rect.center = self.pos
        # Para que o Mob morra quando levar um tapa
        if self.health <= 0:
            self.kill()
        
        # Parte Nova
        # Animação
        now1 = pg.time.get_ticks()
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.game.octopy_images):
                self.frame = 0
            else:
                self.image = self.game.octopy_images[self.frame] 
                self.image.set_colorkey(BLACK)
        # Mob atirando
        if now1 - self.last_update1 > 1000:
            self.last_update1 = now1
            dir = vec(1,0).rotate(self.player.rot)
            #dir = vec(1,0).rotate
            # Para que a posição da bullet fique igual a da imagem (um pouco acima do centro do mob)
            pos = self.pos + BARREL_OFFSET
            Bullet(self.game, self.player, pos, dir)
            #mob.shoot()

    #def shoot(self):
        #bullet=Bullet(self.rect.centerx, self.rect.centery) #no meio x do Octopy e no topo do Octopy
        #all_sprites.add(bullet)
        #bullets.add(bullet)


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
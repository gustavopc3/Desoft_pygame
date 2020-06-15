import pygame as pg
vec = pg.math.Vector2
# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DARKBLUE = (0, 0, 255)


# camera settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16 (Números que, divididos pelo Tilesize, resultam em um número inteiro)
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12 (Números que, divididos pelo Tilesize, resultam em um número inteiro)
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = DARKBLUE

# Define o tamanho dos tiles (Normalmente se utiliza valores que são potências de 2)
TILESIZE = 64 
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMAGE = ''
# Settings do jogador
PLAYER_SPEED = 300
PLAYER_IMG = 'so1peixinho.png'
PLAYER_HEALTH = 100

#Velocidade de rotação do jogador (graus por segundo)
PLAYER_ROT_SPEED = 250

#Settings das balas
BULLET_IMG = 'bullet.png'
BULLET_SPEED = 500
BULLET_RATE = 150
BULLET_DAMAGE = 25

# Settings tapa do peixinho
TAPA_DAMAGE = 100

#Settings do polvo
MOB_HEALTH = 100
BARREL_OFFSET = vec(10, -14)

MOB2_HEALTH = 100
BARREL_OFFSET2 = (10, -14)
# Layers do jogo (Vão ser desenhados em ordem crescente dos números - Backgrpund primeiro e Mob por último)
#BACKGROUND_LAYER = 1
WALL_LAYER = 2
PLAYER_LAYER = 3
MOB_LAYER = 3
MOB2_LAYER = 3
BULLET_LAYER = 4

# Itens:
#ITEM_IMAGES {'health': 'health_pack.png'}

# Sounds:
BG_MUSIC = 'musicadowii.ogg'
#TAPA_HIT_SOUND =
PLAYER_HIT_SOUND = ['player_hit_sound.wav']
#MOB_HIT_SOUND =
#PLAYER_DIE_SOUND =  
#EFFECTS_SOUND = {'level_start': ''}

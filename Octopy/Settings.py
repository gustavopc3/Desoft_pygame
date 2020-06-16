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
TITLE = "Octopy v1.0"
BGCOLOR = DARKBLUE

# Define o tamanho dos tiles (Normalmente se utiliza valores que são potências de 2)
TILESIZE = 64 
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Settings do jogador
PLAYER_SPEED = 300
PLAYER_HEALTH = 100

#Velocidade de rotação do jogador (graus por segundo)
PLAYER_ROT_SPEED = 250

#Settings das balas
BULLET_SPEED = 500
BULLET_RATE = 150
BULLET_DAMAGE = 25

#Settings do polvo
MOB_HEALTH = 100
BARREL_OFFSET = vec(10, -14)

MOB2_HEALTH = 100
BARREL_OFFSET2 = (10, -14)

# Layers do jogo (Vão ser desenhados em ordem crescente dos números - Backgrpund primeiro e Mob por último)
WALL_LAYER = 2
F_LAYER = 2
END_LAYER = 2
PLAYER_LAYER = 3
MOB_LAYER = 3
MOB2_LAYER = 3
BULLET_LAYER = 4

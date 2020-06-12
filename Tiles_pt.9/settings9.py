# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DARKBLUE = (0, 0, 255)

# game settings
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
#Velocidade de rotação do jogador (graus por segundo)
PLAYER_ROT_SPEED = 250

#Settings do polvo
MOB_IMG = 'polvo.png'
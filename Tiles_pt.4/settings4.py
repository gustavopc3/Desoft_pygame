# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16 (Números que, divididos pelo Tilesize, resultam em um número inteiro)
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12 (Números que, divididos pelo Tilesize, resultam em um número inteiro)
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = DARKGREY

# Define o tamanho dos tiles (Normalmente se utiliza valores que são potências de 2)
TILESIZE = 32 
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Settings do jogador
PLAYER_SPEED = 300
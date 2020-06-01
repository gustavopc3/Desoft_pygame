# KidsCanCode - Game Development with Pygame video series
# Tile-based game - Part 4
# Scrolling Map/Camera
# Video link: https://youtu.be/3zV2ewk-IGU

import pygame as pg
import sys
from os import path
from settings4 import *
from sprites4 import *
from tilemap4 import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        # Taxa de repetição dos movimentos (Se a tecla ficar pressionada por meio segundo, o jogador começa a se movimentar continuamente)
        pg.key.set_repeat(500, 100) 
        self.load_data()

    
    def load_data(self):
        # Cria o caminho para o arquivo onde está o mapa do labirinto
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, "map2.txt"))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        # OBS: a função enumerate fornece o Index e o item de uma lista(ex: l[0]=a, enumerate fornece 0 e a)
        for row, tiles in enumerate(self.map.data): #Para cada fileira
            for col, tile in enumerate(tiles): #Para cada fileira/coluna
                if tile == '1':
                    Wall(self, col, row)
                #OBS: É possível colocar o spawn do jogador inserindo um P no mapa
                if tile == 'P':
                    self.player = Player(self, col, row)        
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        #A camera segue o sprite que for colocado entre parenteses)
        self.camera.update(self.player)
    
    # Para desenhar o grid
    def draw_grid(self):
        # Desenha as linhas horizontais
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT)) # Linha criada a partir de qualquer x para o topo/base
        # Desenha as linhas verticais
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y)) # Linha criada a partir de qualquer y para os cantos esquerdo/direito

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                # Define um jeito de sair do jogo
                if event.key == pg.K_ESCAPE:
                    self.quit()
                # Define os movimentos do jogador no teclado
            

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()

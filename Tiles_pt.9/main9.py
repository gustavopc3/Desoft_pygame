# KidsCanCode - Game Development with Pygame video series
# Tile-based game - Part 9
# Scrolling Map/Camera
# Video link: https://youtu.be/3zV2ewk-IGU

import pygame as pg
import sys
from os import path
from settings9 import *
from sprites9 import *
from tilemap9 import *

#OBS!!: Precisamos achar um jeito de mudar a direção do peixe quando ele vai para direita/esquerda
# funções do HUD:
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct >= 0.75:
        col = GREEN
    elif pct >= 0.50:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        # Taxa de repetição dos movimentos (Se a tecla ficar pressionada por meio segundo, o jogador começa a se movimentar continuamente)
        pg.key.set_repeat(500, 100) 
        self.load_data()

    
    def load_data(self):
        # Cria o caminho para o arquivo onde está o mapa do labirinto
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')

        # ///Para usar TILEDMAP/// 

        #map_folder = path.join(game_folder, 'maps')
        #self.map = Tiledmap(path.join(map_folder, 'ARQUIVO TMX'))
        #self.map_img = self.map.make_map()
        #self.map_rect = self.map_img.get_rect()

        self.map = Map(path.join(game_folder, "map4.txt"))
        #Imagens Peixinho esquerda
        self.peixinho_images_esquerda = []
        peixinho_list_esquerda = ["peixinho_00.png", "peixinho_01.png","peixinho_02.png","peixinho_03.png","peixinho_04.png","peixinho_05.png"]
        for img in peixinho_list_esquerda:
            self.peixinho_images_esquerda.append(pg.image.load(path.join(img_folder, img)).convert())
        # Imagens peixinho direita
        self.peixinho_images_direita = []
        peixinho_list_direita = ["peixinho_06.png", "peixinho_07.png","peixinho_08.png","peixinho_09.png","peixinho_10.png","peixinho_11.png"]
        for img in peixinho_list_direita:
            self.peixinho_images_direita.append(pg.image.load(path.join(img_folder, img)).convert())
        # Imagens tapa do peixinho
        self.peixinho_images_tapa = []
        peixinho_list_tapa = ["peixinho_12.png", "peixinho_13.png","peixinho_14.png","peixinho_15.png"]
        for img in peixinho_list_tapa:
            self.peixinho_images_tapa.append(pg.image.load(path.join(img_folder, img)).convert())

        # Define a imagem pro player (inicial)
        self.player_img = self.peixinho_images_esquerda[0]

        # Imagens Octopy
        self.octopy_images = []
        octopy_list = ["octopy_0.png", "octopy_1.png", "octopy_2.png", "octopy_3.png", "octopy_4.png", "octopy_5.png"]
        for img in octopy_list:
            self.octopy_images.append(pg.image.load(path.join(img_folder, img)).convert())

        # Define a imagem inicial do Octopy
        self.mob_img = self.octopy_images[0]
        #self.player_img = pg.image.load(path.join(img_folder, 'so1peixinho.png')).convert_alpha()
        #self.bullet_img = pg.image.load(path.join(img_folder, 'BULLET_IMG')).convert_alpha()
        self.bullet_img = pg.Surface((10,5)) #determina o tamalho, nessa caso pequeno
        self.bullet_img.fill((DARKGREY))
        #self.wall_img = pg.image.load(path.join(img_folder, 'imagem das paredes.png')).convert_alpha()
        #self.mob_img = pg.image.load(path.join(img_folder, 'so1peixinho.png')).convert_alpha()
        # Como adequaar o tamanho da imagem para o tamanho do tile
        #self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE/TILESIZE))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        #self.player = pg.sprite.Group()
        # OBS: a função enumerate fornece o Index e o item de uma lista(ex: l[0]=a, enumerate fornece 0 e a)
        for row, tiles in enumerate(self.map.data): #Para cada fileira
            for col, tile in enumerate(tiles): #Para cada fileira/coluna
                # Adiciona as paredes conforme os '1'no mapa
                if tile == '1':
                    Wall(self, col, row)
                # Adiciona os mobs conforme os 'M'no mapa
                if tile == 'M':
                    Mob(self, self.player, col, row)
                #OBS: É possível colocar o spawn do jogador inserindo um P no mapa
                if tile == 'P':
                    self.player = Player(self, col, row)
        
        # ///Para fazer o spawn do player no TILEDMAP///
        #self.player = Player(self, 5, 5)        
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
        # Quando o player da um tapa no Octopy
        # :
        for event in pg.event.get():
            if event.type == pg.K_SPACE:
                tapas = pg.sprite.spritecollide(self.player, self.mobs, False)
                for tapa in tapas:
                    self.mobs.health -= TAPA_DAMAGE


        #for hit in hits:
            #self.player.health -= BULLET_DAMAGE
            # Game over se o Player perder toda a sua health
            #if self.player.health <= 0:
                #self.playing = False
        # Quando as pedras atingem o player: (OBS: Não da certo fazer com o player)
        hits = pg.sprite.spritecollide(self.player, self.bullets, True, False)
        for hit in hits:
            self.player.health -= BULLET_DAMAGE
            # Game over se o Player perder toda a sua health
            if self.player.health <= 0:
                self.playing = False



    
    # Para desenhar o grid
    def draw_grid(self):
        # Desenha as linhas horizontais
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT)) # Linha criada a partir de qualquer x para o topo/base
        # Desenha as linhas verticais
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y)) # Linha criada a partir de qualquer y para os cantos esquerdo/direito

    def draw(self):
        # Para vermos a quantidade de FPS no jogo enquanto estamos trabalhando nele (precisa estar perto de 60 (definido pro jogo))
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(BGCOLOR)
        #self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        #self.draw_grid()
        for sprite in self.all_sprites:
            #if isinstance(sprite, Player):
                #sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # Para desenhar o HUD
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
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

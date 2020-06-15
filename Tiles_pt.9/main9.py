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
import time

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
        self.current_level = 1


    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    
    def load_data(self):
        # Cria o caminho para o arquivo onde está o mapa do labirinto
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        #self.map_folder = path.join(game_folder, 'mapas')
        self.map_folder = path.join(game_folder, 'maps')

        # Escolha das fontes para os textos no jogo
        self.title_font = path.join(img_folder, 'Octopy.TTF')
        self.hud_font = path.join(img_folder, 'Hud_font.TTF')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        # Carregar a imagem de fundo pra tela de pause
        self.pause_img = pg.image.load(path.join(img_folder, 'Telas_0.png')).convert_alpha()
        # Transformar a imagem para o formato da superfície de jogo
        self.pause_img = pg.transform.scale(self.pause_img, self.screen.get_size())

        # Carregar a imagem de fundo pra tela de game over
        self.game_over_img = pg.image.load(path.join(img_folder, 'Telas_1.png')).convert_alpha()
        # Transformar a imagem para o formato da superfície de jogo
        self.game_over_img = pg.transform.scale(self.game_over_img, self.screen.get_size())

        # Carregar a imagem de fundo pra tela de game over        
        self.next_level_img = pg.image.load(path.join(img_folder, 'Telas_2.png')).convert_alpha()
        # Transformar a imagem para o formato da superfície de jogo        
        self.next_level_img = pg.transform.scale(self.next_level_img, self.screen.get_size())

        #self.map = Map(path.join(game_folder, "map4.txt"))
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

        # Imagens Octopy esquerda:
        self.octopy_esquerda = []
        octopy_left_list = ["octopy_6.png", "octopy_7.png", "octopy_8.png", "octopy_9.png", "octopy_10.png", "octopy_11.png"]
        for img in octopy_left_list:
            self.octopy_esquerda.append(pg.image.load(path.join(img_folder, img)).convert())

        # Define a imagem inicial do Octopy da direita
        self.mob_img = self.octopy_images[0]
        # Define a imagem inicial do Octopy da esquerda
        self.mob_left_img = self.octopy_esquerda[0]


        #self.player_img = pg.image.load(path.join(img_folder, 'so1peixinho.png')).convert_alpha()
        #self.bullet_img = pg.image.load(path.join(img_folder, 'BULLET_IMG')).convert_alpha()
        self.bullet_img = pg.Surface((10,5)) #determina o tamalho, nessa caso pequeno
        self.bullet_img.fill(DARKGREY)
        self.wall_img = pg.image.load(path.join(img_folder, 'tileareia.png')).convert_alpha()
        #self.mob_img = pg.image.load(path.join(img_folder, 'so1peixinho.png')).convert_alpha()
        # Como adequaar o tamanho da imagem para o tamanho do tile
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        #self.bg_img = pg.image.load(path.join(img_folder, 'tileagua.png')).convert_alpha()
        #self.bg_img = pg.transform.scale(self.bg_img, (TILESIZE, TILESIZE))

        # Sound loading
        # Som do background
        pg.mixer.music.load(path.join(music_folder, 'musicadowii.ogg'))

        # Som do começo do jogo
        #self.effects_sounds = {}
        #for type in EFFECTS_SOUNDS:
            #self.effect_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))

        # Som do tapa do peixinho
        #self.tapa_sound = []
        #for snd in TAPA_HIT_SOUND:
            #s = pg.mixer.Sound(path.join(snd_folder, snd))
            #s.set_volume(0.'x') # Valores entre 0 e 1
            #self.tapa_sound.append(s)

        # Som do polvo morrendo
        #self.mob_hit_sound = []
        #for snd in MOB_HIT_SOUND:
            #s = pg.mixer.Sound(path.join(snd_folder, snd))
            #s.set_volume(0.'x') #Valores entre 0 e 1
            #self.mob_hit_sound.append(s)

        # Som do Player sendo atingido pela bullet
        self.player_hit_sound = pg.mixer.Sound(path.join(snd_folder, 'player_hit_sound.wav'))
        #for snd in PLAYER_HIT_SOUND:
            #s = pg.mixer.Sound(path.join(snd_folder, snd))
            #s.set_volume(1) #Valores entre 0 e 1
            #self.player_hit_sound.append(s)

        # Som do player morrendo:
        #self.player_die_sound = []
        #for snd in PLAYER_DIE_SOUND:
            #s = pg.mixer.Sound(path.join(snd_folder, snd))
            #s.set_volume(0.'x') #Valores entre 0 e 1
            #self.player_die_sound.append(s)



    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mobs2 = pg.sprite.Group()

        # OBS: a função enumerate fornece o Index e o item de uma lista(ex: l[0]=a, enumerate fornece 0 e a)
        self.map = Map(path.join(self.map_folder, "map4.txt")) # ORIGINAL
        #self.map = Map(path.join(self.map_folder, "mapa_f1.txt")) # DUDA
        for row, tiles in enumerate(self.map.data): #Para cada fileira
            for col, self.tile in enumerate(tiles): #Para cada fileira/coluna
                # Adiciona as paredes conforme os '1'no mapa
                if self.tile == '1':
                    Wall(self, col, row)
                # Adiciona os mobs conforme os 'M' no mapa
                if self.tile == 'M':
                    Mob(self, self.player, col, row)
                # Adiciona os mobs2 conforme os 'N' no mapa
                if self.tile == 'N':
                    Mob2(self, self.player, col, row)
                #OBS: É possível colocar o spawn do jogador inserindo um P no mapa
                if self.tile == 'P':
                    self.player = Player(self, col, row)
                # Ir para o próximo nível
                #if self.tile == 'F':
                    #self.tile_F.pos == 'F'

             
        self.camera = Camera(self.map.width, self.map.height)
        self.paused = False
        #self.effects_sounds['level_start'].play()

    #def new2(self):
        # initialize all variables and do all the setup for a new game
        #self.all_sprites = pg.sprite.LayeredUpdates()
        #self.walls = pg.sprite.Group()
        #self.mobs = pg.sprite.Group()
        #self.bullets = pg.sprite.Group()
        #self.mobs2 = pg.sprite.Group()

        # OBS: a função enumerate fornece o Index e o item de uma lista(ex: l[0]=a, enumerate fornece 0 e a)
        #self.map = Map(path.join(self.map_folder, "map5.txt"))
        #for row, tiles in enumerate(self.map.data): #Para cada fileira
            #for col, tile in enumerate(tiles): #Para cada fileira/coluna
                # Adiciona as paredes conforme os '1'no mapa
                #if tile == '1':
                    #Wall(self, col, row)
                # Adiciona os mobs conforme os 'M'no mapa
                #if tile == 'M':
                    #Mob(self, self.player, col, row)
                #OBS: É possível colocar o spawn do jogador inserindo um P no mapa
                #if tile == 'P':
                    #self.player = Player(self, col, row)
                # Adiciona o background
                #if tile == 'N':
                    #Mob2(self, self.player, col, row)
                # Ir para o próximo nível
                #if tile == 'F':

        
        # ///Para fazer o spawn do player no TILEDMAP///
        #self.player = Player(self, 5, 5)        
        #self.camera = Camera(self.map.width, self.map.height)
        #self.paused = False
        #self.effects_sounds['level_start'].play()

        
    #def new3(self):
        # initialize all variables and do all the setup for a new game
        #self.all_sprites = pg.sprite.LayeredUpdates()
        #self.walls = pg.sprite.Group()
        #self.mobs = pg.sprite.Group()
        #self.bullets = pg.sprite.Group()
        #self.mobs2 = pg.sprite.Group()

        # OBS: a função enumerate fornece o Index e o item de uma lista(ex: l[0]=a, enumerate fornece 0 e a)
        #self.map = Map(path.join(self.map_folder, "map_f3.txt"))
        #for row, tiles in enumerate(self.map.data): #Para cada fileira
            #for col, tile in enumerate(tiles): #Para cada fileira/coluna
                # Adiciona as paredes conforme os '1'no mapa
                #if tile == '1':
                    #Wall(self, col, row)
                # Adiciona os mobs conforme os 'M'no mapa
                #if tile == 'M':
                    #Mob(self, self.player, col, row)
                #OBS: É possível colocar o spawn do jogador inserindo um P no mapa
                #if tile == 'P':
                    #self.player = Player(self, col, row)
                # Adiciona o background
                #if tile == 'N':
                    #Mob2(self, self.player, col, row)
                # Ir para o próximo nível
                #if tile == 'F':

        
        # ///Para fazer o spawn do player no TILEDMAP///
        #self.player = Player(self, 5, 5)        
        #self.camera = Camera(self.map.width, self.map.height)
        #self.paused = False
        #self.effects_sounds['level_start'].play()



    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            # Vai fazer o update apenas se o jogo não tiver no pause
            if not self.paused:
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
        # Condição do game over:

        # /// Tentativa de fases (NÃO DEU CERTO) ///
        #if self.player.pos == vec(28, 0) * TILESIZE
            #self.current_level += 1
            #if self.current_level == 2:
                #self.new_2()
            #else:
                #self.new_3()
        # Quando o player da um tapa no Octopy
        # :
        #for event in pg.event.get():
            #if event.type == pg.KEYDOWN:
                # Define um jeito de sair do jogo
                #if event.key == pg.K_ESCAPE:
                    #tapas = pg.sprite.spritecollide(self.player, self.mobs, False)
                    #for mob in tapas:
                        #if tapa.type == self.player.tapa:
                            #tapa.kill()
                            #self.mobs.health -= TAPA_DAMAGE
                            #if self.mobs.health <= 0:
                                #self.mobs.kill()


        #for hit in hits:
            #self.player.health -= BULLET_DAMAGE
            # Game over se o Player perder toda a sua health
            #if self.player.health <= 0:
                #self.playing = False
        # Quando as pedras atingem o player: (OBS: Não da certo fazer com o player)
        hits = pg.sprite.spritecollide(self.player, self.bullets, True, False)
        for hit in hits:
            self.player.health -= BULLET_DAMAGE
            self.player_hit_sound.play()
            #choice(self.player_hit_sound).play()
            # Game over se o Player perder toda a sua health
            if self.player.health <= 0:
                #choice(self.game.player_die_sound).play()
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
        #self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite)) # Aplica a câmera ao sprite
        # Para desenhar o HUD
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        #self.draw_text("Tempo: {}".format(self.sec), self.hud_font, 30, WHITE, WIDTH - 10, 10, align='ne')
        if self.paused:
            # Fazer a tela meio fosca por cima da superfície do jogo
            self.screen.blit(self.dim_screen, (0, 0))
            # Desenhar o texto "PAUSED" quando o jogo entrar no pause (os dimensionamentos para a posição foram feitos visualmente)
            self.draw_text("Paused", self.title_font, 105, WHITE, WIDTH/2 - 120, HEIGHT/2 + 130, align="center")
            # Fazer o blit da imagem da tela 0 Octopy
            self.screen.blit(self.pause_img, (0, 0))
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
                if event.key == pg.K_p:
                    self.paused = not self.paused
            # /// Ação do tapa da peixe (NÃO FUNCIONA) ///
                #if event.key == pg.K_SPACE:
                    #self.tapas = pg.sprite.spritecollide(self.player, self.mobs, True, False)
                    #for tapa in self.tapas:
                        #self.mob.health -= TAPA_DAMAGE
                
    # Define a função para a tela de início
    def show_start_screen(self):
        self.screen.fill(BLACK)
        # Desenha a imagem OCTOPY, posições (0, 0) pois ja foi feito o ajuste do tamanho para o tamanho da superfície de jogo
        self.screen.blit(self.pause_img, (0, 0))
        # Desenha o texto na tela, chamando a função draw_text
        self.draw_text("Press a key to start", self.title_font, 75, WHITE, WIDTH/2, HEIGHT/2 + 250, align='center')
        # Faz o flip do display e mostra os desenhos feitos
        pg.display.flip()
        # Função que espera o jogador apertar e soltar uma key para começar
        self.wait_for_key()

    def between_levels_screen(self):
        self.screen.fill(BLACK)
        # Desenha a imagem OCTOPY, posições (0, 0) pois ja foi feito o ajuste do tamanho para o tamanho da superfície de jogo
        self.screen.blit(self.next_level_img, (0, 0))
        # Desenha o texto na tela, chamando a função draw_text
        self.draw_text("Press a key to start", self.title_font, 75, WHITE, WIDTH/2, HEIGHT/2 + 250, align='center')
        # Faz o flip do display e mostra os desenhos feitos
        pg.display.flip()
        # Função que espera o jogador apertar e soltar uma key para começar
        self.wait_for_key()

    
    # Define a função para a tela de game over
    def show_go_screen(self):
        #self.screen.blit(self.dim_screen, (0, 0))
        self.screen.fill(BLACK)
        # Desenha a imagem game over OCTOPY, posições (0, 0) pois ja foi feito o ajuste do tamanho para o tamanho da superfície de jogo
        self.screen.blit(self.game_over_img, (0, 0))
        # Desenha o texto na tela, chamando a função draw_text
        self.draw_text("Press a key to start", self.title_font, 75, WHITE, WIDTH/2, HEIGHT/2 + 275, align='center')
        # Faz o flip do display e mostra os desenhos feitos
        pg.display.flip()
        # Função que espera o jogador apertar e soltar uma key para começar
        self.wait_for_key()

    def wait_for_key(self):
        # Pra que o jogo não recomece se por acaso o jogador continue apertando uma tecla após o game over
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

        

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    #while g.run():
        #if self.playing == False:
            #g.show_go_screen()
        #if self.player.pos == vec (28, 0) * TILESIZE:
            #break
    #g.between_levels_screen()
    #g.new2()
    #while g.run():
        #if self.playing == False:
            #g.show_go_screen()
        #if self.player.pos == vec (28, 0) * TILESIZE:
            #break
    #g.between_levels_screen()
    #g.new3()
    g.show_go_screen()

# Octopy v1.0

import pygame as pg
import sys
from os import path
from Settings import *
from Sprites import *
from Tilemap import *
import time

# funções do HUD:
def draw_player_health(surf, x, y, pct): # Faz o desenho da barra de vidas do player
    if pct < 0: # Porcentagem (da vida), por isso não deve ser negativa
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT) # Desenha a barra de vida
    if pct >= 0.75:
        col = GREEN
    elif pct >= 0.50:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect) # Preenche a barra com as cores
    pg.draw.rect(surf, WHITE, outline_rect, 2) # Faz o outline da barra

# A class game engloba diversas funções que funcionam como mecanismos de jogo
class Game:
    def __init__(self):
        pg.init() # Dá início ao pygame
        pg.mixer.init() # 
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) # Define a superfície da tela
        pg.display.set_caption(TITLE) # Define o título do jogo
        self.clock = pg.time.Clock()
        # Taxa de repetição dos movimentos (Se a tecla ficar pressionada por meio segundo, o jogador começa a se movimentar continuamente)
        pg.key.set_repeat(500, 100) 
        self.load_data()
        self.current_level = 1

    # Função utilizada para incluir textos e definir suas posições na tela
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size) # Define a fonte
        text_surface = font.render(text, True, color) 
        text_rect = text_surface.get_rect()
        # Diferentes locais para o texto
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
        # Cria o caminho para as pastas
        game_folder = path.dirname(__file__) # Pasta de jogo
        img_folder = path.join(game_folder, 'img') # Pasta das imagens
        snd_folder = path.join(game_folder, 'snd') # Pasta dos sons
        music_folder = path.join(game_folder, 'music') # Pasta das músicas
        self.map_folder = path.join(game_folder, 'maps') # Pasta dos mapas

        # Escolha das fontes para os textos no jogo
        self.title_font = path.join(img_folder, 'Octopy.TTF')
        self.hud_font = path.join(img_folder, 'Hud_font.TTF')

        # Definição de uma tela parcialmente escura (da tela pause)
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

        # Carregar a imagem de fundo pra tela de mudança de level        
        self.next_level_img = pg.image.load(path.join(img_folder, 'Telas_2.png')).convert_alpha()
        # Transformar a imagem para o formato da superfície de jogo        
        self.next_level_img = pg.transform.scale(self.next_level_img, self.screen.get_size())

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

        # Define, carrega e redimenciona algumas imagens
        # Bullets
        self.bullet_img = pg.Surface((10,5)) #determina o tamalho, nessa caso pequeno
        self.bullet_img.fill(DARKGREY)
        
        # Paredes
        self.wall_img = pg.image.load(path.join(img_folder, 'tileareia.png')).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        
        # Tile 'F'
        self.bg_img = pg.image.load(path.join(img_folder, 'tileagua.png')).convert_alpha()
        self.bg_img = pg.transform.scale(self.bg_img, (TILESIZE, TILESIZE))

        self.end_img = pg.image.load(path.join(img_folder, 'tileend.png')).convert_alpha()
        self.end_img = pg.transform.scale(self.end_img, (TILESIZE, TILESIZE))

        # Sound loading
        # Som do background
        pg.mixer.music.load(path.join(music_folder, 'musicadowii.ogg'))

        # Som do Player sendo atingido pela bullet
        self.player_hit_sound = pg.mixer.Sound(path.join(snd_folder, 'player_hit_sound.wav'))


    def new(self):
        # Agrupa os sprites por layers (camadas)
        self.all_sprites = pg.sprite.LayeredUpdates()
        # Define os grupos de sprites
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mobs2 = pg.sprite.Group()
        self.fi = pg.sprite.Group()
        self.end = pg.sprite.Group()

        # OBS: a função enumerate fornece o Index e o item de uma lista(ex: l[0]=a, enumerate fornece 0 e a)
        self.map = Map(path.join(self.map_folder, "level1.txt")) # ORIGINAL
        for row, tiles in enumerate(self.map.data): #Para cada fileira
            for col, self.tile in enumerate(tiles): #Para cada fileira/coluna
                if self.tile == 'P':
                    self.player = Player(self, col, row)
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
                #Ir para o próximo nível
                if self.tile == 'F':
                    F(self, col, row)
        
        # Define a câmera
        self.camera = Camera(self.map.width, self.map.height)
        # Parte do mecanismo para realizar o pause durante o jogo
        self.paused = False

    def new2(self):
        # Agrupa os sprites por layers (camadas)
        self.all_sprites = pg.sprite.LayeredUpdates()
        # Define os grupos de sprites
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mobs2 = pg.sprite.Group()
        self.fi = pg.sprite.Group()
        self.end = pg.sprite.Group()

        # OBS: a função enumerate fornece o Index e o item de uma lista(ex: l[0]=a, enumerate fornece 0 e a)
        self.map = Map(path.join(self.map_folder, "level2.txt"))
        for row, tiles in enumerate(self.map.data): #Para cada fileira
            for col, tile in enumerate(tiles): #Para cada fileira/coluna
                if tile == 'P':
                    self.player = Player(self, col, row)

        for row, tiles in enumerate(self.map.data): #Para cada fileira
            for col, tile in enumerate(tiles): #Para cada fileira/coluna
                # Adiciona as paredes conforme os '1'no mapa
                if tile == '1':
                    Wall(self, col, row)
                # Adiciona os mobs conforme os 'M'no mapa
                if tile == 'M':
                    Mob(self, self.player, col, row)
                #OBS: É possível colocar o spawn do jogador inserindo um P no mapa
                # Adiciona o background
                if tile == 'N':
                    Mob2(self, self.player, col, row)
                # Ir para o próximo nível
                if tile == 'F':
                    F(self, col, row)

        # Define a câmera
        self.camera = Camera(self.map.width, self.map.height)
        # Parte do mecanismo para realizar o pause durante o jogo
        self.paused = False
        
    def new3(self):
        # Agrupa os sprites por layers (camadas)
        self.all_sprites = pg.sprite.LayeredUpdates()
        # Define os grupos de sprites
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mobs2 = pg.sprite.Group()
        self.end = pg.sprite.Group()

        # OBS: a função enumerate fornece o Index e o item de uma lista(ex: l[0]=a, enumerate fornece 0 e a)
        self.map = Map(path.join(self.map_folder, "level3.txt"))
        for row, tiles in enumerate(self.map.data): #Para cada fileira
            for col, tile in enumerate(tiles): #Para cada fileira/coluna
                if tile == 'P':
                    self.player = Player(self, col, row)
        for row, tiles in enumerate(self.map.data): #Para cada fileira
            for col, tile in enumerate(tiles): #Para cada fileira/coluna
                # Adiciona as paredes conforme os '1'no mapa
                if tile == '1':
                    Wall(self, col, row)
                # Adiciona os mobs conforme os 'M'no mapa
                if tile == 'M':
                    Mob(self, self.player, col, row)
                #OBS: É possível colocar o spawn do jogador inserindo um P no mapa
                # Adiciona o background
                if tile == 'N':
                    Mob2(self, self.player, col, row)
                #  Finalllll
                if tile == 'E':
                    End(self, col, row)

        # Define a câmera
        self.camera = Camera(self.map.width, self.map.height)
        # Parte do mecanismo para realizar o pause durante o jogo
        self.paused = False


    def run(self):
        # Game loop (se self.playing == False, o jogo acaba)
        self.playing = True
        pg.mixer.music.play(loops=-1) # Deixa a música de fundo em loop
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            # Vai fazer o update apenas se o jogo não tiver no pause
            if not self.paused:
                self.update()
                if self.get_to_end:
                    self.playing = False
            self.draw()

    def quit(self):
        # Define a saída do jogo
        pg.quit()
        sys.exit()

    def eng_game_screen(self):
        self.screen.fill(BLACK)
        # Desenha a imagem OCTOPY, posições (0, 0) pois ja foi feito o ajuste do tamanho para o tamanho da superfície de jogo
        self.screen.blit(self.pause_img, (0, 0))
        # Desenha o texto na tela, chamando a função draw_text
        self.draw_text("CONGRATULATIONS!", self.title_font, 75, WHITE, WIDTH/2, HEIGHT/2 - 275, align='center')
        self.draw_text('You have completed the game', self.title_font, 60, WHITE, WIDTH/2, HEIGHT/2 +250, align='center')
        self.draw_text("Press a key to play again", self.title_font, 45, WHITE, WIDTH/2, HEIGHT/2 +300, align='center')
        # Faz o flip do display e mostra os desenhos feitos
        pg.display.flip()
        # Função que espera o jogador apertar e soltar uma key para realizar ação
        self.wait_for_key()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        #A camera segue o sprite que for colocado entre parenteses)
        self.camera.update(self.player)

        # Quando as pedras atingem o player:
        hits = pg.sprite.spritecollide(self.player, self.bullets, True, False)
        for hit in hits:
            self.player.health -= BULLET_DAMAGE
            self.player_hit_sound.play()

            # Condição de game over
            if self.player.health <= 0:
                self.playing = False
        
        # Sprite collide entre o Player e o grupo de sprites F (passa o nível)
        get_to_p = pg.sprite.spritecollide(self.player, self.fi, False)
        self.get_to_end = pg.sprite.spritecollide(self.player, self.end, False)
        if get_to_p:
            self.current_level += 1
            if self.current_level == 2:
                self.between_levels_screen()
                self.new2()
            else:
                self.between_levels_screen()
                self.new3()


    def draw(self):
        self.screen.fill(BGCOLOR) # A BGCOLOR é azul escuro
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite)) # Aplica a câmera ao sprite
        # Para desenhar o HUD
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
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
                
    # Define a tela de início
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

    # Define a tela do next level
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
    
    # Define a tela de game over
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
        # Pra que o jogo não faça nada até o jogador pressionar uma tecla
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
    while g.update():
        if self.game.get_to_end:
            break
    g.show_go_screen()
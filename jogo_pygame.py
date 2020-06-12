
import pygame
import random
import os # Da os comandos para possibilitar a criação de um caminho para as pastas
import time

WIDTH = 480
HEIGHT = 600
FPS = 60

#Cores (números variam de 0 a 255 para as cores vermelho, verde e azul)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL_ESCURO = (0, 0, 255)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)
ROSA = (255, 0, 255)
AZUL_CLARO = (0, 255, 255)
MARROM = (92,64,51)

# Criando as pastas de assets (imagens e sons)
# OBS: para o Windows vai aparecer: "C:\Users\gustavopinheiro\Documents\img"
# OBS 2: para o MacOS vai aparecer: "/Users/gustavopinheiro/Documents/img"
game_folder = os.path.dirname(__file__) # __file__ é uma ferramenta que reconhece o nome da pasta
img_folder = os.path.join(game_folder, "img") #Junta com o caminho criado para o game, e acrescenta um pedaço (para encontrar a pasta dentro da pasta principal)
# Sprite para o player
class Player(pygame.sprite.Sprite):
    # O código que queremos rodar quando quando criamos o Player
    def __init__(self):
        # Para fazer o sprite funcionar
        pygame.sprite.Sprite.__init__(self)
        # Como o sprite vai ser (imagem)
        self.image =  peixinho_images_esquerda[0]
        self.image.set_colorkey(PRETO)# Para retirar possíveis erros de cores no fundo da imagem
        # Como o sprite vai se posicionar na tela
        self.rect = self.image.get_rect() # Retângulos que definem a altura e a largura da imagem do sprite
        self.radius = 10
        self.rect.center = (WIDTH / 2, HEIGHT / 2) #Define a posição do sprite
        self.rect.bottom=HEIGHT-10
        self.speedx=0
        self.speedy=0
        self.frame_esquerda=0
        self.frame_direita=0
        self.frame_tapa = 0
        self.frame_rate = 300
        self.last_update = pygame.time.get_ticks()
        self.tapa = False
    def update(self): #o que ele faz cada vez que atualiza
        now = pygame.time.get_ticks()
        self.speedx = 0 #não se mova se nada foi apertado
        self.speedy = 0
        keystate = pygame.key.get_pressed() #volta uma lista com que teclas estão apertatdas
        if keystate[pygame.K_LEFT]:
            if now - self.last_update > self.frame_rate:
                self.last_update=now
                self.frame_esquerda +=1
                if self.frame_esquerda == 6:
                    self.frame_esquerda =0
                else:
                    self.image = peixinho_images_esquerda[self.frame_esquerda] 
                    self.image.set_colorkey(PRETO)
        if keystate[pygame.K_RIGHT]:
            if now - self.last_update > self.frame_rate:
                self.last_update=now
                self.frame_direita +=1
                if self.frame_direita == 6:
                    self.frame_direita =0
                else:
                    self.image = peixinho_images_direita[self.frame_direita] 
                    self.image.set_colorkey(PRETO)

        if keystate[pygame.K_SPACE] or self.tapa == True:
                self.tapa = True
                if now - self.last_update > self.frame_rate:
                    self.last_update=now
                    self.frame_tapa +=1
                    if self.frame_tapa == 4 :
                        self.frame_tapa = 0
                        self.tapa = False
                    else:
                        self.image = peixinho_images_tapa[self.frame_tapa] 
                        self.image.set_colorkey(PRETO)

        if keystate[pygame.K_LEFT]:
            self.speedx = -3
        if keystate[pygame.K_RIGHT]:
            self.speedx = 3
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH #nunca pode passar de WIDTH para a direita 
        if self.rect.left < 0:
            self.rect.left = 0 #nunca pode passar do iniciio da tela
            
        if keystate[pygame.K_UP]:
            self.speedy = -1.5
        if keystate[pygame.K_DOWN]:
            self.speedy = 1.5
        if self.rect.top <0: #AQUI QUE NAO FUNCIONAAAAAAAAAAAAAAAAA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.rect.top =0  #nunca pode passar de WIDTH para a direita 
        if self.rect.bottom > HEIGHT:
            self.rect.bottom =HEIGHT#nunca pode passar do iniciio da tela    

        self.rect.x += self.speedx #move a imagem na velocidade do speedx - x é horizontal
        self.rect.y += self.speedy
        
        

        
class Bullet(pygame.sprite.Sprite):
     def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,5)) #determina o tamalho, nessa caso pequeno
        self.image.fill((MARROM)) #pinta de amarelo
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery  = y-14
        self.speedx = random.randrange(3,10)
     def update(self):
         self.rect.x += self.speedx
         if self.rect.left<0: #se a bala sair da tela
                self.kill   #a bala deixa de existir


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = octopy_images[0]
        self.image.set_colorkey(PRETO)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.radius = 15
        pygame.draw.circle (self.image, VERMELHO, self.rect.center, self.radius)
        self.frame=0
        self.frame_rate = 200
        self.last_update = pygame.time.get_ticks()
        self.last_update1 = pygame.time.get_ticks()
    def update(self):
        now1 = pygame.time.get_ticks()
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update=now
            self.frame +=1
            if self.frame == len(octopy_images):
                self.frame=0
            else:
                self.image = octopy_images[self.frame] 
                self.image.set_colorkey(PRETO)
        if now1 - self.last_update1 > 1000:
            self.last_update1=now1
            mob.shoot()   
        
        
    def shoot(self):
        bullet=Bullet(self.rect.centerx, self.rect.centery) #no meio x do jogador e no topo do jogador
        all_sprites.add(bullet)
        bullets.add(bullet)
        
# INICIALIZA O PYGAME E CRIA A JANELA DO JOGO

# Inicializa o Pygame
pygame.init()
# Para colocar o som, é necessário inicializar o mixer
pygame.mixer.init()
# Cria a janela do jogo
screen = pygame.display.set_mode((WIDTH,HEIGHT))
# Introduz um nome para o jogo
pygame.display.set_caption("Octopy")
# Controla a velocidade e garante que o jogo vai rodar no FPS definido
clock = pygame.time.Clock()

#pega todas as imagens 
octopy_images = []
octopy_list = ["octopy_0.png", "octopy_1.png", "octopy_2.png", "octopy_3.png", "octopy_4.png", "octopy_5.png"]
for img in octopy_list:
    octopy_images.append(pygame.image.load(os.path.join(img_folder, img)).convert())

peixinho_images_esquerda = []
peixinho_list_esquerda = ["peixinho_00.png", "peixinho_01.png","peixinho_02.png","peixinho_03.png","peixinho_04.png","peixinho_05.png"]
for img in peixinho_list_esquerda:
    peixinho_images_esquerda.append(pygame.image.load(os.path.join(img_folder, img)).convert())

peixinho_images_direita = []
peixinho_list_direita = ["peixinho_06.png", "peixinho_07.png","peixinho_08.png","peixinho_09.png","peixinho_10.png","peixinho_11.png"]
for img in peixinho_list_direita:
    peixinho_images_direita.append(pygame.image.load(os.path.join(img_folder, img)).convert())

peixinho_images_tapa = []
peixinho_list_tapa = ["peixinho_12.png", "peixinho_13.png","peixinho_14.png","peixinho_15.png"]
for img in peixinho_list_tapa:
    peixinho_images_tapa.append(pygame.image.load(os.path.join(img_folder, img)).convert())

bolha_image=pygame.image.load(os.path.join(img_folder, "bolha_0.png")).convert()

tela_images=[]
tela_list=['telas_0.png', 'telas_1.png', 'telas_2.png'] #está na ordem octopy, game over e next level
for img in tela_list:
    tela_images.append(pygame.image.load(os.path.join(img_folder, img)).convert())


#Grupo de sprites
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group() #group para checar colisões depois
bullets = pygame.sprite.Group()
player = Player() 
mob=Mob()
mobs.add(mob)
all_sprites.add(player) #adiciona player to all sprites
all_sprites.add(mob)
# GAME LOOP
running = True
while running:
    # Mantém o loop na velocidade correta (FPS)
    clock.tick(FPS)

    #Events (Process input):
    for event in pygame.event.get():
        #Para que o botão X da tela sirva para dar exit no jogo
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:    
                tapa= pygame.sprite.spritecollide(player, mobs, False)
                if tapa:
                    running = False

    #Updates     
    all_sprites.update()
    #colisões
    hits= pygame.sprite.spritecollide(player, bullets, True, False) #colisao de sprite e um grupo
    
    #Faz uma lista dos mobs que colidem com o player. se fosse True, deletava as duas sprites
 
    #DRAW/RENDER
    screen.fill(AZUL_ESCURO)
    all_sprites.draw(screen)
    #Fazer isso depois de desenhar tudo (virar do desenho para o display) - DOUBLE BUFFERING
    pygame.display.flip()

pygame.quit()

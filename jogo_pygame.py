
import pygame
import random
import os # Da os comandos para possibilitar a criação de um caminho para as pastas

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
        self.image = pygame.image.load(os.path.join(img_folder, "peixinho.png")).convert() #Função para realizar um desenho padrão
        self.image.set_colorkey(PRETO)# Para retirar possíveis erros de cores no fundo da imagem
        # Como o sprite vai se posicionar na tela
        self.rect = self.image.get_rect() # Retângulos que definem a altura e a largura da imagem do sprite
        self.rect.center = (WIDTH / 2, HEIGHT / 2) #Define a posição do sprite
        self.rect.bottom=HEIGHT-10
        self.speedx=0
        self.speedy=0
        
    def update(self): #o que ele faz cada vez que atualiza
        self.speedx = 0 #não se mova se nada foi apertado
        self.speedy = 0
        keystate = pygame.key.get_pressed() #volta uma lista com que teclas estão apertatdas
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH #nunca pode passar de WIDTH para a direita 
        if self.rect.left < 0:
            self.rect.left = 0 #nunca pode passar do iniciio da tela
            
        if keystate[pygame.K_UP]:
            self.speedy = -2.5
        if keystate[pygame.K_DOWN]:
            self.speedy = 2.5
        if self.rect.top <0: #AQUI QUE NAO FUNCIONAAAAAAAAAAAAAAAAA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.rect.top =0  #nunca pode passar de WIDTH para a direita 
        if self.rect.bottom > HEIGHT:
            self.rect.bottom =HEIGHT#nunca pode passar do iniciio da tela    

        self.rect.x += self.speedx #move a imagem na velocidade do speedx - x é horizontal
        self.rect.y += self.speedy

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,40))
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width) 
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3,3)
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 18: #se sai da tela, cria um novo
            self.rect.x = random.randrange(WIDTH - self.rect.width) 
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1,8)
        
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
#Grupo de sprites
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group() #group para checar colisões depois
player = Player() 
all_sprites.add(player) #adiciona player to all sprites
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
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
            
            
    #Updates
    all_sprites.update()
    
    #ve se há colisão
    hits= pygame.sprite.spritecollide(player, mobs, False) #Faz uma lista dos mobs que colidem com o player. se fosse True, deletava as duas sprites
    if hits: #se tem alcugam coisa em hits
        running=False #acaba o jogo
    #DRAW/RENDER
    screen.fill(AZUL_CLARO)
    all_sprites.draw(screen)
    #Fazer isso depois de desenhar tudo (virar do desenho para o display) - DOUBLE BUFFERING
    pygame.display.flip()

pygame.quit()


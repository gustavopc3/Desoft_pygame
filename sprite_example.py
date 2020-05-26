#Pygame template - esqueleto para novo projeto em pygame 
import pygame
import random

WIDTH = 360
HEIGHT = 480
FPS = 30

#Cores (números variam de 0 a 255 para as cores vermelho, verde e azul)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL_ESCURO = (0, 0, 255)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)
ROSA = (255, 0, 255)
AZUL_CLARO = (0, 255, 255)

# Sprite para o player
class Player(pygame.sprite.Sprite):
    # O código que queremos rodar quando quando criamos o Player
    def __init__(self):
        # Para fazer o sprite funcionar
        pygame.sprite.Sprite.__init__(self)
        # Como o sprite vai ser (imagem)
        self.image = pygame.Surface((50, 50)) #Função para realizar um desenho padrão
        self.image.fill(VERDE)
        # Como o sprite vai
        self.rect = self.image.get_rect() # Retângulos que definem a altura e a largura da imagem do sprite
        self.rect.center = (WIDTH / 2, HEIGHT / 2) #Define a posição do sprite

    def update(self):
        self.rect.x += 5
        if self.rect.left > WIDTH:
            self.rect.right = 0


# INICIALIZA O PYGAME E CRIA A JANELA DO JOGO

# Inicializa o Pygame
pygame.init()
# Para colocar o som, é necessário inicializar o mixer
pygame.mixer.init()
# Cria a janela do jogo
screen = pygame.display.set_mode((WIDTH,HEIGHT))
# Introduz um nome para o jogo
pygame.display.set_caption("My game")
# Controla a velocidade e garante que o jogo vai rodar no FPS definido
clock = pygame.time.Clock()
#Grupo de sprites
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

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
    #DRAW/RENDER
    screen.fill(PRETO)
    all_sprites.draw(screen)
    #Fazer isso depois de desenhar tudo (virar do desenho para o display) - DOUBLE BUFFERING
    pygame.display.flip()

pygame.quit()
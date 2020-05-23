'''
Jogo pygame
Authors: Gustavo Pinheiro
         Maria Eduarda Mourão
         Rafaela Zyingier
'''

import sys
import pygame

CINZA = (127, 127, 127)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)

def main():

    pygame.init()  # inicia rotinas do pygame

    surf = pygame.display.set_mode((400, 400)) # cria superficie para o jogo

    pygame.display.set_caption("Exemplo pygame")
   
    pos_peixinho = [200, 200]
    velocidade_peixinho = [0.5, 0.27]
    delta_peixinho = {"esquerda":0, "direita":0, "acima":0, "abaixo":0}




    clock = pygame.time.Clock() # objeto para controle da atualizações de imagens

    # Game Loop
    while True:
        delta_time = clock.tick(60) # garante um FPS máximo de 60Hz
        
        # Coleta de eventos
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                pygame.quit() # terminado a aplicação pygame
                sys.exit()    # sai pela rotina do sistema
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    delta_peixinho["esquerda"] = 1
                elif evento.key == pygame.K_RIGHT:
                    delta_peixinho["direita"] = 1
                elif evento.key == pygame.K_UP:
                    delta_peixinho["acima"] = 1
                elif evento.key == pygame.K_DOWN:
                    delta_peixinho["abaixo"] = 1


            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT:
                    delta_peixinho["esquerda"] = 0
                if evento.key == pygame.K_RIGHT:
                    delta_peixinho["direita"] = 0
                elif evento.key == pygame.K_UP:
                    delta_peixinho["acima"] = 0
                elif evento.key == pygame.K_DOWN:
                    delta_peixinho["abaixo"] = 0

        surf.fill(CINZA)
        
        pos_peixinho[0] += int((delta_peixinho["direita"] - delta_peixinho["esquerda"]) * velocidade_peixinho[0] * delta_time)  
        pos_peixinho[1] += int((delta_peixinho["abaixo"] - delta_peixinho["acima"]) * velocidade_peixinho[1]* delta_time)
        
        pygame.draw.circle(surf, AMARELO, pos_peixinho, 50)
    
        
       
if __name__ == "__main__":
    main()

import pygame
from settings import *
from debug import debug
import os
import random
import time
import character
import buttons


#teste5

pygame.init()

clock = pygame.time.Clock() #variavel para controlar o FPS, usada no começo do loop de combate


screen = pygame.display.set_mode((WIDHT, HEIGHT)) #inicia a janela baseado nos parametros em Settings

pygame.display.set_caption('Slime Combat II') #Muda o nome da janela do jogo


run = True

background_img = pygame.image.load('graphics/background/background.jpg').convert_alpha() #coloca um background

slime_panel_img = pygame.image.load('graphics/Icons/SlimeStatusBar.png').convert_alpha() #barrinha embaixo do background, onde fica a vida e mana para o protagonista

enemy_panel_img = pygame.image.load('graphics/Icons/EnemyStatusBar.png').convert_alpha() #barrinha embaixo do background, onde fica a vida e mana para inimigos

attack_icon = pygame.image.load('graphics/Icons/Sword.png').convert_alpha()
active_attack_icon = pygame.image.load('graphics/Icons/S_Active.png').convert_alpha()


#combate e turnos
current_fighter = 1
total_fighters = 3
action_cd = 0
action_wait = 30
attack = False
magic = False
potion = False
clicked = False
level_over = 0
game_win = 0




font = pygame.font.SysFont('Times New Roman', 18)#fonte

#RGG
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

#background
def draw_bg():
   screen.blit(background_img, (0,0))

#imprimir texto
def drawn_text(text, font, text_col, x,y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

#paineis para se colocara vida 
def draw_panelSlime():
        screen.blit(slime_panel_img, (0,450))
        drawn_text(f'{Slime.name} HP: {Slime.hp}', font, red, 100, 230)
        drawn_text(f'{Slime.name} MP: {Slime.mp}', font, blue, 100, 250)

def draw_panelEnemy():
        screen.blit(enemy_panel_img, (450,450))
        for count, i in enumerate(enemy_list):
            drawn_text(f'{i.name} HP: {i.hp} {count}', font, red, 550 , 450 + 80*count )
            drawn_text(f'{i.name} MP: {i.mp}', font, blue, 550, 480 + 80*count )


#create enemies
Slime = character.Character(140,300,1,'Slime',100,100,10,10,10,2,2,1,8,0)
Zombie1 = character.Character(700,300,5 ,'Zombie',50,0,10,5,0,0,0,1,7,1)
Zombie2 = character.Character(500,300,5 ,'Zombie',50,0,10,5,0,0,0,1,7,1)
enemy_list = []
enemy_alive = 0
enemy_list.append(Zombie1)
enemy_list.append(Zombie2)


#create buttons
sword_button = buttons.Button(screen, 50,500, attack_icon, 50, 50)


while run:
    clock.tick(FPS) #limita o fps para o colocado em settings

    draw_bg() #mostra background na tela
    draw_panelSlime() #mostra o painel do pc
    
        

    #Gerar personagens
    Slime.update()
    Slime.draw()
    sword_button.draw()
    for Enemy in enemy_list:
        Enemy.draw()
        Enemy.update()
        draw_panelEnemy()

    #controlar o ataque
    attack = False
    magic = False
    potion = False
    taget = None

 
    pygame.mouse.set_visible(True)

    pos = pygame.mouse.get_pos()

        

    for i, enemy in enumerate(enemy_list):
        if sword_button.clicked == True:
            print('ok')
            sword_button.image = active_attack_icon
            if enemy.rect.collidepoint(pos):
                pygame.mouse.set_visible(False)
                screen.blit(attack_icon, pos)
                if clicked == True:
                    attack = True
                    target = enemy_list[i]
                     
        
        if game_win == 0:
        #player actions
            if Slime.alive == True:
                if current_fighter == 1:

                    if attack == True and target.alive == True:
                        action_cd += 1
                        if action_cd >= action_wait:
                            #attack
                            if attack == True and target != None:                        
                                Slime.attack(target)
                                current_fighter += 1
                                action_cd = 0
                                sword_button.clicked = False
                                
            else:
                game_win = -1
                sword_button.clicked = False


            #enemy actions
            for count, enemy in enumerate(enemy_list):
                if current_fighter == 2 + count:
                    if enemy.alive == True:
                        action_cd += 1
                        if action_cd >= action_wait:
                            #attack
                            enemy.attack(Slime)
                            current_fighter += 1
                            action_cd = 0
                            time.sleep(0.08)
                    else:
                        current_fighter += 1


            
            #reset turns
            if current_fighter > total_fighters :
                current_fighter = 1
    if sword_button.clicked == False:
        sword_button.image = attack_icon

    #check para vitoria
    for enemy in enemy_list:
        if enemy.alive == True:
            enemy_alive += 1

    if enemy_alive == 0:
        game_win = 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()


pygame.quit()



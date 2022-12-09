import pygame
from settings import *
from debug import debug
import os

#teste

pygame.init()

clock = pygame.time.Clock() #variavel para controlar o FPS, usada no começo do loop de combate


screen = pygame.display.set_mode((WIDHT, HEIGHT)) #inicia a janela baseado nos parametros em Settings

pygame.display.set_caption('Slime Combat II') #Muda o nome da janela do jogo


run = True

background_img = pygame.image.load('graphics/background/background.jpg').convert_alpha() #coloca um background

slime_panel_img = pygame.image.load('graphics/Icons/SlimeStatusBar.png').convert_alpha() #barrinha embaixo do background, onde fica a vida e mana para o protagonista

enemy_panel_img = pygame.image.load('graphics/Icons/EnemyStatusBar.png').convert_alpha() #barrinha embaixo do background, onde fica a vida e mana para inimigos


#background
def draw_bg():
   screen.blit(background_img, (0,0))




#paineis para se colocara vida 
def draw_panelSlime():
        screen.blit(slime_panel_img, (0,450))
def draw_panelEnemy():
        screen.blit(enemy_panel_img, (450,450))



#Characters

class Character():
    def __init__(self, x, y, scale, name, max_hp, max_mp, strenght, agility, magic, hp_potions, mp_potions, level):  
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mp = max_mp
        self.mp = max_mp
        self.strenght = strenght
        self.agility = agility
        self.magic = magic
        self.hp_potions = hp_potions
        self.mp_potions = mp_potions
        self.alive = True
        img = pygame.image.load(f'graphics/Characters/{self.name}/Idle/0.png')
        self.image = pygame.transform.scale(img, (img.get_width()*scale, img.get_height() * scale))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.level = level


    def draw(self):
        screen.blit(self.image, self.rect)

Slime = Character(140,300,1,'Slime',100,100,10,10,10,2,2,1)
Zombie = Character(700,280,1.7 ,'Zombie',100,100,10,5,0,0,0,1)


while run:

    clock.tick(FPS) #limita o fps para o colocado em settings

    draw_bg() #mostra background na tela
    draw_panelSlime() #mostra o painel do pc
    draw_panelEnemy() #mostra o painel dos inimigos

    #Gerar personagens
    Slime.draw()
    Zombie.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()



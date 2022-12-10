import pygame
from settings import *
from debug import debug
import os
import random
import time

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


#combate e turnos
current_fighter = 1
total_fighters = 3
action_cd = 0
action_wait = 30
attack = False
magic = False
potion = False
clicked = False




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



#Characters

class Character():
    def __init__(self, x, y, scale, name, max_hp, max_mp, strenght, agility, magic, hp_potions, mp_potions, level, frames, weakness):  
        self.name = name #atributos
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mp = max_mp
        self.mp = max_mp
        self.strenght = strenght
        self.agility = agility
        self.magic = magic
        self.hp_potions = hp_potions
        self.mp_potions = mp_potions
        self.weakness = weakness #0 None - 1 Magic - 2 Fire - 3 Ice - 4 Lightning
        self.alive = True
        self.animation_list = [] #animando os frame
        self.update_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.action = 0 # 0 Iddle, 1 Attack, 2 Magic, 3 Hurt, 4 Dead
        #iddle animation
        temp_list = []
        for i in range(frames): #pega quantos frames cada personagem tem e anima
            img = pygame.image.load(f'graphics/Characters/{self.name}/Idle/{i}.png').convert_alpha() 
            img = pygame.transform.scale(img, (img.get_width()*scale, img.get_height() * scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #attack animation
        temp_list = []
        for i in range(frames): #pega quantos frames cada personagem tem e anima
            img = pygame.image.load(f'graphics/Characters/{self.name}/Attack/{i}.png').convert_alpha() 
            img = pygame.transform.scale(img, (img.get_width()*scale, img.get_height() * scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #magic animation
        temp_list = []
        for i in range(frames): #pega quantos frames cada personagem tem e anima
            img = pygame.image.load(f'graphics/Characters/{self.name}/Magic/{i}.png').convert_alpha() 
            img = pygame.transform.scale(img, (img.get_width()*scale, img.get_height() * scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #hurt animation
        temp_list = []
        for i in range(frames): #pega quantos frames cada personagem tem e anima
            img = pygame.image.load(f'graphics/Characters/{self.name}/Hurt/{i}.png').convert_alpha() 
            img = pygame.transform.scale(img, (img.get_width()*scale, img.get_height() * scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #dead animation
        temp_list = []
        for i in range(frames): #pega quantos frames cada personagem tem e anima
            img = pygame.image.load(f'graphics/Characters/{self.name}/Dead/{i}.png').convert_alpha() 
            img = pygame.transform.scale(img, (img.get_width()*scale, img.get_height() * scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)  
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.level = level

    def update(self): #atualiza animacao
        animation_cd = 50
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cd:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 4:
                self.frame_index = len(self.animation_list[self.action])-1
            self.idle()
   
    def idle(self):
            self.action = 0
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()



    def draw(self):
        screen.blit(self.image, self.rect)

    def hurt(self):
            self.action = 3
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        
    def dead(self):
            self.action = 4
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def attack(self,target):
        rand = random.randint(0,50)
        if rand >= 40:
            damage = self.strenght * 2
        else:
             damage = self.strenght
        if target.weakness == 1:
            damage = damage*3
        target.hp -= damage
        target.hurt()
        target.action = 3
        if target.hp < 1:#checa se ta morto ou nao
            target.hp = 0
            target.alive = False
            target.dead()

        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        







Slime = Character(140,300,1,'Slime',100,100,10,10,10,2,2,1,8,0)
Zombie1 = Character(700,300,5 ,'Zombie',50,0,10,5,0,0,0,1,7,1)
Zombie2 = Character(500,300,5 ,'Zombie',50,0,10,5,0,0,0,1,7,1)


enemy_list = []
enemy_list.append(Zombie1)
enemy_list.append(Zombie2)


while run:
    clock.tick(FPS) #limita o fps para o colocado em settings

    draw_bg() #mostra background na tela
    draw_panelSlime() #mostra o painel do pc


    #Gerar personagens
    Slime.update()
    Slime.draw()
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
        if enemy.rect.collidepoint(pos):
            pygame.mouse.set_visible(False)
            screen.blit(attack_icon, pos)
            if clicked == True:
                attack = True
                target = enemy_list[i]

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


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()


pygame.quit()



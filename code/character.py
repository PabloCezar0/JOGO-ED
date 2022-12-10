import pygame
import time
import random
from settings import *

screen = pygame.display.set_mode((WIDHT, HEIGHT))

class Character():
    def __init__(self, x, y, scale, name, max_hp, max_mp, strenght, agility, magic, hp_potions, mp_potions, level, frames, weakness):  
        self.name = name #atributos
        self.x = x
        self.y = y
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
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
                self.rect.center = (self.x,400)
            else:
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
        
import pygame
from settings import *
from debug import debug
import time
import character
import buttons
from fila import Queue
from heap import MinHeap
import random



#teste5

pygame.init()

clock = pygame.time.Clock() #variavel para controlar o FPS, usada no começo do loop de combate


screen = pygame.display.set_mode((WIDHT, HEIGHT)) #inicia a janela baseado nos parametros em Settings

pygame.display.set_caption('Slime Combat II') #Muda o nome da janela do jogo


run = True #necssario para o pygame

background_img = pygame.image.load('graphics/Background/background.png').convert_alpha() #coloca um background

slime_panel_img = pygame.image.load('graphics/Icons/SlimeStatusBar.png').convert_alpha() #barrinha embaixo do background, onde fica a vida e mana para o protagonista

enemy_panel_img = pygame.image.load('graphics/Icons/EnemyStatusBar.png').convert_alpha() #barrinha embaixo do background, onde fica a vida e mana para inimigos

win_screen = pygame.image.load('graphics/Background/Win.png').convert_alpha()#tela de vitoria com os scores


#icones nomes explicam para que cada um serve
attack_icon = pygame.image.load('graphics/Icons/Sword.png').convert_alpha()
active_attack_icon = pygame.image.load('graphics/Icons/S_Active.png').convert_alpha()
potion_icon = pygame.image.load('graphics/Icons/Potion.png').convert_alpha()
mp_potion_icon = pygame.image.load('graphics/Icons/MpPotion.png').convert_alpha()
fireball_icon = pygame.image.load('graphics/Spells/Fireball.png').convert_alpha()
ice_icon = pygame.image.load('graphics/Spells/Ice.png').convert_alpha()
lightning_icon = pygame.image.load('graphics/Spells/Lightning.png').convert_alpha()
active_fireball_icon = pygame.image.load('graphics/Spells/Fireball_A.png').convert_alpha()
active_ice_icon = pygame.image.load('graphics/Spells/Ice_A.png').convert_alpha()
active_lightning_icon = pygame.image.load('graphics/Spells/Lightning_A.png').convert_alpha()
victory_icon = pygame.image.load('graphics/Icons/Victory.png').convert_alpha()
defeat_icon = pygame.image.load('graphics/Icons/Defeat.png').convert_alpha()
restart_icon = pygame.image.load('graphics/Icons/Restart.png').convert_alpha()
left_icon = pygame.image.load('graphics/Icons/Left.png').convert_alpha()
right_icon = pygame.image.load('graphics/Icons/Right.png').convert_alpha()


#variaveis para controlar os turnos e o combate
current_fighter = 1 #lutador 1 protagonista

level_over = 0 #1 acaba o level e manda para o proximo no
game_win = 0 # 1 o jogo vence -1 game over
action_cd = 0
wait_time = 4000
action_wait = wait_time
attack = False #variavel para controlar se ataque ja foir realizado os de baixo fazem o mesmo com magias e pocoes
fire_magic = False
ice_magic = False
lightning_magic = False
clicked = False
potion = False
heal = 0
heal_mp = 0
next_turn = 0







font = pygame.font.SysFont('Times New Roman', 18)#fonte

#RGG
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

#background
def draw_bg():
   screen.blit(background_img, (0,0))

def draw_win():
   screen.blit(win_screen, (0,0))

#imprimir texto
def drawn_text(text, font, text_col, x,y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

#paineis para se colocara vida e pocoes
def draw_panelSlime():
        screen.blit(slime_panel_img, (0,450))
        drawn_text(f'{Slime.name} HP: {Slime.hp}', font, red, 100, 230)
        drawn_text(f'{Slime.name} MP: {Slime.mp}', font, blue, 100, 250)
        drawn_text(f'{Slime.hp_potions}', font, red, 40, 580)
        drawn_text(f'{Slime.mp_potions}', font, blue, 80, 580)

#painel com vida e mana dos inimigos
def draw_panelEnemy(aux):
    if aux.head.data.name != 'Slime':
        screen.blit(enemy_panel_img, (450,450))
        drawn_text(f'{aux.head.data.name} HP: {aux.head.data.hp}', font, red, 550 , 400 + 80 )
        drawn_text(f'{aux.head.data.name} MP: {aux.head.data.mp}', font, blue, 550, 430 + 80 )
    if aux.tail.data.name != 'Slime':
        screen.blit(enemy_panel_img, (450,450))
        drawn_text(f'{aux.tail.data.name} HP: {aux.tail.data.hp}', font, red, 550 , 400 + 80 )
        drawn_text(f'{aux.tail.data.name} MP: {aux.tail.data.mp}', font, blue, 550, 430 + 80 )


#criar botoes para pressionar
sword_button = buttons.Button(screen, 25,460, attack_icon, 50, 50)
potion_button = buttons.Button(screen, 30,540, potion_icon, 30, 30)
mp_button = buttons.Button(screen, 70,540, mp_potion_icon, 30, 30)
fireball_button = buttons.Button(screen, 100,455, fireball_icon, 40, 50)
ice_button = buttons.Button(screen, 160,455, ice_icon, 45, 45)
lightning_button = buttons.Button(screen, 230,455, lightning_icon, 45, 45)
restart_button = buttons.Button(screen, 300,100, restart_icon, 120, 28)
left_button = buttons.Button(screen, 200,100, left_icon, 80, 28)
right_button = buttons.Button(screen, 500,100, right_icon, 80, 28)

#criar inimigos              x  y scale name hp mp str mgc agi def mdef hpP mpP level frame weak
Slime = character.Character(140,370,1,'Slime',100,100,10,100,10,10,10,2,2,1,8,0)
Zombie = character.Character(700,385,5 ,'Zombie',50,0,10,0,3,0,1,0,0,1,7,1)
Zombie2 = character.Character(500,385,5 ,'Zombie',50,0,10,0,3,2,1,0,0,1,7,1)
Skelleton = character.Character(700,360,5 ,'Skelleton',50,0,10,0,3,0,1,0,0,1,18,1)
Skelleton2 = character.Character(500,360,5 ,'Skelleton',50,0,5,0,3,50,1,0,0,1,18,1)


# Cria a árvore min-Heap
percorreHeap = MinHeap(15)

# percorreHeap.insert(Zombie)
# percorreHeap.insert(Zombie2)
# percorreHeap.insert(Skelleton)
# percorreHeap.insert(Skelleton2)

#Bosses
Demon = character.Character(500,130,4 ,'Demon of Fire',50,50,10,0,3,50,1,0,0,1,22,1)
Lich = character.Character(600,200,6 ,'Lich',50,100,10,0,3,50,1,0,0,1,18,1)




#Função que cria o turno da fase
def turnQueue(queue):
    turnAtack(queue)
    aux = queue.dequeue()
    queue.enqueue(aux)


# Função que aciona os ataques
def turnAtack(person):
    global action_cd
    global action_wait
    global next_turn
    attack = False
    magic = random.randint(0,5)
    potion = False
    fire_magic = False
    ice_magic = False
    lightning_magic = False
    aux = None

    

    if person.head.data.name == 'Slime':
        if sword_button.clicked == True:
            if fireball_button.clicked == True or lightning_button.clicked == True or ice_button.clicked == True:
                sword_button.clicked = False
            fireball_button.clicked = False
            ice_button.clicked = False
            lightning_button.clicked = False
            sword_button.image = active_attack_icon
            if person.tail.data.rect.collidepoint(pos):
                pygame.mouse.set_visible(False)
                screen.blit(active_attack_icon, pos)
                if clicked == True:
                    attack = True
                    target = person.tail.data

        if fireball_button.clicked == True:
            if ice_button.clicked == True or lightning_button.clicked == True:
                fireball_button.clicked = False
            ice_button.clicked = False
            lightning_button.clicked = False
            sword_button.clicked = False
            fireball_button.image = active_fireball_icon
            if person.tail.data.rect.collidepoint(pos):
                pygame.mouse.set_visible(False)
                screen.blit(active_fireball_icon, pos)
                if clicked == True:
                    fire_magic = True
                    target = person.tail.data

        if ice_button.clicked == True:
            if lightning_button.clicked == True:
                ice_button.clicked = False
            sword_button.clicked = False
            fireball_button.clicked = False
            lightning_button.clicked = False
            ice_button.image = active_ice_icon
            if person.tail.data.rect.collidepoint(pos):
                pygame.mouse.set_visible(False)
                screen.blit(active_ice_icon, pos)
                if clicked == True:
                    ice_magic = True
                    target = person.tail.data

        if lightning_button.clicked == True:
            sword_button.clicked = False
            fireball_button.clicked = False
            ice_button.clicked = False
            lightning_button.image = active_lightning_icon
            if person.tail.data.rect.collidepoint(pos):
                pygame.mouse.set_visible(False)
                screen.blit(active_lightning_icon, pos)
                if clicked == True:
                    lightning_magic = True
                    target = person.tail.data

        if potion_button.clicked == True and potion == False and Slime.hp_potions > 0: #controla as pocoes, impede o usuario de usar pocao com hp maximo e impede o hp com a cura passar do hp maximo

                if person.head.data.hp == person.head.data.max_hp and potion == False:
                    drawn_text('Health Full', font, red, 240, 230)
                    
                if person.head.data.hp > 50 and person.head.data.hp != person.head.data.max_hp and potion == False:
                    person.head.data.hp += person.head.data.max_hp - person.head.data.hp
                    heal = person.head.data.max_hp - person.head.data.hp
                    drawn_text('{heal}', font, red, 240, 250)
                    potion = True
                    person.head.data.hp_potions -= 1

                if person.head.data.hp <= 50 and potion == False:
                    drawn_text('+50', font, red, 240, 250)    
                    person.head.data.hp += 50
                    potion = True
                    potion -= 1
                    potion_button.clicked = False

        if mp_button.clicked == True and potion == False and Slime.mp_potions > 0 :#controla as pocoes, impede o usuario de usar pocao com mp maximo e impede o hp com a cura passar do mp maximo

            if person.head.data.mp == person.head.data.max_mp and potion == False:
                drawn_text('Mana Full', font, blue, 240, 250)

            if person.head.data.mp <= 50 and potion == False:  
                drawn_text('+50', font, blue, 240, 250)  
                person.head.data.mp += 50
                potion = True            
                person.head.data.mp_potions -= 1
                    
            if person.head.data.mp > 50 and person.head.data.mp != 100 and potion == False:
                person.head.data.mp += person.head.data.max_mp - person.head.data.mp
                heal_mp = person.head.data.max_mp - person.head.data.mp
                drawn_text('{heal_mp}', font, blue, 240, 250)
                potion = True
                person.head.data.mp_potions -= 1
                mp_button.clicked = False
                    
        
            #acao do jogador se o slime tiver vivo ele comeca fighter 1 eh slime 2 eh o inimigo 1 e o 3 inimigo 2
 

        if attack == True: #controla o ataque de fogo
            #attack
            if target != None:                       
                person.head.data.attack(target)
                sword_button.clicked = False
                potion = False
                potion_button.clicked = False
                mp_button.clicked = False
                if person.tail.data.hp == 0:
                    person.tail.data.alive = False
                next_turn = 1



        if fire_magic == True: #controla o ataque de fogo
            if person.head.data.mp >= 15: #so executa o ataque se mana for maior que 15
                #attack
                if target != None:                        
                    person.head.data.fire(target)
                    fireball_button.clicked = False
                    potion = False
                    potion_button.clicked = False
                    mp_button.clicked = False
                    fire_magic = False
                    action_wait = wait_time
                    if person.tail.data.hp == 0:
                        person.tail.data.alive = False
                    next_turn = 1


            else:
                drawn_text('No mana', font, blue, 240, 250) 

        if ice_magic == True: #controla o ataque de gelo
            if person.head.data.mp >= 15: #so executa o ataque se mana for maior que 15
                #attack
                if target != None:                        
                    person.head.data.ice(target)
                    ice_button.clicked = False
                    potion = False
                    potion_button.clicked = False
                    mp_button.clicked = False
                    ice_magic = False
                    action_wait = wait_time
                    if person.tail.data.hp == 0:
                        person.tail.data.alive = False
                    next_turn = 1


            else:
                drawn_text('No mana', font, blue, 240, 250) 


        if lightning_magic == True: #controla o ataque de raio
            if person.head.data.mp >= 15: #so executa o ataque se mana for maior que 15
                #attack
                if  target != None:                        
                    person.head.data.lightning(target)
                    lightning_button.clicked = False
                    potion = False
                    potion_button.clicked = False
                    mp_button.clicked = False
                    lightning_magic = False
                    if person.tail.data.hp == 0:
                        person.tail.data.alive = False
                    next_turn = 1

 
            else:
                drawn_text('No mana', font, blue, 240, 250)  

        if next_turn == 1:
            aux = person.dequeue()
            person.enqueue(aux)
            print(person.head.data.name)
            wait_time = 0
            next_turn = 0

    if person.head.data.name != 'Slime':
        action_cd += 1
        if action_cd >= action_wait:

            if person.head.data.name == Lich and person.head.data.mp < 30  or person.head.data.name == Demon and person.head.data.mp < 15 or magic == 5:

            
                if person.head.data.name == 'Lich' and person.head.data.mp >= 30 and magic == 5:
                    #attack
                    person.head.data.death_magic(person.tail.data)
                    time.sleep(0.08)

                if person.head.data.name == Demon and person.head.data.mp >= 15 and magic == 5:
                    #attack
                    person.head.data.fire(person.tail.data)
                    time.sleep(0.08)
                else:
                    person.head.data.attack(person.tail.data)
                    time.sleep (0.08)

            else:
                person.head.data.attack(person.tail.data)
                time.sleep (0.08)
            
            aux = person.dequeue()
            person.enqueue(aux)
            print(person.head.data.name)
            action_cd = 0


# Função que percorre os leveis da Heap    
def turnLevel(percorreHeap):
    pass

#coloca os inimigos em uma lista 
character_list = Queue()
enemy_alive = 0
character_list.enqueue(Slime)
character_list.enqueue(Lich)
enemy_alive += 1


    

#criar botoes para pressionar
sword_button = buttons.Button(screen, 25,460, attack_icon, 50, 50)
potion_button = buttons.Button(screen, 30,540, potion_icon, 30, 30)
mp_button = buttons.Button(screen, 70,540, mp_potion_icon, 30, 30)
fireball_button = buttons.Button(screen, 100,455, fireball_icon, 40, 50)
ice_button = buttons.Button(screen, 160,455, ice_icon, 45, 45)
lightning_button = buttons.Button(screen, 230,455, lightning_icon, 45, 45)
restart_button = buttons.Button(screen, 300,100, restart_icon, 120, 28)
left_button = buttons.Button(screen, 200,100, left_icon, 80, 28)
right_button = buttons.Button(screen, 500,100, right_icon, 80, 28)



while run == True:
    clock.tick(FPS) #limita o fps para o colocado em settings

    

    while game_win == 0 and run == True:
        draw_bg() #mostra background na tela
        draw_panelSlime() #mostra o painel do pc
        #Gerar personagens
        Slime.update()
        Slime.draw()
        sword_button.draw()
        potion_button.draw()
        fireball_button.draw()
        ice_button.draw()
        mp_button.draw()
        lightning_button.draw()

        if character_list.head.data.name != Slime:
            character_list.head.data.draw()
            character_list.head.data.update()
        if character_list.tail.data.name != Slime:
            character_list.tail.data.draw()
            character_list.tail.data.update()
        
        percorreFila = character_list.head
        aux = []
        while percorreFila:
            aux.insert(0, percorreFila.data)
            percorreFila = percorreFila.next
        

        draw_panelEnemy(character_list)

        #controlar o ataque
        







            

            

    
        pygame.mouse.set_visible(True)#mostra o mouse normal apos ataque

        pos = pygame.mouse.get_pos()#pega a posicao do mosue e coloca em pos

            
    # todos fazem a mesma coisa, ao clicar em algum botao de ataque e colocar o mouse em cima do inimigo o cursos muda para o do icone de ataque ativo selecionado

        if level_over == 0: # se o jogo nao tiver ganho roda o codigo abaixo


            turnAtack(character_list)


            if  character_list.tail.data.name == 'Slime' and character_list.tail.data.hp <= 0:
                level_over = -1
            
            if character_list.head.data.name == 'Slime' and character_list.head.data.hp <= 0:
                level_over = -1          

            if character_list.head.data.name != 'Slime' and character_list.head.data.hp <= 0:
                level_over = 1 

            if character_list.tail.data.name != 'Slime' and character_list.tail.data.hp <= 0:
                level_over = 1      


         


        #faz as imagens serem as padroes apos ataque
        if sword_button.clicked == False:
            sword_button.image = attack_icon
        if fireball_button.clicked == False:
            fireball_button.image = fireball_icon
        if ice_button.clicked == False:
            ice_button.image = ice_icon
        if lightning_button.clicked == False:
            lightning_button.image = lightning_icon

        #check para vitoria
        
        if level_over == 1:
            action_wait = 0
            screen.blit(victory_icon, (250,0))
            left_button.clicked = False
            right_button.clicked = False
            if left_button.draw() or right_button.draw():
                Slime.reset()
                for enemy in aux:
                    enemy.reset()
                    enemy_alive += 1
                current_fighter = 1
                level_over = 0
                sword_button.clicked = False
            fireball_button.clicked = False
            ice_button.clicked = False
            lightning_button.clicked = False
        

            #derrota
        if level_over == -1:
            restart_button.clicked = False
            screen.blit(defeat_icon, (250,0))
            if restart_button.draw():
                Slime.reset()
                for enemy in aux:
                    enemy.reset()
                current_fighter = 1
                level_over = 0
            sword_button.clicked = False
            fireball_button.clicked = False
            ice_button.clicked = False
            lightning_button.clicked = False

        


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False
        pygame.display.update()  

    while game_win == 1:
        draw_win()
        pygame.display.update() 

pygame.quit()
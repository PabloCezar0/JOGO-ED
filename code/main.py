import pygame
from settings import *
from debug import debug
import time
import character
import buttons
from fila import Queue



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
total_fighters = 1 #quantidade de personagens no combate
action_cd = 0
wait_time = 4000
action_wait = wait_time
attack = False #variavel para controlar se ataque ja foir realizado os de baixo fazem o mesmo com magias e pocoes
fire_magic = False
ice_magic = False
lightning_magic = False
potion = False
clicked = False
level_over = 0 #1 acaba o level e manda para o proximo no
game_win = 0 # 1 o jogo vence -1 game over
heal = 0
heal_mp = 0
enemy_magic = 0







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
        screen.blit(enemy_panel_img, (450,450))
        for count, i in enumerate(aux):
            drawn_text(f'{i.name} HP: {i.hp} {count+1}', font, red, 550 , 450 + 80*count )
            drawn_text(f'{i.name} MP: {i.mp}', font, blue, 550, 480 + 80*count )


#criar inimigos              x  y scale name hp mp str mgc agi def mdef hpP mpP level frame weak
Slime = character.Character(140,370,1,'Slime',100,100,5,100,10,0,10,2,2,1,8,0)
Zombie = character.Character(700,385,5 ,'Zombie',50,0,10,0,3,50,1,0,0,1,7,1)
Skelleton = character.Character(700,360,5 ,'Skelleton',50,0,10,0,3,50,1,0,0,1,18,1)




#Bosses
Demon = character.Character(500,130,4 ,'Demon of Fire',50,50,10,0,3,50,1,0,0,1,22,1)
Lich = character.Character(600,200,6 ,'Lich',50,50,10,0,3,50,1,0,0,1,18,1)




#coloca os inimigos em uma lista 
enemy_list = Queue()
enemy_alive = 0
enemy_list.enqueue(Skelleton)
enemy_alive += 1
total_fighters +=1


    

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
        
        percorreFila = enemy_list.head
        aux = []
        while percorreFila:
            aux.insert(0, percorreFila.data)
            percorreFila = percorreFila.next
        
        for Enemy in aux:
            Enemy.draw()
            Enemy.update()
            draw_panelEnemy(aux)

        #controlar o ataque
        attack = False
        magic = False
        potion = False
        taget = None

        if current_fighter == 1:
            action_wait = 0

    
        pygame.mouse.set_visible(True)#mostra o mouse normal apos ataque

        pos = pygame.mouse.get_pos()#pega a posicao do mosue e coloca em pos

            
    # todos fazem a mesma coisa, ao clicar em algum botao de ataque e colocar o mouse em cima do inimigo o cursos muda para o do icone de ataque ativo selecionado
        for i, enemy in enumerate(aux):  

            if level_over == 0: # se o jogo nao tiver ganho roda o codigo abaixo
                if current_fighter == 1:
                    if sword_button.clicked == True:
                        if fireball_button.clicked == True or lightning_button.clicked == True or ice_button.clicked == True:
                            sword_button.clicked = False
                        fireball_button.clicked = False
                        ice_button.clicked = False
                        lightning_button.clicked = False
                        sword_button.image = active_attack_icon
                        if enemy.rect.collidepoint(pos):
                            pygame.mouse.set_visible(False)
                            screen.blit(active_attack_icon, pos)
                            if clicked == True:
                                attack = True
                                target = aux[i]

                    if fireball_button.clicked == True:
                        if ice_button.clicked == True or lightning_button.clicked == True:
                            fireball_button.clicked = False
                        ice_button.clicked = False
                        lightning_button.clicked = False
                        sword_button.clicked = False
                        fireball_button.image = active_fireball_icon
                        if enemy.rect.collidepoint(pos):
                            pygame.mouse.set_visible(False)
                            screen.blit(active_fireball_icon, pos)
                            if clicked == True:
                                fire_magic = True
                                target = aux[i]
            
                    if ice_button.clicked == True:
                        if lightning_button.clicked == True:
                            ice_button.clicked = False
                        sword_button.clicked = False
                        fireball_button.clicked = False
                        lightning_button.clicked = False
                        ice_button.image = active_ice_icon
                        if enemy.rect.collidepoint(pos):
                            pygame.mouse.set_visible(False)
                            screen.blit(active_ice_icon, pos)
                            if clicked == True:
                                ice_magic = True
                                target = aux[i]

                    if lightning_button.clicked == True:
                        sword_button.clicked = False
                        fireball_button.clicked = False
                        ice_button.clicked = False
                        lightning_button.image = active_lightning_icon
                        if enemy.rect.collidepoint(pos):
                            pygame.mouse.set_visible(False)
                            screen.blit(active_lightning_icon, pos)
                            if clicked == True:
                                lightning_magic = True
                                target = aux[i]


                if  current_fighter ==  1 and potion_button.clicked == True and potion == False and Slime.hp_potions > 0: #controla as pocoes, impede o usuario de usar pocao com hp maximo e impede o hp com a cura passar do hp maximo

                    if Slime.hp == Slime.max_hp and potion == False:
                        potion = True
                        drawn_text('Health Full', font, red, 240, 230)
                    
                    if Slime.hp > 50 and Slime.hp != Slime.max_hp and potion == False:
                        Slime.hp += Slime.max_hp - Slime.hp
                        heal = Slime.max_hp - Slime.hp
                        drawn_text('{heal}', font, red, 240, 250)
                        potion = True
                        Slime.hp_potions -= 1

                    if Slime.hp <= 50 and potion == False:
                        drawn_text('+50', font, red, 240, 250)    
                        Slime.hp += 50
                        potion = True
                        potion -= 1
                    
                        
                    
                    

                    potion_button.clicked = False

                if  current_fighter ==  1 and mp_button.clicked == True and potion == False and Slime.mp_potions > 0 :#controla as pocoes, impede o usuario de usar pocao com mp maximo e impede o hp com a cura passar do mp maximo
                    if Slime.mp == Slime.max_mp and potion == False:
                        potion = True
                        drawn_text('Mana Full', font, blue, 240, 250)

                    if Slime.mp <= 50 and potion == False:  
                        drawn_text('+50', font, blue, 240, 250)  
                        Slime.mp += 50
                        potion = True            
                        Slime.mp_potions -= 1
                    
                    if Slime.mp > 50 and Slime.mp != 100 and potion == False:
                        Slime.mp += Slime.max_mp - Slime.mp
                        heal_mp = Slime.max_mp - Slime.mp
                        drawn_text('{heal_mp}', font, blue, 240, 250)
                        potion = True
                        Slime.mp_potions -= 1
                    mp_button.clicked = False
                    
        
            #acao do jogador se o slime tiver vivo ele comeca fighter 1 eh slime 2 eh o inimigo 1 e o 3 inimigo 2
                if Slime.alive == True:

                    if current_fighter == 1:

                        if attack == True and target.alive == True: #controla o ataque fisico
                            action_cd += 1
                            if action_cd >= action_wait:
                                #attack
                                if attack == True and target != None:                        
                                    Slime.attack(target)
                                    current_fighter += 1
                                    action_cd = 0
                                    sword_button.clicked = False
                                    potion = False
                                    potion_button.clicked = False
                                    mp_button.clicked = False
                                    action_wait = wait_time
                                    if target.hp == 0:
                                            target.alive = False
                                            enemy_alive -= 1

                        if fire_magic == True and target.alive == True: #controla o ataque de fogo
                            if Slime.mp >= 15: #so executa o ataque se mana for maior que 15
                                action_cd += 1
                                if action_cd >= action_wait:
                                    #attack
                                    if fire_magic == True and target != None:                        
                                        Slime.fire(target)
                                        current_fighter += 1
                                        action_cd = 0
                                        fireball_button.clicked = False
                                        potion = False
                                        potion_button.clicked = False
                                        mp_button.clicked = False
                                        fire_magic = False
                                        action_wait = wait_time
                                        if target.hp == 0:
                                            target.alive = False
                                            enemy_alive -= 1
                            else:
                                drawn_text('No mana', font, blue, 240, 250) 

                        if ice_magic == True and target.alive == True: #controla o ataque de gelo
                            if Slime.mp >= 15: #so executa o ataque se mana for maior que 15
                                action_cd += 1
                                if action_cd >= action_wait:
                                    #attack
                                    if ice_magic == True and target != None:                        
                                        Slime.ice(target)
                                        current_fighter += 1
                                        action_cd = 0
                                        ice_button.clicked = False
                                        potion = False
                                        potion_button.clicked = False
                                        mp_button.clicked = False
                                        ice_magic = False
                                        action_wait = wait_time
                                        if target.hp == 0:
                                            target.alive = False
                                            enemy_alive -= 1
                            else:
                                drawn_text('No mana', font, blue, 240, 250) 


                        if lightning_magic == True and target.alive == True: #controla o ataque de raio
                            if Slime.mp >= 15: #so executa o ataque se mana for maior que 15
                                action_cd += 1
                                if action_cd >= action_wait:
                                    #attack
                                    if lightning_magic == True and target != None:                        
                                        Slime.lightning(target)
                                        current_fighter += 1
                                        action_cd = 0
                                        lightning_button.clicked = False
                                        potion = False
                                        potion_button.clicked = False
                                        mp_button.clicked = False
                                        lightning_magic = False
                                        action_wait = wait_time
                                        if target.hp == 0:
                                            target.alive = False
                                            enemy_alive -= 1
                            else:
                                 drawn_text('No mana', font, blue, 240, 250)  


                else: 
                    level_over = -1


    
                    
                for count, enemy in enumerate(aux): #controla o ataque do inimigo o target sempre eh o slime
                    if current_fighter == 2 + count:
                        if enemy.alive == True:

                            if enemy == Lich and enemy.mp < 30  or enemy == Demon and enemy_magic < 15 or enemy_magic == 1:
                                action_cd += 1
                                if action_cd >= action_wait:
                                    #attack
                                    enemy.attack(Slime)
                                    enemy_magic = 0
                                    current_fighter += 1
                                    action_cd = 0
                                    time.sleep(0.08)

                            if enemy == Lich and enemy.mp >= 30 and enemy_magic == 0:
                                action_cd += 1
                                if action_cd >= action_wait:
                                    #attack
                                    enemy.death_magic(Slime)
                                    enemy_magic = 1
                                    current_fighter += 1
                                    action_cd = 0
                                    time.sleep(0.08)

                            if enemy == Demon and enemy.mp >= 15 and enemy_magic == 0:
                                action_cd += 1
                                if action_cd >= action_wait:
                                    #attack
                                    enemy.fire(Slime)
                                    enemy_magic = 1
                                    current_fighter += 1
                                    action_cd = 0
                                    time.sleep(0.08)

                            
                        else:
                            current_fighter += 1
                
                #reseta o turno para o protagonista
                if current_fighter > total_fighters :
                    current_fighter = 1
                
                if enemy.alive == False in aux:
                        enemy_alive -= 1

                if enemy_alive == 0:
                    level_over = 1

                print(enemy_alive)

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

# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 10:33:31 2024

@author: ninja
"""

import vie as V
import pygame
from pygame import mixer
import sys
import Timer as T
import Fighter as F
num1="1"
num2="2"
typ1="Zoner"
typ2="Grappler"
nomdecarte="Map_plage"
liste_carte=["Map_retro","Map_plage"]
liste_type = ['Shoto',
              'Grappler',
              'Special',
              'Zoner',
              'Tank']
def afficher_contexte():
    #SCREEN.blit(cadre,  (45, vie1.get_y()-5))
    pygame.draw.rect(SCREEN, (0,0,0), (49, vie1.get_y()-1, 1182 , 32))#cadre
    pygame.draw.rect(SCREEN, (0,255,0), (vie1.get_x(), vie1.get_y(), vie1.get_vie(), 30)) #vie droite
    pygame.draw.rect(SCREEN, (255,0,0), (vie1.get_x_deg(), vie1.get_y(), vie1.get_deg(), 30)) #degat droit
    pygame.draw.rect(SCREEN, (0,255,0), (vie2.get_x(), vie1.get_y(), vie2.get_vie(), 30)) #vie gauche 
    pygame.draw.rect(SCREEN, (255,0,0), (vie2.get_x_deg(), vie1.get_y(), vie2.get_deg(), 30)) #degat gauche
    #affichage Timer
    pygame.draw.rect(SCREEN, (0,0,0), (((larg-50)//2)-26, vie1.get_y()-11, 102, 52))
    pygame.draw.rect(SCREEN, (255, 234, 181), (((larg-50)//2)-25, vie1.get_y()-10, 100, 50))
    if not(Fin):
        SCREEN.blit((Timer.font).render(Timer.text, True, (0, 0, 0)), ((((larg-50)//2)-5), vie1.get_y())) 
    #afficher les rounds gagnés
    SCREEN.blit(round_vide, (555, 140))
    SCREEN.blit(round_vide, (520, 140))
    SCREEN.blit(round_vide, (700, 140))
    SCREEN.blit(round_vide, (735, 140))
    if l1:
        SCREEN.blit(round_plein, (555, 140))
    if r1:
        SCREEN.blit(round_plein, (700, 140))
    if l2:
        SCREEN.blit(round_plein, (520, 140))
    if r2:
        SCREEN.blit(round_plein, (735, 140))  
def commencer_round(num1,num2,typ1,typ2):
    global intro_count,Fighter1,Fighter2
    Timer.rounds(vie1.get_vie(),vie2.get_vie())
    vie1.reset_vie()
    vie2.reset_vie()
    Timer.reset_timer()
    Fighter1=F.Fighter(num1,"Left",typ1)
    Fighter2=F.Fighter(num2,"Right",typ2)
    Fighter1.spawn( SCREEN)
    Fighter2.spawn( SCREEN)
    intro_count=4
def scorer_round():
    
    global l1,l2,r1,r2,Fin
    if Timer.round_cpt.left==1:
        l1=True
    if Timer.round_cpt.right==1:
        r1=True
    if Timer.round_cpt.left==2:
        l2=True
    if Timer.round_cpt.right==2:
        r2=True
    if Timer.round_cpt.left==2 or Timer.round_cpt.right==2:
        Fin=True
def afficher_resultat():
    if Timer.round_cpt.left==Timer.round_cpt.right:
        SCREEN.blit((Timer.font3).render("Draw", True, (0, 0, 0)), (570, 360))   
        SCREEN.blit((Timer.font2).render("Draw", True, (255, 0, 0)), (573, 360))
    elif Timer.round_cpt.left==2:
        SCREEN.blit((Timer.font3).render("Player1 Wins", True, (0, 0, 0)), (470, 360))   
        SCREEN.blit((Timer.font2).render("Player1 Wins", True, (255, 0, 0)), (473, 360))
    else:
        SCREEN.blit((Timer.font3).render("Player2 Wins", True, (0, 0, 0)), (470, 360))
        SCREEN.blit((Timer.font2).render("Player2 Wins", True, (255, 0, 0)), (473, 360))
def commencer_combat(num1,num2,typ1,typ2):
    global Fin,l1,l2,r1,r2,vie1,vie2,Timer,intro_count
    Fin=False
    l1=l2=r1=r2=False
    vie1=V.Vie(1,larg)
    vie2=V.Vie(2,larg)
    Timer=T.Timer(60)
    intro_count=4
    commencer_round(num1, num2, typ1, typ2)
    
pygame.init()
mixer.init()

round_sfx=pygame.mixer.Sound("sfx_fight.mp3")


CLOCK = pygame.time.Clock()
FPS=60
long=720
larg=1280
SCREEN = pygame.display.set_mode((larg, long))
pygame.display.set_caption("Just Fight")


BACKGROUND = pygame.image.load("assets/Carte/"+nomdecarte+".png")


round_vide=pygame.transform.scale(pygame.image.load("assets/round_vide.png"), (25, 25))
round_plein=pygame.transform.scale(pygame.image.load("assets/round_plein.png"), (25, 25))
commencer_combat(num1,num2,typ1,typ2)
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.USEREVENT:
            if not(Fin):
                intro_count-=1
                if intro_count==3:
                    round_sfx.play()

                if intro_count <= 0:
                    Timer.reduction(vie1.get_vie(),vie2.get_vie())
            else:      
                intro_count-=1
                
    SCREEN.blit(BACKGROUND, (0, 0))    
    if intro_count <= 0 and not(Fin) :
        if intro_count==0 and not(Fin):
             SCREEN.blit((Timer.font3).render("Fight!!!", True, (0, 0, 0)), (557, 360))
             SCREEN.blit((Timer.font2).render("Fight!!!", True, (255, 255, 255)), (560, 360))
        if  Timer.round_cpt.left<2 and Timer.round_cpt.right<2:
            Fighter1.mouvement(Fighter2) 
            Fighter2.mouvement(Fighter1) 
            if vie1.get_vie()>0 and vie2.get_vie()>0 and Timer.get_time()!=0:
                Fighter1.draw(Fighter2, vie2, SCREEN)
                Fighter2.draw(Fighter1, vie1, SCREEN)
            else:                
                commencer_round(num1, num2, typ1, typ2)
                scorer_round()
            afficher_contexte()
    elif Fin:
        afficher_contexte()
        SCREEN.blit((Timer.font).render(" KO", True, (0, 0, 0)), ((((larg-50)//2)-5), vie1.get_y())) 
        k = pygame.key.get_pressed()  
        if intro_count < 0:
            if k[pygame.K_v]:
                commencer_combat(num1,num2,typ1,typ2)
        else:
            
            afficher_resultat() 
    else:
        if not(Fin):
            if  intro_count<4 :
                SCREEN.blit((Timer.font3).render(str(intro_count), True, (0, 0, 0)), (637, 360))
                SCREEN.blit((Timer.font2).render(str(intro_count), True, (255, 255, 255)), (640, 360))
            else:
                SCREEN.blit((Timer.font3).render("Round "+str(Timer.roundstr), True, (0, 0, 0)), (537, 360))
                SCREEN.blit((Timer.font2).render("Round "+str(Timer.roundstr), True, (255, 255, 255)), (540, 360))
            Fighter1.spawn( SCREEN)
            Fighter2.spawn( SCREEN)
            afficher_contexte()
    pygame.display.update()
    CLOCK.tick(FPS)
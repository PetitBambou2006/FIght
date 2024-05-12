# -*- coding: utf-8 -*-
"""
Created on Wed May  8 05:15:56 2024

@author: ninja
"""


import pygame,sys
from random import randint

class curseur:
    def __init__(self, j):
        self.j = j
        self.block=True
        liste_touche=[pygame.K_LEFT,pygame.K_RIGHT,pygame.K_i,pygame.K_e,pygame.K_q,pygame.K_d]
        self.lock=self.final_lock=False
        self.liste_type=['Shoto',
                      'Grappler',
                      'Zoner',
                      'Special']
        self.cadre=pygame.image.load("assets/cadre_perso.png")
        self.shoto1g=pygame.transform.scale(pygame.image.load("assets/Perso/Shoto/1/Left/stand_g.png"),(100,200))
        self.shoto2g=pygame.transform.scale(pygame.image.load("assets/Perso/Shoto/2/Left/stand_g.png"),(100,200))
        self.shoto1d=pygame.transform.scale(pygame.image.load("assets/Perso/Shoto/1/Right/stand_d.png"),(100,200))
        self.shoto2d=pygame.transform.scale(pygame.image.load("assets/Perso/Shoto/2/Right/stand_d.png"),(100,200))

        self.grapler1g=pygame.transform.scale(pygame.image.load("assets/Perso/Grappler/1/Left/stand_g.png"),(100,200))
        self.grapler2g=pygame.transform.scale(pygame.image.load("assets/Perso/Grappler/2/Left/stand_g.png"),(100,200))
        self.grapler1d=pygame.transform.scale(pygame.image.load("assets/Perso/Grappler/1/Right/stand_d.png"),(100,200))
        self.grapler2d=pygame.transform.scale(pygame.image.load("assets/Perso/Grappler/2/Right/stand_d.png"),(100,200))
        
        self.zoner1g=pygame.transform.scale(pygame.image.load("assets/Perso/Zoner/1/Left/stand_g.png"),(100,200))
        self.zoner2g=pygame.transform.scale(pygame.image.load("assets/Perso/Zoner/2/Left/stand_g.png"),(100,200))
        self.zoner1d=pygame.transform.scale(pygame.image.load("assets/Perso/Zoner/1/Right/stand_d.png"),(100,200))
        self.zpner2d=pygame.transform.scale(pygame.image.load("assets/Perso/Zoner/2/Right/stand_d.png"),(100,200))
        
        self.special1g=pygame.transform.scale(pygame.image.load("assets/Perso/Special/1/Left/stand_g.png"),(100,200))
        self.special2g=pygame.transform.scale(pygame.image.load("assets/Perso/Special/2/Left/stand_g.png"),(100,200))
        self.special1d=pygame.transform.scale(pygame.image.load("assets/Perso/Special/1/Right/stand_d.png"),(100,200))
        self.special2d=pygame.transform.scale(pygame.image.load("assets/Perso/Special/2/Right/stand_d.png"),(100,200))
        
        if j == 1:
            self.lock_b=liste_touche[-3]
            self.gauche=liste_touche[-2]
            self.droite=liste_touche[-1]
            self.x = 401
            self.y = 480
            self.x_lock=200
            self.y_lock=660
            self.coul =(255, 0, 0)
        else:
            self.x = 880
            self.y = 440
            self.x_lock=1000
            self.y_lock=660
            self.coul =(0, 0, 255)
            self.gauche=liste_touche[0]
            self.droite=liste_touche[1]
            self.lock_b=liste_touche[2]
    def mouvement(self):
        touche = pygame.key.get_pressed()
        if not( touche[self.droite]) and not(touche[self.gauche]): 
            self.block=False
        if not(touche[self.lock_b]):
            self.final_block=False
        if not(self.lock) and not(self.block):
            if touche[self.droite] :
                self.x += 100
                self.block=True
            if touche[self.gauche] :
                self.x -= 100
                self.block=True
            if self.x > 880 :  
                self.x -= 500
            if self.x < 400 :
                self.x += 500
            if touche[self.lock_b]:
                if self.x<500:
                    self.type=self.liste_type[0]
                if 500<self.x and self.x<600:
                    self.type=self.liste_type[1]
                if 600<self.x and self.x<700:
                    self.type=self.liste_type[randint(0,3)]
                    self.x=self.x_lock+randint(-20,20)
                    self.final_lock=True
                if 700<self.x and self.x<800:
                    self.type=self.liste_type[2]
                if 800<self.x:
                    self.type=self.liste_type[-1]
                    
                    
                self.x=self.x_lock
                self.y=self.y_lock
                self.lock=True
                self.final_block=True
        elif self.lock and not(self.final_lock) : 
            if not(self.block):
                
                if touche[self.droite] and not(self.block) :
                    self.x += 20
                    self.block=True             
                if touche[self.gauche] and not(self.block):
                    self.x -= 20
                    self.block=True
                if self.x_lock+30<self.x:
                    self.x-=40
                if self.x_lock>self.x:
                    self.x+=40
            if touche[self.lock_b]and not(self.final_block):
                self.final_lock=True
        
            
                
                
    def resultat(self):   
        if self.j!=1:
            if self.x<self.x_lock:
                return (2,"Right",self.type)
            else:
                return (1,"Right",self.type)
        else:
            if self.x<self.x_lock:
                return (1,"Left",self.type)
            else:
                return (2,"Left",self.type )      
    def draw(self,SCREEN):
        if not(self.lock):
            pygame.draw.rect(SCREEN,self.coul,(self.x,self.y,20,40))
        SCREEN.blit(self.cadre, (400, 520))
        SCREEN.blit(self.shoto1g, (400, 520))
        SCREEN.blit(self.grapler1g, (500, 520))
        SCREEN.blit(self.zoner1d, (700, 520))
        SCREEN.blit(self.special1d, (800, 520))
        self.perso(SCREEN)
    def perso(self,SCREEN):
        if self.j==1:
            if not(self.lock):
                if self.x<500:
                    SCREEN.blit(self.shoto1g, (200, 520))           
                if 500<self.x and self.x<600:
                    SCREEN.blit(self.grapler1g, (200, 520))
                if 700<self.x and self.x<800:
                    SCREEN.blit(self.zoner1g, (200, 520))
                if 800<self.x:
                    SCREEN.blit(self.special1g, (200, 520)) 
            else:
                if self.x==self.x_lock:
                    SCREEN.blit(pygame.transform.scale(pygame.image.load("assets/Perso/"+self.type+"/1/Left/stand_g.png"),(100,200)), (200, 520)) 
                else:
                    SCREEN.blit(pygame.transform.scale(pygame.image.load("assets/Perso/"+self.type+"/2/Left/stand_g.png"),(100,200)), (200, 520)) 
        else:
            if not(self.lock):
                if self.x<500:
                    SCREEN.blit(self.shoto1d, (1000, 520))           
                if 500<self.x and self.x<600:
                    SCREEN.blit(self.grapler1d, (1000, 520))
                if 700<self.x and self.x<800:
                    SCREEN.blit(self.zoner1d, (1000, 520))
                if 800<self.x:
                    SCREEN.blit(self.special1d, (1000, 520)) 
            else:
                if self.x==self.x_lock:
                    SCREEN.blit(pygame.transform.scale(pygame.image.load("assets/Perso/"+self.type+"/1/Right/stand_d.png"),(100,200)), (1000, 520)) 
                else:
                    SCREEN.blit(pygame.transform.scale(pygame.image.load("assets/Perso/"+self.type+"/2/Right/stand_d.png"),(100,200)), (1000, 520)) 
            
        


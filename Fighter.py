# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 12:27:34 2024

@author: ninja
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 11:43:01 2024

@author: ninja
"""




import pygame
from pygame import mixer

class Fighter:
    def __init__(self, skin, side, typ):

        liste_type = {'Shoto': {'speed': 12, 'defense': 10, 'light': 50, 'mid': 60, 'heavy': 75, 'taille': 230, 'skillset': ("S", "S", "S")},
                      'Grappler': {'speed': 5, 'defense': 20, 'light': 40, 'mid': 50, 'heavy': 100, 'taille': 250, 'skillset': ("S", "G", "G")},
                      'Special': {'speed': 5, 'defense': 20, 'light': 40, 'mid': 60, 'heavy': 100, 'taille': 250, 'skillset': ("S", "P", "S")},
                      'Zoner': {'speed': 8, 'defense': 0, 'light': 30, 'mid': 60, 'heavy': 80, 'taille': 210, 'skillset': ("P", "S", "P")},
                      'Tank': {'speed': 7, 'defense': 30, 'light': 40, 'mid': 60, 'heavy': 80, 'taille': 230, 'skillset': ("S", "G", "S")}}
        liste_bouton = {"Left": {"gauche": pygame.K_q,
                                 "droite": pygame.K_d,
                                 "haut": pygame.K_z,
                                 "bas": pygame.K_s,
                                 "light": pygame.K_e,
                                 "mid": pygame.K_r,
                                 "heavy": pygame.K_t},
                        "Right": {"gauche": pygame.K_LEFT,
                                  "droite": pygame.K_RIGHT,
                                  "haut": pygame.K_UP,
                                  "bas": pygame.K_DOWN,
                                  "light": pygame.K_i,
                                  "mid": pygame.K_o,
                                  "heavy": pygame.K_p},
                        }
        self.liste_bouton = liste_bouton[side]
        self.liste_etat = ["bloque", "bouge", "attaque"]
        self.skin = str(skin)
        self.sol = 700
        self.typ2 = typ
        self.side = side
        if self.side == 'Left':
            self.comp = "g"
            self.comp2 = "d"
            self.side2 = side2 = "Right"
            self.x = 300

        else:
            self.comp = "d"
            self.comp2 = "g"
            self.side2 = side2 = "Left"
            self.x = 980
        # liste des attributs
        self.typ = liste_type[typ]
        self.vitesse = self.typ['speed']
        self.defense = self.typ['defense']
        self.att_l = self.typ['light']
        self.att_m = self.typ['mid']
        self.att_h = self.typ['heavy']
        self.skillset = self.typ["skillset"]
        # liste des états
        self.etat = "bloque"
        self.blocking = True
        self.blockingbas = False
        self.jumping = False
        self.se_faire_attaquer = False
        self.cote = True

        # liée au mouvement
        self.taille_b = self.typ['taille']
        self.taille = self.taille_b
        self.y = self.sol-self.taille
        self.larg = 100
        self.Y_GRAVITY = 1
        self.JUMP_HEIGHT = 25
        self.Y_VELOCITY = self.JUMP_HEIGHT
        self.cpt = 0
        self.pas = 80//self.vitesse

        # stoppeur d'attaque
        self.cpt_l = self.cpt_m = self.cpt_h = 0
        self.arret_l1= self.arret_m1 = self.arret_h1 = False
        self.assis_de_base1 = self.assis_de_base2 = self.assis_de_base3 = False
        self.cpt_sefairemal=0

        # checkeur d'état
        self.cotee = "base"
        # les projectiles
        self.existe = False
        self.liste_projectile = []
        self.coef_larg1=self.coef_larg2=self.coef_larg3=1
        if self.skillset[0]=="S":
            self.coef_larg1= 1.5
        if self.skillset[0]=="G":
            self.coef_larg1= 2
        if self.skillset[1]=="S":
            self.coef_larg2= 1.5
        if self.skillset[1]=="G":
            self.coef_larg2= 2
        if self.skillset[2]=="S":
            self.coef_larg3= 1.5
        if self.skillset[2]=="G":
            self.coef_larg3= 2
        self.att_l_sfx=pygame.mixer.Sound("assets/Perso/"+str(typ)+"/Sfx/att_l_sfx.mp3")
        if not(typ=="Special"or typ=="Zoner"):
            self.att_m_sfx=pygame.mixer.Sound("assets/Perso/"+str(typ)+"/Sfx/att_m_sfx.mp3")
        self.att_h_sfx=pygame.mixer.Sound("assets/Perso/"+str(typ)+"/Sfx/att_h_sfx.mp3")
        self.subir_sfx=pygame.mixer.Sound("assets/Perso/"+str(typ)+"/Sfx/subir_sfx.mp3")
        self.subir_sfx.set_volume(0.25)
        
        # subir
        self.p00 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side +
                                                           "/se_prend_un_coup_"+self.comp+".png"),
                                         (self.larg, self.taille/2))
        self.p0 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side +
                                                           "/se_prend_un_coup_"+self.comp+".png"),
                                         (self.larg, self.taille))
        # pas1
        self.p1 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side +
                                                           "/stand_"+self.comp+".png"),
                                         (self.larg, self.taille))
        self.ps1 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side +
                                                           "/stand2_"+self.comp+".png"),
                                         (self.larg, self.taille))
        self.p2 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side +
                                                           "/crouch_"+self.comp+".png"),
                                         (self.larg, self.taille/2))
        self.p3 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side +
                                                           "/jump_"+self.comp+".png"),
                                         (self.larg, self.taille))
        if self.skillset[0]!="P":
            self.p4 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side +
                                                           "/att_l_"+self.comp+".png"),
                                         (self.larg*self.coef_larg1, self.taille))
            self.p7 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side +
                                                           "/att_l_"+self.comp+".png"),
                                         (self.larg*self.coef_larg1, self.taille/2))
        else:
            self.p4 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side +
                                                           "/stand_"+self.comp+".png"),
                                         (self.larg, self.taille))
            self.p7 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side +
                                                           "/stand_"+self.comp+".png"),
                                         (self.larg, self.taille/2))
        if self.skillset[1]!="P":
            self.p5 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side +
                                                           "/att_m_"+self.comp+".png"),
                                         (self.larg*self.coef_larg2, self.taille))
            self.p8 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side +
                                                           "/att_m_"+self.comp+".png"),
                                         (self.larg*self.coef_larg2, self.taille/2))
        else:
            self.p5 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side +
                                                           "/stand_"+self.comp+".png"),
                                         (self.larg, self.taille))
            self.p8 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side +
                                                           "/stand_"+self.comp+".png"),
                                         (self.larg, self.taille/2))
        if self.skillset[2]!="P":
            self.p6 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side +
                                                           "/att_h_"+self.comp+".png"),
                                         (self.larg*self.coef_larg3, self.taille))
            self.p9 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side +
                                                           "/att_h_"+self.comp+".png"),
                                         (self.larg*self.coef_larg3, self.taille/2))
        else:
            self.p6 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side +
                                                           "/stand_"+self.comp+".png"),
                                         (self.larg, self.taille))
            self.p9 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side +
                                                           "/stand_"+self.comp+".png"),
                                         (self.larg, self.taille/2))
        self.p10 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side +
                                                           "/garde_"+self.comp+".png"),
                                         (self.larg, self.taille))

        
        """
        self.p00="subir assis"
        self.p0="subir"
        self.p1="stand"
        self.ps1="stand2"
        self.p2="crouch"
        self.p3="jump"
        self.p4="att_l"
        self.p5="att_m"
        self.p6="att_h"
        self.p7="att_l_crouch"
        self.p8="att_m_crouch"
        self.p9="att_h_crouch"
        self.p10="garde"
        """
        self.p11 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side2 +
                                                            "/stand_"+self.comp2+".png"),
                                          (self.larg, self.taille))
        # subir
        self.p21 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side2 +
                                                           "/se_prend_un_coup_"+self.comp2+".png"),
                                         (self.larg, self.taille))
        self.p210 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side2 +
                                                           "/se_prend_un_coup_"+self.comp2+".png"),
                                         (self.larg, self.taille/2))
        # pas1
        self.p11 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side2 +
                                                           "/stand_"+self.comp2+".png"),
                                         (self.larg, self.taille))
        self.ps2 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side2 +
                                                           "/stand2_"+self.comp2+".png"),
                                         (self.larg, self.taille))
        self.p12 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side2 +
                                                           "/crouch_"+self.comp2+".png"),
                                         (self.larg, self.taille/2))
        self.p13 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side2 +
                                                           "/jump_"+self.comp2+".png"),
                                         (self.larg, self.taille))
        if self.skillset[0]!="P":
            self.p14 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side2 +
                                                           "/att_l_"+self.comp2+".png"),
                                         (self.larg*self.coef_larg1, self.taille))
            self.p17 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side2 +
                                                           "/att_l_"+self.comp2+".png"),
                                         (self.larg*self.coef_larg1, self.taille/2))
        else:
            self.p14 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side2 +
                                                           "/stand_"+self.comp2+".png"),
                                         (self.larg, self.taille))
            self.p17 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side2 +
                                                           "/stand_"+self.comp2+".png"),
                                         (self.larg, self.taille/2))
        if self.skillset[1]!="P":
            self.p15 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side2 +
                                                           "/att_m_"+self.comp2+".png"),
                                         (self.larg*self.coef_larg2, self.taille))
            self.p18 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side2 +
                                                           "/att_m_"+self.comp2+".png"),
                                         (self.larg*self.coef_larg2, self.taille/2))
        else:
            self.p15 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side2 +
                                                           "/stand_"+self.comp2+".png"),
                                         (self.larg, self.taille))
            self.p18 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side2 +
                                                           "/stand_"+self.comp2+".png"),
                                         (self.larg, self.taille/2))
        if self.skillset[2]!="P":
            self.p16 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side2 +
                                                           "/att_h_"+self.comp2+".png"),
                                         (self.larg*self.coef_larg3, self.taille))
            self.p19 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side2 +
                                                           "/att_h_"+self.comp2+".png"),
                                         (self.larg*self.coef_larg3, self.taille/2))
        else:
            self.p16 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side2 +
                                                           "/stand_"+self.comp2+".png"),
                                         (self.larg, self.taille))
            self.p19 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side2 +
                                                           "/stand_"+self.comp2+".png"),
                                         (self.larg, self.taille/2))
        self.p20 = pygame.transform.scale(pygame.image.load("assets/Perso/"+typ+"/"+str(skin)+"/"+side2 +
                                                           "/garde_"+self.comp2+".png"),
                                         (self.larg, self.taille))

        

    def mouvement(self, ennemi):
        touche = pygame.key.get_pressed()
        b = self.liste_bouton
        ba = ennemi.liste_bouton
        if self.y <= self.sol-self.taille_b:
            self.saut()
        if not(touche[b["gauche"]]) and not(touche[b["haut"]]) and not(touche[b["bas"]]) and not(touche[b["droite"]]) and not(touche[b["light"]]) and not(touche[b["heavy"]]) and not(touche[b["mid"]]) and not( self.arret_h1) and not (self.arret_l1) and not (self.arret_m1) and not(self.se_faire_attaquer) :
            self.blocking = True
        if self.y > self.sol-self.taille_b and not(touche[b["bas"]]):
            self.y -= self.taille
            self.taille = self.taille_b
        if not(self.arret_l1) and not (self.arret_h1) and not(self.arret_m1)and not(self.se_faire_attaquer):

            if touche[b["haut"]] and self.y == (self.sol-self.taille_b):
                self.jumping = True
            if touche[b["light"]] and not(self.se_faire_attaquer):
                self.blocking = False
            if touche[b["bas"]] and self.taille >= self.taille_b and not(self.jumping):
                self.taille = self.taille/2
                self.y += self.taille
                if (self.side == "Left" and self.cotee == "base" and touche[b["gauche"]]) or (self.side == "Left" and self.cotee == "no" and touche[b["droite"]]) or (self.side == "Right" and self.cotee == "no" and touche[b["gauche"]]) or (self.side == "Right" and self.cotee == "base" and touche[b["droite"]]):
                    self.blocking = True
                else:
                    self.blocking = False
            if (self.x < ennemi.x and self.side == "Left") or (self.x > ennemi.x and self.side != "Left"):
                self.cotee = "base"
            else:
                self.cotee = "no"
            if touche[b["droite"]] and not(self.se_faire_attaquer) and self.x < 1180 and ((self.side == "Left" and self.cotee == "base") or (self.side != "Left" and self.cotee != "base")):
                self.blocking = False
                if self.x+(self.larg/2) < ennemi.x or (self.y+self.taille_b < ennemi.y+ennemi.taille_b and not(touche[ba["bas"]])) or (self.y+self.taille < ennemi.y and touche[ba["bas"]]):
                    self.cpt += 1
                    if self.cpt % self.vitesse == 0:
                        self.cote = not(self.cote)
                    if self.taille == self.taille_b:
                        self.x += self.vitesse
                    else:
                        self.x += (self.vitesse/5)
            if touche[b["gauche"]] and not(self.se_faire_attaquer) and self.x > 0 and ((self.side == "Left" and self.cotee == "base") or (self.side != "Left" and self.cotee != "base")):
                self.blocking = True
                self.cpt += 1
                if self.cpt % self.vitesse == 0:
                    self.cote = not(self.cote)
                if self.taille == self.taille_b:
                    self.x -= self.vitesse
                else:
                    self.x -= (self.vitesse/5)
            if touche[b["droite"]] and not(self.se_faire_attaquer) and self.x < 1180 and ((self.side == "Left" and self.cotee == "no") or (self.side != "Left" and self.cotee == "base")):
                self.blocking = True
                self.cpt += 1
                if self.cpt % self.vitesse == 0:
                    self.cote = not(self.cote)
                if self.taille == self.taille_b:
                    self.x += self.vitesse
                else:
                    self.x += (self.vitesse/5)

            if touche[b["gauche"]] and not(self.se_faire_attaquer) and self.x > 0 and ((self.side == "Left" and self.cotee == "no") or ((self.side != "Left" and self.cotee == "base"))):
                self.blocking = False
                if self.x > ennemi.x+ennemi.larg or (self.y+self.taille < ennemi.y and touche[ba["bas"]]) or (self.y+self.taille_b < ennemi.y+ennemi.taille_b and not(touche[ba["bas"]])):
                    self.cpt += 1
                    if self.cpt % self.vitesse == 0:
                        self.cote = not(self.cote)
                    if self.taille == self.taille_b:
                        self.x -= self.vitesse
                    else:
                        self.x -= (self.vitesse/5)

    def saut(self):
        if self.jumping:
            self.y -= self.Y_VELOCITY
            self.Y_VELOCITY -= self.Y_GRAVITY
            if self.Y_VELOCITY < -self.JUMP_HEIGHT:
                self.jumping = False
                self.Y_VELOCITY = self.JUMP_HEIGHT

    def draw(self, Fighter2, vie2, SCREEN):
        touche = pygame.key.get_pressed()
        b = self.liste_bouton
        if self.se_faire_attaquer:
            self.blocking=False
            
            if self.taille_b==self.taille:  
                if self.cotee=='base':
                    SCREEN.blit(self.p0, (self.x, self.y))
                else:
                    SCREEN.blit(self.p21, (self.x, self.y))
            else:
                if self.cotee=='base':
                    SCREEN.blit(self.p00, (self.x, self.y))
                else:
                    SCREEN.blit(self.p210, (self.x, self.y))
            self.cpt_sefairemal-=2
            if self.cpt_sefairemal<=0:
                self.se_faire_attaquer=False
                self.blocking=True
        if self.existe:
            for i in self.liste_projectile:
                i.mouvements()
                i.draw(SCREEN)
                if i.x+150 < 0 or i.x > 1280 or i.touchable(Fighter2):
                    if i.touchable(Fighter2) and not(Fighter2.blocking):
                        if i.num==1:
                            if self.skillset[0]=="P":
                                vie2.degat(self.att_l, Fighter2.defense)
                                Fighter2.subir_sfx.play()
                            else:
                                vie2.degat(self.att_m, Fighter2.defense)
                                Fighter2.subir_sfx.play()
                        else:
                            vie2.degat(self.att_h, Fighter2.defense)
                    self.liste_projectile.remove(i)
        if not(self.jumping) and not(self.se_faire_attaquer):
            self.position = "NORMAL"
            if (touche[b["bas"]]):
                self.position = "Low"
            if self.arret_h1 or self.arret_l1 or self.arret_m1:

                if self.cpt_l == 0:
                    self.arret_l1 = False
                    self.assis_de_base1 = False
                if self.arret_l1:
                    if self.assis_de_base1:
                        self.attaque("Light", "Low", SCREEN)
                    else:
                        self.attaque("Light", "NORMAL", SCREEN)
                    self.blocking = False
                    self.cpt_l -= 1

                if self.cpt_m == 0:
                    self.arret_m1 = False
                    self.assis_de_base2 = False
                if self.arret_m1:
                    if self.assis_de_base2:
                        self.attaque("Mid", "Low", SCREEN)
                    else:
                        self.attaque("Mid", "NORMAL", SCREEN)
                    self.blocking = False
                    self.cpt_m -= 1

                if self.cpt_h == 0:
                    self.arret_h1 = False
                    self.assis_de_base3 = False
                if self.arret_h1:
                    if self.assis_de_base3:
                        self.attaque("Heavy", "Low", SCREEN)
                    else:
                        self.attaque("Heavy", "NORMAL", SCREEN)
                    self.blocking = False
                    self.cpt_h -= 1
                

            elif (touche[b["mid"]] and not(self.arret_m1)):
                if not(self.typ2=="Special"or self.typ2=="Zoner"):
                    self.att_m_sfx.play()
                if self.position == "Low":
                    self.assis_de_base2 = True
                self.blocking = False
                if self.skillset[1]=="P":
                    self.attaque("Mid", self.position, SCREEN)
                    self.projectile = Projectile(self,1)
                    self.liste_projectile.append(self.projectile)
                else:
                    self.attaque("Mid", self.position, SCREEN)
                    
                if not(Fighter2.blocking) and self.touchable(Fighter2) and vie2.get_vie() > 0:
                    vie2.degat(self.att_m, Fighter2.defense)
                    Fighter2.subir_sfx.play()
                    if not(self.skillset[1]=="P"):
                        Fighter2.se_faire_attaquer=True
                        Fighter2.cpt_sefairemal+=60

                self.existe = True
                self.arret_m1 = True
                self.cpt_m = 30
            elif touche[b["light"]] and not (self.arret_l1) :
                self.att_l_sfx.play()
                self.arret_l1 = True
                self.blocking = False
                
               

                if self.position == "Low":
                    self.assis_de_base1 = True
                if self.skillset[0]=="P":
                    self.cpt_l = 10
                    self.existe = True
                    self.attaque("Light", self.position, SCREEN)
                    self.projectile = Projectile(self,1)
                    self.liste_projectile.append(self.projectile)
                else:
                    self.attaque("Light", self.position, SCREEN)
                    self.cpt_l = 20
                if not(Fighter2.blocking) and self.touchable(Fighter2) and vie2.get_vie() > 0:
                    vie2.degat(self.att_l, Fighter2.defense)
                    Fighter2.subir_sfx.play()
                    if not(self.skillset[0]=="P"):
                        Fighter2.se_faire_attaquer=True
                        Fighter2.cpt_sefairemal+=50


            elif touche[b["heavy"]] and not (self.arret_h1) :
                self.blocking = False
                self.arret_h1 = True
                self.att_h_sfx.play()
                if self.skillset[2]=="P":
                    self.cpt_h = 30
                else:
                    self.cpt_h = 40
                if touche[b["bas"]]:
                    self.assis_de_base3 = True
                if self.skillset[2]=="P":
                    self.existe = True
                    self.attaque("Heavy", self.position, SCREEN)
                    self.projectile = Projectile(self,2)
                    self.liste_projectile.append(self.projectile)
                else:
                    self.attaque("Heavy", self.position, SCREEN)
                if not(Fighter2.blocking) and self.touchable(Fighter2) and vie2.get_vie() > 0:
                    vie2.degat(self.att_h, Fighter2.defense)
                    Fighter2.subir_sfx.play()
                    if not(self.skillset[2]=="P"):
                        Fighter2.se_faire_attaquer=True
                        Fighter2.cpt_sefairemal+=80

                

            elif touche[b["bas"]] and not(touche[b["light"]]) and not(touche[b["mid"]]) and not(touche[b["heavy"]]) and not(self.arret_l1) and not(self.arret_m1) and not(self.arret_h1):
                if self.cotee == "base":
                    SCREEN.blit(self.p2, (self.x, self.y))
                else:
                    SCREEN.blit(self.p12, (self.x, self.y))

            elif self.cote and not(touche[b["light"]]) and not(touche[b["heavy"]]) and not(self.arret_l1) and not(self.arret_h1):
                if self.cotee == "base":
                    if not (self.blocking):
                        SCREEN.blit(self.p1, (self.x, self.y))
                    else:
                        SCREEN.blit(self.p10, (self.x, self.y))
                else:
                    if not (self.blocking):
                        SCREEN.blit(self.p11, (self.x, self.y))
                    else:
                        SCREEN.blit(self.p20, (self.x, self.y))

            elif not(touche[b["bas"]]) and not(self.arret_l1):

                if self.cotee == "base":
                    if not (self.blocking):
                        SCREEN.blit(self.ps1, (self.x, self.y))
                    else:
                        SCREEN.blit(self.p10, (self.x, self.y))
                else:
                    if not (self.blocking):
                        SCREEN.blit(self.ps2, (self.x, self.y))
                    else:
                        SCREEN.blit(self.p20, (self.x, self.y))

        elif self.jumping :
            self.blocking = False
            if self.cotee == "base":
                SCREEN.blit(self.p3, (self.x, self.y,))
            else:
                SCREEN.blit(self.p13, (self.x, self.y,))

    def attaque(self, puissance, hauteur, SCREEN):
        if self.cotee == "base":
            if puissance == "Light":
                if hauteur == "Low":
                    SCREEN.blit(self.p7, (self.x, self.y))
                else:
                    SCREEN.blit(self.p4, (self.x, self.y))
            if puissance == "Mid":
                if hauteur == "Low":
                    SCREEN.blit(self.p8, (self.x, self.y))
                else:
                    SCREEN.blit(self.p5, (self.x, self.y))
            if puissance == "Heavy":
                if hauteur == "Low":
                    SCREEN.blit(self.p9, (self.x, self.y))
                else:
                    SCREEN.blit(self.p6, (self.x, self.y))
        else:
            if puissance == "Light":
                if hauteur == "Low":
                    SCREEN.blit(self.p17, (self.x, self.y))
                else:
                    SCREEN.blit(self.p14, (self.x, self.y))
            if puissance == "Mid":
                if hauteur == "Low":
                    SCREEN.blit(self.p18, (self.x, self.y))
                else:
                    SCREEN.blit(self.p15, (self.x, self.y))
            if puissance == "Heavy":
                if hauteur == "Low":
                    SCREEN.blit(self.p19, (self.x, self.y))
                else:
                    SCREEN.blit(self.p16, (self.x, self.y))

    def touchable(self, ennemi):
        if (self.comp == "g" and self.cotee == "base") or (self.comp == "d" and self.cotee != "base"):
            if (self.x+self.larg >= ennemi.x and self.x+self.larg <= ennemi.x+ennemi.larg) and (self.y+80 >= ennemi.y and self.y <= ennemi.y+ennemi.taille_b):
                return True
            return False
        elif (self.comp == "d" and self.cotee == "base") or (self.comp == "g" and self.cotee != "base"):
            if (self.x <= ennemi.x+ennemi.larg and self.x > ennemi.x) and (self.y+80 >= ennemi.y and self.y <= ennemi.y+ennemi.taille_b):
                return True
            return False

    def spawn(self, SCREEN):
        self.blocking = True
        self.blockingbas = False
        self.jumping = False
        self.se_faire_attaquer = False
        self.cote = True
        self.taille_b = self.typ['taille']
        self.taille = self.taille_b
        self.y = self.sol-self.taille
        self.larg = 100
        self.Y_GRAVITY = 1
        self.JUMP_HEIGHT = 25
        self.Y_VELOCITY = self.JUMP_HEIGHT
        self.liste_projectile = []
        if self.side == "Left":
            self.x = 300
        else:
            self.x = 980

        SCREEN.blit(self.p1, (self.x, self.y))


class Projectile:
    def __init__(self, Fighter,num):
        self.num=num
        if self.num==1:
        
            self.p1 = pygame.transform.scale(pygame.image.load("assets/Perso/"+Fighter.typ2+"/"+Fighter.skin+"/"+Fighter.side +
                                                               "/projectile_"+Fighter.comp+".png"), (70, 50))
            self.p2 = pygame.transform.scale(pygame.image.load("assets/Perso/"+Fighter.typ2+"/"+Fighter.skin+"/"+Fighter.side2 +
                                                               "/projectile_"+Fighter.comp2+".png"), (70, 50))
        else:
            self.p1 = pygame.transform.scale(pygame.image.load("assets/Perso/"+Fighter.typ2+"/"+Fighter.skin+"/"+Fighter.side +
                                                               "/projectile2_"+Fighter.comp+".png"), (70, 50))
            self.p2 = pygame.transform.scale(pygame.image.load("assets/Perso/"+Fighter.typ2+"/"+Fighter.skin+"/"+Fighter.side2 +
                                                              "/projectile2_"+Fighter.comp2+".png"), (70, 50))
        self.y = Fighter.y+40

        if (Fighter.side == "Left" and Fighter.cotee == "base") or (Fighter.side != "Left" and Fighter.cotee != "base"):
            self.x = Fighter.x+Fighter.larg
            self.sens = "Droite"

        else:
            self.x = Fighter.x
            self.sens = "Gauche"
        if Fighter.cotee == "base":
            self.p = self.p1
        else:
            self.p = self.p2
        self.depart = self.x

    def mouvements(self):
        if self.sens == "Droite":
            self.x += 8
        else:
            self.x -= 8

    def draw(self, SCREEN):
        SCREEN.blit(self.p, (self.x, self.y))

    def touchable(self, cible):
        if self.sens == "Gauche":
            if (self.x > cible.x and self.x < cible.x+cible.larg) and (self.y+50 > cible.y and self.y < cible.y+cible.taille_b):
                return True
            return False
        else:
            if (self.x < cible.x+cible.larg and self.x >= cible.x) and (self.y+50 > cible.y and self.y <= cible.y+cible.taille_b):
                return True
            return False

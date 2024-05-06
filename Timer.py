# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 08:28:37 2024

@author: ninja
"""
import pygame
class Timer:
    def __init__(self,cpt):
        self.cpt_b=cpt
        self.counter= self.cpt_b
        self.text = str(self.counter).rjust(3)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        self.font = pygame.font.SysFont('Consolas', 30)
        self.font2 = pygame.font.SysFont('Times New Roman',60)
        self.font3 = pygame.font.SysFont('Times New Roman',60)
        self.round=0
        self.roundstr=str(self.round)
        self.round_cpt=Round()
        
    def reduction(self,vie1,vie2):
        if self.counter!=0:
            self.counter -= 1
            self.text = str(self.counter).rjust(3) 
            
            
        else :
            self.rounds(vie1,vie2)
            self.roundstr=str(self.round)
            self.reset_timer()
    def reset_timer(self):
        self.counter= self.cpt_b
        self.text = str(self.counter).rjust(3)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        self.font = pygame.font.SysFont('Consolas', 30)
        
        
    def rounds(self,vie1,vie2):
        self.round+=1
        self.roundstr=str(self.round)
        if self.round>1:
            self.round_cpt.round_count(vie1,vie2)
        
    def get_time(self):
        return self.counter

class Round:
    def __init__(self):
        self.left=self.right=0
    def round_count(self,vie1,vie2):
        if self.left >1 or self.right>1:
            if self.left>self.right:
                print("left Wins")
            else:
                print("left Wins")
        
        else:
            if vie1==vie2:
                self.left+=1
                self.right+=1
            elif vie1>vie2:
                self.left+=1
            else:
                self.right+=1
        
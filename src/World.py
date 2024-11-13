'''
World.py อันนี้เอาไว้สำหรับสร้างด่าน/โชว์ด่าน

World.py ต้องมี Attribute อะไรบ้าง
1. Background สำหรับ Display
2. Player -- ซึ่งมาจาก EntityBase อีกที
3. Enemies -- ซึ่งมาจาก EntityBase อีกที
4. List of Enemies -- ซึ่งเป็น List ของ Enemies อีกทีนึง

ใน EntityBase มีอะไร
1. direction -- Up Down Left Right
2. animation_list -- 

World.py ต้องมี Function อะไรบ้าง

'''

import random
from src.entity_defs import *
from src.constants import *
from src.Dependencies import *
from src.EntityBase import EntityBase
from src.entity_defs import EntityConf
from src.player import *
import pygame

class World:
    def __init__(self, wave_number, player: Player):
        self.width = WIDTH
        self.height = HEIGHT
        
        self.bg_image = pygame.image.load("graphics/battlefield.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH,HEIGHT))
        
        
        self.entities = []
        #self.GenerateEntities()

    def GenerateEntities(self,level) :
        pass 

    def update(self, dt, events):
        pass

    def render(self, screen: pygame.Surface):
        
        
        screen.blit(self.bg_image, (0,0))
        pass

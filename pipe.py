import pygame as pg
from random import randint

class Pipe:
    def __init__(self,scale_factor,move_speed):
        self.image_up = pg.transform.scale_by(pg.image.load("Assets/sprites/pipeup.png").convert_alpha(),scale_factor)
        self.image_down = pg.transform.scale_by(pg.image.load("Assets/sprites/pipedown.png").convert_alpha(),scale_factor)

        self.image_up = pg.transform.scale(self.image_up, (80, 500))
        self.image_down = pg.transform.scale(self.image_down, (80, 500))


        self.rect_up = self.image_up.get_rect()
        self.rect_down = self.image_down.get_rect()
        self.pipe_distance = 200
        self.rect_up.x = 600
        self.rect_up.y = randint(250,520)
        self.rect_down.x = 600
        self.rect_down.y = self.rect_up.y - self.pipe_distance - self.rect_up.height
        self.move_speed = move_speed


    def drawPipe(self,win):
        win.blit(self.image_up,self.rect_up)
        win.blit(self.image_down,self.rect_down)

    def update(self,dt):
        self.rect_up.x -= int(self.move_speed*dt)
        self.rect_down.x-= int(self.move_speed*dt)
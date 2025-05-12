import pygame as pg
import sys , time
from bird import Bird
from pipe import Pipe
pg.init()

class Game:
    def __init__(self):
        # setting window config.
        self.width = 600
        self.height = 768
        self.scale_factor =2.1
        self.win = pg.display.set_mode((self.width,self.height))
        self.move_speed = 250
        self.is_enter_pressed = False
        self.is_game_started = True
        self.pipes = []
        self.pipe_generate_counter = 71
        self.monitoring = False
        self.score = 0
        self.font = pg.font.Font("Assets/sprites/font.ttf",24)
        self.score_text = self.font.render("Score: 0",True,(0,0,0))
        self.score_text_rect = self.score_text.get_rect(center = (100,30))
        self.high_score=0
        self.h_score_text = self.font.render("High Score: 0",True,(0,0,0))
        self.h_score_text_rect = self.h_score_text.get_rect(center = (150,600))
        self.restart_text = self.font.render("Restart",True,(0,0,0))
        self.restart_text_rect = self.score_text.get_rect(center = (300,700))
        self.has_collided = False
        self.start_message = pg.image.load("Assets/sprites/message.png").convert_alpha()
        self.start_message_rect = self.start_message.get_rect(center = (300,400))


        self.sounds = self.sounds = {
        'point': pg.mixer.Sound('Assets/audio/point.wav'),
        'flap': pg.mixer.Sound('Assets/audio/wing.wav'),
          'hit': pg.mixer.Sound('Assets/audio/hit.wav'),
          'die': pg.mixer.Sound('Assets/audio/die.wav')
}

        self.clock=pg.time.Clock()
        self.bird = Bird(self.scale_factor)

        self.setUpBaseAndBg()

        

        self.gameLoop()

    def gameLoop(self):
        last_time = time.time()
        while True:
            # calculating delta time
            new_time = time.time()
            dt = new_time - last_time
            last_time=new_time
            
    
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN and self.is_game_started:
                    if event.key == pg. K_RETURN :
                      self.is_enter_pressed = True
                      self.bird.update_on = True
                    if event.key == pg. K_SPACE and self.is_enter_pressed:
                        self.bird.flap(dt)
                        self.sounds['flap'].play()

                if event.type == pg.MOUSEBUTTONUP :
                     if self.restart_text_rect.collidepoint(pg.mouse.get_pos()):
                         self.restartGame()

            self.UpdateEverything(dt)
            self.checkScore()
            self.checkCollisions()
            self.drawEverything()
            pg.display.update()  
            self.clock.tick(60)

    def restartGame(self):
       self.score = 0
       self.monitoring = False
       self.h_score_text = self.font.render("High Score: 0",True,(0,0,0))
       self.score_text = self.font.render("Score: 0",True,(0,0,0))
       self.is_enter_pressed = False
       self.is_game_started =True
       self.bird.resetposition()
       self.pipes.clear()
       self.pipe_generate_counter = 71
       self.bird.update_on = False
       self.has_collided = False


    def checkScore(self):
       if len(self.pipes)>0: 

           if (self.bird.rect.left > self.pipes[0].rect_down.left and 
            self.bird.rect.right < self.pipes[0].rect_down.right and not self.monitoring):
               self.monitoring = True
           if self.bird.rect.left > self.pipes[0].rect_down.right and self.monitoring:
               self.monitoring = False 
               self.sounds['point'].play()
               self.score+=1
               self.high_score =self.score
               self.score_text = self.font.render(f"Score : {self.score} ",True,(0,0,0))
               self.h_score_text = self.font.render(f"High Score: {self.high_score} ",True,(0,0,0))

          
    def checkCollisions(self): 
      if not self.has_collided:                          
        if len(self.pipes):
            if self.bird.rect.bottom >533:
                self.sounds['hit'].play()  # Play hit sound when bird hits the ground
                self.sounds['die'].play()  
                self.has_collided = True
                self.bird.update_on = False
                self.is_enter_pressed = False
                self.is_game_started = False
            if (self.bird.rect.colliderect(self.pipes[0].rect_down) or self.bird.rect.colliderect(self.pipes[0].rect_up)):
                self.sounds["hit"].play()
                self.sounds['die'].play()
                self.has_collided = True
                self.bird.update_on = False
                self.is_enter_pressed = False
                self.is_game_started = False
                


    def UpdateEverything(self,dt):
        if self.is_enter_pressed :
            # moving the ground
            self.base1_rect.x-=int(self.move_speed*dt)
            self.base2_rect.x-=int(self.move_speed*dt)

            if self.base1_rect.right <=0:
             self.base1_rect.x=self.base2_rect.right 
            if self.base2_rect.right <=0:
             self.base2_rect.x=self.base1_rect.right

             # generating pipes

            if self.pipe_generate_counter > 70:
               self.pipes.append(Pipe(self.scale_factor,self.move_speed))
               self.pipe_generate_counter =0
            self.pipe_generate_counter+=1

            # moving the pipes

            for pipe in self.pipes:
                pipe.update(dt)

            # removing pipes if out of screen
             
            if len(self.pipes) !=0:
                if self.pipes[0].rect_up.right <0:
                   self.pipes.pop(0)

            # moving the bird
        self.bird.update(dt)


    def drawEverything(self):
        self.win.blit(self.bg_img,(0,-350)) 
        for pipe in self.pipes:
            pipe.drawPipe(self.win)
        self.win.blit(self.base1_img,self.base1_rect)
        self.win.blit(self.base2_img,self.base2_rect)  
        self.win.blit(self.bird.image,self.bird.rect)
        self.win.blit(self.score_text,self.score_text_rect)
        if not self.is_enter_pressed:
         self.win.blit(self.start_message,self.start_message_rect)
        if  not self.is_game_started:
            self.win.blit(self.restart_text,self.restart_text_rect)
            self.win.blit(self.h_score_text,self.h_score_text_rect)
            
            


    def setUpBaseAndBg(self):

       # set images for background and base
        self.bg_img = pg.transform.scale_by(pg.image.load("Assets/sprites/background.png").convert(),self.scale_factor)
        self.base1_img =  pg.transform.scale_by(pg.image.load("Assets/sprites/base.png").convert(),self.scale_factor)
        self.base2_img = pg.transform.scale_by(pg.image.load("Assets/sprites/base.png").convert(),self.scale_factor)
        
        self.base1_rect = self.base1_img.get_rect()
        self.base2_rect = self.base2_img.get_rect()

        self.base1_rect.x = 0
        self.base2_rect.x = self.base1_rect.right
        
        self.base1_rect.y = 533
        self.base2_rect.y = 533
        
       

game=Game()

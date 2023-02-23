from player import *
from blocks import *
from camera import *

class Game:
    #level specific parameters that are for the camera
    left_border = 0
    right_border = WIDTH * 3/2
    bottom_border = HEIGHT

    def __init__(self):
       self.p = Player(WIDTH/2, HEIGHT/2)
       self.b = Block_Manager()
       self.camera = Camera(WIDTH*7/12, HEIGHT/3) #parameters are the distances away from the edge before the camera should start moving

       self.last_pressed = False #to prevent holding jump button
    
    def update(self, mouse, dt):
        self.b.update(mouse, dt)
        self.camera.update(self.p, self.left_border, self.right_border, self.bottom_border) #distances before the camera stops following and hugs wall
        self.p.check_collisions(self.b.blocks, dt)
        

        pressed = pygame.key.get_pressed()

        if pressed[K_w] and not self.last_pressed and (self.p.is_grounded or self.p.is_wall_sliding):
            self.p.jump()
            self.last_pressed = True
        
        #this is so you can't hold the jump key continuously
        #these are the conditions for jumping, either on the ground or wall sliding
        if self.last_pressed and not pressed[K_w]:
            self.last_pressed = False

        if pressed[K_a] and not self.p.is_moving_right:
            self.p.move_left()
            self.p.is_moving_left = True
        else:
            self.p.is_moving_left = False

        if pressed[K_d] and not self.p.is_moving_left:
            self.p.move_right()
            self.p.is_moving_right = True
        else:
            self.p.is_moving_right = False


        if pressed[K_s]:
            if self.p.is_sticking: #if on the bottom of a sticky block, jump down
                self.p.is_sticking = False
            else:
                self.p.crouch()
                self.p.is_crouching = True
        else:
            self.p.is_crouching = False

        
        #updating player last
        self.p.update(dt)

    def draw(self, screen):
        self.b.draw(screen, self.camera.d)
        self.p.draw(screen, self.camera.d)
        
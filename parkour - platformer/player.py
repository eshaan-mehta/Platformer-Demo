from setup import *

class Player:
    color = (181, 128, 54)
    standing_height = 40
    crouch_height = 20

    width, height = 20, standing_height
    ground_resistance = 0.005
    ground_m_a = 0.002
    crouch_acceleration = 0.002/3
    sticky_resistance = 0.01
    sticky_m_a = 0.0005
    ground_jump_power = 0.6
    gravity = 0.0015
    wall_slide_speed = 0.05
    wall_push_off = 0.5
    
    def __init__(self, x, y):
        self.movement_acceleration = self.ground_m_a
        self.resistance = self.ground_resistance
        
        self.jump_power = self.ground_jump_power

        self.d = pygame.Vector2(x, y)
        self.v = pygame.Vector2(0,0)
        self.a = pygame.Vector2(0, self.gravity)

        self.is_jumping = False
        self.is_grounded = False
        self.is_crouching = False
        self.is_moving_left = False
        self.is_moving_right = False

        self.is_wall_sliding = False
        self.push_dir = "" #direction that player will go after wall jump
        self.prev_wall = "" #side of the players body that was touching the wall
        self.prev_wall_y = 0
        self.is_sticking = False

    def jump(self):
        self.v.y = -self.jump_power
        self.is_wall_sliding = False

        if self.push_dir != "":
            self.v.x = self.wall_push_off if self.push_dir == "r" else -self.wall_push_off
            self.prev_wall = "l" if self.push_dir == "r" else "r"

    def crouch(self):
        self.height = self.crouch_height
        self.movement_acceleration = self.crouch_acceleration

    def move_left(self):
        self.a.x += -self.movement_acceleration

    def move_right(self):
        self.a.x += self.movement_acceleration

    def check_collisions(self, blocks, dt):
        epsilon_x = abs(self.v.x) * dt
        epsilon_y = abs(self.v.y) * dt

        top = self.d.y
        bottom = self.d.y + self.height
        left = self.d.x
        right = self.d.x + self.width


        #bottom of screen collision
        if abs(bottom - HEIGHT) <= epsilon_y :
            self.d.y = HEIGHT - self.height
            self.is_grounded = True
        
        for block in blocks:
            block_top = block.d.y
            block_bottom = block.d.y + block.height
            block_left = block.d.x
            block_right = block.d.x + block.width

            if left < block_right and right > block_left:
                if abs(bottom - block_top) <= epsilon_y:
                    self.d.y = block_top - self.height
                    self.is_grounded = True

                if abs(top - block_bottom) <= epsilon_y and block.bottom != "hollow":
                    self.d.y = block_bottom
                    self.is_sticking = True if block.bottom == "sticky" else False

                    if self.is_jumping:
                        self.v.y = 0
                        
            
            if bottom > block_top and top < block_bottom and block.bottom != "hollow":
                #right side of player collision
                if abs(right - block_left) <= epsilon_x:
                    self.d.x = block_left - self.width
                    if self.v.x > 0: 
                        self.v.x = 0

                    if not self.is_grounded and block.is_slidable[0] and self.is_moving_right and (not self.prev_wall == "r" or self.d.y > self.prev_wall_y):
                        self.push_dir = "l"
                        self.prev_wall_y = self.d.y
                        self.is_wall_sliding = True
                
                #left side of player collisions
                if abs(left - block_right) <= epsilon_x:
                    self.d.x = block_right
                    if self.v.x < 0:
                        self.v.x = 0

                    if not self.is_grounded and block.is_slidable[1] and self.is_moving_left and (not self.prev_wall == "l" or self.d.y > self.prev_wall_y):
                        self.push_dir = "r"
                        self.prev_wall_y = self.d.y
                        self.is_wall_sliding = True

                
                    
        if self.is_grounded and not self.is_jumping:
            self.v.y = 0
            self.prev_wall = ""
            self.prev_wall_y = 0

    def update(self, dt):
        self.d += self.v * dt
        self.v += self.a * dt
        self.v.x *= max(0, 1 - dt*self.resistance)

        self.is_jumping = True if self.v.y < 0 else False

        if self.is_sticking:
            self.v.y = 0
            self.resistance = self.sticky_resistance
            self.movement_acceleration = self.sticky_m_a
        else:
            self.resistance = self.ground_resistance
            if not self.is_crouching:
                self.movement_acceleration = self.ground_m_a
        
        if self.is_wall_sliding:
            self.a.y = 0
            self.v.y = self.wall_slide_speed * dt
        else:
            self.a.y = self.gravity

        
        #variable resets
        self.a.x = 0
        self.height = self.standing_height
        self.is_grounded = False
        
        self.is_wall_sliding = False
        self.push_dir = ""
        self.is_sticking = False

    def draw(self, screen, camera):
        r = pygame.Rect(self.d.x - camera.x, self.d.y - camera.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, r)



from setup import *

class Camera:

    def __init__(self, player_offset_x, player_offset_y):
        self.d = pygame.Vector2(0,0)
        self.offset = pygame.Vector2(-player_offset_x, -player_offset_y)


    def update(self, player, left_border, right_border, bottom_border):
        self.d.x += int(player.d.x - self.d.x + self.offset.x) #camera.x sticks to offset.x distance away from player.x
        self.d.y += int(player.d.y - self.d.y + self.offset.y) #camera.y sticks to offset.y distance away from player.y

        self.d.x = max(left_border, self.d.x) #setting up the maximum for the left side camera
        self.d.x = min(self.d.x, right_border - WIDTH) #setting the maximum for the right side camera

        self.d.y = min(self.d.y, bottom_border - HEIGHT) #prevent bottom of the camera from going below the bottom of the world
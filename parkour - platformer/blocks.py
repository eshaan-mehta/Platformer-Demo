from setup import *


class Block:  
    def __init__(self, x, y, width, height, can_move, slidable_l, slidable_r, bottom, color):
        self.d = pygame.Vector2(x, y)
        self.v = pygame.Vector2(0, 0)

        self.width = width
        self.height = height
        
        self.can_move = can_move
        self.is_slidable = [slidable_l, slidable_r]

        #block bottom are solid, hollow, sticky
        self.bottom = bottom
        self.color = color

        self.selected = False
        self.last_pressed = False

    def check_mouse_collision(self, mouse):
        return (mouse.x >= self.d.x and mouse.x <= self.d.x + self.width) and (mouse.y >= self.d.y and mouse.y <= self.d.y + self.height) 


    def update(self, mouse, dt):
        self.d += self.v * dt

        if self.check_mouse_collision(mouse) and pygame.mouse.get_pressed()[0] and not self.last_pressed:
            self.selected = not self.selected
            #gonna need a prev mouse pos var to keep track. self.d += mouse - prev_mouse

        

    def is_on_screen(self, rect):
        return True
        #return ((rect.left > 0 and rect.x < WIDTH) or (rect.right > 0 and rect.right < WIDTH) or (rect.left <= 0 and rect.right >= WIDTH)) and ((rect.top > 0 and rect.top < HEIGHT) or (rect.bottom > 0 and rect.bottom < HEIGHT) or (rect.top <= 0 and rect.bottom >= HEIGHT))

    def draw(self, screen, camera):
        r = pygame.Rect(self.d.x - camera.x, self.d.y - camera.y, self.width, self.height)
        
        if self.is_on_screen(r):
            pygame.draw.rect(screen, self.color, r)



class Block_Manager:
    file_name = "game blocks demo.txt"
    colors = {"black": (0, 0, 0), "neon": (196, 252, 28), "red": (200, 0, 0), "green": (155, 222, 104)}
    num_attributes = 9

    default_size = pygame.Vector2(100, 20)

    def __init__(self):
        self.blocks = []
        
        self.create_game_map()
        
    def create_game_map(self):
        f = open(self.file_name)
        text = f.read()
        f.close()

        num_blocks = len(text.split('\n'))#counts number of lines in txt file

        text = text.split() #splits file per word

        for i in range(num_blocks):

            #two endpoints of each line, formula is row number(i) * # of things in each row
            b = [text[j] for j in range(i*self.num_attributes, (i + 1)*self.num_attributes)]

            can_move = True if b[4] == 'True' else False
            can_slide_l = True if b[5] == 'True' else False
            can_slide_r = True if b[6] == 'True' else False

            self.blocks.append(Block(int(b[0]), int(b[1]), int(b[2]), int(b[3]), can_move, can_slide_l, can_slide_r, b[7], self.colors[b[8]]))

    def update(self, mouse, dt):

        for block in self.blocks:
            block.update(mouse, dt)

    def draw(self, screen, camera):
        for block in self.blocks:
            block.draw(screen, camera)
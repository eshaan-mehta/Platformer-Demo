from game import *

background_color = (140, 196, 250)
is_running = True


g = Game()


while is_running:
    #delta time calculation
    dt = CLOCK.tick()

    pygame.display.set_caption("FPS: " + str(int(CLOCK.get_fps())))
    screen.fill(background_color)

    mouse = pygame.Vector2(pygame.mouse.get_pos())

    g.update(mouse, dt)
    g.draw(screen)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                is_running = False
    
    pygame.display.update()
pygame.quit()
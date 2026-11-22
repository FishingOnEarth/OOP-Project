import pygame
import config
import renderer

pygame.init()
screen=pygame.display.set_mode(config.WINDOW_SIZE)

position=(100,200)

running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    
    renderer.draw_background(screen)
    renderer.draw_car(screen,position,config.CAR_COLOR)


    pygame.display.flip()

pygame.quit()

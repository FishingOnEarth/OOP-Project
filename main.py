import pygame
import config
import renderer
from wavefront import wavefront
pygame.init()
screen=pygame.display.set_mode(config.WINDOW_SIZE)
clock=pygame.time.Clock()

simulation_time=0
wavefronts=[]
position=(100,200)
wave1=wavefront(position,0)
wavefronts.append(wave1)
path_start=(50,225)
path_end=(750,225)

running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    simulation_time+=clock.tick(60)/1000
    renderer.draw_scene(screen,path_start,path_end,source_position=0,source_velocity=0,observer_position=0,observer_velocity=0,wavefronts=wavefronts,simulation_time=simulation_time,sound_speed=config.SOUND_SPEED)

    pygame.display.flip()

pygame.quit()

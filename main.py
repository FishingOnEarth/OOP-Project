import pygame
import config
import renderer
from wavefront import Wavefront
from car import Car
from interface import *

pygame.init()
screen=pygame.display.set_mode(config.WINDOW_SIZE)
clock=pygame.time.Clock()
simulation_time=0
wavefronts=[]

source_position=(100,200)
wave1=Wavefront(source_position,0)
wavefronts.append(wave1)
path_start=(50,225)
path_end=(350,100)
last_emission_time=0
car_speed=100
source_car=Car(path_start, car_speed,path_end )

observer=Car((50,300),100,(400,300))

running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    dt=clock.tick(60)/1000
    simulation_time+=dt
    source_car.update(dt)
    observer.update(dt)
    if simulation_time-last_emission_time>=0.2:
        wave=Wavefront(source_car.position,simulation_time)
        last_emission_time=simulation_time
        wavefronts.append(wave)

    
    renderer.draw_scene(screen,path_start,path_end,source_car.position,source_car.velocity(),observer.position,observer.velocity(),wavefronts=wavefronts,simulation_time=simulation_time,sound_speed=config.SOUND_SPEED)
    pygame.display.flip()

pygame.quit()

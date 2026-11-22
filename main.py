import pygame
import config
import renderer
from wavefront import Wavefront
from car import Car
from audio_manager import AudioManager
from doppler import Doppler
from interface import *

pygame.init()
screen=pygame.display.set_mode(config.WINDOW_SIZE)
panel_rect=pygame.Rect(800, 0, 250, 600)
clock=pygame.time.Clock()
simulation_time=0
wavefronts=[]

ui=Interface(panel_rect)
f_obs=AudioManager()
doppler=Doppler()
source_position=(100,200)
wave1=Wavefront(source_position,0)
wavefronts.append(wave1)
path_start=(50,225)
path_end=(350,100)
last_emission_time=0
car_speed=100
source_car=Car(path_start, car_speed,path_end )
observer=Car((750,300),100,(50,300))


#f_obs.start()

running=True
while running:
    for event in pygame.event.get():
        ui.handle_event(event)
        if event.type==pygame.QUIT:
            running=False
    dt=clock.tick(60)/1000

    if ui.consume_reset_request():
        ui.base_freq_slider.value=440.0
        ui.source_speed_slider.value = 50.0
        ui.observer_speed_slider.value = 0.0
        source_car=Car(path_start, car_speed,path_end )
        observer=Car((750,300),100,(50,300))
        source_car.speed=ui.source_speed
        observer.speed=ui.observer_speed
        simulation_time=0
        last_emission_time=0
        wavefronts.clear()
        f_obs.reset(ui.base_freq)
        ui.set_observed_frequency(ui.base_freq)
    
    if ui.running:
        simulation_time+=dt
        source_car.speed=ui.source_speed
        observer.speed=ui.observer_speed

        source_car.update(dt)
        observer.update(dt)
        fo=doppler.dopplermath(source_car, observer, ui.base_freq)
        ui.set_observed_frequency(fo)

        f_obs.set_frequency(fo)
        f_obs.start()

        if simulation_time-last_emission_time>=0.2:
            wave=Wavefront(source_car.position,simulation_time)
            last_emission_time=simulation_time
            wavefronts.append(wave)
    else:
        f_obs.stop()
    
    renderer.draw_scene(screen,path_start,path_end,source_car.position,source_car.velocity(),observer.position,observer.velocity(),wavefronts=wavefronts,simulation_time=simulation_time,sound_speed=config.SOUND_SPEED)
    ui.draw(screen)
    pygame.display.flip()
    

f_obs.cleanup()
pygame.quit()

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

path_start = (10, 45)
path_end = (70, 20)
observer_start = (150, 60)
observer_end = (10, 60)
last_emission_time = 0

source_car = Car(path_start, ui.source_speed, path_end)
observer = Car(observer_start, ui.observer_speed, observer_end)

car_speed=100

source_position=(20,40)
wave1=Wavefront(source_position,0)
wavefronts.append(wave1)




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
        observer=Car((150,60),100,(10,60))
        source_car.speed=ui.source_speed
        observer.speed=ui.observer_speed
        simulation_time=0
        last_emission_time=0
        wavefronts.clear()
        f_obs.reset(ui.base_freq)
        ui.set_observed_frequency(ui.base_freq)
    
    if ui.running:
        simulation_time+=dt*0.2
        source_car.speed=ui.source_speed
        observer.speed=ui.observer_speed

        source_car.update(dt*0.2)
        observer.update(dt*0.2)
        fo=doppler.dopplermath(source_car, observer, ui.base_freq)
        ui.set_observed_frequency(fo)

        f_obs.set_frequency(fo)
        f_obs.start()

        if simulation_time-last_emission_time>=0.04:
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

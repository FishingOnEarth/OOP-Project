# Team members: Xuanchen Yu, Yiwen Ma, Jiaqi Sun
# Purpose: Runs the simulation loop and coordinates input, motion, graphics, and audio.

import pygame
import config
import renderer
from wavefront import Wavefront
from car import Car
from audio_manager import AudioManager
from doppler import Doppler
from interface import *
from assets import load_image

pygame.init()
screen=pygame.display.set_mode(config.WINDOW_SIZE)
panel_rect=pygame.Rect(800, 0, 250, 600)
clock=pygame.time.Clock()
simulation_time=0
wavefronts=[]

car_size = (config.CAR_WIDTH, config.CAR_HEIGHT)
source_image = load_image("images/source.png", car_size)
observer_image = load_image("images/obs.png", car_size)
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


#user select start and end point
pending_start=None
route_selected=False

running=True
while running:
    for event in pygame.event.get():
        ui.handle_event(event)
        if event.type==pygame.QUIT:
            running=False

        #detect a click to configure start point
        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                if not ui.running:
                    x,y = event.pos
                    if x<panel_rect.left: #check that the click is left of the panel
                        last_click=(x/config.PIXELS_PER_METRE,y/config.PIXELS_PER_METRE)
                        if pending_start==None:
                            pending_start=last_click
                        elif last_click != pending_start:
                            path_start=pending_start
                            path_end=last_click
                            route_selected=True
                            source_car=Car(path_start, ui.source_speed, path_end)
                            pending_start=None


    dt=clock.tick(60)/1000

    if ui.consume_reset_request():
        ui.base_freq_slider.value=440.0
        ui.source_speed_slider.value = 50.0
        ui.observer_speed_slider.value = 0.0

        source_car=Car(path_start, ui.source_speed,path_end )
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
    
    renderer.draw_scene(screen,path_start,path_end,source_car.position,source_car.velocity(),observer.position,observer.velocity(),wavefronts=wavefronts,simulation_time=simulation_time,sound_speed=config.SOUND_SPEED,source_image=source_image,observer_image=observer_image,pending_start=pending_start,route_selected=route_selected)
    ui.draw(screen)
    pygame.display.flip()
    

f_obs.cleanup()
pygame.quit()

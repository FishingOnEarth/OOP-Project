import pygame
import config 
from wavefront import wavefront

def draw_rectangle(screen):
    pygame.draw.rect(screen, config.CAR_COLOR, (100, 100, 50, 50))


def draw_scene(screen,path_start,path_end,source_position,source_velocity,observer_position,observer_velocity,wavefronts,simulation_time,sound_speed):
    '''Draws one frame by calling the other drawing functions in order'''
    draw_background(screen)
    draw_road(screen,path_start,path_end)
    for wave in wavefronts:
        center=wave.source_position
        radius=wave.radius(simulation_time,sound_speed)
        draw_wavefront(screen,center,radius)



def draw_background(screen):
    '''Fills the screen with the backgournd color, clearing the previous frame'''
    screen.fill(config.BACKGROUND_COLOR)
    

def draw_road(screen,start,end):
    '''Draws the road between the start and end points'''
    pygame.draw.line(screen,config.LINE_COLOR,start,end,config.LINE_WIDTH)

def draw_car(screen,position,color):
    '''draws one car at its current position using its assigned color'''
    rect=pygame.Rect(0,0,config.CAR_WIDTH,config.CAR_HEIGHT)
    rect.center = position
    pygame.draw.rect(screen,color,rect)


def draw_wavefront(screen,center,radius):
    '''draws one circle using its fixed center and current radius'''
    pygame.draw.circle(screen,config.LINE_COLOR,center,radius,config.LINE_WIDTH)


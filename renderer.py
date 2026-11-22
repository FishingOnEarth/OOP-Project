import pygame
import config 
from wavefront import Wavefront

def draw_rectangle(screen):
    pygame.draw.rect(screen, config.SOURCE_COLOR, (100, 100, 50, 50))


def draw_scene(screen,path_start,path_end,source_position,source_velocity,observer_position,observer_velocity,wavefronts,simulation_time,sound_speed):
    '''Draws one frame by calling the other drawing functions in order'''
    draw_background(screen)
    draw_road(screen,path_start,path_end)
    #drawing for source car and arrow
    draw_car(screen,source_position,config.SOURCE_COLOR)
    draw_velocity_arrow(screen, source_position,source_velocity,config.SOURCE_COLOR)
    #drawing for observer and arrow
    draw_car(screen,observer_position,config.OBS_COLOR)
    draw_velocity_arrow(screen, observer_position,observer_velocity,config.OBS_COLOR)

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

def draw_velocity_arrow(screen, position,velocity,color):
    '''	Draws an arrow pointing in the car’s direction of motion. A longer arrow represents a higher speed.'''
    vx,vy=velocity
    x,y=position
    #find where the arrow ends
    dx=vx*config.ARROW_SCALE
    dy=vy*config.ARROW_SCALE 
    x_final,y_final=(x+dx,y+dy)
    final_pos=(x_final,y_final)
    length = (dx**2 + dy**2)**0.5
    if length == 0:
        return
    #find points to the triangle tip of the angle
    tip=final_pos
    unit_x=dx/length
    unit_y=dy/length
    base_x=x_final-unit_x*config.ARROW_SIZE
    base_y=y_final-unit_y*config.ARROW_SIZE
    side_x=-unit_y*config.ARROW_SIZE/2
    side_y=unit_x*config.ARROW_SIZE/2
    points=[tip,(base_x+side_x,base_y+side_y), (base_x - side_x, base_y - side_y)]
    pygame.draw.line(screen, color, position,final_pos)
    pygame.draw.polygon(screen, color, points)
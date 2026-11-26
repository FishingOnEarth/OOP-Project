# Team members: Xuanchen Yu, Yiwen Ma, Jiaqi Sun
# Purpose: Draws the cars, trail, velocity arrows, and sound wavefronts.

import pygame
import config 
from wavefront import Wavefront

def draw_rectangle(screen):
    pygame.draw.rect(screen, config.SOURCE_COLOR, (100, 100, 50, 50))


def draw_scene(screen,path_start,path_end,source_position,source_velocity,observer_position,observer_velocity,wavefronts,simulation_time,sound_speed,source_image,observer_image,pending_start=None,route_selected=None):
    '''Draws one frame by calling the other drawing functions in order'''
    draw_background(screen)
    draw_road(screen,path_start,source_position)
    #drawing for source car and arrow
    draw_car(screen,source_position,source_image)
    draw_velocity_arrow(screen, source_position,source_velocity,config.SOURCE_COLOR)
    #drawing for observer and arrow
    draw_car(screen,observer_position,observer_image)
    draw_velocity_arrow(screen, observer_position,observer_velocity,config.OBS_COLOR)

    for wave in wavefronts:
        center=wave.source_position
        radius=wave.radius(simulation_time,sound_speed)
        draw_wavefront(screen,center,radius)

    if pending_start is not None:
        pygame.draw.circle(screen,config.MARKER_COLOR,to_pixels(pending_start),3)
    elif route_selected:
        pygame.draw.circle(screen,config.MARKER_COLOR,to_pixels(path_start),3)
        pygame.draw.circle(screen,config.MARKER_COLOR,to_pixels(path_end),3)





def draw_background(screen):
    '''Fills the screen with the backgournd color, clearing the previous frame'''
    screen.fill(config.BACKGROUND_COLOR)
    

def draw_road(screen,start,end):
    '''Draws the road represented by a trail of dots between the start and end points'''
    start=to_pixels(start)
    end=to_pixels(end)
    xi,yi=start
    xf,yf=end
    dx=xf-xi
    dy=yf-yi
    length=(dx**2 + dy**2)**0.5
    if length==0:
        return
    ux,uy=dx/length,dy/length
    for dot in range(1,int(length/20)):
        dot_center=(xi+dot*20*ux,yi+dot*20*uy)
        pygame.draw.circle(screen,config.MARKER_COLOR,dot_center,3)

def draw_car(screen,position,image):
    '''draws one car at its current position using its assigned color'''
    '''
    rect=pygame.Rect(0,0,config.CAR_WIDTH,config.CAR_HEIGHT)
    position=to_pixels(position)
    rect.center = position
    pygame.draw.rect(screen,color,rect)
    '''
    rect=image.get_rect(center=to_pixels(position))
    screen.blit(image,rect)


def draw_wavefront(screen,center,radius):
    '''draws one circle using its fixed center and current radius'''
    center=to_pixels(center)
    radius=round(radius*config.PIXELS_PER_METRE)
    pygame.draw.circle(screen,config.LINE_COLOR,center,radius,config.LINE_WIDTH)

def draw_velocity_arrow(screen, position,velocity,color):
    '''	Draws an arrow pointing in the car’s direction of motion. A longer arrow represents a higher speed.'''
    vx,vy=velocity
    position=to_pixels(position)
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

def to_pixels(position):
    x, y = position
    return (
        round(x * config.PIXELS_PER_METRE),
        round(y * config.PIXELS_PER_METRE),
    )
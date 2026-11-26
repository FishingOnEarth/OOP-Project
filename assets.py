# Team members: Xuanchen Yu, Yiwen Ma, Jiaqi Sun
# Purpose: Loads and scales images for the simulation and its controls.

import pygame

def load_image(path,size):
    """Load an image and resize it to fit the requested bounds."""
    # A single scale factor preserves the original aspect ratio.
    image=pygame.image.load(path).convert_alpha()
    width,height=image.get_size()
    max_width, max_height = size
    scale=min(max_width/width,max_height/height)
    new_size = (max(1,round(width*scale)),max(1,round(height*scale)))
    
    
    return pygame.transform.smoothscale(image,new_size)
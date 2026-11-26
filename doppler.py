# Team members: Xuanchen Yu, Yiwen Ma, Jiaqi Sun
# Purpose: Calculates the frequency heard by the observer from the motion of both cars.

class Doppler:
    def __init__(self, soundspeed = 343):
        self.soundspeed = soundspeed

    def dopplermath(self, source, observer, frequency):
        xs, ys = source.position
        xo, yo = observer.position 

        dx = xo-xs
        dy = yo - ys

        d = (dx**2 + dy**2)**0.5

        if d == 0:
            raise ValueError 

        vsx, vsy = source.velocity()
        vox, voy = observer.velocity()

        vsr = (vsx*dx/d) + (vsy*dy/d)
        vor = (vox*dx/d) + (voy*dy/d)

        fo = frequency * ((self.soundspeed - vor)/(self.soundspeed - vsr))

        return fo

from car import Car
from doppler import Doppler

source = Car((0, 0), 20, (100, 0))
observer = Car((200, 0), 10)

doppler = Doppler()

print(doppler.dopplermath(source, observer, 440)) 
        







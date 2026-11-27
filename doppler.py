# Team members: Xuanchen Yu, Yiwen Ma, Jiaqi Sun
# Purpose: Calculates the frequency heard by the observer from the motion of both cars.

class Doppler:
    #calculate observed frequency
    def __init__(self, soundspeed = 343):
        #initialize the speed of sound to 343 m/s by default
        self.soundspeed = soundspeed

    def dopplermath(self, source, observer, frequency):
        #get the positions of the source and observer
        xs, ys = source.position
        xo, yo = observer.position 

        #Calculate horizontal and vertical distance from the source to the observer
        dx = xo-xs
        dy = yo - ys

        # Calculate the distance between the source and observer
        d = (dx**2 + dy**2)**0.5

        # Prevent division by zero when both objects occupy the same position
        if d == 0:
            raise ValueError 

        # Get the horizontal and vertical velocity components of both objects
        vsx, vsy = source.velocity()
        vox, voy = observer.velocity()

        # Calculate radial velacity of source and observer
        vsr = (vsx*dx/d) + (vsy*dy/d)
        vor = (vox*dx/d) + (voy*dy/d)

        # Calculate the observed frequency using the Doppler effect formula
        fo = frequency * ((self.soundspeed - vor)/(self.soundspeed - vsr))

        return fo

from car import Car

source = Car((0, 0), 20, (100, 0))
observer = Car((200, 0), 10)

doppler = Doppler()

print(doppler.dopplermath(source, observer, 440)) 
        







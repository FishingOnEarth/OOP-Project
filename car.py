# Team members: Xuanchen Yu, Yiwen Ma, Jiaqi Sun
# Purpose: Tracks each car along its path and calculates its velocity.

import math

class Car:
    #simulate movment of the car
    def __init__(self, start, speed, end=None):
        self.position = start
        self.speed = speed
        self.end = end
        #check if car is already at its end point
        self.finished = (end is not None and start == end)

    def velocity(self):
        #move left horizontally if no end point is specifies
        if self.end is None:
            return -self.speed, 0

        #Get current positions
        xi, yi = self.position
        xf, yf = self.end

        # Calculate horizontal and vertical displacement
        x = xf - xi
        y = yf - yi

        distance = math.dist(self.position, self.end)

        # Return zero velocity if the car has reached its destination
        if distance == 0:
            return 0, 0

        # Calculate horizontal and vertical velocity components
        vx = self.speed * x / distance
        vy = self.speed * y / distance

        return vx, vy

    def update(self, dt):
        # Stop updating the position once the destination is reached
        if self.finished:
            return

        if self.end is not None:
            distance_remaining = math.dist(self.position, self.end)

            # Prevent the car from overshooting its destination
            if self.speed * dt >= distance_remaining:
                self.position = self.end
                self.finished = True
                return

        # Get the velocity components and current position
        vx, vy = self.velocity()
        x, y = self.position

        # Update the position using velocity and elapsed time
        self.position = (x + vx * dt, y + vy * dt)

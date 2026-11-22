import math

class Car:
    def __init__(self, start, speed, end=None):
        self.position = start
        self.speed = speed
        self.end = end
        self.finished = (end is not None and start == end)

    def velocity(self):
        if self.end is None:
            return -self.speed, 0

        xi, yi = self.position
        xf, yf = self.end

        x = xf - xi
        y = yf - yi

        distance = math.dist(self.position, self.end)

        if distance == 0:
            return 0, 0

        vx = self.speed * x / distance
        vy = self.speed * y / distance

        return vx, vy

    def update(self, dt):
        if self.finished:
            return

        if self.end is not None:
            distance_remaining = math.dist(self.position, self.end)

            if self.speed * dt >= distance_remaining:
                self.position = self.end
                self.finished = True
                return

        vx, vy = self.velocity()
        x, y = self.position

        self.position = (x + vx * dt, y + vy * dt)

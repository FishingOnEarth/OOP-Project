class wavefront:
    def __init__(self,source_position,emmited_at):
        '''Saves where and when the source emmitted the wavefront'''
        self.source_position=source_position
        self.emmited_at=emmited_at

    def radius(self,simulation_time,sound_speed):
        '''calculates how far the wavefront has expanded by multiplying its age by the speed of sound'''
        age=simulation_time-self.emmited_at
        radius=age*sound_speed
        return radius


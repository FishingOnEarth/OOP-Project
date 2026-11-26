# Team members: Xuanchen Yu, Yiwen Ma, Jiaqi Sun
# Purpose: Stores where and when a wave was emitted and calculates its expanding radius.

class Wavefront:
    """Represent one expanding sound wave from a fixed emission point."""
    # Each emission has its own origin and time.
    def __init__(self,source_position,emmited_at):
        '''Saves where and when the source emmitted the wavefront'''
        # Keep the original position as the source moves on.
        self.source_position=source_position
        self.emmited_at=emmited_at

    def radius(self,simulation_time,sound_speed):
        '''calculates how far the wavefront has expanded by multiplying its age by the speed of sound'''
        # Only the time since this particular emission contributes to its radius.
        age=simulation_time-self.emmited_at
        radius=age*sound_speed
        return radius


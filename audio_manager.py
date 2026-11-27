# Team members: Xuanchen Yu, Yiwen Ma, Jiaqi Sun
# Purpose: Generates the tone heard by the observer and controls its pitch and volume.

#Audio control using pyo

import time
from pyo import Server, Sine, SigTo
import math

class AudioManager:
    #volume 0.1 smoother during rapid pitch (frequency) sweeps
    def __init__(self, base_freq: float = 440.0, volume: float = 0.1, glide_time: float = 0.02):
        self.base_freq = float(base_freq)
        self.target_volume = max(0.0, min(1.0, float(volume))) #clamp volume between 0 and 1
        self.min_freq = 20.0
        self.max_freq = 18000.0 #range of frequency where human can hear, although this simulation will probably not reach this far
        #just in case for the math (doppler equation)

        #boot audio server for lifetime, no need to re-start for every refresh
        self.server = Server().boot()

        #control signals for frequency and gain in volume
        '''smooth control for frequency using freq_sig to glide toward target frequency
        over glide_time instead of jumping straight to other frequency, which may create click and zippering sound'''
        self.freq_sig = SigTo(value= self.base_freq, time= glide_time, init= self.base_freq)
        
        #smooth control for volume and amplitude gliding over 15 ms
        self.amp_sig = SigTo(value= 0.0, time = 0.015, init= 0.0)

        #continuous sine oscillator and route to output
        self.tone = Sine(freq=self.freq_sig, mul= self.amp_sig).out() #generates sine wave, mul = amplitude multiplier, control volume
        self.is_running = False

    def clamp_freq(self, freq: float):
        #limit the frequency to be within audible range 20-18000 Hz
        if freq is None or not math.isfinite(freq) or freq <= 0:
            return self.freq_sig.value
        return max(self.min_freq, min(self.max_freq, float(freq)))

    def start(self):
        #turn on volume, update status is running
        if not self.is_running:
            self.server.start()
            self.is_running = True
        self.amp_sig.value = self.target_volume

    def set_frequency(self, freq: float):
        safe_freq = self.clamp_freq(freq)
        self.freq_sig.value = safe_freq

    def stop(self):
        '''only turn off the volume (temporarily), but the server is still booted and running'''
        self.amp_sig.value = 0.0


    def reset(self, base_freq: float | None = None):
        if base_freq is not None and math.isfinite(base_freq) and base_freq > 0:
            self.base_freq = float(base_freq) #check whether valid
        self.stop() #also temporarily mutes volume, still runs
        self.freq_sig.value = self.base_freq #resets

    def cleanup(self): #when simulation closes
        #shuts down the server only when exit the simulation
        self.amp_sig.value = 0.0
        if self.is_running:
            self.server.stop()
            self.is_running = False
        self.server.shutdown() 
        #no need to boot and shutdown every single time
#Audio control using pyo

#raise error for frequency beyond range of human hearing
import time
from pyo import Server, Sine, SigTo

class AudioManager:
    def __init__(self, base_freq: float = 440.0, volume: float = 0.1, glide_time: float = 0.02):
        self.base_freq = float(base_freq)
        self.target_volume = max(0.0, min(1.0, float(volume)))
        self.min_freq = 20.0
        self.max_freq = 18000.0 #range of frequency where human can hear, although this simulation will probably not reach this far
        #just in case for the math

        #boot audio server
        self.server = Server().boot()

        #control signals for frequency and gain in volume
        self.freq_sig = SigTo(value= self.base_freq, time= glide_time, init= self.base_freq)
        self.amp_sig = SigTo(value= 0.0, time = 0.015, init= 0.0)

        #continuous sine oscillator and route to output
        self.tone = Sine(freq=self.freq_sig, mul= self.amp_sig).out()
        self.is_running = False

    def clamp_freq(self, freq: float):
        if freq is None or not math.isfinite(freq) or freq <= 0:
            return self.freq_sig.value
        return max(self.min_freq, min(self.max_freq, float(freq)))

    def start(self):
        if not self.is_running:
            self.server.start()
            self.is_running = True
        self.amp_sig.value = self.target_volume

    def set_frequncy(self, freq: float):
        safe_freq = self.clamp_freq(freq)
        self.freq_sig.value = safe_freq

    def stop(self):
        self.amp_sig.value = 0.0

    def reset(self, base_freq: float | None = None):
        if base_freq is not None and math.isfinite(base_freq) and base_freq > 0:
            self.base_freq = float(base_freq)
        self.stop()
        self.freq_sig.value = self.base_freq

    def cleanup(self):
        self.amp_sig.value = 0.0
        if self.is_running:
            self.server.stop()
            self.is_running = False
        self.server.shutdown()
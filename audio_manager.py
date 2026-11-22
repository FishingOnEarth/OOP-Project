#Audio control using pyo

#raise error for frequency beyond range of human hearing

import time
from pyo import Server, Sine

server = Server().boot()
server.start()

# Keep mul modest (0.1) so pitch changes stay comfortable on the ears
tone = Sine(freq=440, mul=0.1).out()
time.sleep(2.0)

tone.freq = 550
time.sleep(2.0)

server.stop()
server.shutdown()
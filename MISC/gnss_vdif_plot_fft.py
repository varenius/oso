import numpy as np
import matplotlib.pyplot as plt

inf = "gsa05_o8_0055.102731.vdif.bbc01.ascii"

data = []
for line in open(inf):
    data.append(line.strip())
data = np.array(data)

ps = np.abs(np.fft.fft(data))**2
sample_rate = 128e6
time_step = 1.0/sample_rate
freqs = np.fft.fftfreq(data.size, time_step)

idx = np.argsort(freqs)

plt.plot(freqs[idx], ps[idx])
plt.show()

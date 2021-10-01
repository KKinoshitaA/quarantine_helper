import serial
import matplotlib.pyplot as plt
import numpy as np

SAMPLES = 512
FFT_SAMPLES = int(SAMPLES/2)

fig, ax = plt.subplots()

arr = [0] * FFT_SAMPLES
x = range(0, FFT_SAMPLES)

ser = serial.Serial('/dev/tty.usbmodem1141301', 115200, timeout=None)

while True:
    for i in range(0, FFT_SAMPLES):
        val = float(ser.readline().decode().replace('\r', '').replace('\n', ''))
        arr[i] = val

    ax.set_xlim(0, FFT_SAMPLES)
    ax.set_ylim(0, 2000)
    line, = ax.plot(x, arr, color='blue')
    plt.pause(0.1)
    line.remove()

ser.close()
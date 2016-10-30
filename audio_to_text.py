import scipy.io.wavfile
import math
import colorsys
from PIL import Image

def hsv2rgb(h,s,v):
    return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

filename = 'new'

FSample, samples = scipy.io.wavfile.read(filename + '.wav')

trimmer = []
for x in range(0, len(samples)):
    if x % 5 == 0:
        trimmer.append(samples[x])

formatted = []
for x in range(0, len(trimmer)):
    if x % 3 == 0:
        formatted.append([])
    v = float(trimmer[x])
    v += 16384
    v /= 16384
    if x % 3 == 0:
        v *= 360
        v = int(v)
    else:
        v *= 100
        v = int(v)
        v %= 100
        v = float(v)
        v /= 100
    formatted[len(formatted) - 1].append(v)

while len(formatted[len(formatted) - 1]) < 3:
    formatted[len(formatted) - 1].append(0)

dim = int(math.floor(math.sqrt(len(formatted))))

img = Image.new('RGB', (dim, dim), 'black')
pixels = img.load()
for x in range(0, dim):
    for y in range(0, dim):
        val = hsv2rgb(formatted[x * dim + y][0], formatted[x * dim + y][1], formatted[x * dim + y][2])
        pixels[x, y] = val

img.resize((900, 900), Image.NEAREST).save(filename + '.png')

print "Complete"

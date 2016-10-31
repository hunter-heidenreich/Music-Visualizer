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

mmax = long(max(samples))
mmin = long(min(samples))
print mmax
print mmin
rrange = long(mmax - mmin)
print rrange
formatted = []
for x in range(0, len(trimmer)):
    if x % 3 == 0:
        formatted.append([])
    v = float(trimmer[x])
    v -= mmin
    v = long(v)
    v %= 10000
    v = float(v) / 10000
    v *- 0.6
    #v /= rrange
    print v
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

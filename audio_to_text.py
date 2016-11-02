import pyaudio
import wave
import numpy as np
from math import*
import random

def decider(val, highest):
    return highest * ((sin(float(val) / pi) ** 2) + (cos(highest / (0.000001 + pi * float(val)))) ** 2)


imgname = raw_input("Enter the name you want to save the image as (no spaces): ")
wf = wave.open(imgname + '.wav', 'rb')

f = open(imgname + '.txt','w+')
chunk = 1024

p=pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

data = wf.readframes(chunk)
while data != '':
    stream.write(data)
    data = np.fromstring(data, dtype=np.int16)
    f.write(str(data) + "\n")
    print(data)
    data = wf.readframes(chunk)
f.close()
stream.close()
p.terminate()

raw = open(imgname + ".txt","r+")

processed = []
rgb_arr = []
for line in raw:
	line = line.replace("...","").replace("\n","").replace(" ","").replace(",","").replace("[","").replace("]","").replace("-","")
	processed.append(int(line))
highest = max(processed);
for i in range(0, len(processed)):
	processed[i] = highest % processed[i]

for val in processed:
	if val == 0L:
		processed.remove(val)
	else:
		l = str(val)
		n = 3
		ex = ([l[i:i+n] for i in range(0, len(l), n)])

		rgb = []
		for color in ex:
			if len(rgb) < 3:
				rgb.append((int(decider(color, highest))%127))
			else:
				rgb_arr.append(rgb)
				rgb = []
				rgb.append(int(decider(color, highest))%127)

dimen = int(sqrt(len(rgb_arr))) // 2

from PIL import Image
img = Image.new( 'RGB', (dimen, dimen), (0,0,0))
pixels = img.load()
mixture_rgb = (rgb_arr[50][0], rgb_arr[50][1], rgb_arr[50][2])
for x in range(0,((dimen)**2)):
    pixels[x // dimen, x % dimen] = (rgb_arr[x][0] + mixture_rgb[0], rgb_arr[x][1] + mixture_rgb[1], rgb_arr[x][2] + mixture_rgb[2])

imgname += ".png"
img.resize((800, 800), Image.NEAREST).save(imgname)
print "The file has been produced in the same folder as this script under the name " + imgname

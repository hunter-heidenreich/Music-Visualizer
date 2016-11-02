import pyaudio
import wave
import numpy as np
from math import*
import random
from PIL import Image
import os

def decider(val, highest):
    return highest * sqrt((sin(float(val) / pi) ** 2) + (cos(highest / (0.000001 + pi * float(val)))) ** 2)


def sort_type(arr, type_of_sort):
    return {
        'color': sort_by_colors,
        'red': sort_by_red,
        'green': sort_by_green,
        'blue': sort_by_blue
    }[type_of_sort](arr)


def sort_by_colors(arr):
    for x in range(0, len(arr)):
        for y in range(x + 1, len(arr)):
            if(arr[x] > arr[y]):
                temp = arr[x]
                arr[x] = arr[y]
                arr[y] = temp
    return arr


def sort_by_red(arr):
    for x in range(0, len(arr)):
        for y in range(x + 1, len(arr)):
            if(arr[x][0] > arr[y][0]):
                temp = arr[x]
                arr[x] = arr[y]
                arr[y] = temp
    return arr


def sort_by_green(arr):
    for x in range(0, len(arr)):
        for y in range(x + 1, len(arr)):
            if(arr[x][1] > arr[y][1]):
                temp = arr[x]
                arr[x] = arr[y]
                arr[y] = temp
    return arr


def sort_by_blue(arr):
    for x in range(0, len(arr)):
        for y in range(x + 1, len(arr)):
            if(arr[x][2] > arr[y][2]):
                temp = arr[x]
                arr[x] = arr[y]
                arr[y] = temp
    return arr


def extract_sound_data(sound_file):
    print 'EXTRACTING ' + sound_file + '.wav'
    wf = wave.open(sound_file + '.wav', 'rb')

    f = open(sound_file + '.txt','w+')
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
        data = wf.readframes(chunk)
    f.close()
    stream.close()
    p.terminate()


def process_data_file(text_file):
    print 'PROCESSING ' + text_file + '.wav'
    raw = open(text_file + ".txt","r+")
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
    				rgb.append((int(decider(color, highest))%255))
    			else:
    				rgb_arr.append(rgb)
    				rgb = []
    				rgb.append(int(decider(color, highest))%255)
    os.remove(text_file + '.txt')
    return rgb_arr


def draw_image(rgb_arr, name, file_ext, sorting='color', final_size=(2480, 2480)):
    print 'DRAWING...'
    dimen = int(sqrt(len(rgb_arr)))
    img = Image.new('RGB', (dimen, dimen), 'black')
    pixels = img.load()
    mixture_rgb = (255, 255, 255)
    rgb_arr = sort_type(rgb_arr, sorting)
    for x in range(0, (dimen ** 2)):
        pixels[x // dimen, x % dimen] = ((rgb_arr[x][0] + mixture_rgb[0]) // 2, (rgb_arr[x][1] + mixture_rgb[1]) // 2, (rgb_arr[x][2] + mixture_rgb[2]) // 2)
    img.resize(final_size, Image.NEAREST).save(name + '-' + sorting + '.' + file_ext)
    print 'EXPORTED ' + name + '-' + sorting + '.' + file_ext


if __name__ == '__main__':
    sort_types = ['color', 'red', 'green', 'blue']
    name = raw_input("Enter the name of your .wav file (no extension, please): ")
    extract_sound_data(name)
    rgb_arr = process_data_file(name)
    for sort in sort_types:
        draw_image(rgb_arr, name, 'png', sorting=sort)

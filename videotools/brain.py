from sys import argv,exit,stderr
import barheight
import processor
import subprocess
from scipy.io import wavfile as wavf

help_message = "Usage: python3 brain.py <audio file> [ -r|f|b|BC|BG|E|BO|BOC ]\n" + \
               "\t-r (resolution)\t\t\tnext two args must be positive ints, width then height (default: 1920 x 1080)\n" + \
               "\t-f (framerate)\t\t\tnext arg must be a positive int (default: 24)\n" + \
               "\t-b (bar count)\t\t\tnext arg must be a positive int (default: 100)\n" + \
               "\t-BC (RGB bar color)\t\tnext three args must be ints from 0-255 (inc, inc) (default: (0, 0, 255))\n" + \
               "\t-BG (RBG background color)\tnext three args must be ints from 0-255 (inc, inc) (default: (0, 0, 0))\n" + \
               "\t-BO (border width)\t\tnext arg must be a float from 0-1 (default: .1)\n" + \
               "\t-BOC (border color)\t\tnext three args must be ints from 0-255 (inc, inc) (default: (255, 255, 255))"


video_width, video_height = 1920, 1080
framerate = 24
bar_count = 100
bar_color_RGB = (0, 0, 255)
background_color_RGB = (0, 0, 0)
empty_space = .15
border_width = .1
border_color_RGB = (255, 255, 255)
wavfile = None
name = ''


i = 1
while i < len(argv):
    if i == 1:
        if argv[i][-3:] != 'wav':
            stderr.write('The first argument must be the name of a wav file, support for other audio types is coming soon!\n')
            exit(1)
        else:
            wavfile = argv[i]
            name = argv[1][:-4]
            i += 1
    if i >= len(argv):
        break
    
    try:
        if argv[i] == '-r':
            video_width = int(argv[i+1])
            video_height = int(argv[i+2])
            i += 3
            continue
        elif argv[i] == '-f':
            framerate = int(argv[i+1])
            print('f')
            i += 2
            continue
        elif argv[i] == '-b':
            bar_count = int(argv[i+1])
            print('b', argv[i+2])
            i += 2
            continue
        elif argv[i] == '-BC':
            bar_color_RGB = (int(argv[i+1]), int(argv[i+2]), int(argv[i+3]))
            print('BC')
            i += 4
            continue
        elif argv[i] == '-BG':
            background_color_RGB = (int(argv[i+1]), int(argv[i+2]), int(argv[i+3]))
            print('BG')
            i += 4
            continue
        elif argv[i] == '-BO':
            border_width = float(argv[i+1])
            print('BO')
            i += 2
            continue
        elif argv[i] == '-BOC':
            border_color_RGB = (int(argv[i+1]), int(argv[i+2]), int(argv[i+3]))
            print('BOC')
            i += 4
        else:
            raise ValueError
    except:
        print(help_message)
        exit(1)

try:
    wavfile = wavf.read(wavfile)
except:
    stderr.write('Error opening audio file\n')
    exit(1)
    
generator = barheight.VideoProcessor(video_width, video_height, framerate, bar_count, wavfile)
video_bar_height = generator.decompose()

renderer = processor.VideoCreator(video_width, video_height, framerate, bar_count, name)
renderer.create_video(video_bar_height, border_width, border_color_RGB, empty_space, background_color_RGB, bar_color_RGB)

subprocess.run(args=['rm', name + '.mp4'])
subprocess.run(args=' '.join(['ffmpeg -i', '_' + name + '.mp4', \
                              '-i', argv[1], \
                              '-c:v copy -c:a aac', \
                              name + '.mp4']), shell=True)
subprocess.run(args=['rm', '_' + name + '.mp4'])

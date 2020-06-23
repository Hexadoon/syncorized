from sys import argv,exit,stderr
import barheight
import processor
import subprocess
import cv2
from scipy.io import wavfile as wavf
import random
import os 
import ffmpeg 

help_message = "Usage: python3 brain.py <audio file> [ -r|f|b|BC|BG|E|BO|BOC|p|h ]\n" + \
               "\t-r (resolution)\t\t\tnext two args must be positive ints, width then height (default: 1920 x 1080)\n" + \
               "\t-f (framerate)\t\t\tnext arg must be a positive int (default: 24)\n" + \
               "\t-b (bar count)\t\t\tnext arg must be a positive int (default: 100)\n" + \
               "\t-BC (RGB bar color)\t\tnext three args must be ints from 0-255 (inc, inc) (default: (0, 0, 255))\n" + \
               "\t-BG (RBG background color)\tnext three args must be ints from 0-255 (inc, inc) (default: (0, 0, 0))\n" + \
               "\t-BO (border width)\t\tnext arg must be a float from 0-1 (default: .1)\n" + \
               "\t-BOC (border color)\t\tnext three args must be ints from 0-255 (inc, inc) (default: (255, 255, 255))\n" + \
               "\t-p (preview mode)\t\tinstead of reading a wav file, running the program will produce a single image with the given specs\n" + \
               "\t-h (help mode)\t\t\tprints this message and terminates"

if '-h' in argv:
    print(help_message)
    exit(0)

# variables considered, these are the defaults if they aren't specified
video_width, video_height = 1920, 1080
framerate = 24
bar_count = 100
bar_color_RGB = (0, 0, 255)
background_color_RGB = (0, 0, 0)
empty_space = .15 # not changeable, didn't think it'd make sense to be able to 
border_width = .1
border_color_RGB = (255, 255, 255)
wavfile = None
preview_mode = False

# path represents the whole filepath, including the name of the file
path = ''

# this loop just reads the command line arguments 
i = 1
while i < len(argv):
    if i == 1:
        # wavfile must be the first argument if -p isn't specified
        if argv[i][-3:] != 'wav' and ('-p' not in argv):
            stderr.write('The first argument must be the name of a wav file, support for other audio types is coming soon!\n')
            exit(1)
        elif ('-p' not in argv):
            wavfile = argv[i]

            # if there is no /, then it must be in this directory
            path = argv[1][:-4] 
            if '/' not in path: 
                path = os.getcwd() + '/' + path

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
            i += 2
            continue
        elif argv[i] == '-b':
            bar_count = int(argv[i+1])
            i += 2
            continue
        elif argv[i] == '-BC':
            bar_color_RGB = (int(argv[i+1]), int(argv[i+2]), int(argv[i+3]))
            i += 4
            continue
        elif argv[i] == '-BG':
            background_color_RGB = (int(argv[i+1]), int(argv[i+2]), int(argv[i+3]))
            i += 4
            continue
        elif argv[i] == '-BO':
            border_width = float(argv[i+1])
            i += 2
            continue
        elif argv[i] == '-BOC':
            border_color_RGB = (int(argv[i+1]), int(argv[i+2]), int(argv[i+3]))
            i += 4
        elif argv[i] == '-p':
            preview_mode = True
            i += 1
        else:
            raise ValueError
    except:
        print(help_message)
        exit(1)

try:
    print(wavfile)
    if wavfile is not None:
        wavfile = wavf.read(wavfile)
except:
    stderr.write('Error opening audio file\n')
    exit(1)

# if -p is called, instead of calling the whole video, it only calls renderer.process_frame and saves that image
if preview_mode is True:
    random.seed(225511) # seeded for consistency 
    preview_bars = []

    # to capture the general shape of the waveform, the bars are generated with random deviations of a 1/x curce
    for i in range(bar_count):
        preview_bars.append(random.random()/(i+1))
    
    # this is pretty ugly ngl but it creates the preview frame
    renderer = processor.VideoCreator(video_width, video_height, framerate, bar_count, 'preview')
    preview_frame = renderer.process_frame(preview_bars, border_width, border_color_RGB[::-1], \
                    empty_space, background_color_RGB[::-1], bar_color_RGB[::-1], video_width//bar_count, \
                    (video_width % bar_count)//2, video_height/max(preview_bars))

    cv2.imwrite("preview.png", preview_frame)

# the actual video generation comes in two parts, the first is computing the heights of the bars, the second is 
# turning the bar heights into a video
else:
    # calculate the heights of the bars
    generator = barheight.VideoProcessor(video_width, video_height, framerate, bar_count, wavfile)
    video_bar_height = generator.decompose()

    # convert the heights into video (note: no audio here yet, and temporarily this saves a file called '_<name>.mp4' which is deleted
    renderer = processor.VideoCreator(video_width, video_height, framerate, bar_count, path)
    renderer.create_video(video_bar_height, border_width, border_color_RGB, empty_space, background_color_RGB, bar_color_RGB)
    
    # remove the file if it exists already
    if os.path.exists(path + '.mp4'):
        os.remove(path + '.mp4')
    
    # merge the video and audio by parsing the individual streams and outputting them together into one file
    video_input = ffmpeg.input(path + '_.mp4').video
    audio_input = ffmpeg.input(argv[1]).audio
    ffmpeg.output(audio_input, video_input, path + '.mp4').run()

    # remove the temporary file
    os.remove(path + '_.mp4')

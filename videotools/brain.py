from sys import argv,exit,stderr
import barheight
import processor
import cv2
from scipy.io import wavfile as wavf
import random
import os 
import ffmpeg 

help_message = "Usage: python3 brain.py <audio file> [ -r|f|b|l|BC|BG|BO|BOC|p|h ]\n" + \
               "\t-r (resolution)\t\t\tnext two args must be positive ints, width then height (default: 1920 x 1080)\n" + \
               "\t-f (framerate)\t\t\tnext arg must be a positive int (default: 24)\n" + \
               "\t-b (bar count)\t\t\tnext arg must be a positive int (default: 100)\n" + \
               "\t-BC (RGB bar color)\t\tnext three args must be ints from 0-255 (inc, inc) (default: (0, 0, 255))\n" + \
               "\t-BG (RGB background color)\tnext three args must be ints from 0-255 (inc, inc) (default: (0, 0, 0))\n" + \
               "\t\t\t\t\tOR the path of an image to be used as the background and the type of fit\n" + \
               "\t-BO (border width)\t\tnext arg must be a float from 0-1 (default: .1)\n" + \
               "\t-BOC (border color)\t\tnext three args must be ints from 0-255 (inc, inc) (default: (255, 255, 255))\n" + \
               "\t-l (layout)\t\t\tnext arg is the layout number, 0 is line, 1 is circle (default: 0)\n" + \
               "\t-p (preview mode)\t\tinstead of reading a wav file, running the program will produce a single image with the given specs\n" + \
               "\t-h (help mode)\t\t\tprints this message and terminates"

if '-h' in argv:
    print(help_message)
    exit(0)

# variables considered, these are the defaults if they aren't specified
video_width, video_height = 1920, 1080
framerate = 24
bar_count = 100
bar_layout = 0
bar_color = (255, 0, 0)
background = (0, 0, 0)
empty_space = .15 # not changeable, didn't think it'd make sense to be able to 
border_width = .1
border_color = (255, 255, 255)
fill_type = 0
wavfile = None
preview_mode = False
bg_is_image = False
clean_wav = False

# path represents the whole filepath, including the name of the file
path = ''

# this loop just reads the command line arguments 
i = 1
while i < len(argv):
    if i == 1:
        # wavfile must be the first argument if -p isn't specified
        if not (argv[i][-3:] == 'wav' or argv[i][-3:] == 'mp3') and ('-p' not in argv):
            stderr.write('The first argument must be the name of a wav or mp3 file\n')
            exit(1)
        
        # make the conversion if an mp3 is given (drops a free wav in your folder too, may want to delete it though)
        if argv[i][-3:] == 'mp3':
            if os.path.exists(argv[1][:-3] + 'wav'):
                os.remove(argv[1][:-3] + 'wav')

            ffmpeg.output(ffmpeg.input(argv[1]).audio, filename=argv[1][:-3]+'wav', f='wav').run()
            argv[1] = argv[1][:-3]+'wav'
            clean_wav = True
        if ('-p' not in argv):
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
            bar_color = (int(argv[i+3]), int(argv[i+2]), int(argv[i+1]))
            i += 4
            continue
        elif argv[i] == '-BG':
            if i+3 >= len(argv) or '-' in argv[i+3]:
                background = argv[i+1]
                fill_type = int(argv[i+2])
                bg_is_image = True
                i += 3
            else:
                background = (int(argv[i+3]), int(argv[i+2]), int(argv[i+1]))
                bg_is_image = False
                i += 4
            continue
        elif argv[i] == '-BO':
            border_width = float(argv[i+1])
            i += 2
            continue
        elif argv[i] == '-BOC':
            border_color = (int(argv[i+3]), int(argv[i+2]), int(argv[i+1]))
            i += 4
        elif argv[i] == '-l':
            bar_layout = int(argv[i+1])
            i += 2
            continue
        elif argv[i] == '-p':
            preview_mode = True
            i += 1
            continue
        else:
            raise ValueError
    except:
        print(help_message)
        exit(1)

try:
    if wavfile is not None:
        wavfile = wavf.read(wavfile)
except:
    stderr.write('Error opening audio file\n')
    exit(1)

renderer = processor.VideoCreator(video_width, video_height, framerate, path, bar_count, bar_layout, border_width, \
                                  empty_space, bar_color, border_color, background, bg_is_image, fill_type)

# if -p is called, instead of calling the whole video, it only calls renderer.process_frame and saves that image
if preview_mode is True:
    random.seed(225511) # seeded for consistency 
    preview_bars = []

    # to capture the general shape of the waveform, the bars are generated with random deviations of a 1/x curce
    for i in range(bar_count):
        preview_bars.append(random.random()/(i+1))
    
    preview_frame = renderer.process_frame(preview_bars, video_height/max(preview_bars) * (.5 if bar_layout != 0 else 1))

    cv2.imwrite("preview.png", preview_frame)

# the actual video generation comes in two parts, the first is computing the heights of the bars, the second is 
# turning the bar heights into a video
else:
    if not os.path.exists('chunks'):
        os.mkdir('chunks')

    # calculate the heights of the bars
    generator = barheight.VideoProcessor(video_width, video_height, framerate, bar_count, wavfile)
    video_bar_height = generator.decompose()

    # convert the heights into video (note: no audio here yet, and temporarily this saves a file called '_<name>.mp4' which is deleted
    renderer.create_video(video_bar_height)
    
    # remove the file if it exists already
    if os.path.exists(path + '.mp4'):
        os.remove(path + '.mp4')
    
    # merges all the chunks into one file (chunkorder is a list of the names of chunks)
    ffmpeg.input('chunkorder.txt', format='concat', safe=0).output(path + '_.mp4', c='copy').overwrite_output().run()
    
    # merge the video and audio by parsing the individual streams and outputting them together into one file
    video_input = ffmpeg.input(path + '_.mp4').video
    audio_input = ffmpeg.input(argv[1]).audio
    ffmpeg.output(audio_input, video_input, path + '.mp4').overwrite_output().run()
        
            
    # remove the temporary file
    if os.path.exists(path + '_.mp4'):
        os.remove(path + '_.mp4')
    
    remover = open('chunkorder.txt', 'r')
    # I'm just flexing here, this removes all the files listed in chunkorder
    [os.remove(chunk[6:-2]) if os.path.exists(chunk[6:-2]) else 0 for chunk in remover.readlines()]
    os.remove('chunkorder.txt')
    os.rmdir('chunks')
    if clean_wav:
        os.remove(path + '.wav')
    remover.close()

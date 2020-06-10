import barheight
from sys import argv,stderr,exit
from scipy.io import wavfile as wavf
import numpy as np
import cv2

video_width = 1920 
video_height = 1080
framerate = 24
blocks = 100

# CURRENTLY UNUSED AND ALMOST EXACTLY THE SAME AS THE BODY OF THE FOR LOOP BELOW 
def process_frame(frame_data, border_width, border_BGR, empty_space, background_BGR, bar_BGR, bar_width, scale):
    ''' turns the data for a frame into a np array representing the frame '''
    
    # instantiate the frame as an ndarray with shape (w, h, 3), the last being the background color 
    curr_frame = np.full((video_height, video_width, 3), background_BGR, dtype=np.uint8)

    for x, bar_height in enumerate(frame_data): 
        # the border is formed by drawing a rectangle of border_color under a rectangle of bar_color
        corner_DL = (int(bar_width*(x + border_width + empty_space/2)), \
                     int(video_height//2 + scale*bar_height))

       
        corner_UR = (int(bar_width*(x + 1 - empty_space/2 - border_width)), \
                     int(video_height//2 - scale*bar_height))


        border_size = int(border_width*bar_width) 
        
        
        border_BGR = (int(border_BGR[0]), int(border_BGR[1]), int(border_BGR[2]))
        bar_BGR = (int(bar_BGR[0]), int(bar_BGR[1]), int(bar_BGR[2]))
        cv2.rectangle(curr_frame, corner_DL, corner_UR, border_BGR, 2*border_size)
        cv2.rectangle(curr_frame, corner_DL, corner_UR, tuple(bar_BGR), -1)
    
    return curr_frame

def create_video(border_width, border_color_RGB, empty_space, background_color_RGB, bar_color_RGB):
    ''' takes in a bunch of specs and writes the video '''
    if len(argv) != 2:
        stderr.write("Incorrect args\n")
        exit(1)
    
    # opencv inexplicably uses BGR so this is unfortunately necessary
    border_BGR = border_color_RGB[::-1]
    background_BGR = background_color_RGB[::-1]
    bar_BGR = bar_color_RGB[::-1]

    # slightly jank way of checking if the correct filetype is given
    # literally searches for the last '.' in the string, checks if following
    # text is 'wav'
    # at least I don't need to import regexes
    filetype = argv[1][-argv[1][::-1].index('.'):] 
    
    if filetype == 'wav':
        
        # read the wav file
        wavfile = 0
        try:
            wavfile = wavf.read(argv[1])
        except:
            stderr.write("Error opening file\n")
            exit(3)
        
        # create the video controller with the right specs
        controller = barheight.VideoController(video_width, video_height, framerate, blocks, wavfile)
        
        # get the bar heights
        video_bar_height = controller.decompose()
        scale = video_height/np.amax(video_bar_height)        
        
        # set up the video generator
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter('./test.mp4', fourcc, framerate, (video_width, video_height))

        # finally, generate the video from the frames
        bar_width = video_width//blocks

        #process_video = np.vectorize(process_frame, signature='(m),(),(3),(),(3),(3),(),()->(h,w,3)')
        #video_frames = process_video(video_bar_height, border_width, border_BGR, empty_space, \
        #                             background_BGR, bar_BGR, bar_width, scale)
        
        started = False

        for frame in video_bar_height:
            # instantiate the frame as an ndarray with shape (w, h, 3), the last being the background color 
            curr_frame = np.full((video_height, video_width, 3), background_BGR, dtype=np.uint8)
            
            for x, bar_height in enumerate(frame):
                # this is so that when there's silence at the beginning of an audio file, it won't draw 
                # the borders of the blocks while they aren't moving, it's just courtesy code
                if started == False:
                    if bar_height == 0:
                        continue
                    else:
                        started = True
                        break
                
                # the border is formed by drawing a rectangle of border_color under a rectangle of bar_color
                corner_DL = (int(bar_width*(x + border_width + empty_space/2)), \
                             int(video_height//2 + scale*bar_height))
                #             int(min((video_height + bar_height//1000)//2, video_height)))
               
                corner_UR = (int(bar_width*(x + 1 - empty_space/2 - border_width)), \
                             int(video_height//2 - scale*bar_height))
                #             int(max((video_height - bar_height//1000)//2, 0)))

                border_size = int(border_width*bar_width) 
                #if count == 0:
                #    print(border_size)
                #    count += 1
                
                #print(border_BGR, type(border_BGR))
                cv2.rectangle(curr_frame, corner_DL, corner_UR, border_BGR, 2*border_size)
                cv2.rectangle(curr_frame, corner_DL, corner_UR, bar_BGR, -1)
                #break
            #break
            video.write(curr_frame)
        video.release()
        
    else:
        # temporary, don't worry, I'll add conversions dw
        stderr.write("Please use a .wav\n")
        exit(2)

if __name__ == '__main__':
    create_video(.1, (255, 255, 255), .15, (50, 50, 50), (255, 0, 255))

import barheight
from sys import argv,stderr,exit
import numpy as np
import cv2
from tqdm import tqdm

class VideoCreator:
    
    def __init__(self, width, height, fps, bars, song):
        self.video_width = width 
        self.video_height = height
        self.framerate = fps
        self.blocks = bars
        self.wavfile = song
    
    
    def process_frame(self, frame_data, border_width, border_BGR, empty_space, \
                      background_BGR, bar_BGR, bar_width, end_spacing, scale):
        ''' turns the data for a frame into a np array representing the frame '''
        
        # instantiate the frame as an ndarray with shape (w, h, 3), the last being the background color 
        curr_frame = np.full((self.video_height, self.video_width, 3), background_BGR, dtype=np.uint8)

        for x, bar_height in enumerate(frame_data): 
            # the border is formed by drawing a rectangle of border_color under a rectangle of bar_color
            corner_DL = (int(bar_width*(x + border_width + empty_space/2)) + end_spacing, \
                         int(self.video_height//2 + scale*bar_height))

           
            corner_UR = (int(bar_width*(x + 1 - empty_space/2 - border_width)) + end_spacing, \
                         int(self.video_height//2 - scale*bar_height))


            border_size = int(border_width*bar_width) 
            
            
            border_BGR = (int(border_BGR[0]), int(border_BGR[1]), int(border_BGR[2]))
            bar_BGR = (int(bar_BGR[0]), int(bar_BGR[1]), int(bar_BGR[2]))
            cv2.rectangle(curr_frame, corner_DL, corner_UR, border_BGR, 2*border_size)
            cv2.rectangle(curr_frame, corner_DL, corner_UR, bar_BGR, -1)
        
        return curr_frame

    def create_video(self, video_bar_height, border_width, border_color_RGB, empty_space, background_color_RGB, bar_color_RGB):
        ''' takes in a bunch of specs and writes the video '''
        
        # opencv inexplicably uses BGR so this is unfortunately necessary
        border_BGR = border_color_RGB[::-1]
        background_BGR = background_color_RGB[::-1]
        bar_BGR = bar_color_RGB[::-1]

        # keep the bars in the bounds of the screen
        scale = self.video_height/np.amax(video_bar_height)        
        
        # set up the video generator
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter('./test.mp4', fourcc, self.framerate, (self.video_width, self.video_height))

        # finally, generate the video from the frames
        bar_width = self.video_width//self.blocks

        # to account for rounding errors in the amount of blocks
        end_spacing = (self.video_width % self.blocks) // 2
        for frame in tqdm(video_bar_height, desc='writing video'):
            curr_frame = self.process_frame(frame, border_width, border_BGR, empty_space, background_BGR, \
                          bar_BGR, bar_width, end_spacing, scale)
            
            video.write(curr_frame)
        video.release()

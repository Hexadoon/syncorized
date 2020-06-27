import barheight
from sys import argv,stderr,exit
from math import sqrt
import os
import numpy as np
import cv2
import threading

class VideoCreator:
    
    def __init__(self, width, height, fps, bars, path):
        self.video_width = width 
        self.video_height = height
        self.framerate = fps
        self.blocks = bars
        self.title = path + '_.mp4'
    
    
    def process_frame(self, frame_data, border_width, border_BGR, empty_space, \
                      background_BGR, bar_BGR, bar_width, end_spacing, scale):
        ''' turns the data for a frame into a np array representing the frame '''
        
        # instantiate the frame as an ndarray with shape (w, h, 3), the last being the background color 
        curr_frame = np.full((self.video_height, self.video_width, 3), background_BGR, dtype=np.uint8)

        for x, bar_height in enumerate(frame_data): 
            # calculates the corners of the current bar
            corner_DL = (int(bar_width*(x + border_width + empty_space/2)) + end_spacing, \
                         int(self.video_height//2 + scale*bar_height))
           
            corner_UR = (int(bar_width*(x + 1 - empty_space/2 - border_width)) + end_spacing, \
                         int(self.video_height//2 - scale*bar_height))

            # cacluates the pixel width of the border
            border_size = int(border_width*bar_width) 
            
            # cleans the input colors (everything *must* be an integer)
            border_BGR = (int(border_BGR[0]), int(border_BGR[1]), int(border_BGR[2]))
            bar_BGR = (int(bar_BGR[0]), int(bar_BGR[1]), int(bar_BGR[2]))
            
            cv2.rectangle(curr_frame, corner_DL, corner_UR, border_BGR, 2*border_size)
            cv2.rectangle(curr_frame, corner_DL, corner_UR, bar_BGR, -1)
        
        return curr_frame
    
    def process_chunk(self, video_chunk, border_width, border_BGR, empty_space, \
                      background_BGR, bar_BGR, bar_width, end_spacing, scale, count):
        ''' takes a portion of the video (in the form of an np array of shape (length, bar_count) 
            then processes the portion into its own video and writes it (used to thread) '''
        # setup for the videowriter for this chunk
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
        video = cv2.VideoWriter(os.getcwd() + '/chunks/chunk' + str(count) + '.mp4', fourcc, self.framerate, \
                                (self.video_width, self.video_height))
        
        for frame in video_chunk:
            # simply run process frame and write to the video
            vframe = self.process_frame(frame, border_width, border_BGR, empty_space, background_BGR, bar_BGR, bar_width, end_spacing, scale)
            video.write(vframe)

        video.release()
        print(count, 'done')

    def create_video(self, video_bar_height, border_width, border_color_RGB, empty_space, background_color_RGB, bar_color_RGB):
        ''' takes in a bunch of specs and writes the video '''
        
        # opencv inexplicably uses BGR so this is unfortunately necessary
        border_BGR = border_color_RGB[::-1]
        background_BGR = background_color_RGB[::-1]
        bar_BGR = bar_color_RGB[::-1]

        # keep the bars in the bounds of the screen
        scale = self.video_height/np.amax(video_bar_height)        
        
        # finally, generate the video from the frames
        bar_width = self.video_width//self.blocks

        # to account for rounding errors in the amount of blocks
        end_spacing = (self.video_width % self.blocks) // 2
        print('writing chunks')
        
        # filelist just keeps track of the chunks, important for eventually merging
        filelist = open('chunkorder.txt', 'w') 

        # breaks up the video so there a roughly equal amount of threads and frames per thread
        # ideally I bump the number, as merging is *significantly* faster than writing the video
        # but then I run the risk of using all your memory and tanking the computer/queue up too many
        # threads and get no speedup at all, this just feels like a good balance
        step = int(sqrt(video_bar_height.shape[0]))
        threads = []
        for i in range(video_bar_height.shape[0]//step+1):
            # keep track of this file
            filelist.write("file './chunks/chunk" + str(i) + ".mp4'\n")
            
            # set up the thread
            curr_thread = threading.Thread(target=self.process_chunk, args= \
                    (video_bar_height[step*i : step*(i+1), :], border_width, border_BGR, empty_space, background_BGR, \
                    bar_BGR, bar_width, end_spacing, scale, i))
            curr_thread.start()
            threads.append(curr_thread)
        
        filelist.close()
    
        # this makes sure every chunk is written before the code goes ahead and starts merging the chunks
        for t in threads:
            t.join()



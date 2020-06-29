import barheight
from sys import argv,stderr,exit
from math import sqrt
import os
import numpy as np
import cv2
import threading

class VideoCreator:

    def __init__(self, width, height, fps, path, bars, border_width, empty_space, bar_color, border_color, background, bg_is_image):
        self.video_width = width 
        self.video_height = height
        self.framerate = fps
        self.title = path + '_.mp4'
        
        self.blocks = bars
        self.border_width = border_width
        self.empty_space = empty_space

        self.bar_color = bar_color
        self.border_color = border_color
        self.background = background

        self.bgimage = bg_is_image
        if bg_is_image:
            self.prepare_background(background)

        self.bar_width = self.video_width//self.blocks
        self.border_size = int(self.border_width*self.bar_width)
        self.end_spacing = (self.video_width % self.blocks) // 2


    def prepare_background(self, background):
        unprepped = cv2.imread(background)
        print(unprepped.shape)
        if unprepped.shape[0:2] != (self.video_height, self.video_width):
            scale_factor = 1/min(unprepped.shape[0]/self.video_height, unprepped.shape[1]/self.video_width)
            print(scale_factor)
            unprepped = cv2.resize(unprepped, None, fx=scale_factor, fy=scale_factor)
            crop_dims = ((unprepped.shape[0] - self.video_height)//2, (unprepped.shape[0] + self.video_height)//2, 
                         (unprepped.shape[1] - self.video_width) //2, (unprepped.shape[1] + self.video_width) //2)

            prepped = unprepped[crop_dims[0]:crop_dims[1], crop_dims[2]:crop_dims[3], :]
        print(prepped.shape) 
        self.bg_array = prepped


    def process_frame(self, frame_data, scale):
        ''' turns the data for a frame into a np array representing the frame '''
        
        # instantiate the frame as an ndarray with shape (h w, 3), the last channel being the background color
        # or if the background is an image, set it as the image (scaled to fit the screen)
        if self.bgimage:
            curr_frame = np.copy(self.bg_array)
        else:
            curr_frame = np.full((self.video_height, self.video_width, 3), self.background, dtype=np.uint8)

        for x, bar_height in enumerate(frame_data): 
            # calculates the corners of the current bar
            corner_DL = (int(self.bar_width*(x + self.border_width + self.empty_space/2)) + self.end_spacing, \
                         int(self.video_height//2 + scale*bar_height))
           
            corner_UR = (int(self.bar_width*(x + 1 - self.empty_space/2 - self.border_width)) + self.end_spacing, \
                         int(self.video_height//2 - scale*bar_height))

            # cleans the input colors (everything *must* be an integer)
            #border_BGR = (int(border_BGR[0]), int(border_BGR[1]), int(border_BGR[2]))
            #bar_BGR = (int(bar_BGR[0]), int(bar_BGR[1]), int(bar_BGR[2]))
            
            cv2.rectangle(curr_frame, corner_DL, corner_UR, self.border_color, 2*self.border_size)
            cv2.rectangle(curr_frame, corner_DL, corner_UR, self.bar_color, -1)
        
        return curr_frame
    
    def process_chunk(self, video_chunk, scale, count):
        ''' takes a portion of the video (in the form of an np array of shape (length, bar_count) 
            then processes the portion into its own video and writes it (used to thread) '''
        # setup for the videowriter for this chunk
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
        video = cv2.VideoWriter(os.getcwd() + '/chunks/chunk' + str(count) + '.mp4', fourcc, self.framerate, \
                                (self.video_width, self.video_height))
        
        for frame in video_chunk:
            # simply run process frame and write to the video
            vframe = self.process_frame(frame, scale)
            video.write(vframe)

        video.release()

    def create_video(self, video_bar_height):
        ''' takes in a bunch of specs and writes the video '''
        
        # keep the bars in the bounds of the screen
        scale = self.video_height/np.amax(video_bar_height)        
        
        print('writing chunks')
        
        # filelist just keeps track of the chunks, important for eventually merging
        filelist = open('chunkorder.txt', 'w') 

        # breaks up the video so there a roughly equal amount of threads and frames per thread
        # ideally I bump the number of threads, as merging is *significantly* faster than writing the video
        # but then I run the risk of using all your memory and tanking the computer/queue up too many
        # threads and get no speedup at all, this just feels like a good balance
        step = int(sqrt(video_bar_height.shape[0]))
        threads = []
        for i in range(video_bar_height.shape[0]//step+1):
            # keep track of this file
            filelist.write("file './chunks/chunk" + str(i) + ".mp4'\n")
            
            # set up the thread
            curr_thread = threading.Thread(target=self.process_chunk, args= \
                    (video_bar_height[step*i : step*(i+1), :], scale, i))
            curr_thread.start()
            threads.append(curr_thread)
        
        filelist.close()
    
        # this makes sure every chunk is written before the code goes ahead and starts merging the chunks
        for t in threads:
            t.join()



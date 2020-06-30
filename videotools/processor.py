import barheight
from sys import argv,stderr,exit
from math import sqrt,pi,cos,sin
import os
import numpy as np
import cv2
import threading

class VideoCreator:

    def __init__(self, width, height, fps, path, bars, bar_layout, border_width, empty_space, bar_color, border_color, background, bg_is_image, fill_type):
        self.video_width = width 
        self.video_height = height
        self.framerate = fps
        self.title = path + '_.mp4'
        
        self.blocks = bars
        self.bar_layout = bar_layout
        self.border_width = border_width
        self.empty_space = empty_space

        self.bar_color = bar_color
        self.border_color = border_color
        self.background = background

        self.bgimage = bg_is_image
        self.prepare_background(background, fill_type)

        self.bar_width = self.video_width//self.blocks
        self.border_size = int(self.border_width*self.bar_width)
        self.end_spacing = (self.video_width % self.blocks) // 2

    def prepare_background(self, background, fill_type):
        ''' if the background is an image, instead of loading each frame, it sets up 
            a template and has the code copy it, which is much faster '''
        
        if self.bgimage:
            unprepped = cv2.imread(background)
            if unprepped.shape[0:2] != (self.video_height, self.video_width):
                # if you chose to fill to screen, maintaining aspect ratio and cropping the image
                if fill_type == 0:
                    # scale factor is the same for x and y, chosen to be the larger of the two
                    scale_factor = max(self.video_height/unprepped.shape[0], self.video_width,unprepped.shape[1])
                    #scale_factor = 1/min(unprepped.shape[0]/self.video_height, unprepped.shape[1]/self.video_width)

                    # scales the image, then crops it so that the center of the image is in the background
                    unprepped = cv2.resize(unprepped, None, fx=scale_factor, fy=scale_factor)
                    crop_dims = ((unprepped.shape[0] - self.video_height)//2, (unprepped.shape[0] + self.video_height)//2, 
                                 (unprepped.shape[1] - self.video_width) //2, (unprepped.shape[1] + self.video_width) //2)

                    self.bg_array = unprepped[crop_dims[0]:crop_dims[1], crop_dims[2]:crop_dims[3], :]
            
                # if you chose to stretch to fit the screen, not maintaining aspect ratio but keeping the whole image
                else:
                    vscale = self.video_height/unprepped.shape[0]
                    hscale = self.video_width/unprepped.shape[1]
                    self.bg_array = cv2.resize(unprepped, None, fx=hscale, fy=vscale)
            else:
                self.bg_array = unprepped
        else:
            self.bg_array = np.full((self.video_height, self.video_width, 3), self.background, dtype=np.uint8)

        if self.bar_layout != 0:
            self.bg_array = cv2.circle(self.bg_array, (self.video_width//2, self.video_height//2), self.video_height//4, self.bar_color, -1)

    def transform_rect(self, rect, angle):
        ''' takes a list of points, rotates them by angle clockwise and move them to the center '''
        c, s = cos(angle), sin(angle)
        for pt in rect:
            pt[0], pt[1] = pt[0]*c - pt[1]*s + self.video_width//2, pt[0]*s + pt[1]*c + self.video_height//2


    def process_frame(self, frame_data, scale):
        ''' turns the data for a frame into a np array representing the frame '''
        
        # the background is a copy of the background array we prepared
        curr_frame = np.copy(self.bg_array)

        for x, bar_height in enumerate(frame_data): 
            if self.bar_layout == 0:
                # calculates the corners of the current bar
                corner_DL = (int(self.bar_width*(x + self.border_width + self.empty_space/2)) + self.end_spacing, \
                             int(self.video_height//2 + scale*bar_height))
               
                corner_UR = (int(self.bar_width*(x + 1 - self.empty_space/2 - self.border_width)) + self.end_spacing, \
                             int(self.video_height//2 - scale*bar_height))
                
                # draws rectangles accordingly
                cv2.rectangle(curr_frame, corner_DL, corner_UR, self.border_color, 2*self.border_size)
                cv2.rectangle(curr_frame, corner_DL, corner_UR, self.bar_color, -1)
            else:
                # define the angle to rotate and the rectangle to be rotated
                angle = -2*pi*x/self.blocks

                # the bar starts as a vertical bar, defined to be above the origin at a distance of height/4
                # and dimensions (bar_width, bar_height*scale)
                curr_bar = np.array([[-self.bar_width//2, -self.video_height//4], \
                                     [self.bar_width//2, -self.video_height//4], \
                                     [self.bar_width//2, -(self.video_height//4 + scale*bar_height)], \
                                     [-self.bar_width//2, -(self.video_height//4 + scale*bar_height)]], dtype=np.int32)
                
                # rotate the rectangle
                self.transform_rect(curr_bar, angle)
                
                cv2.polylines(curr_frame, [curr_bar], True, self.border_color, 2*self.border_size)
                cv2.fillPoly(curr_frame, [curr_bar], self.bar_color)
        
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
        scale = self.video_height/np.amax(video_bar_height) * (.5 if self.bar_layout != 0 else 1)
        
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



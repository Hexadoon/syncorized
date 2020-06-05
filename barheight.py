import numpy as np

magnitude = np.vectorize(np.absolute, signature='(m,n)->(m,n)')
vfft = np.vectorize(np.fft.rfft, signature='(m,n)->(m,k)')

# for a given frame, returns the heights of each bar
def bar_height(frame, blocks, points_per_bar):
    heights = [] 
    for i in range(blocks):
        curr_h = 0
        for j in range(points_per_bar):
            if frame[i*points_per_bar+j] > curr_h:
                curr_h = frame[i*points_per_bar + j]

        heights.append(curr_h)

    return np.array(heights)

# given an audio file and samples_per_frame (which is the sample rate divided by
# the frame rate), decomposes the audio and returns a 2D numpy array where 
# axis 0 is frame and axis 1 is the height of the bar in that frame
def decompose(samples_per_frame, blocks, audio):
    print("converting to mono")
    if audio.shape[1] > 1:
        # convert stereo to mono via simply adding the channels
        audio = np.sum(audio, axis=1)
    
    # now 'audio' represents an array of audio frames, where each array
    # corresponds to a frame in the video
    print(f"converted. resizing {audio.shape[0]}")
    audio.resize(samples_per_frame, audio.shape[0]//samples_per_frame-1)
    
    # transformed applies a real-values fast fourier transform on each frame
    # a frame is a sectiond of samples in the wav file, as framerate goes up
    # the accuracy decreases, while the framerate of the video increases
    # 60 fps is probably a good compromise
    print(f"resized. transforming {audio.shape}->{audio.shape[0]*audio.shape[1]}")
    transformed = vfft(a=audio)

    # the output of the rfft is complex, we want the magnitudes of these numbers
    # to get the actual magnitude of that frequency (which will be the height of the bar)
    print(f"transformed, taking magnitudes {transformed.shape}")
    transformed = magnitude(transformed)
    print("magnitudes taken, calculating bar heights")    
    
    points_per_bar = (transformed.shape[1]//blocks) // 16
    #                 ^samples per frame    ^ per bar  ^ we only *really* want the info 
    #                                                    stored in the lower part

    get_heights = np.vectorize(bar_height, \
            signature='(m),()->(k)')
    video_bar_heights = get_heights(transformed, blocks, points_per_bar)
    
    print(f"bar heights calculated {video_bar_heights.shape}")

    return video_bar_heights 


import cv2
import functions
from scipy.io import wavfile


class Video:
    def __init__(self, videofile):
        functions.extract_audio(videofile)
        data = wavfile.read(r'temp\extracted_audio.wav')


        self.sampling_freq = data[0]
        data = data[1]

        frames = data.shape[0]
        print"frames!!!", frames
        channels = data.shape[1]
        self.audio_capacity = frames * channels

        cap = cv2.VideoCapture(videofile)
        success, image = cap.read()
        height = image.shape[0]
        width = image.shape[1]
        channels = image.shape[2]
        no_of_frames = cap.get(7)
        print 'no_of_frames', no_of_frames
        self.fps = cap.get(5)
        self.framesize = width * height * channels
        self.vid_capacity = width * height * channels * no_of_frames
        self.vid_capacity = int(self.vid_capacity)
        print 'vid_capacity', self.vid_capacity
        capacity_bits = self.vid_capacity + self.audio_capacity
        self.s_capacity_bytes = int(capacity_bits / 7)
        print 'audio capacity', self.audio_capacity
        print 'capacity', self.s_capacity_bytes



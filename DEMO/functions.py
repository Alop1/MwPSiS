import numpy
from PIL import Image
import subprocess
import os
import cv2
import time

def det_cap(audio_cap, video_cap, message):
    message_len = len(message)
    capacity = audio_cap + video_cap
    cap_no_gaps = audio_cap * 2
    while cap_no_gaps % 7 != 0:
        cap_no_gaps += 1
    cap_no_gaps /= 7
    #print cap_no_gaps
    i = cap_no_gaps
    sum_gaps = 0
    while i < message_len:
        character_bin = dec2bin(ord(message[i]))
        sum_gaps += int(character_bin[3:6], 2)
        #print sum_gaps
        i += 1

    if message_len * 7 + sum_gaps + 7 <= capacity:
        return True
    else:
        return False



def rand_max(audio_cap, video_cap, message_len):
    message_len += 7
    print 'message len',message_len
    capacity = audio_cap + video_cap
    print 'capacity',capacity
    cap_no_gaps = audio_cap * 2
    print cap_no_gaps
    if message_len < cap_no_gaps:           #???
        return 0
    while cap_no_gaps % 7 != 0:
        cap_no_gaps += 1
    #print 'cap no gaps', cap_no_gaps
    message_len -= cap_no_gaps
    #print 'message len po zakodowaniu w audio', message_len
    capacity -= cap_no_gaps
    #print 'pozostala pojemnosc',capacity
    spare_bits = capacity - message_len
    #print 'tyle wolnych bitow',spare_bits
    randmax = (spare_bits)/ ((message_len) / 7)
    return int(randmax)


# funkcja zamieniajaca liczbe dziesietna na string reprezentujacy jej zapis na 7 bitach


def dec2bin(n):
    s = ''
    i = 7
    while n > 0:
        d = str(n % 2)
        s = d + s
        n /= 2
        i -= 1
    s = '0' * i + s
    return s


# funkcja zamieniajaca obraz na numpy array


def image2array(filename):
    im = Image.open(filename)
    data = numpy.array(im)
    return data

# funkcja ekstrahujaca strumien audio z pliku wideo


def extract_audio(filename):
    print "extract audio"
    if not os.path.exists('temp'):
        print "przed tempem"
        os.makedirs('temp')

    print "mamy tempa", os.getcwd()
    out_filename = os.getcwd() + r'\temp\extracted_audio.wav'
    print out_filename
    cmd = ["ffmpeg", "-y",
           "-i", filename,
           out_filename,
           'temp\\extracted_audio.wav',
           '-loglevel', 'quiet']
    print cmd
    subprocess.call(cmd)

# funkcja ekstrahujaca ramki z pliku wideo


def extract_frames(videofile):
    # os.chdir("C:/Users/user/Documents/GitHub/MwPSiS/DEMO/")
    if not os.path.exists('temp\\frames'):
        os.makedirs('temp\\frames')


    cmd = ["ffmpeg",
           '-i', videofile,
           'temp\\frames\\frame%d.png',
           '-loglevel', 'quiet']
    time.sleep(20)

    subprocess.call(cmd)


# funkcja tworzaca steganograficzne wideo


def make_vid(fps, filename):

    cmd = ["ffmpeg", "-y",
           #"-y", #"-f", "image2",
           "-framerate", "%f" % fps,
           '-i', 'temp\\frames\\frame%d.png',
           '-vcodec', 'ffv1',
           'temp\\stegovid_no_sound.avi',
           '-loglevel', 'quiet']
    subprocess.call(cmd)

    cmd = ["ffmpeg", "-y",
           "-i", "temp\\stegoaudio.wav",
           "-i", "temp\\stegovid_no_sound.avi",
           '-vcodec', 'copy',
           '-acodec', 'copy',
           filename, '-loglevel', 'quiet']

    subprocess.call(cmd)



import functions
from PIL import Image
import os
from scipy.io import wavfile
import random
import time

def encode(videofile, message, mode, seed = None, randmax = None):
    functions.extract_frames(videofile)
    functions.extract_audio(videofile)

    if mode == 'n':
        random.seed(seed)

    audiodata = wavfile.read('temp\\extracted_audio.wav')
    sampling_freq = audiodata[0]
    audiodata = audiodata[1]
    in_video = False
    frame_no = 1
    frame_path = 'temp\\frames\\frame' + str(frame_no) + '.png'
    imdata = functions.image2array(frame_path)
    a = 0
    i = 0
    length = len(message)
    audio_ended = False
    k = 0
    audiogap = 0
    #imgap = 0
    if mode == 'sp':
        imgap = randmax
    else:
        imgap = 0

    if not os.path.exists('temp\\frames'):
        os.makedirs('temp\\frames')
    temp = 1
    for character in message:
        # print temp
        # temp += 1
        character_bin = functions.dec2bin(ord(character))           #koduje zanki na bity

        if length == 1:             # w sumie nic znaczacego
            character_bin += '0000000'

        length -= 1

        for bit in character_bin:
            k += 1

            if not in_video:
                if a == len(audiodata.flat):
                    audio_ended = True

                if int(bit) != audiodata.flat[a] % 2:
                    audiodata.flat[a] += 1

            else:
                if i == len(imdata.flat):

                    if frame_no > 0:
                        im = Image.fromarray(imdata)
                        im.save(frame_path)
                        #print "zapisujemy ramke nr", frame_path

                    frame_no += 1
                    frame_path = 'temp\\frames\\frame' + str(frame_no) + '.png'
                    print "Kodowanie w ramce nr", str(frame_no)
                    imdata = functions.image2array(frame_path)
                    i = 0

                if int(bit) != imdata.flat[i] % 2:
                    if imdata.flat[i] == 255:
                        imdata.flat[i] -= 1
                    else:
                        imdata.flat[i] += 1

            if k % 7 == 0:
                if audio_ended:
                    if mode == 'n':
                        imgap = random.randint(1, randmax)

                    elif mode == 'd':
                        imgap = int(character_bin[3:6], 2)

                if in_video:
                    if i + 1 + imgap < len(imdata.flat):
                        i = i + 1 + imgap

                    else:

                        if frame_no > 0:
                            im = Image.fromarray(imdata)
                            im.save(frame_path)
                            #print "zapisujemy ramke nr", frame_path

                        frame_no += 1
                        i = imgap - (len(imdata.flat) - 1 - i)
                        frame_path = 'temp\\frames\\frame' + str(frame_no) + '.png'
                        print "Kodowanie w ramce nr", str(frame_no)
                        imdata = functions.image2array(frame_path)

                else:
                    if a + 1 + audiogap < len(audiodata.flat):
                        a = a + 1 + audiogap
                    else:
                        if not audio_ended:
                            audio_ended = True
                            in_video = not in_video

            elif in_video:
                i += 1
            else:
                if a+1 != len(audiodata.flat):
                    a += 1
                else:
                    audio_ended = True
                    in_video = not in_video

            if not audio_ended:
                in_video = not in_video

    im = Image.fromarray(imdata)

    im.save(frame_path)
    # print "czas start"
    # time.sleep(15)

    print "kliknieto enter"
    wavfile.write('temp\\stegoaudio.wav', sampling_freq, audiodata)

#
# def decode(filename, mode, seed = None, randmax = None):
#     functions.extract_frames(filename)
#     functions.extract_audio(filename)
#
#     if mode == 'n':
#         random.seed(seed)
#
#     audiodata = wavfile.read('temp\\extracted_audio.wav')
#     audiodata = audiodata[1]
#     frame_no = 1
#     frame_path = 'temp\\frames\\frame' + str(frame_no) + '.png'
#     imdata = functions.image2array(frame_path)
#     bit_count = 0
#     d = ""
#     s = ""
#     i = 0
#     a = 0
#     in_video = False
#     audio_ended = False
#     audiogap = 0
#     #imgap = 0
#     if mode == 'sp':
#         imgap = randmax
#     else:
#         imgap = 0
#
#     if not os.path.exists('temp\\frames'):
#         os.makedirs('temp\\frames')
#
#     while True:
#
#         if bit_count == 7:
#
#             if s == '0000000':
#                 break
#
#             if audio_ended:
#                 if mode == 'n':
#                     imgap = random.randint(1, randmax)
#
#                 elif mode == 'd':
#                     imgap = int(s[3:6], 2)
#
#             d += chr(int(s, 2))
#             s = ""
#             bit_count = 0
#
#             if in_video:
#                 if i + imgap < len(imdata.flat):
#                     i = i + imgap
#                 else:
#                     i = imgap - (len(imdata.flat) - i)
#                     frame_no += 1
#                     frame_path = 'temp\\frames\\frame' + str(frame_no) + '.png'
#                     print "Dekodowanie z ramki nr", str(frame_no)
#                     imdata = functions.image2array(frame_path)
#
#             else:
#                 if a + imgap < len(audiodata.flat):
#                     a += audiogap
#                 else:
#                     audio_ended = True
#
#         if in_video:
#             if i == len(imdata.flat):
#                 frame_no += 1
#                 frame_path = 'temp\\frames\\frame' + str(frame_no) + '.png'
#                 print "Dekodowanie z ramki nr", str(frame_no)
#                 imdata = functions.image2array(frame_path)
#                 i = 0
#
#             s += str(imdata.flat[i] % 2)
#             bit_count += 1
#             i += 1
#
#         else:
#             if a == len(audiodata.flat):
#                 audio_ended = True
#             s += str(audiodata.flat[a] % 2)
#             bit_count += 1
#             if a+1 != len(audiodata.flat):
#                 a += 1
#             else:
#                 audio_ended = True
#                 in_video = not in_video
#
#         if not audio_ended:
#             in_video = not in_video
#
#     return d

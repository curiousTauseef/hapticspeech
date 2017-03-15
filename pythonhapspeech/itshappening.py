from os import listdir
from os.path import isfile, join
import os

import random
from struct import pack, unpack
from math import sin, pi
import wave
import pyaudio  
import math
import pygame
import time

# basic settings
pygame.init()

width = 800
height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((width,height))
pygame.display.set_caption('Haptic Speech Experiment')
clock = pygame.time.Clock()

wavpath = "stimuli/"

"""============================================================="""
# # creates text boxes
# def text_objects(text, font):
# 	textSurface = font.render(text, True, black)
# 	return textSurface, textSurface.get_rect()

# # displays text in a textbox
# def message_display(text):
# 	largeText = pygame.font.Font('freesansbold.ttf',115)
# 	TextSurf, TextRect = text_objects(text, largeText)
# 	TextRect.center = ((display_width/2),(display_height/2))
# 	gameDisplay.blit(TextSurf, TextRect)

# 	pygame.display.update()

# 	time.sleep(2)
	
# 	game_loop()

# grabs a song from directory and plays it
def play_wavfile(filename):
	RATE=44100
	chunk = 1024

	filepath = os.path.join(wavpath, filename)

	def translate(value, leftMin, leftMax, rightMin, rightMax):
	    # Figure out how 'wide' each range is
	    leftSpan = leftMax - leftMin
	    rightSpan = rightMax - rightMin

	    # Convert the left range into a 0-1 range (float)
	    valueScaled = float(value - leftMin) / float(leftSpan)

	    # Convert the 0-1 range into a value in the right range.
	    return rightMin + (valueScaled * rightSpan)

	f = wave.open(filepath,"rb")  
	print("\n\nopening: "+filepath)
	print("samplerate: "+str(f.getframerate()))
	print("frames: "+str(f.getnframes()))
	print("channels: "+str(f.getnchannels()))
	print("sample width: "+str(f.getsampwidth()))


	## GENERATE STEREO FILE ##
	wv = wave.open('temp.wav', 'w')
	wv.setparams((2, 2, RATE, 0, 'NONE', 'not compressed'))
	maxVol=2**14-1.0 #maximum amplitude
	wvData=""
	i = 0

	for i in range(0, f.getnframes()):
	
		frameSample = f.readframes(1)
		# print len(frameSample)
		if len(frameSample):
			try:
				data = unpack('h',frameSample)
			except:
				print ("Unpacking error, may be from an invalid frameSample")
				print ("frame sample length: "+str(len(frameSample)))
				print ("frame sample string: "+frameSample)
			
		else:
			data = 0
		if data:
			amp = math.sqrt(data[0]**2)
			wvData+=pack('h', data[0])
			wvData+=pack('h', amp*sin(i*800.0/RATE)) #200Hz right
		else:
			break
	wv.writeframes(wvData)
	wv.close()

	print("processed file!")


	# --------------------------------------------------------
	# playback processed audio
	# --------------------------------------------------------

	#open a wav format music  
	f = wave.open(r"temp.wav","rb")  
	#instantiate PyAudio  
	p = pyaudio.PyAudio()  
	#open stream  
	stream = p.open(format = p.get_format_from_width(f.getsampwidth()), 
	                channels = 2,  
	                rate = f.getframerate(),  
	                output = True)  
	#read data  
	data = f.readframes(chunk)

	print("playback initialized!")

	while data:
	    stream.write(data)
	    data = f.readframes(chunk)

	#stop stream  
	stream.stop_stream()  
	stream.close()  

	print("playback ended.")
	#close PyAudio  
	p.terminate()  

# returns a randomized list of songs in the directory
def get_wavfiles():
	path = "stimuli/"
	# put names of wavfiles in a list
	wavfiles = [f for f in listdir(path) if isfile(join(path, f))]
	if '.DS_Store' in wavfiles:
		wavfiles.remove('.DS_Store')
	random.shuffle(wavfiles)
	return wavfiles
"""============================================================="""

def game_loop():

	wavfiles = get_wavfiles()

	gameExit = False
	num_of_files = len(wavfiles)
	file_index = 0

	play_wavfile(wavfiles[file_index])

	while not gameExit:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					if file_index == 0:
						pass
					else:
						file_index -= 1
						play_wavfile(wavfiles[file_index])

				if event.key == pygame.K_RIGHT:
					if file_index == num_of_files:
						pass
					else:
						file_index += 1
						play_wavfile(wavfiles[file_index])
						print("file index: "+str(file_index))
						print("wave file: "+str(wavfiles[file_index]))
						break

			# may not need this part
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					pass

		gameDisplay.fill(white)
		pygame.display.update()
		clock.tick(60)


game_loop()
pygame.quit()
quit()
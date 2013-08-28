from time import sleep
import random
import pifacedigitalio as piface
piface.init()
pfd = piface.PiFaceDigital()
current = 0
set_time = 2000
time_left = set_time
score = 0
misses = 0

def next_number():
	return random.randint(0,7)

def next_button():
	global current
	global previous
	global score
	global misses
	global set_time
	global time_left
	previous = current
	current = 1<<next_number()
	while current == previous:
		current = 1<<next_number()
    
	if ((score + misses) %10) ==0:
		if set_time > 125:
			set_time -=50
			print "Time left is: %s" %set_time
	time_left = set_time
	pfd.output_port.value = current

next_button()
previous_pressed = 255

while True:
    
	in_bit_pattern = pfd.input_port.value
	if in_bit_pattern != previous_pressed:
		previous_pressed = in_bit_pattern
		if in_bit_pattern > 0:
            
			if in_bit_pattern == current:
				print “Correct!”
				next_button()
				score += 1
				print “Your score %d” %score
			else:
				print "Wrong one!"
				score -= 1
				print "Your score %d" %score
	elif time_left==0:
		misses +=1
		print "Missed one!"
		next_button()
        
		if misses == 10:
			break
	time_left -=1
pfd.output_port.value = 0
print "\nGame over!\n"
print "Your score was: %s" %score

import sys, pygame, pygame.midi, rtmidi, time
# require the package python-rtmidi installed with pip


### INPUT SETUP ###
pygame.init()
pygame.midi.init()

# list all midi devices
for x in range( 0, pygame.midi.get_count()//2 ):
	print(x,":", pygame.midi.get_device_info(x))

# select input id 
print("Select Input index")
input_str = input()
input_int = int(input_str)

# open a specific midi device
inp = pygame.midi.Input(input_int)
print("Input Setup Completed")
print("")

### OUTPUT SETUP ###
midiout = rtmidi.MidiOut()

# list output devices
available_ports = midiout.get_ports()
print("Available Outputs:",available_ports)

# select output
print("Select Output index")
output_str = input()
output_int = int(output_str)

# open specific output
midiout.open_port(output_int)
print("Output Setup Completed")
print("")


# Display options
WIDTH = 300
HEIGHT = 200
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('MIDI converter')

# Effective cycle
going = True

# run the event loop
while going:
    if inp.poll():
    	# Queue max length is the parameter
        current_note = inp.read(1000)
        # Transfer the note 
        note_msg = [current_note[0][0][0], current_note[0][0][1], current_note[0][0][2]]
        
        # DTX Snare 31 to standard 38 acoustic snare
        if note_msg[1] == 31:
        	note_msg[1] = 38 

        # DTX Kick 33 to standard 35 kick
        if note_msg[1] == 33:
            note_msg[1] = 35 

        midiout.send_message(note_msg)
        
        if current_note[0][0][0] != 248:
        	print(note_msg)
    # wait for not use 100% of cpu
    pygame.time.wait(1)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            going = False

# Exit 
del midiout
pygame.quit()
print("Bye")

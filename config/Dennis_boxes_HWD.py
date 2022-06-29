from devices import *

board = Breakout_1_2() # Instantiate breakout board.

# Instantiate Five Poke
# Port 1 on the Five poke board is connected to port 1 on the breakout board.
# Port 2 on the Five poke board is connected to port 3 on the breakout board.
five_poke = Five_poke(ports=[board.port_1, board.port_3])

# Intantiate reward port poke plugged into port 2 on breakout board.
reward_port = Poke(port=board.port_2, rising_event='poke_6', falling_event='poke_6_out')

# Instantiate audio board plugged into port 4 on breakout board.
speaker = Audio_board(port=board.port_4)

# Instantiate syringe pump stepper motor plugged into port 5 on breakout board.
# Connect the pass through adapter between the breakout and the stepper driver.
syringe_pump = Stepper_motor(port=board.port_5)

#Instantiate the house light plugged into POW_A on the pass through adapter.
#house_light = Digital_output(pin=board.port_5.POW_A)

# Instantiate BNC connector 1 on the breakout board as a digital output for 
# sync with Ephys etc.
BNC = Digital_output(pin=board.BNC_1)

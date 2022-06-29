
from pyControl.utility import *
import hardware_definition as hw

# State machine.

states = ['state1', 'state2','state3', 'state4','state5', 'state6']

events = ['poke_1', 'poke_1_out',
          'poke_2', 'poke_2_out',
          'poke_3', 'poke_3_out',
          'poke_4', 'poke_4_out',
          'poke_5', 'poke_5_out',
          'poke_6', 'poke_6_out']

initial_state = 'state6'

v.state_dur = 500

def state1(event):
    if event=='entry':
        hw.five_poke.poke_1.LED.on()
        timed_goto_state('state2',v.state_dur)
    elif event=='exit':
        hw.five_poke.poke_1.LED.off()

def state2(event):
    if event=='entry':
        hw.five_poke.poke_2.LED.on()
        timed_goto_state('state3',v.state_dur)
    elif event=='exit':
        hw.five_poke.poke_2.LED.off()

def state3(event):
    if event=='entry':
        hw.five_poke.poke_3.LED.on()
        timed_goto_state('state4',v.state_dur)
    elif event=='exit':
        hw.five_poke.poke_3.LED.off()

def state4(event):
    if event=='entry':
        hw.five_poke.poke_4.LED.on()
        timed_goto_state('state5',v.state_dur)
    elif event=='exit':
        hw.five_poke.poke_4.LED.off()

def state5(event):
    if event=='entry':
        hw.five_poke.poke_5.LED.on()
        timed_goto_state('state6',v.state_dur)
    elif event=='exit':
        hw.five_poke.poke_5.LED.off()

def state6(event):
    if event=='entry':
        hw.house_light.on()
        timed_goto_state('state1',v.state_dur)
    elif event=='exit':
        hw.house_light.off()

def all_states(event):
    if event == 'poke_6':
        goto_state('state6')
    if event=='poke_1':
        goto_state('state1')
    if event=='poke_2':
        goto_state('state2')
    if event=='poke_3':
        goto_state('state3')
    if event=='poke_4':
        goto_state('state4')
    if event=='poke_5':
        goto_state('state5')

def run_end():
    hw.off() # Turn off all outputs.
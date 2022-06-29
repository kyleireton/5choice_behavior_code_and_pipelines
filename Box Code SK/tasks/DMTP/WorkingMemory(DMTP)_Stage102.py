# important note:- Do not change any print stings if you intended to use pyOS5 GUI
#@ Author : Sampath
#This script is to run DMTP (Delayed Matched Response) working memory task and for more deatils look at Task_desription.ppt
#SP => Sample Phase
#CP => Choice Phase

import random as rnd
import hardware_definition as hw
from pyControl.utility import *

target_port_list = [1, 2, 4, 5]
Hole1_choices = [4]
Hole2_choices = [5]
Hole3_choices = [0]
Hole4_choices = [1]
Hole5_choices = [2]

# list of states, for pyControl
states = ['start',
          'sample_state',
          'choice_state',
          'pre_reward_delay',
          'post_reward_delay',
          'sp_reward',
          'cp_reward',         
          'iti',
          'penalty_omission_sample',
          'penalty_omission_choice',
          'penalty_choice',
          'penalty_sample']

# list of events, for pyControl
events = ['session_timer',
          'poke_1',  # Hole 1
          'poke_2',  # Hole 2
          'poke_3',  # Hole 3
          'poke_4',  # Hole 4
          'poke_5',  # Hole 5
          'poke_6',  # (reward; in)
          'poke_6_out',  # (reward; out)
          'port_lights_timer', # turn off five choice light and advance to limited hold(LH) stage
          'reward_in_timer',  # turn off reward port light to reinforce to leave receptacle
          'omission_sample', # timer omission after SD+LH for SP
          'omission_choice'] # timer omission after SD+LH for SP
#Initial state required by pycontrol framework
initial_state = 'start'

# Dur Variables

v.SP_state_dur = 20 * second
v.CP_state_dur = 20 * second
v.LH_dur = 1 * second
v.ITI_dur = 5 * second
v.penalty_dur = 5 * second
v.pre_delay_dur = 0 * second
v.post_delay_dur = 2 * second
v.reward_stimulation_dur = 2 * second
v.session_duration = 30 * minute

# Rerward rate volume Variables
v.steps_rate = 1000
v.steps_rate_choice = 2000
v.n_steps_choice = 2800
v.n_steps_sample = 500

#State defines begening
def run_start():
    set_timer('session_timer', v.session_duration)
    hw.house_light.off()

#State defines End
def run_end():
    hw.off()
    hw.house_light.off()


# start state code
def start(event):
    if event == 'entry':
        hw.reward_port.LED.on()
        hw.syringe_pump.backward(v.steps_rate, v.n_steps_sample)
    elif event == 'exit':
        hw.reward_port.LED.off()
        disarm_timer('reward_in_timer')
    elif event == 'poke_6':
        set_timer('reward_in_timer', v.reward_stimulation_dur)
    elif event == 'poke_6_out':
        print('SP_reward : 10')
        goto_state('sample_state')


# Sample Phase
def sample_state(event):
    if event == 'entry':
        v.sp_target = 0
        print('sample_phase')
        set_timer('port_lights_timer', v.SP_state_dur)
        set_timer('omission_sample', (v.SP_state_dur + v.LH_dur))
        v.sp_target = rnd.choice(target_port_list)        
        print('v.sp_target:{}'.format(v.sp_target))
        if v.sp_target == 1:
            hw.five_poke.poke_1.LED.on()
        elif v.sp_target == 2:
            hw.five_poke.poke_2.LED.on()
        elif v.sp_target == 3:
            hw.five_poke.poke_3.LED.on()
        elif v.sp_target == 4:
            hw.five_poke.poke_4.LED.on()
        elif v.sp_target == 5:
            hw.five_poke.poke_5.LED.on()
    elif event == 'poke_1' and v.sp_target == 1 \
            or event == 'poke_2' and v.sp_target == 2 \
            or event == 'poke_3' and v.sp_target == 3 \
            or event == 'poke_4' and v.sp_target == 4 \
            or event == 'poke_5' and v.sp_target == 5:
        print('Correct_sample')
        goto_state('pre_reward_delay')
    elif event == 'poke_1' and v.sp_target != 1 \
            or event == 'poke_2' and v.sp_target != 2 \
            or event == 'poke_3' and v.sp_target != 3 \
            or event == 'poke_4' and v.sp_target != 4 \
            or event == 'poke_5' and v.sp_target != 5:
        print('Incorrect_sample')
        goto_state('penalty_sample')
    elif event == 'exit':
        hw.five_poke.poke_1.LED.off()
        hw.five_poke.poke_2.LED.off()
        hw.five_poke.poke_3.LED.off()
        hw.five_poke.poke_4.LED.off()
        hw.five_poke.poke_5.LED.off()
        disarm_timer('port_lights_timer')
        disarm_timer('omission_sample')

# Delay before reward
def pre_reward_delay(event):
    if event == "entry":
        print("post_reward_delay")
        timed_goto_state('sp_reward', v.pre_delay_dur)
    elif event == 'poke_1' and v.sp_target == 1\
            or event == 'poke_2' and v.sp_target == 2\
            or event == 'poke_3' and v.sp_target == 3\
            or event == 'poke_4' and v.sp_target == 4\
            or event == 'poke_5' and v.sp_target == 5:
        print('perseverate_sample')
    elif event == "exit":
        timed_goto_state('sp_reward', v.pre_delay_dur)

#Reward for SP
def sp_reward(event):
    if event == 'entry':
        hw.reward_port.LED.on()
    elif event == 'poke_6':
        hw.syringe_pump.backward(v.steps_rate, v.n_steps_sample)
        print('reward_sample_taken')
        set_timer('reward_in_timer', v.reward_stimulation_dur)
    elif event == 'poke_6_out':
        goto_state('post_reward_delay')
    elif event == 'poke_1' and v.sp_target == 1 \
            or event == 'poke_2' and v.sp_target == 2 \
            or event == 'poke_3' and v.sp_target == 3 \
            or event == 'poke_4' and v.sp_target == 4 \
            or event == 'poke_5' and v.sp_target == 5:
        print('perseverate_sample')   
    elif event == 'exit':
        hw.reward_port.LED.off()
        disarm_timer('reward_in_timer')

#Delay after SP reward
def post_reward_delay(event):
    if event == "entry":
        print("post_reward_delay")
        timed_goto_state('choice_phase', v.post_delay_dur)
    elif event == 'poke_1' and v.sp_target == 1\
            or event == 'poke_2' and v.sp_target == 2\
            or event == 'poke_3' and v.sp_target == 3\
            or event == 'poke_4' and v.sp_target == 4\
            or event == 'poke_5' and v.sp_target == 5:
        print('Premature_choice_correct')
    elif event == "exit":
        timed_goto_state('choice_state', v.post_delay_dur)

# Choice Phase
def choice_state(event):
    if event == 'entry' and v.sp_target == 1:
        print('choice_phase')
        v.cp_target = rnd.choice(Hole1_choices)
        print('v.cp_target:{}'.format(v.cp_target))
        set_timer('port_lights_timer', v.CP_state_dur)
        set_timer('omission_choice', (v.CP_state_dur + v.LH_dur))
        if v.cp_target == 2:
            hw.five_poke.poke_2.LED.on()
            hw.five_poke.poke_1.LED.on()
        if v.cp_target == 3:
            hw.five_poke.poke_3.LED.on()
            hw.five_poke.poke_1.LED.on()
        if v.cp_target == 4:
            hw.five_poke.poke_4.LED.on()
            hw.five_poke.poke_1.LED.on()
        if v.cp_target == 5:
            hw.five_poke.poke_5.LED.on()
            hw.five_poke.poke_1.LED.on()
    elif event == 'entry' and v.sp_target == 2:
        print('choice_phase')
        v.cp_target = rnd.choice(Hole2_choices)
        print('v.cp_target:{}'.format(v.cp_target))
        set_timer('port_lights_timer', v.CP_state_dur)
        set_timer('omission_choice', (v.CP_state_dur + v.LH_dur))
        if v.cp_target == 1:
            hw.five_poke.poke_1.LED.on()
            hw.five_poke.poke_2.LED.on()
        if v.cp_target == 3:
            hw.five_poke.poke_3.LED.on()
            hw.five_poke.poke_2.LED.on()
        if v.cp_target == 4:
            hw.five_poke.poke_4.LED.on()
            hw.five_poke.poke_2.LED.on()
        if v.cp_target == 5:
            hw.five_poke.poke_5.LED.on()
            hw.five_poke.poke_2.LED.on()
    elif event == 'entry' and v.sp_target == 3:
        print('choice_phase')
        v.cp_target = rnd.choice(Hole3_choices)
        print('v.cp_target:{}'.format(v.cp_target))
        set_timer('port_lights_timer', v.CP_state_dur)
        set_timer('omission_choice', (v.CP_state_dur + v.LH_dur))
        if v.cp_target == 1:
            hw.five_poke.poke_1.LED.on()
            hw.five_poke.poke_3.LED.on()
        if v.cp_target == 2:
            hw.five_poke.poke_2.LED.on()
            hw.five_poke.poke_3.LED.on()
        if v.cp_target == 4:
            hw.five_poke.poke_4.LED.on()
            hw.five_poke.poke_3.LED.on()
        if v.cp_target == 5:
            hw.five_poke.poke_5.LED.on()
            hw.five_poke.poke_3.LED.on()
    elif event == 'entry' and v.sp_target == 4:
        print('choice_phase')
        v.cp_target = rnd.choice(Hole4_choices)
        print('v.cp_target:{}'.format(v.cp_target))
        set_timer('port_lights_timer', v.CP_state_dur)
        set_timer('omission_choice', (v.CP_state_dur + v.LH_dur))
        if v.cp_target == 1:
            hw.five_poke.poke_1.LED.on()
            hw.five_poke.poke_4.LED.on()
        if v.cp_target == 2:
            hw.five_poke.poke_2.LED.on()
            hw.five_poke.poke_4.LED.on()
        if v.cp_target == 3:
            hw.five_poke.poke_3.LED.on()
            hw.five_poke.poke_4.LED.on()
        if v.cp_target == 5:
            hw.five_poke.poke_5.LED.on()
            hw.five_poke.poke_4.LED.on()
    elif event == 'entry' and v.sp_target == 5:
        v.cp_target = rnd.choice(Hole5_choices)
        print('v.cp_target:{}'.format(v.cp_target))
        print('choice_phase')
        set_timer('port_lights_timer', v.CP_state_dur)
        set_timer('omission_choice', (v.CP_state_dur + v.LH_dur))
        if v.cp_target == 1:
            hw.five_poke.poke_1.LED.on()
            hw.five_poke.poke_5.LED.on()
        if v.cp_target == 2:
            hw.five_poke.poke_2.LED.on()
            hw.five_poke.poke_5.LED.on()
        if v.cp_target == 3:
            hw.five_poke.poke_3.LED.on()
            hw.five_poke.poke_5.LED.on()
        if v.cp_target == 4:
            hw.five_poke.poke_4.LED.on()
            hw.five_poke.poke_5.LED.on()
    elif event == 'poke_1' and v.sp_target == 1\
            or event == 'poke_2' and v.sp_target == 2\
            or event == 'poke_3' and v.sp_target == 3\
            or event == 'poke_4' and v.sp_target == 4\
            or event == 'poke_4' and v.sp_target == 5:
        print('Correct_choice')
        goto_state('cp_reward')
    elif event == 'poke_1' and v.cp_target == 1\
            or event == 'poke_2' and v.cp_target == 2\
            or event == 'poke_3' and v.cp_target == 3\
            or event == 'poke_4' and v.cp_target == 4\
            or event == 'poke_4' and v.cp_target == 5:
        print('incorrect_choice_lit')
        goto_state('penalty_choice')
    elif event == 'poke_1' and v.cp_target != 1 and v.sp_target != 1\
            or event == 'poke_2' and v.cp_target != 2 and v.sp_target != 2\
            or event == 'poke_3' and v.cp_target != 3 and v.sp_target != 3\
            or event == 'poke_4' and v.cp_target != 4 and v.sp_target != 4\
            or event == 'poke_4' and v.cp_target != 5 and v.sp_target != 5:
        print('Incorrect_choice')
        goto_state('penalty_choice')
    elif event == 'exit':
        hw.five_poke.poke_1.LED.off()
        hw.five_poke.poke_2.LED.off()
        hw.five_poke.poke_3.LED.off()
        hw.five_poke.poke_4.LED.off()
        hw.five_poke.poke_5.LED.off()
        disarm_timer('port_lights_timer')
        disarm_timer('omission_choice')
        
#Reward for CP
def cp_reward(event):
    if event == 'entry':
        hw.reward_port.LED.on()
    elif event == 'poke_6':
        hw.syringe_pump.backward(v.steps_rate_choice, v.n_steps_choice)
        print('reward_choice_taken')
        set_timer('reward_in_timer', v.reward_stimulation_dur)
    elif event == 'poke_6_out':
        goto_state('iti')
    elif event == 'exit':
        hw.reward_port.LED.off()
        disarm_timer('reward_in_timer')

#Penalty foe omission in SP
def penalty_omission_sample(event):
    if event == 'entry':
        hw.five_poke.poke_1.LED.off()
        hw.five_poke.poke_2.LED.off()
        hw.five_poke.poke_3.LED.off()
        hw.five_poke.poke_4.LED.off()
        hw.five_poke.poke_5.LED.off()
        print('penalty')
        hw.house_light.on()
        hw.reward_port.LED.off()
        timed_goto_state('iti', v.penalty_dur)
    elif event == 'poke_1'\
            or event == 'poke_2'\
            or event == 'poke_3'\
            or event == 'poke_4'\
            or event == 'poke_5':
        print('attempts_dur_penalty_sample')
    elif event == 'exit':
        hw.house_light.off()

#Penalty foe omission in CP
def penalty_omission_choice(event):
    if event == 'entry':
        print('penalty')
        hw.house_light.on()
        hw.reward_port.LED.off()
        timed_goto_state('iti', v.penalty_dur)
    elif event == 'exit':
        hw.house_light.off()
    elif event == 'poke_1'\
            or event == 'poke_2'\
            or event == 'poke_3'\
            or event == 'poke_4'\
            or event == 'poke_5':
        print('attempts_dur_penalty_choice')

#Penalty foe Incorrect response in SP
def penalty_sample(event):
    if event == 'entry':
        hw.house_light.on()
        hw.reward_port.LED.off()
        timed_goto_state('iti', v.penalty_dur)
    elif event == 'exit':
        hw.house_light.off()
    elif event == 'poke_1'\
            or event == 'poke_2'\
            or event == 'poke_3'\
            or event == 'poke_4'\
            or event == 'poke_5':
        print('attempts_dur_penalty_sample')

#Penalty foe Incorrect response in CP
def penalty_choice(event):
    if event == 'entry':
        hw.house_light.on()
        hw.reward_port.LED.off()
        timed_goto_state('iti', v.penalty_dur)
    elif event == 'poke_1'\
            or event == 'poke_2'\
            or event == 'poke_3'\
            or event == 'poke_4'\
            or event == 'poke_5':
        print('attempts_dur_penalty_choice')
    elif event == 'exit':
        hw.house_light.off()

#ITI
def iti(event):
    if event == 'entry':
        print('iti_sample')
        timed_goto_state('sample_state', v.ITI_dur)
    elif event == 'poke_1'\
            or event == 'poke_2'\
            or event == 'poke_3'\
            or event == 'poke_4'\
            or event == 'poke_5':
        print('Premature_response')
    elif event == 'exit':
        hw.house_light.off()

#Catch up with all states events
def all_states(event):
    if event == 'session_timer':
        print("Event Closing")
        stop_framework()
    elif event == 'port_lights_timer':
        hw.five_poke.poke_1.LED.off()
        hw.five_poke.poke_2.LED.off()
        hw.five_poke.poke_3.LED.off()
        hw.five_poke.poke_4.LED.off()
        hw.five_poke.poke_5.LED.off()
    elif event == 'reward_in_timer':
        hw.reward_port.LED.off()
    elif event == 'omission_sample':
        print('omission_sample')
        hw.five_poke.poke_1.LED.off()
        hw.five_poke.poke_2.LED.off()
        hw.five_poke.poke_3.LED.off()
        hw.five_poke.poke_4.LED.off()
        hw.five_poke.poke_5.LED.off()
        goto_state('penalty_omission_sample')
    elif event == 'omission_choice':        
        print('omission_choice')
        hw.five_poke.poke_1.LED.off()
        hw.five_poke.poke_2.LED.off()
        hw.five_poke.poke_3.LED.off()
        hw.five_poke.poke_4.LED.off()
        hw.five_poke.poke_5.LED.off()
        goto_state('penalty_omission_choice')
    elif event == 'poke_1' or event == 'poke_2' or event == 'poke_3' or event == 'poke_4' or event == 'poke_5':
        print('5_poke_entries')
    elif event == 'poke_6_out':
        print('receptacle_entries')


# End of the task file

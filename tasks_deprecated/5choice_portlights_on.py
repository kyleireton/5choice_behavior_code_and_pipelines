# necessary imports to begin code

from pyControl.utility import *
import hardware_definition as hw
import random

target_port_list = ['1', '2', '3', '4', '5']

# list of states, for pyControl

states = ['start',
          'taste_task',
          'reward',
          'penalty',
          'ITI']

# list of events, for pyControl

events = ['session_timer',
          'poke_1',     # port 1
          'poke_2',     # port 2
          'poke_3',     # port 3
          'poke_4',     # port 4
          'poke_5',     # port 5
          'poke_6',     # port 6 (reward; in)
          'poke_6_out',  # port 6 (reward; out)
          '1',
          '2',
          '3',
          '4',
          '5',
          'kill_port_lights',
          'kill_reward',
          'penalty_omission']  # timer to kill session

# initial state name (required by pyControl)

initial_state = ('start')

# variables needed

v.session_duration = 20*minute      # Session duration
v.steps_rate = 1000                 # this is step rate for stepper motor if you want to use peristaltic pump it will be 1000
v.n_steps = 1000                    # this is number of steps for stepper motor if you want to use peristaltic pump it will be 1000
v.state_dur = 3*second             # this state the duration of the choice_state#
v.LH_dur = 2*second                 # limited hold duration
v.reward_stimulation_dur = 5*second # Reward duration this duration
v.ITI_dur = 0*second                # this state the duration of the Intra_trail_interval
v.penalty_dur = 2*second            # punishment duration(All lights off)
v.choice_time = 0                   # stores the exact time of choice start 
v.reward_start_time = 0             # start_time when right poke occurs
v.iti_start_time = 0
v.reward_latency_list = []          # stores all the reward latencies and evaluates mean
v.correct_latency_list = []         # stores all the correct latencies and evaluates mean
v.incorrect_latency_list = []       # stores all the incorrect latencies and evaluates mean
v.premature_response_latency_list = []

# coding in list of nose port target choices. randomly select from this v.variable at each choice phase start
# initially setting v.target to 0 just as placeholder, since appears I can reset value to whatever during task state!!

v.target = 0

# criteria to meet to advance stage

v.Correct = 50
v.Accuracy = 30
v.Correct = 20
v.Omission = 50
v.premature = 50

# initiate and end code

def run_start():

    set_timer('session_timer', v.session_duration)
    hw.reward_port.SOL.on()
    hw.five_poke.poke_1.LED.on()
    hw.five_poke.poke_2.LED.on()
    hw.five_poke.poke_3.LED.on()
    hw.five_poke.poke_4.LED.on()
    hw.five_poke.poke_5.LED.on()
    
def run_end():

    hw.off()
    hw.reward_port.SOL.off()

# start state code

def start(event):

    if event =='entry':
        hw.reward_port.SOL.on()
    elif event =='exit':
        hw.reward_port.SOL.off()

# task phase code block

def taste_task(event):

    if event == 'entry':
        hw.five_poke.poke_1.LED.on()
        hw.five_poke.poke_2.LED.on()
        hw.five_poke.poke_3.LED.on()
        hw.five_poke.poke_4.LED.on()
        hw.five_poke.poke_5.LED.on()
    elif event == 'exit':
        hw.five_poke.poke_1.LED.off()
        hw.five_poke.poke_2.LED.off()
        hw.five_poke.poke_3.LED.off()
        hw.five_poke.poke_4.LED.off()
        hw.five_poke.poke_5.LED.off()

    elif event == 'poke_1' or event == 'poke_2' or event == 'poke_3' or event == 'poke_4' or event == 'poke_5':
        current_time = get_current_time()
        correct_latency = current_time - v.choice_time
        v.correct_latency_list.append(correct_latency)
        v.reward_start_time = current_time
        print("correct_latency_mean: {}".format(mean(v.correct_latency_list)))
        print('Correct_response')
        goto_state('reward')

# reward state

def reward(event):

    if event == 'entry':
        hw.reward_port.LED.on()
        hw.syringe_pump.backward(v.steps_rate, v.n_steps)
    elif event == 'exit':
        hw.reward_port.LED.off()
        disarm_timer('kill_reward')

    elif event == 'poke_6':
        reward_latency = get_current_time() - v.reward_start_time
        v.reward_latency_list.append(reward_latency)
        print("Reward Latency Mean: {}".format(mean(v.reward_latency_list)))
        print('Reward')
        set_timer('kill_reward', v.reward_stimulation_dur)
    elif event == 'poke_6_out':
        goto_state('ITI')

    elif event == 'poke_1' \
            or event == 'poke_2' \
            or event == 'poke_3' \
            or event == 'poke_4' \
            or event == 'poke_5':
        print('perseverate')
# ITI state

def ITI(event):

    if event =='entry':
        v.iti_start_time = get_current_time()
        timed_goto_state('taste_task', v.ITI_dur)

# catch-all state to detect timers, esp. session ending

def all_states(event):

    if event == 'session_timer':
        print("Event Closing")
        print("Correct Latency List: {}".format(v.correct_latency_list))
        print("Incorrect Latency List: {}".format(v.incorrect_latency_list))
        print("Reward Latency List: {}".format(v.reward_latency_list))
        print("Premature Latency List: {}".format(v.premature_response_latency_list))
        stop_framework()

    elif event == 'kill_port_lights':
        hw.five_poke.poke_1.LED.off()
        hw.five_poke.poke_2.LED.off()
        hw.five_poke.poke_3.LED.off()
        hw.five_poke.poke_4.LED.off()
        hw.five_poke.poke_5.LED.off()

    elif event == 'kill_reward':
        hw.reward_port.LED.off()

    elif event == 'penalty_omission':
        print('omission')
        goto_state('penalty')
# necessary imports to begin code

from pyControl.utility import *
import hardware_definition as hw
import random

target_port_list = ['1', '2', '3', '4', '5']

# list of states, for pyControl

states = ['start',
          'choice_task',
          'reward1',
          'reward2',
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

v.session_duration = 30*minute      # Session duration
v.steps_rate = 500                 # this is step rate for stepper motor if you want to use peristaltic pump it will be 1000
v.n_steps = 17                    # this is number of steps for stepper motor if you want to use peristaltic pump it will be 1000
v.state_dur = 2*second             # this state the duration of the choice_state#
v.LH_dur = 2*second                 # limited hold duration
v.reward_stimulation_dur = 3.5*second # Reward duration this duration
v.ITI_dur = 9*second                # this state the duration of the Intra_trail_interval
v.penalty_dur = 5*second            # punishment duration(All lights off)
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
    
def run_end():

    hw.off()
    hw.reward_port.SOL.off()

# start state code

def start(event):
    if event =='entry':
        hw.reward_port.LED.on()
        hw.syringe_pump.forward(v.steps_rate, v.n_steps)
    elif event =='exit':
        hw.reward_port.LED.off()
        hw.speaker.off()
        print("ITI_duration: {}".format(v.ITI_dur))
        print("SD_duration: {}".format(v.state_dur))
        print("LH_duration: {}".format(v.LH_dur))
        print('Trial_start')

    elif event == 'poke_6':
        hw.reward_port.LED.off()
        set_timer('kill_reward', v.reward_stimulation_dur)

# task phase code block

def choice_task(event):
    if event == 'entry':
        v.choice_time = get_current_time()
        print('Sample_state')
        set_timer('kill_port_lights'
                  , v.state_dur)
        set_timer('penalty_omission'
                  , (v.state_dur + v.LH_dur))
        set_timer(random.choice(target_port_list)
                  , 0)
    elif event == 'exit':
        hw.five_poke.poke_1.LED.off()
        hw.five_poke.poke_2.LED.off()
        hw.five_poke.poke_3.LED.off()
        hw.five_poke.poke_4.LED.off()
        hw.five_poke.poke_5.LED.off()
        disarm_timer('kill_port_lights')
        disarm_timer('penalty_omission')

    elif event == '1':
        v.target = 1
        hw.five_poke.poke_1.LED.on()
        print('light1')
    elif event == '2':
        v.target = 2
        hw.five_poke.poke_2.LED.on()
        print('light2')
    elif event == '3':
        v.target = 3
        hw.five_poke.poke_3.LED.on()
        print('light3')
    elif event == '4':
        v.target = 4
        hw.five_poke.poke_4.LED.on()
        print('light4')
    elif event == '5':
        v.target = 5
        hw.five_poke.poke_5.LED.on()
        print('light5')

    elif event == 'poke_1' and v.target == 1\
            or event == 'poke_2' and v.target == 2\
            or event == 'poke_3' and v.target == 3\
            or event == 'poke_4' and v.target == 4\
            or event == 'poke_5' and v.target == 5:
        current_time = get_current_time()
        correct_latency = current_time - v.choice_time
        v.correct_latency_list.append(correct_latency)
        v.reward_start_time = current_time
        print("Correct_latency: {}".format(correct_latency))
        print('Correct_response')
        goto_state('reward1')

    elif event == 'poke_1' and v.target != 1 \
            or event == 'poke_2' and v.target != 2 \
            or event == 'poke_3' and v.target != 3 \
            or event == 'poke_4' and v.target != 4 \
            or event == 'poke_5' and v.target != 5:
        incorrect_latency = get_current_time() - v.choice_time
        v.incorrect_latency_list.append(incorrect_latency)
        print("Incorrect_latency: {}".format(incorrect_latency))
        print('Incorrect_response')
        goto_state('penalty')

# reward state

def reward1(event):
    if event == 'entry':
        hw.reward_port.LED.on()
        hw.syringe_pump.forward(v.steps_rate, v.n_steps)
    elif event == 'exit':
        hw.reward_port.LED.off()

    elif event == 'poke_6':
        reward_latency = get_current_time() - v.reward_start_time
        v.reward_latency_list.append(reward_latency)
        print("Reward_latency: {}".format(reward_latency))
        print('Reward_taken')
        
        goto_state('reward2')

    elif event == 'poke_1' \
            or event == 'poke_2' \
            or event == 'poke_3' \
            or event == 'poke_4' \
            or event == 'poke_5':
        print('perseverate')

def reward2(event):

    if event == 'entry':
        set_timer('kill_reward', v.reward_stimulation_dur)        

    elif event == 'poke_1' \
            or event == 'poke_2' \
            or event == 'poke_3' \
            or event == 'poke_4' \
            or event == 'poke_5':
        print('perseverate')

# penalty state

def penalty(event):

    if event == 'entry':
        print('penalty')
        hw.reward_port.SOL.on()
        hw.reward_port.LED.off()
        timed_goto_state('ITI', v.penalty_dur)
    elif event == 'exit':
        hw.reward_port.SOL.off()

    if event == 'poke_1' \
            or event == 'poke_2' \
            or event == 'poke_3' \
            or event == 'poke_4' \
            or event == 'poke_5':
        print('attempts_dur_penalty')

# ITI state

def ITI(event):

    if event =='entry':
        print('iti_start_time')
        v.iti_start_time = get_current_time()
        timed_goto_state('choice_task', v.ITI_dur)
    elif event == 'poke_1' \
            or event == 'poke_2' \
            or event == 'poke_3' \
            or event == 'poke_4' \
            or event == 'poke_5':
        premature_response_latency = get_current_time() - v.iti_start_time
        v.premature_response_latency_list.append(premature_response_latency)
        print("Premature_latency: {}" .format(premature_response_latency))
        print('Premature_response')
        goto_state('penalty')

# catch-all state to detect timers, esp. session ending

def all_states(event):

    if event == 'session_timer':
        print("cl: {}".format(v.correct_latency_list))
        print("il: {}".format(v.incorrect_latency_list))
        print("rl: {}".format(v.reward_latency_list))
        print("pl: {}".format(v.premature_response_latency_list))
        print("Event Closing")
        print("Event Closing")
        stop_framework()
    elif event == 'kill_port_lights':
        hw.five_poke.poke_1.LED.off()
        hw.five_poke.poke_2.LED.off()
        hw.five_poke.poke_3.LED.off()
        hw.five_poke.poke_4.LED.off()
        hw.five_poke.poke_5.LED.off()
    elif event == 'kill_reward':
        goto_state('ITI')
    elif event == 'penalty_omission':
        print('omission')
        goto_state('penalty')
    elif event == 'poke_1' or event == 'poke_2' or event == 'poke_3' or event == 'poke_4' or event == 'poke_5':
        print('5_poke_entries')
    elif event == 'poke_6_out':
        print('receptacle_entries')
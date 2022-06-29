# necessary imports to begin code

from pyControl.utility import *
import hardware_definition as hw
import random

target_port_list = ['1', '2', '3', '4', '5']

# list of states, for pyControl

states = ['start',
          'choice_task',
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
          'SD_timeout',
          'kill_reward',
          'penalty_omission']  # timer to kill session

# initial state name (required by pyControl)

initial_state = ('start')

# variables needed

v.session_duration = 30*minute      # Session duration
v.steps_rate = 1000                 # this is step rate for stepper motor if you want to use peristaltic pump it will be 1000
v.n_steps = 1000                    # this is number of steps for stepper motor if you want to use peristaltic pump it will be 1000
v.state_dur = 20*second             # this state the duration of the choice_state#
v.LH_dur = 2*second                 # limited hold duration
v.reward_stimulation_dur = 2*second # Reward duration this duration
v.ITI_dur = 2*second                # this state the duration of the Intra_trail_interval
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

# list of performance measures, to count in each session (will be compared to criteria for advancing training stage)

v.num_trials = 0
v.num_premature = 0
v.num_accurate = 0
v.num_inaccurate = 0
v.num_omission = 0
v.num_penalty = 0

v.per_premature = 0
v.per_correct = 0
v.per_accurate = 0
v.per_inaccurate = 0
v.per_omission = 0
v.per_penalty = 0


# initiate and end code

def run_start():

    print('code_start')
    hw.reward_port.SOL.on()
    set_timer('session_timer', v.session_duration)
    
def run_end():

    print("code_end")
    hw.reward_port.SOL.off()
    hw.off()

# start state code

def start(event):

    if event =='entry':
        print('start')
        hw.reward_port.LED.on()
        hw.syringe_pump.backward(v.steps_rate, v.n_steps)
    elif event =='exit':
        hw.reward_port.LED.off()
        disarm_timer('kill_reward')

    elif event == 'poke_6':
        set_timer('kill_reward', v.reward_stimulation_dur)
        print("startphase_rewardpoke")
    elif event == 'poke_6_out':
        print('trial_start')
        print("SD_duration: {}".format(v.state_dur))
        print("LH_duration: {}".format(v.LH_dur))
        print("ITI_duration: {}".format(v.ITI_dur))
        hw.speaker.off()
        goto_state('ITI')

# ITI phase code block

def ITI(event):

    if event =='entry':
        print('ITI')
        v.iti_start_time = get_current_time()
        timed_goto_state('choice_task', v.ITI_dur)

    elif event == 'poke_1' \
            or event == 'poke_2' \
            or event == 'poke_3' \
            or event == 'poke_4' \
            or event == 'poke_5':
        print('premature_poke')
        v.num_premature +=1

        premature_response_latency = (get_current_time() - v.iti_start_time)
        v.premature_response_latency_list.append(premature_response_latency)
        print("Premature Response Latency: {}" .format(mean(v.premature_response_latency_list)))
        goto_state('penalty')
    
    elif event == 'poke_6':
        print('ITI_rewardpoke')

# task phase code block

def choice_task(event):

    if event == 'entry':
        print('choice_task')
        v.choice_time = get_current_time()
        set_timer('SD_timeout', v.state_dur)
        set_timer('penalty_omission', (v.state_dur + v.LH_dur))
        set_timer(random.choice(target_port_list), 0)
    elif event == 'exit':
        set_timer('kill_port_lights', 0)
        disarm_timer('SD_timeout')
        disarm_timer('penalty_omission')

    elif event == '1':
        v.target = 1
        hw.five_poke.poke_1.LED.on()
        print('SD')
        print("lighton1")
    elif event == '2':
        v.target = 2
        hw.five_poke.poke_2.LED.on()
        print('SD')
        print("lighton2")
    elif event == '3':
        v.target = 3
        hw.five_poke.poke_3.LED.on()
        print('SD')
        print("lighton3")
    elif event == '4':
        v.target = 4
        hw.five_poke.poke_4.LED.on()
        print('SD')
        print("lighton4")
    elif event == '5':
        v.target = 5
        hw.five_poke.poke_5.LED.on()
        print('SD')
        print("lighton5")

    elif event == 'poke_1' and v.target == 1\
            or event == 'poke_2' and v.target == 2\
            or event == 'poke_3' and v.target == 3\
            or event == 'poke_4' and v.target == 4\
            or event == 'poke_5' and v.target == 5:
        print('poke_accurate')
        v.num_accurate += 1
        current_time = get_current_time()
        correct_latency = (current_time - v.choice_time)
        v.correct_latency_list.append(correct_latency)
        v.reward_start_time = current_time
        print("correct_latency_mean: {}".format(mean(v.correct_latency_list)))
        goto_state('reward')

    elif event == 'poke_1' and v.target != 1 \
            or event == 'poke_2' and v.target != 2 \
            or event == 'poke_3' and v.target != 3 \
            or event == 'poke_4' and v.target != 4 \
            or event == 'poke_5' and v.target != 5:
        print('poke_inaccurate')
        v.num_inaccurate += 1
        incorrect_latency = (get_current_time() - v.choice_time)
        v.incorrect_latency_list.append(incorrect_latency)
        print("incorrect_latency: {}".format(mean(v.incorrect_latency_list)))
        goto_state('penalty')

    elif event == 'poke_6':
        print('task_rewardpoke')

# reward state

def reward(event):

    if event == 'entry':
        print('reward')
        v.num_trials += 1
        hw.reward_port.LED.on()
        hw.syringe_pump.backward(v.steps_rate, v.n_steps)
    elif event == 'exit':
        hw.reward_port.LED.off()
        disarm_timer('kill_reward')

    elif event == 'poke_6':
        reward_latency = get_current_time() - v.reward_start_time
        v.reward_latency_list.append(reward_latency)
        print("reward_rewardpoke")
        print("Reward Latency Mean: {}".format(mean(v.reward_latency_list)))
        set_timer('kill_reward', v.reward_stimulation_dur)
    elif event == 'poke_6_out':
        goto_state('ITI')

    elif event == 'poke_1' \
            or event == 'poke_2' \
            or event == 'poke_3' \
            or event == 'poke_4' \
            or event == 'poke_5' :
        print('poke_during_reward')

# penalty state

def penalty(event):

    if event == 'entry':
        hw.reward_port.SOL.off()
        hw.reward_port.LED.off()
        timed_goto_state('ITI', v.penalty_dur)
        v.num_trials += 1
        v.num_penalty += 1
    elif event == 'exit':
        hw.reward_port.SOL.on()

    elif event == 'poke_1' \
            or event == 'poke_2' \
            or event == 'poke_3' \
            or event == 'poke_4' \
            or event == 'poke_5' :
        print('poke_during_penalty')
    elif event == 'poke_6':
        print('penalty_rewardpoke')

# catch-all state to detect timers, esp. session ending

def all_states(event):

    if event == 'session_timer':

        print("Event Closing")

        print("Premature Latency List: {}".format(v.premature_response_latency_list))
        print("Incorrect Latency List: {}".format(v.incorrect_latency_list))
        print("Correct Latency List: {}".format(v.correct_latency_list))
        print("Reward Latency List: {}".format(v.reward_latency_list))

        v.per_penalty = (v.num_penalty / v.num_trials)
        print("#, per_penalty")
        print (v.num_penalty)
        print (v.per_penalty)

        v.per_premature = (v.num_premature / v.num_trials)
        print ("#, per_premature")
        print (v.num_premature)
        print (v.per_premature)

        v.per_omission = (v.num_omission / v.num_trials)
        print ("#, per_omission")
        print (v.num_omission)
        print (v.per_omission)

        v.per_inaccurate = (v.num_inaccurate / (v.num_trials - (v.num_omission + v.num_premature)))
        print ("#, per_inaccurate")
        print (v.num_inaccurate)
        print (v.per_inaccurate)
        
        v.per_accurate = (v.num_accurate / (v.num_trials - (v.num_omission + v.num_premature)))
        print ("#, per_accurate")
        print (v.num_accurate)
        print (v.per_accurate)

        v.per_correct = (v.num_accurate / v.num_trials)
        print ("#, per_correct")
        print (v.num_accurate)
        print (v.per_correct)

        print ("# trials")
        print (v.num_trials)

        stop_framework()

    elif event == 'SD_timeout':
        set_timer('kill_port_lights', 0)
        print("SD_timeout")
        print("LH")

    elif event == 'penalty_omission':
        print("LH_timeout")
        print("omission")
        v.num_omission += 1
        goto_state('penalty')

    elif event == 'kill_port_lights':
        hw.five_poke.poke_1.LED.off()
        hw.five_poke.poke_2.LED.off()
        hw.five_poke.poke_3.LED.off()
        hw.five_poke.poke_4.LED.off()
        hw.five_poke.poke_5.LED.off()

    elif event == 'kill_reward':
        hw.reward_port.LED.off()
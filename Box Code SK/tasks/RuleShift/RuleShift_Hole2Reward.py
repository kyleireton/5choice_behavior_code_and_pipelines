# --------------------------RuleShift Reward for Hole-2 Protocol Task File----------------------
# Subject were habituated to hole 2 and 4 previously now they need to learn new rule, i.e only one hole
# .... (either 2 or 4 depending on reward hole) gives reward, irrespective of illumination (hole_2 or hole_4)
# cue presentation [2 or 4] ==> Correct response @ Illuminated reward hole            ==> reward(@reward port) ==> iti**
# cue presentation [2 or 4] ==> Correct response @ non Illuminated hole reward hole   ==> reward(@reward port) ==> iti**
# cue presentation [2 or 4] ==> Incorrect response @ non Illuminated hole  ==> penalty (house light off) ==> iti**
# cue presentation [2 or 4] ==> Incorrect response @ Illuminated hole4     ==> penalty (house light off) ==> iti**
# cue presentation [2 or 4] ==> No response (omission)                     ==> penalty (house light off) ==> iti**
# **any response at 5-Poke during the iti is considered as premature response and trial starts again after penalty(house light off)

# important note:- Do not change any print stings if you intended to use pyOS5 GUI
# --------------------------------------------------------------------------
# ----------------------------------------
# Imports
from pyControl.utility import *
import hardware_definition as hw
import random

# ------------------------------------

reward_hole = 2  # by changing this to 4 can change reward for poke_4
# list of states, for pyControl

states = ['start',
          'cue_light',
          'reward',
          'penalty',
          'iti']

# list of events, for pyControl
events = ['session_timer',
          'poke_1',  # port 1
          'poke_2',  # port 2
          'poke_3',  # port 3
          'poke_4',  # port 4
          'poke_5',  # port 5
          'poke_6',  # port 6 (reward; in)
          'poke_6_out',  # port 6 (reward; out)
          'port_lights_timer',
          'reward_in_timer',
          'penalty_omission']

# initial state name (required by pyControl)
initial_state = ('start')

# variables needed

v.session_duration = 45 * minute  # Session duration
v.state_dur        = 8 * second  # this state the duration of the choice_state#
v.iti_dur          = 2 * second  # this state the duration of the Intra_trail_interval
v.LH_dur           = 1 * second  # limited hold duration
v.reward_stim_dur  = 2 * second  # Reward duration this duration
v.penalty_dur      = 3 * second  # punishment duration(All lights off)
v.steps_rate       = 1000  # this is step rate for stepper motor if you want to use peristaltic pump it will be 1000
v.n_steps          = 2000  # this is number of steps for stepper motor if you want to use peristaltic pump it will be 1000
v.target = 0


# initiate and end code
def run_start():
    set_timer('session_timer', v.session_duration)
    hw.house_light.on()


def run_end():
    hw.off()
    hw.house_light.off()


# Initial state
def start(event):
    if event == 'entry':
        hw.reward_port.LED.on()
        hw.syringe_pump.backward(v.steps_rate, v.n_steps)
    elif event == 'exit':
        hw.reward_port.LED.off()
        disarm_timer('reward_in_timer')
    elif event == 'poke_6':
        set_timer('reward_in_timer', v.reward_stim_dur)
    elif event == 'poke_6_out':
        print("iti_duration: {}".format(v.iti_dur))
        print("SD_duration: {}".format(v.state_dur))
        print("LH_duration: {}".format(v.LH_dur))
        print('Trial_start')
        goto_state('cue_light')


# Cue presenting state
def cue_light(event):
    if event == 'entry':
        print('Sample_state')
        set_timer('port_lights_timer'
                  , v.state_dur)
        set_timer('penalty_omission'
                  , (v.state_dur + v.LH_dur))
        v.target = random.randint(1, 2)  # randomly select int between 1-5 and variable as v.target
        print('v.target:{}'.format(v.target))
        if v.target == 1:
            hw.five_poke.poke_2.LED.on()  # 5-choice hole_2 light on
            print('hole2_lit_on')
        elif v.target == 2:
            hw.five_poke.poke_4.LED.on()  # 5-choice hole_4 light on
            print('hole4_lit_on')
    elif event == 'exit':
        hw.five_poke.poke_1.LED.off()  # 5-choice hole_1 light off
        hw.five_poke.poke_2.LED.off()  # 5-choice hole_2 light off
        hw.five_poke.poke_3.LED.off()  # 5-choice hole_3 light off
        hw.five_poke.poke_4.LED.off()  # 5-choice hole_4 light off
        hw.five_poke.poke_5.LED.off()  # 5-choice hole_5 light off
        disarm_timer('port_lights_timer')
        disarm_timer('penalty_omission')

        # if hole light2 on response is poke2 and reward hole is 2
    elif event == 'poke_2' and v.target == 1 and reward_hole == 2:
        print('Correct_lit')
        goto_state('reward')
        # if hole light4 on response is poke4 and reward hole is 4
    elif event == 'poke_4' and v.target == 2 and reward_hole == 4:
        print('Correct_lit')
        goto_state('reward')
        # if hole light2 on response is poke2 and reward hole is 2
    elif event == 'poke_2' and v.target == 2 and reward_hole == 2:
        print('Correct_unlit')
        goto_state('reward')
        # if hole light2 on response is poke4 and reward hole is 4
    elif event == 'poke_4' and v.target == 1 and reward_hole == 4:
        print('Correct_unlit')
        goto_state('reward')
        # if hole light2 on response is poke2 and reward hole is 4
    elif event == 'poke_2' and v.target == 1 and reward_hole != 2:
        print('Incorrect_lit')
        goto_state('penalty')
        # if hole light4 on response is poke4 and reward hole is 2
    elif event == 'poke_4' and v.target == 2 and reward_hole != 4:
        print('Incorrect_lit')
        goto_state('penalty')
        # if hole light2 on response is poke4 and reward hole is 2
    elif event == 'poke_4' and v.target == 1 and reward_hole != 4:
        print('Incorrect_unlit')
        goto_state('penalty')
        # if hole light4 on response is poke2 and reward hole is 4
    elif event == 'poke_2' and v.target == 2 and reward_hole != 2:
        print('Incorrect_unlit')
        goto_state('penalty')
        # Any response at hole 1,3,5 are dark incorrect since they never ment to be illumination choice
    elif event == 'poke_1' or event == 'poke_3' or event == 'poke_5':
        print('Incorrect_dark_hole135')
        goto_state('penalty')


# reward state
def reward(event):
    if event == 'entry':
        hw.reward_port.LED.on()
        hw.syringe_pump.backward(v.steps_rate, v.n_steps)
    elif event == 'exit':
        hw.reward_port.LED.off()
        disarm_timer('reward_in_timer')
    elif event == 'poke_6':
        print('Reward_taken')
        set_timer('reward_in_timer', v.reward_stim_dur)
    elif event == 'poke_6_out':
        goto_state('iti')
    elif event == 'poke_2' and v.target == 1 and reward_hole == 2 \
            or event == 'poke_4' and v.target == 2 or reward_hole == 4:
        print('perseverate')


# penalty state
def penalty(event):
    if event == 'entry':
        print('penalty')
        hw.house_light.off()
        hw.reward_port.LED.off()
        timed_goto_state('iti', v.penalty_dur)
    elif event == 'exit':
        hw.house_light.on()
    elif event == 'poke_1' \
            or event == 'poke_2' \
            or event == 'poke_3' \
            or event == 'poke_4' \
            or event == 'poke_5':
        print('attempts_dur_penalty')


# iti state
def iti(event):
    if event == 'entry':
        print('iti_start_time')
        timed_goto_state('cue_light', v.iti_dur)
    elif event == 'poke_1' \
            or event == 'poke_2' \
            or event == 'poke_3' \
            or event == 'poke_4' \
            or event == 'poke_5':
        print('Premature_response')
        goto_state('penalty')


# catch-all state to detect timers, esp. session ending
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
    elif event == 'penalty_omission':
        print('Omission')
        goto_state('penalty')
    elif event == 'poke_1' or event == 'poke_2' or event == 'poke_3' or event == 'poke_4' or event == 'poke_5':
        print('5_poke_entries')
    elif event == 'poke_6_out':
        print('receptacle_entries')

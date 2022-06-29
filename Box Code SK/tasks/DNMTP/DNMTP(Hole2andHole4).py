#--------------------------2 Choice-DNMTP----------------------
# important note:- Do not change any print stings if you intended to use pyOS5 GUI
# DNMTP task which is started on 12/08/2019 this is only operates two hole i.e 2 and 4 and this is simplest task in DNMT
# One of the five_poke LEDs turns on randomly (cue presentation) and subject has to make response within the specified period of time(SD+LH)
# SamplePhase = cue presentation (hole-2 or hole-4 ==> Correct poke (illuminated hole)    ==> reward(@reward port) ==> ChoisePhase
# ChoisePhase = cue presentation (hole-2 or hole-4 ==> Correct poke (**illuminated hole4) ==> reward(@reward port) ==> ChoisePhase ==> iti
# if subject poke illuminated incorrect (incorrect_lit), if subject poke non illuminated incorrect (incorrect)

#----------------------------------------------------------

from pyControl.utility import *
import hardware_definition as hw
import random

target_port_list = ['2', '4', '4', '2', '2', '4']  # list for sample phase programmes pick 1 of these variables

states = ['start',
          'sample_task',
          'reward_choice',
          'reward_sample',
          'delay_after_reward_1',
          'delay_after_reward_2',
          'choice_task_1',
          'choice_task_2',
          'ITI_1',
          'ITI_2',
          'penalty_omission_sample',
          'penalty_omission_choice',
          'penalty_choice',
          'penalty_sample']

# list of events, for pyControl

events = ['session_timer',
          'poke_1',  # port 1
          'poke_2',  # port 2
          'poke_3',  # port 3
          'poke_4',  # port 4
          'poke_5',  # port 5
          'poke_6',  # port 6 (reward; in)
          'poke_6_out',  # port 6 (reward; out)
          '2',
          '4',
          'port_lights_timer', # turn off five choice light and advance to limited hold(LH) stage
          'reward_in_timer',   # turn off reward port light to reinforce to leave receptacle
          'omission_sample',
          'omission_choice']

initial_state = ('start')

v.session_duration = 30 * minute
v.steps_rate = 600
v.steps_rate_choice = 2000
v.n_steps_choice = 2500
v.n_steps_sample = 300
v.n_steps_init = 500
v.state_dur = 8 * second
v.state_choice_dur = 5 * second
v.LH_dur = 1 * second
v.reward_stimulation_dur = 2 * second
v.ITI_1_dur = 5 * second
v.ITI_2_dur = 10 * second
v.delay_dur = 2 * second
v.penalty_dur = 5 * second
v.target = 0
v.choice = 0


def run_start():    
    set_timer('session_timer', v.session_duration)
    hw.house_light.off()


def run_end():    
    hw.off()
    hw.house_light.off()


def start(event):    
    if event == 'entry':
        hw.reward_port.LED.on()
        hw.syringe_pump.backward(v.steps_rate_choice, v.n_steps_init)
    elif event == 'exit':
        hw.reward_port.LED.off()
        disarm_timer('reward_in_timer')
    elif event == 'poke_6':
        set_timer('reward_in_timer', v.reward_stimulation_dur)
    elif event == 'poke_6_out':
        print('SP_reward : 10')
        goto_state('sample_task')


def sample_task(event):
    if event == 'entry':
        print('sample_phase')
        set_timer('port_lights_timer', v.state_dur)
        set_timer('omission_sample', (v.state_dur + v.LH_dur))
        set_timer(random.choice(target_port_list), 0)
    elif event == 'exit':
        hw.five_poke.poke_1.LED.off()
        hw.five_poke.poke_2.LED.off()
        hw.five_poke.poke_3.LED.off()
        hw.five_poke.poke_4.LED.off()
        hw.five_poke.poke_5.LED.off()
        disarm_timer('port_lights_timer')
        disarm_timer('omission_sample')
    elif event == '2':
        v.target = 2
        hw.five_poke.poke_2.LED.on()
	print("v.target: {}".format(v.target))
    elif event == '4':
        v.target = 4
        hw.five_poke.poke_4.LED.on()
	print("v.target: {}".format(v.target))
    elif event == 'poke_2' and v.target == 2:
        hw.BNC_1.off()
        hw.BNC_3.on()
        print('Correct_sample')
        goto_state('reward_sample')
    elif event == 'poke_4' and v.target == 4:
        print('Correct_sample')
        hw.BNC_1.off()
        hw.BNC_3.on()
        goto_state('reward_sample')
    elif event == 'poke_1' or event == 'poke_2' and v.target != 2 \
            or event == 'poke_3' or event == 'poke_4' and v.target != 4 \
            or event == 'poke_5':
        hw.BNC_1.off()
        hw.BNC_4.on()
        print('Incorrect_sample')
        goto_state('penalty_sample')


def reward_sample(event):
    if event == 'entry':
        hw.reward_port.LED.on()
        hw.syringe_pump.backward(v.steps_rate, v.n_steps_sample)
    elif event == 'exit':
        hw.reward_port.LED.off()
        disarm_timer('reward_in_timer')
    elif event == 'poke_6':
        print('reward_sample_taken')
        set_timer('reward_in_timer', v.reward_stimulation_dur)
    elif event == 'poke_6_out' and v.target == 2:
        goto_state('delay_after_reward_1')
    elif event == 'poke_6_out' and v.target == 4:
        goto_state('delay_after_reward_2')


def delay_after_reward_1(event):
    if event == "entry":
        print("delay_after_reward")
        timed_goto_state('choice_task_1', v.delay_dur)
    elif event == "exit":
        timed_goto_state('choice_task_1', v.delay_dur)


def delay_after_reward_2(event):
    if event == "entry":
        print("delay_after_reward")
        timed_goto_state('choice_task_2', v.delay_dur)
    elif event == "exit":
        timed_goto_state('choice_task_2', v.delay_dur)


def choice_task_1(event):
    if event == 'entry':
        print('choice_phase')
        set_timer('port_lights_timer', v.state_choice_dur)
        set_timer('omission_choice', (v.state_choice_dur + v.LH_dur))
        hw.five_poke.poke_2.LED.on()
        hw.five_poke.poke_4.LED.on()
    elif event == 'exit':
        hw.five_poke.poke_2.LED.off()
        hw.five_poke.poke_4.LED.off()
        disarm_timer('omission_choice')
    elif event == 'poke_4':
        print('Correct_choice')
        goto_state('reward_choice')
    elif event == 'poke_2':
        print('incorrect_choice_lit')
        goto_state('penalty_choice')
    elif event == 'poke_1' or event == 'poke_3' or event == 'poke_5':
        print('Incorrect_choice')
        goto_state('penalty_choice')


def choice_task_2(event):
    if event == 'entry':
        print('choice_phase')
        set_timer('port_lights_timer', v.state_choice_dur)
        set_timer('omission_choice', (v.state_choice_dur + v.LH_dur))
        hw.five_poke.poke_2.LED.on()
        hw.five_poke.poke_4.LED.on()
    elif event == 'exit':
        hw.five_poke.poke_2.LED.off()
        hw.five_poke.poke_4.LED.off()
        disarm_timer('omission_choice')
    elif event == 'poke_2':
        print('Correct_choice')
        goto_state('reward_choice')
    elif event == 'poke_4':
        print('incorrect_choice_lit')
        goto_state('penalty_choice')
    elif event == 'poke_1' or event == 'poke_3' or event == 'poke_5':
        print('Incorrect_choice')
        goto_state('penalty_choice')


def reward_choice(event):
    if event == 'entry':    
        hw.reward_port.LED.on()
        hw.syringe_pump.backward(v.steps_rate_choice, v.n_steps_choice)
    elif event == 'exit':
        hw.reward_port.LED.off()
        disarm_timer('reward_in_timer')
    elif event == 'poke_6':
        print('reward_choice_taken')
        set_timer('reward_in_timer', v.reward_stimulation_dur)
    elif event == 'poke_6_out':
        goto_state('ITI_2')
    elif event == 'poke_1' or event == 'poke_2' or event == 'poke_3' or event == 'poke_4' or event == 'poke_5':
        print('perseverate')


def penalty_omission_sample(event):
    if event == 'entry':
        hw.BNC_1.off()
        print('penalty')
        hw.house_light.on()
        hw.reward_port.LED.off()
        timed_goto_state('ITI_1', v.penalty_dur)
    elif event == 'exit':
        hw.house_light.off()
    elif event == 'poke_1' or event == 'poke_2' or event == 'poke_3' or event == 'poke_4' or event == 'poke_5':
        print('attempts_dur_penalty_sample')


def penalty_omission_choice(event):
    if event == 'entry':
        print('penalty')
        hw.house_light.on()
        hw.reward_port.LED.off()
        timed_goto_state('ITI_1', v.penalty_dur)
    elif event == 'exit':
        hw.house_light.off()
    elif event == 'poke_1' or event == 'poke_2' or event == 'poke_3' or event == 'poke_4' or event == 'poke_5':
        print('attempts_dur_penalty_choice')


def penalty_sample(event):
    if event == 'entry':
        hw.house_light.on()
        hw.reward_port.LED.off()
        timed_goto_state('ITI_1', v.penalty_dur)
    elif event == 'exit':
        hw.house_light.off()
    elif event == 'poke_1' or event == 'poke_2' or event == 'poke_3' or event == 'poke_4' or event == 'poke_5':
        print('attempts_dur_penalty_sample')


def penalty_choice(event):
    if event == 'entry':
        hw.house_light.on()
        hw.reward_port.LED.off()
        timed_goto_state('ITI_1', v.penalty_dur)
    elif event == 'exit':
        hw.house_light.off()
    elif event == 'poke_1' or event == 'poke_2' or event == 'poke_3' or event == 'poke_4' or event == 'poke_5':
        print('attempts_dur_penalty_choice')


def ITI_1(event):
    if event == 'entry':
        print('iti_sample')
        timed_goto_state('sample_task', v.ITI_1_dur)
    elif event == 'poke_1' or event == 'poke_2' or event == 'poke_3' or event == 'poke_4' or event == 'poke_5':
        print('Premature_response')


def ITI_2(event):
    if event == 'entry':
        print('iti_sample')
        timed_goto_state('sample_task', v.ITI_2_dur)
    elif event == 'poke_1' or event == 'poke_2' or event == 'poke_3' or event == 'poke_4' or event == 'poke_5':
        print('Premature_response')


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
        goto_state('penalty_omission_sample')
    elif event == 'omission_choice':
        print('omission_choice')
        goto_state('penalty_omission_choice')
    elif event == 'poke_1' or event == 'poke_2' or event == 'poke_3' or event == 'poke_4' or event == 'poke_5':
        print('5_poke_entries')
    elif event == 'poke_6_out':
        print('receptacle_entries')

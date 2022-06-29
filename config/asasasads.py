# necessary imports to begin code

from pyControl.utility import *
import hardware_definition as hw
import random

target_port_list = ['1', '2', '3', '4', '5']
target_port_list_a = ['3', '4']
target_port_list_b = ['4', '5']
target_port_list_c = ['1', '5']
target_port_list_d = ['1', '2']
target_port_list_e = ['2', '3']

# list of states, for pyControl

states = ['start',
          'sample_task',
          'reward_choice',
          'reward_sample_1',
          'reward_sample_2',
          'reward_sample_3',
          'reward_sample_4',
          'reward_sample_5',
          'delay_1',
          'delay_2',
          'delay_3',
          'delay_4',
          'delay_5',
          'choice_task_1',
          'choice_task_2',
          'choice_task_3',
          'choice_task_4',
          'choice_task_5',
          'ITI',
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
          '1',
          '2',
          '3',
          '4',
          '5',
          '6',
          '7',
          '8',
          '9',
          '10',
          'kill_port_lights',
          'kill_reward',
          'omission_sample',
          'omission_choice']

initial_state = ('start')

v.session_duration = 30 * minute
v.steps_rate = 1000
v.steps_rate_choice = 2000
v.n_steps_choice = 2800
v.n_steps_sample = 250
v.state_dur = 20 * second
v.state_choice_dur = 20 * second
v.LH_dur = 1 * second
v.reward_stimulation_dur = 2 * second
v.ITI_dur = 5 * second
v.delay_dur = 2 * second
v.penalty_dur = 5 * second
v.target = 0
v.choice = 0
v.accuracy = 80
v.correct_per = 50
v.correct_num = 50
v.omission = 50


def run_start():
    set_timer('session_timer', v.session_duration)
    hw.reward_port.SOL.off()


def run_end():
    hw.off()
    hw.reward_port.SOL.off()


def start(event):
    if event == 'entry':
        hw.reward_port.LED.on()
        hw.syringe_pump.backward(v.steps_rate, v.n_steps_sample)
    elif event == 'exit':
        hw.reward_port.LED.off()
        disarm_timer('kill_reward')
    elif event == 'poke_6':
        set_timer('kill_reward', v.reward_stimulation_dur)
    elif event == 'poke_6_out':
        print('SP_reward : 10')
        goto_state('sample_task')


def sample_task(event):
    if event == 'entry':
        v.choice_time = get_current_time()
        set_timer('kill_port_lights', v.state_dur)
        set_timer('omission_sample', (v.state_dur + v.LH_dur))
        set_timer(random.choice(target_port_list), 0)
    elif event == 'exit':
        hw.five_poke.poke_1.LED.off()
        hw.five_poke.poke_2.LED.off()
        hw.five_poke.poke_3.LED.off()
        hw.five_poke.poke_4.LED.off()
        hw.five_poke.poke_5.LED.off()
        disarm_timer('kill_port_lights')
        disarm_timer('omission_sample')
    elif event == '1':
        v.target = 1
        hw.five_poke.poke_1.LED.on()
    elif event == '2':
        v.target = 2
        hw.five_poke.poke_2.LED.on()
    elif event == '3':
        v.target = 3
        hw.five_poke.poke_3.LED.on()
    elif event == '4':
        v.target = 4
        hw.five_poke.poke_4.LED.on()
    elif event == '5':
        v.target = 5
        hw.five_poke.poke_5.LED.on()
    elif event == 'poke_1' and v.target == 1:
        print('Correct_sample')
        goto_state('reward_sample_1')
    elif event == 'poke_2' and v.target == 2:
        print('Correct_sample')
        goto_state('reward_sample_2')
    elif event == 'poke_3' and v.target == 3:
        print('Correct_sample')
        goto_state('reward_sample_3')
    elif event == 'poke_4' and v.target == 4:
        print('Correct_sample')
        goto_state('reward_sample_4')
    elif event == 'poke_5' and v.target == 5:
        print('Correct_sample')
        goto_state('reward_sample_5')
    elif event == 'poke_1' and v.target != 1 or event == 'poke_2' and v.target != 2 \
            or event == 'poke_3' and v.target != 3 or event == 'poke_4' and v.target != 4 \
            or event == 'poke_5' and v.target != 5:
        Incorrect_latency_sample = get_current_time() - v.choice_time
        print("Incorrect_latency_sample: {}".format(Incorrect_latency_sample))
        print('Incorrect_sample')
        goto_state('penalty_sample')

def reward_sample_1(event):
    if event == 'entry':
        hw.reward_port.LED.on()
        hw.syringe_pump.backward(v.steps_rate, v.n_steps_sample)
    elif event == 'exit':
        hw.reward_port.LED.off()
        disarm_timer('kill_reward')
    elif event == 'poke_6':
        set_timer('kill_reward', v.reward_stimulation_dur)
    elif event == 'poke_6_out':
        goto_state('delay_1')
    elif event == 'poke_1':
        print('perseverate_sample')

def reward_sample_2(event):
    if event == 'entry':
        hw.reward_port.LED.on()
        hw.syringe_pump.backward(v.steps_rate, v.n_steps_sample)
    elif event == 'exit':
        hw.reward_port.LED.off()
        disarm_timer('kill_reward')
    elif event == 'poke_6':
        set_timer('kill_reward', v.reward_stimulation_dur)
    elif event == 'poke_6_out':
        goto_state('delay_2')
    elif event == 'poke_2':
        print('perseverate_sample')

def reward_sample_3(event):
    if event == 'entry':
        hw.reward_port.LED.on()
        hw.syringe_pump.backward(v.steps_rate, v.n_steps_sample)
    elif event == 'exit':
        hw.reward_port.LED.off()
        disarm_timer('kill_reward')
    elif event == 'poke_6':
        set_timer('kill_reward', v.reward_stimulation_dur)
    elif event == 'poke_6_out':
        goto_state('delay_3')
    elif event == 'poke_3':
        print('perseverate_sample')

def reward_sample_4(event):
    if event == 'entry':
        hw.reward_port.LED.on()
        hw.syringe_pump.backward(v.steps_rate, v.n_steps_sample)
    elif event == 'exit':
        hw.reward_port.LED.off()
        disarm_timer('kill_reward')
    elif event == 'poke_6':
        set_timer('kill_reward', v.reward_stimulation_dur)
    elif event == 'poke_6_out':
        goto_state('delay_4')
    elif event == 'poke_4':
        print('perseverate_sample')

def reward_sample_5(event):
    if event == 'entry':
        hw.reward_port.LED.on()
        hw.syringe_pump.backward(v.steps_rate, v.n_steps_sample)
    elif event == 'exit':
        hw.reward_port.LED.off()
        disarm_timer('kill_reward')
    elif event == 'poke_6':
        set_timer('kill_reward', v.reward_stimulation_dur)
    elif event == 'poke_6_out':
        goto_state('delay_5')
    elif event == 'poke_5':
        print('perseverate_sample')


def delay_1(event):
    if event == "entry":
        timed_goto_state('choice_task_1', v.delay_dur)
    elif event == 'poke_1':
        print('Premature_choice_correct')
    elif event == 'poke_2' or event == 'poke_3' or event == 'poke_4' or event == 'poke_5':
        print('Premature_choice_incorrect')
    elif event == "exit":
        timed_goto_state('choice_task_1', v.delay_dur)


def delay_2(event):
    if event == "entry":
        timed_goto_state('choice_task_2', v.delay_dur)
    elif event == 'poke_2':
        print('Premature_choice_correct')
    elif event == 'poke_1' or event == 'poke_3' or event == 'poke_4' or event == 'poke_5':
        print('Premature_choice_incorrect')
    elif event == "exit":
        timed_goto_state('choice_task_2', v.delay_dur)


def delay_3(event):
    if event == "entry":
        timed_goto_state('choice_task_3', v.delay_dur)
    elif event == 'poke_3':
        print('Premature_choice_correct')
    elif event == 'poke_1' or event == 'poke_2' or event == 'poke_4' or event == 'poke_5':
        print('Premature_choice_incorrect')
    elif event == "exit":
        timed_goto_state('choice_task_3', v.delay_dur)

def delay_4(event):
    if event == "entry":
        timed_goto_state('choice_task_4', v.delay_dur)
    elif event == 'poke_4':
        print('Premature_choice_correct')
    elif event == 'poke_1' or event == 'poke_2' or event == 'poke_3' or event == 'poke_5':
        print('Premature_choice_incorrect')
    elif event == "exit":
        timed_goto_state('choice_task_4', v.delay_dur)


def delay_5(event):
    if event == "entry":
        timed_goto_state('choice_task_5', v.delay_dur)
    elif event == 'poke_5':
        print('Premature_choice_correct')
    elif event == 'poke_1' or event == 'poke_2' or event == 'poke_3' or event == 'poke_4':
        print('Premature_choice_incorrect')
    elif event == "exit":
        timed_goto_state('choice_task_5', v.delay_dur)

def choice_task_1(event):
    if event == 'entry':
        v.choice_time = get_current_time()
        set_timer('kill_port_lights', v.state_choice_dur)
        set_timer('omission_choice', (v.state_choice_dur + v.LH_dur))
        hw.five_poke.poke_1.LED.on()
        set_timer(random.choice(target_port_list_a), 0)
    elif event == 'exit':
        hw.five_poke.poke_1.LED.off()
        hw.five_poke.poke_3.LED.off()
        hw.five_poke.poke_4.LED.off()
        disarm_timer('omission_choice')
    elif event == '3':
        v.choice = 8
        hw.five_poke.poke_3.LED.on()
    elif event == '4':
        v.choice = 9
        hw.five_poke.poke_4.LED.on()
    elif event == 'poke_3' and v.choice == 8 or event == 'poke_4' and v.choice == 9:
        print('incorrect_choice_lit')
        goto_state('penalty_choice')
    elif event == 'poke_1':
        print('Correct_choice')
        goto_state('reward_choice')
    elif event == 'poke_2' or event == 'poke_5' or event == 'poke_3' and v.choice != 8 \
            or event == 'poke_4' and v.choice != 9:
        print('Incorrect_choice')
        goto_state('penalty_choice')


def choice_task_2(event):
    if event == 'entry':
        v.choice_time = get_current_time()
        set_timer('kill_port_lights', v.state_choice_dur)
        set_timer('omission_choice', (v.state_choice_dur + v.LH_dur))
        hw.five_poke.poke_2.LED.on()
        set_timer(random.choice(target_port_list_b), 0)
    elif event == 'exit':
        hw.five_poke.poke_2.LED.off()
        hw.five_poke.poke_4.LED.off()
        hw.five_poke.poke_5.LED.off()
        disarm_timer('omission_choice')
    elif event == '4':
        v.choice = 9
        hw.five_poke.poke_4.LED.on()
    elif event == '5':
        v.choice = 10
        hw.five_poke.poke_5.LED.on()
    elif event == 'poke_4' and v.choice == 9 or event == '5' and v.choice == 10:
        print('incorrect_choice_lit')
        goto_state('penalty_choice')
    elif event == 'poke_2':
        print('Correct_choice')
        goto_state('reward_choice')
    elif event == 'poke_1' or event == 'poke_3' or event == 'poke_4' and v.choice != 9 \
            or event == '5' and v.choice != 10:
        print('Incorrect_choice')
        goto_state('penalty_choice')


def choice_task_3(event):
    if event == 'entry':
        v.choice_time = get_current_time()
        set_timer('kill_port_lights', v.state_choice_dur)
        set_timer('omission_choice', (v.state_choice_dur + v.LH_dur))
        hw.five_poke.poke_3.LED.on()
        set_timer(random.choice(target_port_list_c), 0)
    elif event == 'exit':
        hw.five_poke.poke_3.LED.off()
        hw.five_poke.poke_5.LED.off()
        hw.five_poke.poke_1.LED.off()
        disarm_timer('omission_choice')
    elif event == '1':
        v.choice = 6
        hw.five_poke.poke_1.LED.on()
    elif event == '5':
        v.choice = 10
        hw.five_poke.poke_5.LED.on()
    elif event == 'poke_1' and v.choice == 6 or event == 'poke_5' and v.choice == 10:
        print('incorrect_choice_lit')
        goto_state('penalty_choice')
    elif event == 'poke_3':
        print('Correct_choice')
        goto_state('reward_choice')
    elif event == 'poke_2' or event == 'poke_4' or event == 'poke_1' and v.choice != 6 \
            or event == 'poke_5' and v.choice != 10:
        print('Incorrect_choice')
        goto_state('penalty_choice')


def choice_task_4(event):
    if event == 'entry':
        v.choice_time = get_current_time()
        set_timer('kill_port_lights', v.state_choice_dur)
        set_timer('omission_choice', (v.state_choice_dur + v.LH_dur))
        hw.five_poke.poke_4.LED.on()
        set_timer(random.choice(target_port_list_d), 0)
    elif event == 'exit':
        hw.five_poke.poke_4.LED.off()
        hw.five_poke.poke_2.LED.off()
        hw.five_poke.poke_1.LED.off()
        disarm_timer('omission_choice')
    elif event == '2':
        v.choice = 7
        hw.five_poke.poke_2.LED.on()
    elif event == '1':
        v.choice = 6
        hw.five_poke.poke_1.LED.on()
    elif event == 'poke_2' and v.choice == 7 or event == 'poke_1' and v.choice == 6:
        print('incorrect_choice_lit')
        goto_state('penalty_choice')
    elif event == 'poke_4':
        print('Correct_choice')
        goto_state('reward_choice')
    elif event == 'poke_3' or event == 'poke_5' or event == 'poke_2' and v.choice != 7 \
            or event == 'poke_1' and v.choice != 6:
        print('Incorrect_choice')
        goto_state('penalty_choice')


def choice_task_5(event):
    if event == 'entry':
        v.choice_time = get_current_time()
        set_timer('kill_port_lights', v.state_choice_dur)
        set_timer('omission_choice', (v.state_choice_dur + v.LH_dur))
        hw.five_poke.poke_5.LED.on()
        set_timer(random.choice(target_port_list_e), 0)
    elif event == 'exit':
        hw.five_poke.poke_5.LED.off()
        hw.five_poke.poke_3.LED.off()
        hw.five_poke.poke_2.LED.off()
        disarm_timer('omission_choice')
    elif event == '3':
        v.choice = 8
        hw.five_poke.poke_3.LED.on()
    elif event == '2':
        v.choice = 7
        hw.five_poke.poke_2.LED.on()
    elif event == 'poke_3' and v.choice == 8 or event == 'poke_2' and v.choice == 7:
        print('incorrect_choice_lit')
        goto_state('penalty_choice')
    elif event == 'poke_5':
        print('Correct_choice')
        goto_state('reward_choice')
    elif event == 'poke_1' or event == 'poke_4' or event == 'poke_3' and v.choice != 8 \
            or event == 'poke_2' and v.choice != 7:
        print('Incorrect_choice')
        goto_state('penalty_choice')


def reward_choice(event):
    if event == 'entry':
        hw.reward_port.LED.on()
        hw.syringe_pump.backward(v.steps_rate_choice, v.n_steps_choice)
    elif event == 'exit':
        hw.reward_port.LED.off()
        disarm_timer('kill_reward')
    elif event == 'poke_6':
        set_timer('kill_reward', v.reward_stimulation_dur)
    elif event == 'poke_6_out':
        goto_state('ITI')
    elif event == 'poke_1' or event == 'poke_2' or event == 'poke_3' or event == 'poke_4' or event == 'poke_5':
        print('perseverate')


def penalty_omission_sample(event):
    if event == 'entry':
        print('penalty')
        hw.reward_port.SOL.on()
        hw.reward_port.LED.off()
        timed_goto_state('ITI', v.penalty_dur)
    elif event == 'exit':
        hw.reward_port.SOL.off()
    elif event == 'poke_1' or event == 'poke_2' or event == 'poke_3' or event == 'poke_4' or event == 'poke_5':
        print('attempts_dur_penalty_sample')


def penalty_omission_choice(event):
    if event == 'entry':
        print('penalty')
        hw.reward_port.SOL.on()
        hw.reward_port.LED.off()
        timed_goto_state('ITI', v.penalty_dur)
    elif event == 'exit':
        hw.reward_port.SOL.off()
    elif event == 'poke_1' or event == 'poke_2' or event == 'poke_3' or event == 'poke_4' or event == 'poke_5':
        print('attempts_dur_penalty_choice')


def penalty_sample(event):
    if event == 'entry':
        hw.reward_port.SOL.on()
        hw.reward_port.LED.off()
        timed_goto_state('ITI', v.penalty_dur)
    elif event == 'exit':
        hw.reward_port.SOL.off()
    elif event == 'poke_1' or event == 'poke_2' or event == 'poke_3' or event == 'poke_4' or event == 'poke_5':
        print('attempts_dur_penalty_sample')


def penalty_choice(event):
    if event == 'entry':
        hw.reward_port.SOL.on()
        hw.reward_port.LED.off()
        timed_goto_state('ITI', v.penalty_dur)
    elif event == 'exit':
        hw.reward_port.SOL.off()
    elif event == 'poke_1' or event == 'poke_2' or event == 'poke_3' or event == 'poke_4' or event == 'poke_5':
        print('attempts_dur_penalty_choice')


def ITI(event):
    if event == 'entry':
        v.iti_start_time = get_current_time()
        timed_goto_state('sample_task', v.ITI_dur)
    elif event == 'poke_1' or event == 'poke_2' or event == 'poke_3' or event == 'poke_4' or event == 'poke_5':

        print('Premature_response')


def all_states(event):
    if event == 'session_timer':
        print("Event Closing")
        stop_framework()
    elif event == 'kill_port_lights':
        hw.five_poke.poke_1.LED.off()
        hw.five_poke.poke_2.LED.off()
        hw.five_poke.poke_3.LED.off()
        hw.five_poke.poke_4.LED.off()
        hw.five_poke.poke_5.LED.off()
    elif event == 'kill_reward':
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

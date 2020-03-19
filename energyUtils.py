
from lorawan_toa.lorawan_toa import get_toa
from mathUtils import *

import math

power_dbm_to_mA = [(0, 22), (1, 23), (2, 24), (3, 24), (4, 24), (5, 25), (6, 25),
                    (7, 25), (8, 25),(9, 26),(10, 31),(11, 32), (12, 34), (13, 35), (14, 44), 
                    (15, 82), (16, 85), (17, 90), (18, 105), (19, 115), (20, 125)]

current_sleep_mA_semtech = 0.0000001
current_idle_mA_semtech = current_sleep_mA_semtech
current_receive_mA_semtech = 2.521


current_sleep_mA_paper = 0.0008230
current_idle_mA_paper = 0.0012816
current_receive_mA_paper = 14.28

current_sleep_mA = current_sleep_mA_paper
current_idle_mA = current_idle_mA_paper
current_receive_mA = current_receive_mA_paper

time_sleep_1_window_ms = 1000 # is the time in sleep mode of the first windows of receive
time_receive_1_window_ms = 500 # is the time in receive mode of the first windows of receive
time_sleep_2_window_ms = 1000 # is the time in sleep mode of the secound windows of receive
time_receive_2_window_ms = 500 # is the time in receive mode of the secound windows of receive
voltage_supply = 3.3
time_idle_1_window_ms = 1000

def packageWorkCalculator(time_on_air, power_in_dbm, mode = 'tx_rx_rx'):
    '''
    Parameters
        time_on_air: time of the packet in ms
        power: power of transmission in dBm

    Return:
        Work used in miliJoule
    '''
    power_in_W = -1

    for a,b in power_dbm_to_mA:
        if a == power_in_dbm:
            power_in_W = (b/1000)*3.3

    if power_in_W == -1:
        print ("ERROR: The power: %d dBm is not programmed" % power_in_dbm)
        exit(-1)

    joule_tx = jouleCalculator(power_in_W, time_on_air/1000)["mJ"]

    joule_idle = jouleCalculator((current_idle_mA/1000)*3.3, (time_idle_1_window_ms)/1000)["mJ"] #have 2 windows
    joule_rx = jouleCalculator((current_receive_mA/1000)*3.3, (time_receive_1_window_ms)/1000)["mJ"] #have 2 windows

    if mode == 'tx_rx_rx':

        return joule_tx + 2*joule_idle + 2*joule_rx
    elif mode == 'tx_rx':
        return joule_tx + joule_idle + joule_rx
    else:
        print("ERROR: mode isn't implemented")
            

def workInBaterry(voltage, current_mAh):
    '''
    Parameters
        voltage: is the voltage suppled by the battery
        current_mAh: is the equivalent current that a battery could supply in 1 hour
    Return 
        is the total energy provided in Joules
    '''   
    
    work_J = jouleCalculator(voltage*(current_mAh/1000), 60*60)['J']
    return work_J

def lifeTimeWorkCalculator(life_time_sec, time_to_send_a_tx_ms, tx_power_in_dbm, number_of_package, mode = 'tx_rx_rx'):
    '''
    Parameters
        life_time_sec: is the time that should be calculated the energy expended by the device
        time_to_send_a_tx_ms: is the TOA on tx mode in milisecond
        tx_power_in_dbm: is the tx power in dbm
        number_of_package: is the number of packages sended in the life_time_in_sec
    Return
        is the total of energy expended in Joule
    '''

    

    def workInTx():
        
        time_in_tx_mode_sec = (time_to_send_a_tx_ms/1000)*number_of_package
        for dbm, current_mA in power_dbm_to_mA:
            if dbm == tx_power_in_dbm:
                power_in_W = powerCalculator(current_mA, voltage_supply)['W']
        
        work_in_tx_J = jouleCalculator(power_in_W, time_in_tx_mode_sec)['J']
        return work_in_tx_J, time_in_tx_mode_sec

    def workInIdle(time_in_idle_sec):
        power_idle_W = powerCalculator(current_idle_mA, voltage_supply)['W']
        work_in_idle_J = jouleCalculator(power_idle_W, time_in_idle_sec)['J']
        return work_in_idle_J

    def workInRxWindow(time_receive_window_ms, time_sleep_window_ms):

        power_sleep_W = powerCalculator(current_sleep_mA, voltage_supply)['W']
        power_receive_W = powerCalculator(current_receive_mA, voltage_supply)['W']
        
        work_in_rec_J = jouleCalculator(power_receive_W, (time_receive_window_ms/1000)*number_of_package)['J']
        work_in_sleep_J = jouleCalculator(power_sleep_W, (time_sleep_window_ms/1000)*number_of_package)['J']

        time_in_window = (time_receive_window_ms/1000)*number_of_package + (time_sleep_window_ms/1000)*number_of_package
        
        return (work_in_rec_J + work_in_sleep_J), time_in_window


    if mode == 'tx':
        tx_work, tx_time = workInTx() 
        total_work = tx_work + workInIdle(life_time_sec - tx_time)

    elif mode == 'tx_rx':
        # here need be implemented the transmission with one window of receiver
        tx_work, tx_time = workInTx() 
        rx_work, rx_time = workInRxWindow(time_receive_1_window_ms, time_sleep_1_window_ms)
        total_work = tx_work + rx_work + workInIdle(life_time_sec - (tx_time + rx_time ))

    elif mode == 'tx_rx_rx':
        # here need be implemented the transmission with two window of receiver
        tx_work, tx_time = workInTx() 
        rx_work_first_window, rx_time_first_window = workInRxWindow(time_receive_1_window_ms, time_sleep_1_window_ms)
        rx_work_second_window, rx_time_second_window = workInRxWindow(time_receive_2_window_ms, time_sleep_2_window_ms)
        total_work = tx_work + rx_work_first_window + rx_work_second_window + workInIdle(life_time_sec - (tx_time + rx_time_first_window + rx_time_second_window ))
    
    return total_work
    
def batteryTimeOfLife(joules, messages_in_day, time_to_send_a_tx_ms, tx_power_in_dbm, transmission_mode = "tx"):
    '''
    Parameters
        joules: Is the amount of work in a battery
        messages_in_day: is the number of messages sended in a day
        time_to_send_a_tx_ms: is the TOA on tx mode in milisecond
        tx_power_in_dbm: is the tx power in dbm
        transmission_mode = 
    Return 
        return the number of days that a battery could supply energy
         send a specific number of messages a day
    '''

    work_in_day = lifeTimeWorkCalculator(24*60*60, time_to_send_a_tx_ms, tx_power_in_dbm, messages_in_day, mode = transmission_mode)
    return (joules/work_in_day), work_in_day
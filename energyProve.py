import sys
sys.path.append("..")

import matplotlib.pyplot as plt
from lorawan_toa.lorawan_toa import get_toa
#from lorawan_toa.lorawan_toa import mpsrange

calc_semtech_power_mw = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
calc_semtech_power_dbm = [22, 23, 24, 24, 24, 25, 25, 25, 25, 26, 31, 32, 34, 35, 44, 82, 85, 90, 105, 115, 125]

power_dbm_to_mA = [(0, 22), (7, 25), (14, 44), (20, 125)]

voltage_supply = 3.3

def plotCalcSemtechPower_mA_by_dbm():
    plt.plot(calc_semtech_power_mw, calc_semtech_power_dbm)
    plt.xlabel('power in mA')
    plt.ylabel('power in dBm')
    plt.show()

def energyCalculator(time_on_air, power_in_dbm):
    '''
    Parameters
        time_on_air: time of the packet in ms
        power: power of transmission in dBm

    Return:
        Energy used in miliJoule
    '''
    power_in_W = -1

    for a,b in power_dbm_to_mA:
        if a == power_in_dbm:
            power_in_W = (b/1000)*3.3

    if power_in_W == -1:
        print ("ERROR: The power: %d dBm is not programmed" % power_in_dbm)
        exit(-1)

    miliJoule = power_in_W*time_on_air

    return miliJoule

if __name__== "__main__":
    ret = get_toa(9, 7)

    print ("r_sym: symbol rate in *second* : %d" % ret["r_sym"])
    print ("t_sym: the time on air in millisecond*. : %d" % ret["t_sym"])
    print ("t_preamble: : %d" % ret["t_preamble"])
    print ("v_ceil: : %d" % ret["v_ceil"])
    print ("symbol_size_payload: : %d" % ret["n_sym_payload"])
    print ("t_payload: : %d" % ret["t_payload"])
    print ("t_packet: the time on air in *milisecond*. : %d" % ret["t_packet"])

    print ("Power in miliJoule is: %f" % energyCalculator(ret["t_packet"], 14))
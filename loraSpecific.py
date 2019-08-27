import math
from mathUtils import *
from linkBudget import *

snr_per_sf_datasheet = [(7, -7.5), (8, -10), (9, -12.5), (10, -15), (11, -17.5), (12, -20)] #extraxt from datasheet
snr_qsf_raza_125bw = [(7, -6), (8, -9), (9, -12), (10, -15), (11, -17.5), (12, -20)] #extraxt from raza

snr_per_sf = snr_qsf_raza_125bw 

#this variable is how many times the SFx use TOA more than SF7 
time_on_air_in_reference_sf7_list = [24.033195, 13.104072, 7.203980, 3.601990, 1.800995, 1.000000]

last_distance_of_sf = [2000, 4000, 6000, 8000, 10000, 12000]
#last_distance_of_sf = [2200, 3000, 4000, 5000, 6000, 7800]
sfs = ["SF7", "SF8", "SF9", "SF10", "SF11", "SF12"]

last_distance_90_percent_DER_H1_per_sf = [1755, 2280, 2930, 3775, 4661, 5754]
last_distance_80_percent_DER_H1_per_sf = [2271, 2926, 3825, 4917, 6059, 7516]

devices_in_each_sf = [0]*6
def getSF(distance, max_radius, method , number_of_devices):

    sf = "SF0"
    int_sf = 0

    if method == "RADIAL":
        sf_base = int(distance/(max_radius/6))
        sf = sfs[sf_base if sf_base<6 else 5]
        int_sf = sf_base + 7
    
    elif method == "SAME_TIME_ON_AIR":
        #this method try set the sum of time on air of all devices equal
        sf = "SF12"
        int_sf = 12
        max_distance_per_sf = last_distance_90_percent_DER_H1_per_sf
        sum_total_time = sum(time_on_air_in_reference_sf7_list)
        for sf_base in range(6):
            #is number total of SF 
            sf_device_time_on_air = round(number_of_devices*(time_on_air_in_reference_sf7_list[sf_base]/sum_total_time))
            if distance < max_distance_per_sf[sf_base]:
                if devices_in_each_sf[sf_base] < sf_device_time_on_air:
                    devices_in_each_sf[sf_base] = devices_in_each_sf[sf_base] + 1
                    sf = sfs[sf_base if sf_base<6 else 5]
                    int_sf = sf_base + 7
                    break
    #    print(percent_time_on_air)
    #    print(devices_time_on_air)
    return [sf, int_sf]


def loraSensitivity(sf, bw):
    """
    Considering a package of 25 bytes
    Parameters
        sf: sf desired from 7 to 12
        bw: the bandwidth used, normally (125000, 250000, 500000)
    """
    NF = 6

    for sf_base, snr in snr_per_sf:
        if sf == sf_base:
            sensitivity = -174 + 10*math.log10(bw) + NF + snr
    
    return sensitivity

def SNR_qsf_linear(sf):
    """
    SNR = 10.^([ -6, -9, -12, -15, -17.5, -20 ]./10);
    """

    for sf_base, snr in snr_qsf_raza_125bw:
        if sf == sf_base:
            SNR_linear = 10**(snr/10)
    return SNR_linear
    
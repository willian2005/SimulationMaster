import math
from mathUtils import *
from linkBudget import *
from loraTheoricalSimulation import P1TheoricalFromH1
from loraTheoricalSimulation import P1TheoricalFromH1MultGatewayDiversity
from loraUtils import *

#this variable is how many times the SFx use TOA more than SF7 
time_on_air_in_reference_sf7_list = [24.033195, 13.104072, 7.203980, 3.601990, 1.800995, 1.000000]

last_distance_of_sf = [2000, 4000, 6000, 8000, 10000, 12000]
#last_distance_of_sf = [2200, 3000, 4000, 5000, 6000, 7800]
sfs = ["SF7", "SF8", "SF9", "SF10", "SF11", "SF12"]

#last_distance_90_percent_DER_H1_per_sf = [1755, 2280, 2930, 3775, 4661, 5754]
#last_distance_80_percent_DER_H1_per_sf = [2271, 2926, 3825, 4917, 6059, 7516]

devices_in_each_sf = [0]*6
def getSF(distance, max_radius, method , number_of_devices, n, h1_target = 0.9, power = 14, h1_mult_gateway_diversity = False, number_of_gateways = 1):

    sf = "SF0"
    int_sf = 0

    if method == "RADIAL":
        sf_base = int(distance/(max_radius/6))
        sf = sfs[sf_base if sf_base<6 else 5]
        int_sf = sf_base + 7


    elif method == "SAME_TIME_ON_AIR" or method == "SAME_TIME_ON_AIR_BY_GATEWAY" or method == "JUST_POWER_ADR":
        sf = "SF12"
        int_sf = 12
        sum_total_time = sum(time_on_air_in_reference_sf7_list)
        for sf_base in range(6):
            #is number total of SF 
            sf_device_time_on_air = round(number_of_devices*(time_on_air_in_reference_sf7_list[sf_base]/sum_total_time))
            
            if method == "SAME_TIME_ON_AIR_BY_GATEWAY":
                sf_device_time_on_air = sf_device_time_on_air*number_of_gateways
            
            if method == "JUST_POWER_ADR":
                sf_device_time_on_air = sf_device_time_on_air*99999

            if devices_in_each_sf[sf_base] < sf_device_time_on_air:
                if h1_mult_gateway_diversity == True:
                    power_from_h1 = P1TheoricalFromH1MultGatewayDiversity(h1_target, (sf_base+7), distance, n)
                else:
                    power_from_h1 = P1TheoricalFromH1(h1_target, (sf_base+7), distance, n)

                if  power_from_h1 <= power:
                    devices_in_each_sf[sf_base] = devices_in_each_sf[sf_base] + 1
                    sf = sfs[sf_base]
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

    
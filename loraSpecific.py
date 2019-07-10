import math

snr_per_sf_datasheet = [(7, -7.5), (8, -10), (9, -12.5), (10, -15), (11, -17.5), (12, -20)] #extraxt from datasheet
snr_qsf_raza_125bw = [(7, -6), (8, -9), (9, -12), (10, -15), (11, -17.5), (12, -20)] #extraxt from raza

snr_per_sf = snr_qsf_raza_125bw 


last_distance_of_sf = [2000, 4000, 6000, 8000, 10000, 12000]
#last_distance_of_sf = [2200, 3000, 4000, 5000, 6000, 7800]
sfs = ["SF7", "SF8", "SF9", "SF10", "SF11", "SF12"]

def getSF(distance, max_radius):

    sf = "SF0"
    int_sf = 0

    sf = sfs[int(distance/(max_radius/6))]
    int_sf = int(distance/(max_radius/6)) + 7
    print("SF - %s int sf - %d - distance - %d"%(sf, int_sf, distance))
    """
    for i in range(len(last_distance_of_sf)):
        if distance < last_distance_of_sf[i]:
            sf = sfs[i]
            int_sf = 7+i
            break
    if distance > last_distance_of_sf[-1]:
        sf =  "SF12"
        int_sf = 12  
    """
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
    
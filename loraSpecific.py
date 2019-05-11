import math

snr_per_sf_datasheet = [(7, -7.5), (8, -10), (9, -12.5), (10, -15), (11, -17.5), (12, -20)] #extraxt from datasheet
snr_qsf_raza_125bw = [(7, -6), (8, -9), (9, -12), (10, -15), (11, -17.5), (12, -20)] #extraxt from raza

snr_per_sf = snr_qsf_raza_125bw 

def getSF(distance):

    if distance < 2000:
        sf = "SF7"
    elif distance < 4000: 
        sf = "SF8"
    elif distance < 6000:
        sf = "SF9"
    elif distance < 8000:
        sf = "SF10"
    elif distance < 10000:
        sf = "SF11"
    else:
        sf = "SF12"

    return sf
    
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
    
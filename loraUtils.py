snr_per_sf_datasheet = [(7, -7.5), (8, -10), (9, -12.5), (10, -15), (11, -17.5), (12, -20)] #extraxt from datasheet
snr_qsf_raza_125bw = [(7, -6), (8, -9), (9, -12), (10, -15), (11, -17.5), (12, -20)] #extraxt from raza

snr_per_sf = snr_qsf_raza_125bw 

def SNR_qsf_linear(sf):
    """
    SNR = 10.^([ -6, -9, -12, -15, -17.5, -20 ]./10);
    """

    for sf_base, snr in snr_per_sf:
        if sf == sf_base:
            SNR_linear = 10**(snr/10)
    return SNR_linear
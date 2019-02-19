import sys
sys.path.append("..")

import matplotlib.pyplot as plt
from lorawan_toa.lorawan_toa import get_toa

calc_semtech_power_mw = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
calc_semtech_power_dbm = [22, 23, 24, 24, 24, 25, 25, 25, 25, 26, 31, 32, 34, 35, 44, 82, 85, 90, 105, 115, 125]

def plotCalcSemtechPower_mA_by_dbm():
    plt.plot(calc_semtech_power_mw, calc_semtech_power_dbm)
    plt.xlabel('power in mA')
    plt.ylabel('power in dBm')
    plt.show()

#def timeInSpectrum(self, dr, bytes, region):

if __name__== "__main__":
    ret = get_toa(20, 7)
    print ("PHY payload size    : Bytes",  ret["phy_pl_size"])

    """
    print ("MAC payload size    : %d Bytes" % ret["mac_pl_size"])
    print ("Spreading Factor    : %d" % ret["sf"])
    print ("Band width          : %d kHz" % ret["bw"])
    print ("Low data rate opt.  : %s" % ret["ldro"])
    print ("Explicit header     : %s" % ret["eh"])
    print ("CR (coding rate)    : %d (4/%d)" % (ret["cr"], 4+ret["cr"]))
    print ("Symbol Rate         : %.3f symbol/s" % ret["r_sym"])
    print ("Symbol Time         : %.3f msec/symbol" % ret["t_sym"])
    print ("Preamble size       : %d symbols" % ret["preamble"])
    print ("Packet symbol size  : %d symbols" % ret["n_sym_payload"])
    print ("Preamble ToA        : %.3f msec" % ret["t_preamble"])
    print ("Payload ToA         : %.3f msec" % ret["t_payload"])
    print ("Time on Air         : %.3f msec" % ret["t_packet"])
    print ("Duty Cycle          : %d %%" % ret["duty_cycle"])
    print ("Min span of a cycle : %.3f sec" % ret["t_cycle"])
    print ("Max Frames per day  : %d frames" % ret["max_packets_day"])
    plotCalcSemtechPower_mA_by_dbm()
"""
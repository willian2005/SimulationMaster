import math

def jouleCalculator(power_in_w, time_in_s):
    
    ret = {}
    ret["J"] = power_in_w*time_in_s 
    ret["mJ"] = power_in_w*time_in_s*1000 
    return ret

def powerCalculator(current_mA, voltage):

    ret = {}
    ret["W"] = (current_mA/1000)*voltage
    ret["mW"] = current_mA*voltage
    return ret

def varianceWhiteNoise(bw = 125000, noise_figure = 6):
    """
    Parameters:
        bw: bandwidth in Hz

    """
    noise = (10**((-204+noise_figure+(10*math.log10(bw)))/10)) #;  % Watts^2 - Variance of Additive White Gaussian Noise
    return noise
    
# Function to convert from mW to dBm
def mW2dBm(mW):
    return 10.*math.log10(mW)

# Function to convert from dBm to mW
def dBm2mW(dBm):
    return 10**((dBm)/10.)
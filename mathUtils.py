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
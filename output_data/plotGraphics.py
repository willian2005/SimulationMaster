import matplotlib.pyplot as plt

from CYCLES_1000_PER_INTERACTION_1000_Gx_4000_Gy_12000 import *
from CYCLES_1000_PER_INTERACTION_1000_Gx_6000_Gy_12000 import *
from CYCLES_1000_PER_INTERACTION_1000_Gx_8000_Gy_12000 import *
from CYCLES_1000_PER_INTERACTION_1000_Gx_10000_Gy_12000 import *
from CYCLES_1000_PER_INTERACTION_1000_Gx_12000_Gy_12000 import *


def plotGraphicsTogether():


    plt.plot(distances_gx_12000_gy_12000, q1sm_gx_12000_gy_12000, "b-" , label="Q1 - GW_12000_12000", linewidth=1)
    plt.plot(distances_gx_10000_gy_12000, q1sm_gx_10000_gy_12000, "g-" , label="Q1 - GW_10000_12000", linewidth=1)
    plt.plot(distances_gx_8000_gy_12000, q1sm_gx_8000_gy_12000, "m-" , label="Q1 - GW_8000_12000", linewidth=1)
    plt.plot(distances_gx_6000_gy_12000, q1sm_gx_6000_gy_12000, "r-" , label="Q1 - GW_6000_12000", linewidth=1)
    plt.plot(distances_gx_4000_gy_12000, q1sm_gx_4000_gy_12000, "y-" , label="Q1 - GW_4000_12000", linewidth=1)

    plt.ylim(0, 1.1)
    plt.legend(loc='upper right')
    plt.savefig("plotQ1Together.png")
    plt.show()


if __name__== "__main__":
    
    plotGraphicsTogether()

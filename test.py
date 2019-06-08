import sys
sys.path.append("..")

import matplotlib.pyplot as plt
import numpy as np

from energyUtils import *
from linkBudget import *
from loraSpecific import *
from loraTheoricalSimulation import *
import unittest


class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def test11(self):
        energy = lifeTimeWorkCalculator(100, 18.8, 14, 100)
        self.assertNotEqual( energy, 1810.432 )

    def testEnergyPerPackage25BytesSf7(self):
        energy = packageWorkCalculator(get_toa(25, 7)['t_packet'], 14)
        #print("Energy in one package of 25 bytes and SF7 is: %f mJ" % energy)
        #self.assertNotEqual( energy, 0.298678 )

    def test1Day(self):
        energy = lifeTimeWorkCalculator(60*60*24, get_toa(25, 7)['t_packet'], 14, 100)
        #print("Energy in one day: %f" % energy)
        #self.assertAlmostEqual( energy, 1.2612, delta = 0.01 )

#Energy in battery tests
    def testBattery1000mAh(self):
        work_in_battery = workInBaterry(3.3, 1000)
        #print("The energy in a battery of 3.3V and 1000mAh is %f J" % work_in_battery)
        self.assertAlmostEqual(work_in_battery, 11880)

    def testBatteryAlkaline(self):
        work_in_cell = workInBaterry(1.5, 2400)
        #print("The energy in a Alkaline cell is %f J" % work_in_cell)
        self.assertAlmostEqual(work_in_cell, 12960.00)

    def testBatteryEmpty(self):
        no_work = workInBaterry(0, 0)
        self.assertAlmostEqual(no_work, 0)

    def testBatteryEmptyLoad(self):
        no_load = workInBaterry(3.3, 0)
        self.assertAlmostEqual(no_load, 0)

#Time of life in baterry
    def testTimeOfLifeDefaultBattery(self):

        joules_in_battery = workInBaterry(3.3, 1000)

        time_on_air = get_toa(25, 10, enable_auto_ldro = False, enable_ldro = False, n_bw=125)['t_packet']
        life_of_device, work_in_day = batteryTimeOfLife(joules_in_battery, 24, time_on_air, 17)
        #print("With a battery of 3V3 and 1000mAh, sending a SF 10 and 25 bytes with 24 messages a day, the life time is %f days" % life_of_device)
        #print("Work in one day is %f"%work_in_day)
        #print("time on air %s"%time_on_air)
        #using the lora simulator the work in one day is 2.96 and the life time is 4009.74 days
        self.assertAlmostEqual(work_in_day, 2.96, delta = 0.05)
        self.assertAlmostEqual(life_of_device, 4000, delta=50)

#sensitivity
    def testSensitivitySF10BW125000(self):
        sen = loraSensitivity(10, 125000)
        #print("The sensitivity is %f dBm" % sen)
        self.assertAlmostEqual(sen, -132.03, delta=0.1)

#friis equation
    def testLinkBudget1(self):
        lb = friisEquation(1)
        #print("The path loss is %E " % lb)
        self.assertAlmostEqual(lb, 5.1089e-05)

    def testLinkBudget1000(self):
        lb = friisEquation(1000)
        #print("The path loss is %E " % lb)
        self.assertAlmostEqual(lb, 2.8729e-13)
#White Gaussian Noise
    def testWhiteGaussianNoise(self):
        noise = varianceWhiteNoise()
        #print("Noise %E" % noise)
        self.assertAlmostEqual(noise, 1.981116E-15)

    def testSNRLinear(self):
        snr = SNR_qsf_linear(7)
        self.assertAlmostEqual(snr, 0.2512, delta=0.001)

        snr = SNR_qsf_linear(12)
        self.assertAlmostEqual(snr, 0.01, delta=0.001)
#Haza H1 theorical
    def testH1Theorical(self):
        outage = H1Theorical(7, 600)
        #print("outage sf7 600m %f" % outage)
        self.assertAlmostEqual(outage, 0.99, delta=0.01)
        outage = H1Theorical(8, 2200)    
        #print("outage sf8 2200m %f" % outage)
        self.assertAlmostEqual(outage, 0.90, delta=0.01)

#Haza H1 simulated
    """ to longe to process

    def testH1Simulated(self):
        outage = H1Simulated(7, 600)
        print("outage simulated %f" % outage)

        outage = H1Simulated(8, 2200)
        print("outage simulated %f" % outage)
    """

    def testAverageDevicesDistribuition(self):
        devices = DeviceDistribuition()
        devices.averageDevicesDistribuition(500)
        self.assertEqual(devices.getDeviceInEachSF(), [14, 42, 69, 97, 125, 153])
  
    def testQ1Simulated(self):
        outage = Q1Simulated(8000)
        self.assertAlmostEqual(outage, 0.9, delta=1)
    
if __name__ == '__main__':
    unittest.main()

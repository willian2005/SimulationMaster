import sys
sys.path.append("..")

import matplotlib.pyplot as plt
import numpy as np

from energyUtils import *
import unittest

class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def test_11(self):
        energy = lifeTimeEnergyCalculator(100, 18.8, 14, 100)
        self.assertNotEqual( energy, 1810.432 )

    def test_energy_per_package_25_bytes_sf7(self):
        energy = packageEnergyCalculator(get_toa(25, 7)['t_packet'], 14)
        print("Energy in one package of 25 bytes and SF7 is: %f mJ" % energy)
        self.assertNotEqual( energy, 0.298678 )

    def test_1_day(self):
        energy = lifeTimeEnergyCalculator(60*60*24, get_toa(25, 7)['t_packet'], 14, 100)
        print("Energy in one day: %f" % energy)
        self.assertAlmostEqual( energy, 1.2612, delta = 0.01 )


if __name__ == '__main__':
    unittest.main()

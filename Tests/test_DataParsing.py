
import unittest
import collections
import numpy as np

from Database.dataParsing import *

collections.Callable = collections.abc.Callable

class testDataParsing(unittest.TestCase):

    def test_get_seal_species_str(self):
        x="Phoca Vitulina"
        y="Halichoerus Grypus"
        z="Halichoe Grypus"
        self.assertEqual(get_seal_species_str(x),"PV")
        self.assertEqual(get_seal_species_str(y), "HG")
        self.assertEqual(get_seal_species_str(z), None)

    def test_get_values(self):
        # Checks so that the output is correct when all parameters are correct
        x = np.array([['a', 'LOW'], ['WBC', 8.6],['LYMF', 10],['GRAN', 6],['MID', 123],['HCT', 42],
                      ['MCV', 76],['RBC', 99],['HGB', 1],['MCH', 25],['MCHC', 100],['MPV', 0],['PLT', 666]], dtype=object)
        tag=69
        sex=0
        species="PV"
        survival = "Released"
        values=get_values(x,survival,tag,sex,species)
        print(values)
        self.assertEqual(values[0][0],tag)
        self.assertEqual(values[0][14], sex)
        self.assertEqual(values[0][12], 666)

        #Survival should be True
        self.assertEqual(values[0][13],True)

        # Survival should be false
        survival="dead"
        values = get_values(x, survival, tag, sex, species)
        self.assertEqual(values[0][13], False)

if __name__ == '__main__':
    unittest.main()




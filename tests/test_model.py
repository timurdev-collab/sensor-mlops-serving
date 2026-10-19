import unittest
from service.model import predict

class ModelTests(unittest.TestCase):
    def test_normal(self):
        self.assertFalse(predict({'pressure_bar':4,'flow_lpm':90,'temperature_c':20})['anomaly'])
    def test_anomaly(self):
        result=predict({'pressure_bar':2,'flow_lpm':60,'temperature_c':20})
        self.assertTrue(result['anomaly'])
        self.assertIn('low_pressure',result['reasons'])
    def test_invalid(self):
        with self.assertRaises(ValueError):
            predict({'pressure_bar':-1,'flow_lpm':90,'temperature_c':20})

if __name__=='__main__':
    unittest.main()

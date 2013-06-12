import unittest
from lib.wiegand import serial_to_wiegand

TAG_DATA = [{
    'serial': '\x022700DE21BB63\r\n\x03',
    'wiegand': '3BC4376'
}, {
    'serial': '\x025100A7864232\r\n\x03',
    'wiegand': '14F0C85'
}]


class TestWiegand(unittest.TestCase):

    def test_serial_to_wiegand(self):
        for d in TAG_DATA:
            wiegand = serial_to_wiegand(d['serial'])
            assert d['wiegand'] == wiegand, "%s != %s" % (wiegand, d['wiegand'])


if __name__ == '__main__':
    unittest.main()

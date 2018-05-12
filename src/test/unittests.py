import os
import unittest
from src.common import *


class KeepTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print 'setUpClass'

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        print 'tearDownClass'

    def test_parse_id_singles(self):
        rd = parse_id('0')
        print(rd)
        self.assertTrue(rd.success)
        workspace_id, element_id = rd.data
        self.assertEqual(workspace_id, get_working_workspace())
        self.assertEqual(element_id, 0)

        rd = parse_id('10000')
        print(rd)
        self.assertTrue(rd.success)
        workspace_id, element_id = rd.data
        self.assertEqual(workspace_id, get_working_workspace())
        self.assertEqual(element_id, 10000)

        rd = parse_id('1234/')
        print(rd)
        self.assertTrue(rd.success)
        workspace_id, element_id = rd.data
        self.assertEqual(workspace_id, 1234)
        self.assertEqual(element_id, None)

    def test_parse_id_tuples(self):
        self.assertEqual(True, True)
        rd = parse_id('0/0')
        print(rd)
        self.assertTrue(rd.success)
        workspace_id, element_id = rd.data
        self.assertEqual(workspace_id, 0)
        self.assertEqual(element_id, 0)


        rd = parse_id('0/10000')
        print(rd)
        self.assertTrue(rd.success)
        workspace_id, element_id = rd.data
        self.assertEqual(workspace_id, 0)
        self.assertEqual(element_id, 10000)

        rd = parse_id('/10000')
        print(rd)
        self.assertTrue(rd.success)
        workspace_id, element_id = rd.data
        self.assertEqual(workspace_id, get_working_workspace())
        self.assertEqual(element_id, 10000)


################################################################################
def main():
    unittest.main()


# in root of project - `python -m src.test.unittests`
if __name__ == '__main__':
    main()

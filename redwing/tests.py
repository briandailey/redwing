from redwing import IntegerDataType, NumericDataType
import unittest

class TestDataTypes(unittest.TestCase):
    def setUp(self):
        pass

    def test_integer_type_check(self):
        integer_data_type = IntegerDataType()

        self.assertTrue(integer_data_type.test_type('1'))
        self.assertTrue(integer_data_type.test_type('9494'))
        self.assertTrue(integer_data_type.test_type('1234'))

        self.assertFalse(integer_data_type.test_type('01'))
        self.assertFalse(integer_data_type.test_type('0.1'))
        self.assertFalse(integer_data_type.test_type('5.1'))
        self.assertFalse(integer_data_type.test_type('test'))

    def test_numeric_type_check(self):
        numeric_data_type = NumericDataType()

        self.assertFalse(numeric_data_type.test_type('01'))
        self.assertFalse(numeric_data_type.test_type('0909'))
        self.assertFalse(numeric_data_type.test_type('7528395.942.3'))
        self.assertFalse(numeric_data_type.test_type('f'))
        self.assertFalse(numeric_data_type.test_type('--12'))

        self.assertTrue(numeric_data_type.test_type('.6'))
        self.assertTrue(numeric_data_type.test_type('0'))
        self.assertTrue(numeric_data_type.test_type('-12.1'))
        self.assertTrue(numeric_data_type.test_type('-666'))
        self.assertTrue(numeric_data_type.test_type('0.1'))
        self.assertTrue(numeric_data_type.test_type('409'))
        self.assertTrue(numeric_data_type.test_type('2957'))
        self.assertTrue(numeric_data_type.test_type('9090'))
        self.assertTrue(numeric_data_type.test_type('90.213'))
        self.assertTrue(numeric_data_type.test_type('-12'))
        self.assertTrue(numeric_data_type.test_type('-1'))
        self.assertTrue(numeric_data_type.test_type('4'))
        self.assertTrue(numeric_data_type.test_type('5'))
        self.assertTrue(numeric_data_type.test_type('0.1'))


if __name__ == '__main__':
    unittest.main(verbosity=2)

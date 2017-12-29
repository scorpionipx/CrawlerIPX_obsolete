"""
    Test function to execute all tests found within current directory
"""
import sys
import xmlrunner

try:
    import unittest2 as unittest
except ImportError:
    import unittest


def main():
    tests = unittest.TestLoader().discover('.', 'test_*.py')
    test_result = xmlrunner.XMLTestRunner(output='test-reports').run(tests)

    return not test_result.wasSuccessful()


if __name__ == '__main__':
    sys.exit(main())

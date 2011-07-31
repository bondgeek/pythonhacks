#!/usr/bin/env python

import random
import unittest

#Subclassing unittest.TestCase creates a class whose methods 
#can be treated as test cases.
#
#- Method names beginnng with 'test' are test cases
#- setUp() and tearDown() methods will be run prior to, and after each test,
#  respectively.
#- self.assertEqual(...), self.assert_(...), self.assertRaises(...) accumulate 
#  the results of the correspond 'assert' statements which are later reported.
#- unittest.main() runs through all the test cases and reports the results in 
#  minimal, simple format. "primarily for making test modules conveniently 
#  executable", according to the doc string.
#

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def testshuffle(self):
        # make sure the shuffled sequence does not lose any elements
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, range(10))

    def testchoice(self):
        element = random.choice(self.seq)
        self.assert_(element in self.seq)

    def testsample(self):
        self.assertRaises(ValueError, random.sample, self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assert_(element in self.seq)

    
   
if __name__ == '__main__':
    import optparse
    optparser = optparse.OptionParser()
    
    optparser.add_option("-v", "--verbose", action="store_true",
                         dest="verbose", default=False,
                         help="display in verbosity")
    
    (options, args) = optparser.parse_args()
    
    if options.verbose:
        print("\n\nVerbose.\n")
        suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else:
        print("\nTest")
        unittest.main()

 
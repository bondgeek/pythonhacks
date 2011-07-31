#!/usr/bin/env python
import sys

def testopt(argstr = None):
    from optparse import OptionParser
    
    print("sys.argv:\n%s\n" % sys.argv)

    parser = OptionParser()
    parser.add_option("-f", "--flg",
                action="store_const", const="flg",
                dest="case", default = "noflag",
                help="""a flag""")
    parser.add_option("-d", metavar="N [default=0]",
                        action="store", type="int", dest="num",
                        default=0,
                        help="number of dates")

    (options, args) = parser.parse_args(argstr)

    print args
    print options.case
    print options.num

if __name__ == "__main__":
    print("First run--args from command line")
    testopt()

    print "\nNow with passed string"
    argstring = "-d 8 --flg yes"
    print("%s  --split: %s\n" %  (argstring, argstring.split()))

    testopt(argstring.split())


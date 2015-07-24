#!/usr/bin/env python

import fileinput
import sys
from argparse import ArgumentParser
from hipchat_msg_parser import MsgParser

def process_args():
    parser = ArgumentParser(description='Parse HipChat messages.')

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--retain", dest="retain", action="store_true",
                       help="Retains the structure of the message in the output.")

    parser.set_defaults(retain=False)

    return parser


def main():
    parser = process_args()
    args = parser.parse_args()
    count = 0

    if args.retain is True:
        pass
    else:
        pass

    for line in fileinput.input():
        msg = line.rstrip()
        if len(msg):
            mp = MsgParser()
            print "Input: ", msg
            print "Ouput:"
            mp.parse(msg)
            ret = mp.report()
            print ret
            print


if __name__ == "__main__":
    sys.exit(main())

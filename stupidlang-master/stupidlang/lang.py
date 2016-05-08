#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following line in the
entry_points section in setup.cfg:

    console_scripts =
     fibonacci = stupidlang.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""

import argparse
import sys
import os.path

from stupidlang import __version__

from .run import repl, run_program
from .env_dictimpl import Env
from .evaluator import global_env

__author__ = "Rahul Dave"
__copyright__ = "Rahul Dave"
__license__ = "mit"





def parse_args(args):
    """
    Parse command line parameters

    :param args: command line parameters as list of strings
    :return: command line parameters as :obj:`airgparse.Namespace`
    """
    parser = argparse.ArgumentParser(
        description="A stupid lispish language")
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='stupidlang {ver}'.format(ver='0.0.0'))
    parser.add_argument(
        '-i',
        '--interactive',
        action = 'store_true',
        help='starts a REPL to run stupidlang code')
    parser.add_argument(
        '-l',
        '--load',
    nargs=1,
        help="a file to load before running the repl, implies -i")
    parser.add_argument(
        dest="programfile",
    nargs='?',
        help="the program to run. the last value will be printed")
    ns = parser.parse_args(args)
    if (bool(ns.interactive) | bool(ns.load)) & bool(ns.programfile):
        parser.error('-i or -l cannot be given together with a program file')
    if len(args)==0:
        parser.error('atleast one of -i, -l file, or file must be specified')
    if bool(ns.load) and not os.path.isfile(ns.load[0]):
        parser.error("Loaded file must exist or be file")
    if bool(ns.programfile) and not os.path.isfile(ns.programfile):
        parser.error("Program file must exist or be file")
    return ns


def main(args):
    args = parse_args(args)
    env=global_env(Env)
    if args.interactive:
        repl(env)
        return None
    elif bool(args.load):
        with open(args.load[0]) as f:
            run_program(f, env)
            repl(env)
            return None
    else:
        with open(args.programfile) as f:
            return run_program(f, env)



def run():
    print("stupidlang version {}".format(__version__))
    print(main(sys.argv[1:]))


if __name__ == "__main__":
    run()

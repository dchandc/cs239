#!/usr/bin/python

import argparse, re, sys

parser = argparse.ArgumentParser()
parser.add_argument('output_file', type=argparse.FileType('r'), help='file containing method calls and test results')
args = parser.parse_args()

for line in args.output_file:
	print line

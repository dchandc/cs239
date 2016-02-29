#!/usr/bin/python

import argparse, re, sys

class MethodStats:
	def __init__(self, name):
		self.name = name
		self.numPassed = 0
		self.numFailed = 0

parser = argparse.ArgumentParser()
parser.add_argument('output_file', type=argparse.FileType('r'), help='file containing method calls and test results')
args = parser.parse_args()

line_index = 0
for line in args.output_file:
	line_index += 1
	fields = line.strip().split()
	if len(fields) != 2:
		if len(fields) > 0:
			print 'malformed line[{0}]: {1}'.format(line_index, line)
		continue

	if fields[0] == '[Call]':
		print 'call'
	elif fields[0] == '**TestResult:':
		print 'result'

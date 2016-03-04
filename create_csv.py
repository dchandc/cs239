#!/usr/bin/python

import argparse, re, sys, math

def calculateSS(num_passed, total_passed, num_failed, total_failed):
	scores = {}

	if total_passed == 0 or total_failed == 0:
		sys.exit('Invalid test results')

	pct_passed = float(num_passed) / float(total_passed)
	pct_failed = float(num_failed) / float(total_failed)

	if num_passed > 0 or num_failed > 0:
		scores['Tarantula'] = pct_failed / (pct_passed + pct_failed)
	else:
		scores['Tarantula'] = -1

	if num_passed > 0 or num_failed > 0:
		scores['SBI'] = float(num_failed) / float(num_passed + num_failed)
	else:
		scores['SBI'] = -1

	scores['Jaccard'] = float(num_failed) / float(total_failed + num_passed)

	if num_passed > 0 or num_failed > 0:
		scores['Ochiai'] = float(num_failed) / math.sqrt(total_failed * (num_passed + num_failed))
	else:
		scores['Ochiai'] = -1	

	return scores

class MethodStats:
	num_passed = 0
	num_failed = 0

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<' + self.name + ', passed: ' + str(self.num_passed) + ', failed: ' + str(self.num_failed) + '>'

parser = argparse.ArgumentParser()
parser.add_argument('output_file', type=argparse.FileType('r'), help='file containing method calls and test results')
args = parser.parse_args()

all_method_stats = {}
current_method_stats = {}
total_passed = 0
total_failed = 0
line_index = 0
for line in args.output_file:
	line_index += 1
	fields = line.strip().split()
	if len(fields) != 2:
		if len(fields) > 0:
			print 'malformed line[{0}]: {1}'.format(line_index, line)
		continue

	if fields[0] == '[Call]':
		if fields[1] not in current_method_stats:
			current_method_stats[fields[1]] = 1
	elif fields[0] == '**TestResult:':
		if fields[1] == 'Pass':
			total_passed += 1
		elif fields[1] == 'Fail':
			total_failed += 1

		for key in current_method_stats.keys():
			if key not in all_method_stats:
				all_method_stats[key] = MethodStats(key)

			if fields[1] == 'Pass':
				all_method_stats[key].num_passed += 1 
			elif fields[1] == 'Fail':
				all_method_stats[key].num_failed += 1 
		current_method_stats = {}

with open('scores.csv', 'w+') as f:
	for key in all_method_stats:
		print all_method_stats[key]
		stats = all_method_stats[key]
		scores = calculateSS(stats.num_passed, total_passed, stats.num_failed, total_failed)
		f.write('{0},{1},{2},{3},{4},{6:.2f},{6:.2f},{7:.2f},{8:.2f}\n'.format(key, stats.num_passed, total_passed, stats.num_failed, total_failed, scores['Tarantula'], scores['SBI'], scores['Jaccard'], scores['Ochiai']))

print 'Totals - passed: ' + str(total_passed) + ', failed: ' + str(total_failed)

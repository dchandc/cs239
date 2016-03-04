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

	def __init__(self, class_name, method_name):
		self.class_name = class_name
		self.method_name = method_name

	def __repr__(self):
		return '<' + self.class_name + '::' + self.method_name + ', passed: ' + str(self.num_passed) + ', failed: ' + str(self.num_failed) + '>'

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
		lst = fields[1].split('::')
		if lst[1] == '<init>':
			continue
		if lst[0] not in current_method_stats:
			current_method_stats[lst[0]] = {lst[1]: 1}
		else:
			current_method_stats[lst[0]][lst[1]] = 1
	elif fields[0] == '**TestResult:':
		if fields[1] == 'Pass':
			total_passed += 1
		elif fields[1] == 'Fail':
			total_failed += 1

		for class_name in current_method_stats.keys():
			if class_name not in all_method_stats:
				all_method_stats[class_name] = {}

			for method_name in current_method_stats[class_name].keys():
				if method_name not in all_method_stats[class_name]:
					all_method_stats[class_name][method_name] = MethodStats(class_name, method_name)

				if fields[1] == 'Pass':
					all_method_stats[class_name][method_name].num_passed += 1
				elif fields[1] == 'Fail':
					all_method_stats[class_name][method_name].num_failed += 1
		current_method_stats = {}

with open('scores.csv', 'w+') as f:
	for class_name in all_method_stats:
		for method_name in all_method_stats[class_name]:
			print all_method_stats[class_name][method_name]
			method_stats = all_method_stats[class_name][method_name]
			scores = calculateSS(method_stats.num_passed, total_passed, method_stats.num_failed, total_failed)
			f.write('{0},{1},{2},{3},{4},{5},{6:.2f},{7:.2f},{8:.2f},{9:.2f}\n'.format(class_name, method_name, method_stats.num_passed, total_passed, method_stats.num_failed, total_failed, scores['Tarantula'], scores['SBI'], scores['Jaccard'], scores['Ochiai']))

print 'Totals - passed: ' + str(total_passed) + ', failed: ' + str(total_failed)

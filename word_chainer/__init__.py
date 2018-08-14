#!/usr/bin/env python3
#
#	word_chainer - Simple word chainer
#
#	Copyright (C) 2018 2sh <contact@2sh.me>
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from random import choices, choice

class WordChainer:
	def __init__(self, brain):
		if isinstance(brain, str):
			brain = open(brain, "r")
		self.brain = brain
		self.words = {}
		self.line_offsets = []
		while True:
			offset = self.brain.tell()
			line = self.brain.readline()
			if not line:
				break
			for word in line.strip().split(" "):
				self.words.setdefault(word.lower(), set()).add(offset)
			self.line_offsets.append(offset)
	
	def create_sentence(self, contains=None,
			max_lookback=2, min_lookback=None):
		if isinstance(max_lookback, str): max_lookback = int(max_lookback)
		if isinstance(min_lookback, str): min_lookback = int(min_lookback)
		if min_lookback is None or max_lookback < min_lookback:
			min_lookback = max_lookback
		
		if contains:
			output = contains.split()
		else:
			self.brain.seek(choice(self.line_offsets))
			word = self.brain.readline().split(" ", 1)[0]
			output = [word]
		
		output_offsets = [self.words[w.lower()] for w in output]
		
		is_sentence_start = not contains
		
		for is_right in ([False, True] if contains else [True]):
			while True:
				minlb = min(len(output), min_lookback)
				maxlb = min(len(output), max_lookback)
				
				possible = {}
				for val in range(minlb, maxlb+1):
					if is_right:
						lookback = output[-val:]
						lookback_offsets = output_offsets[-val:]
					else:
						lookback = output[:val]
						lookback_offsets = output_offsets[:val]
					
					search_string = " " + (" ".join(lookback)) + " "
					for offset in set.intersection(*lookback_offsets):
						self.brain.seek(offset)
						line = " " + self.brain.readline().strip() + " "
						
						index = line.lower().find(search_string.lower())
						if index == -1:
							continue
						if(is_sentence_start and
								minlb < min_lookback and index != 0):
							continue
						
						if is_right:
							word = line[(index+len(search_string)):]
						else:
							word = line[:index]
						
						if word:
							if is_right:
								word = word.split(" ", 1)[0]
							else:
								word = word.rsplit(" ", 1)[-1]
						else:
							word = None
						
						if val > possible.setdefault(word, val):
							possible[word] = val
				
				word = choices(*zip(*possible.items()))[0]
				if word is None:
					if not is_right:
						is_sentence_start = True
					break
				if is_right:
					output.append(word)
					output_offsets.append(self.words[word.lower()])
				else:
					output.insert(0, word)
					output_offsets.insert(0, self.words[word.lower()])
		return " ".join(output)

def _main():
	# word_chainer <file> <count> <contains> <max_lookback> <min_lookback>
	import sys
	wc = WordChainer(sys.argv[1])
	for i in range(sys.argv[2]):
		print(wc.create_sentence(sys.argv[3:])

#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as f:
	long_description = f.read()

setuptools.setup(
	name="word_chainer",
	version="1.1.1",
	
	author="2sh",
	author_email="contact@2sh.me",
	
	description="Simple word chainer",
	long_description=long_description,
	long_description_content_type="text/markdown",
	
	url="https://github.com/2sh/word_chainer",
	
	packages=["word_chainer"],
	
	python_requires='>=3.6',
	classifiers=(
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
		"Operating System :: OS Independent"
	),
	
	entry_points={"console_scripts":["word_chainer=word_chainer:_main"]}
)

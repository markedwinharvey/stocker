#!/usr/bin/env python
from setuptools import setup
def main():
	setup(
		name='stocker',
		version=0.1,
		description='Retrieve and process historical data by ticker symbol',
		packages=['stocker'],
		author='meh'
	)
if __name__ == '__main__':
	main()
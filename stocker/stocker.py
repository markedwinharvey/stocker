#!/usr/bin/env python
'''
Retrieve and plot historical data for user-selected ticker symbols
'''
import os
import sys
import subprocess as sp
from datetime import datetime as dt

import requests
import numpy as np

import matplotlib as mpl
mpl.use('TkAgg')
mpl.rc('figure',facecolor='white')

import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 12,8






#----- class declarations -----#

symbols = {}

class book():	
	def __init__(self,data):
		attrs = [x.replace(' ','_').lower() for x in data[0]]
		#print attrs
		for i in range(len(attrs)):
			setattr(
				self,
				attrs[i],
				data.T[i][1:][::-1]
			)

		date_mod = [ tuple( int(y) for y in x.split('-') ) for x in self.date ]
		
		setattr(
			self,
			'epoch',
			[dt(*x).strftime('%s') for x in date_mod]
		)
		

#----- function declarations -----#

def exit():
	print; print 'Exiting...'; print; sys.exit()


def retrieve_data(sym):
	url = 'http://chart.finance.yahoo.com/table.csv?s=%s&amp;a=3&amp;b=1&amp;c=2010&amp;d=3&amp;e=1&amp;f=2020&amp;g=d&amp;ignore=.csv'%sym
	r = requests.get(url)
	if r.status_code != 200:
		print 'Error retrieving page: Status',r.status_code
		print 'Reason:',r.reason
		if r.status_code == 404:
			print 'Ticker symbol \'%s\' not found'%sym
		exit()
	return r.text


def plot_data(symbols,sym,y_vals,**daterange):
	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	
	plt.scatter(
		range( len( getattr(symbols[sym],y_vals) ) ),	#x values
		getattr(symbols[sym],y_vals),					#y values
			
	)
	
	ax.set_title(sym)
	ax.set_xlabel('time')
	ax.set_ylabel(y_vals)
	#ax.set_axis_bgcolor('black')
	
	#label points
	entries = len(symbols[sym].date)
	
	num_labels = 20
	n=entries/num_labels
	
	
	dates = []
	for p in range(entries):
		if p % entries/num_labels == 0:
			date = getattr(symbols[sym],'date')[p*n].split('-')
			date = '-'.join([date[1],date[2],date[0][2:]])
			dates.append(date)
	
	ax.set_xticks(np.linspace(0,entries,num_labels))
	ax.set_xticklabels(dates,rotation=-45,ha='left',minor=False)
			
	
	plt.tight_layout()
	
	plt.show()	


def get_option(a):
	options = [x.lower().replace(' ','_') for x in a[0][1:]]
	print 'Select from data options by number: '

	while 1:	
		for i in range(len(options)):
			print ' ',i,options[i]
			
		op = raw_input('Option: ')	
		
		try:
			op = int(op)
			if op in range(len(options)):
				return options[op]
		except:
			print 'Invalid option.'


def get_prefs():
	if not os.path.exists('prefs'):
		open('prefs','w').write('')
		return None
	return open('prefs','r').read()		


def save_data(sym,csv_data,a):
	date2 = a[1][0]
	date1 = a[-1][0]
	filepath = './data/%s_%s_-_%s'%(sym,date1,date2)
	if not os.path.exists(filepath):
		with open(filepath,'w') as f:
			f.write(csv_data)


def main():
	print '#----- stocker.py -----#'
		
	sym = raw_input('Enter ticker symbol: ').upper()
	csv_data = retrieve_data(sym)
	
		
	a = np.array([x.split(',') for x in csv_data.split('\n') if x])
	
	symbols[sym] = book(a)
	
	#y_vals = get_option(a)
	y_vals = 'high'
	
	prefs = get_prefs()
	
	save_data(sym,csv_data,a)
	
	plot_data(symbols,sym,y_vals,date_range='all')
	
	
	
	
	
	
	
	
	
	
if __name__ == '__main__':
	main()
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import pandas
import os
import traceback
from moonpy import *
import socket 
import traceback
from astropy.io import ascii 


#### BULD THIS TO RUN ON UMBRIEL OR TETHYS!
#moonpydir = os.path.realpath(__file__)
#moonpydir = moonpydir[:moonpydir.find('/mp_lcfind.py')]

try:

	hostname = socket.gethostname()
	if ('tethys' in hostname) and ('sinica' in hostname):
		moonpydir = '/data/tethys/Documents/Software/MoonPy'
		central_data_dir = '/data/tethys/Documents/Central_Data'
		projectdir = '/data/tethys/Documents/Projects/single_transit_period_regression'
	elif ('Alexs-MacBook') in hostname:
		moonpydir = '/Users/hal9000/Documents/Software/MoonPy'
		central_data_dir = '/Users/hal9000/Documents/Central_Data'
		projectdir = '/Users/hal9000/Documents/Projects/single_transit_period_regression'

	#### prep_for_CNN -- use a NEW cnnlc_path!!!!!

	koifile = ascii.read(moonpydir+'/cumkois_mast.csv')
	kepoi_names = np.array(koifile['kepoi_name']).astype(str)
	koi_disposition = np.array(koifile['koi_disposition']).astype(str)

	koi_names = []
	for kepoi in kepoi_names:
		koi = kepoi
		while koi.startswith('K') or koi.startswith('0'):
			koi = koi[1:]
		koi = 'KOI-'+str(koi)
		koi_names.append(koi)

	##### now for each koi, we're gonna generate CNN lcs.
	##### to do that, we first need to detrend them.
	##### then use prep_for_CNN().

	if os.path.exists(projectdir+'/kois_already_processed.txt'):
		processed_kois_file = open(projectdir+'/kois_already_processed.txt', mode='r')
		processed_kois = []
		for nline,line in enumerate(processed_kois_file):
			processed_kois.append(line[:-1])
		processed_kois_file.close()

		print('processed_kois: ', processed_kois)



	else:
		print('kois_already_processed.txt does not exist.')
		processed_kois = []


	continue_query = input('Do you want to continue? y/n: ')
	if continue_query != 'y':
		raise Exception('you opted not to continue.')


	for koi in koi_names:
		print(koi)

		
		if koi in processed_kois:
			print(str(koi)+' already processed!')
			continue

		koi_mplc = MoonpyLC(targetID=koi, clobber='y')

		#### detrend it
		koi_mplc.detrend(dmeth='medfilt', medfilt_kernel_transit_multiple=2) 

		### create cnn segments
		koi_mplc.prep_for_CNN(cnnlc_path=projectdir+'/cnn_lcs/'+str(koi))

		#### if this all went well, add to processed_kois list and processed_kois_file.
		processed_kois.append(koi)
		print("# kois processed: "+str(len(processed_kois)))

		processed_kois_file = open(projectdir+'/kois_already_processed.txt', mode='a')
		processed_kois_file.write(str(koi)+'\n')
		processed_kois_file.close()

		print(' ')
		print(' ')


except:
	traceback.print_exc()



	

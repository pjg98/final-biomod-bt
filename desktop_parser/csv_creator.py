
#Creates for Zephyr BioModule csv file for the .dat file retreived via Bluetooth

import csv
import util


def create_data_file(filename, type):
#Determines type of data wanted and runs the appropriate parser.

	if type == 'ECG':
		ecg_file(filename)
	elif type == 'RES':
		res_file(filename)
	elif type == 'BOTH':
		ecg_file(filename)
		res_file(filename)
	elif type == 'ACC':
		acc_file(filename)
	else:
		print("Invalid type of data: try 'ECG', 'RES', 'ACC', or 'BOTH'.")
	
def ecg_file(filename):
#Creates an ECG csv file from recorded data in a .dat format.
	save_file = 'ecg_save_file.csv'
	f = open(save_file, 'a', newline = '')
	writer = csv.writer(f)
	payloads = util.payload_retv(filename, 'ECG')
	
	for i in range(len(payloads)):
		timestamp = util.get_timestamp(payloads[i])
		sample_set = util.get_sample_set(payloads[i])
		sample_list = util.parser_10bit(sample_set)
		curr_milli = timestamp[3]
		
		#Writes the data to the file and increments the milliseconds on the timestamp
		for j in range(len(sample_list)):
			curr_milli = curr_milli + 4
			millisec = util.millis(curr_milli)
			time = timestamp[0:3] + [millisec]
			sample = sample_list[j]
			
			writer.writerow([time, sample])

def res_file(filename):
#Creates a RES csv file from recorded data in a .dat format.
	
	save_file = 'res_save_file.csv'
	f = open(save_file, 'a', newline = '')
	writer = csv.writer(f)
	payloads = util.payload_retv(filename, 'RES')
	
	for i in range(len(payloads)):
		timestamp = util.get_timestamp(payloads[i])
		sample_set = util.get_sample_set(payloads[i])
		sample_list = util.parser_10bit(sample_set)
		curr_milli = timestamp[3]
		
		#Writes the data to the file and increments the milliseconds on the timestamp
		for j in range(len(sample_list)):
			curr_milli = curr_milli + 56
			millisec = util.millis(curr_milli)
			time = timestamp[0:3] + [millisec]
			sample = sample_list[j]
			
			writer.writerow([time, sample])

def acc_file(filename):
#Creates an ACC csv file from recorded data in a .dat format.

	savefile = 'acc_save_file.csv'
	f = open(savefile, 'a', newline = '')
	writer = csv.writer(f)
	payloads = util.payload_retv(filename, 'ACC')
	
	for i in range(len(payloads)):
		timestamp = util.get_timestamp(payloads[i])
		curr_milli = timestamp[3]
		sample_set = util.get_sample_set(payloads[i])
		sample_list = util.parser_acc(sample_set)

		#Writes the data to the file and increments the milliseconds on the timestamp
		for j in range(len(sample_list)):
			curr_milli = curr_milli + 20
			millisec = util.millis(curr_milli)
			time = timestamp[0:3] + [millisec]

			curr_sample = sample_list[j]
			x_sample = curr_sample[0]
			y_sample = curr_sample[1]
			z_sample = curr_sample[2]
			
			writer.writerow([time, x_sample, y_sample, z_sample])
			
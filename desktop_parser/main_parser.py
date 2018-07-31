
#Alter ONLY this program to parse a file. File must be in the same directory as this program.

#Program to run in order to parse a .dat file retreived from the Raspberry Pi

import csv_creator
from time import time

def main():
	
	#Insert the name of the file below
	file_to_parse = 'zephyr_packet_file15.dat' 
	
	#Insert what kind of data (ECG, RES, ACC) to get below. (BOTH will parse both ECG and RES data)
	data_type = 'BOTH'
	
	#Adds a start/stop timer for time taken to complete the parsing. 
	start_time = time()
	
	csv_creator.create_data_file(file_to_parse, data_type)
	
	end_time = time()
	
	time_taken = end_time - start_time
	print('Time taken: ' + str(time_taken))

main()
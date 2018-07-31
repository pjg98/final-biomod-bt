
#Utilities file for the Zephyr BioModule 

def payload_retv(filename, keyword):
	
	#Extracts the payloads for a certain type of data, returning a list of the payloads. 
	#Use keywords: ECG, RES, ACC
	
	file = open(filename, 'r')
	line = file.readline()
	
	#Initialize variables
	errors = 0
	payload = []
	
	#Determines what ID to scan for in the .dat file to retreive the proper payloads
	if keyword == 'ECG':
		ID_check = '22'
	elif keyword == 'RES':
		ID_check = '21'
	elif keyword == 'ACC':
		ID_check = '25'
	elif keyword != 'ECG' or 'RES':
		ID_check = ''
		print('Invalid data type: use a string "ECG" or "RES"')
	
	#Scans through all the packets/lines of the .dat file for packets of a certain data type.
	while line != '':
		ID = line[2:4]
		if ID == ID_check:
			#Error test for later implementation - does nothing now
			if line[0:2] == '02':
				pass
			else:
				errors += 1
			#Determines length of payload from hex-string and converts to integer
			pay_len = 2*int(line[4:6],16)
			curr_payload = line[6:pay_len+6]
			payload.append(curr_payload)
			
			#Loops to next packet
			line = file.readline()
		else:
			#Loops to next packet if ID_check does not pass
			line = file.readline()
		#payload returned in form of a list with all payload packets for specified type of data
	return payload 

def get_sample_set(single_payload):
	
	#Receives a single payload and returns samples - nothing done with timestamp
	
	#Initialize variables
	samples = []
	
	sample_set = single_payload[18:]

	#Returns samples in a list, in order
	return sample_set
	
def get_timestamp(payload):
#Given the payload, retreives the timestamp and converts it to a readable format. 

	curr_pay = payload
	seq_num = int(curr_pay[0:2], 16) #Only stored, can be used later
	
	#Formats the timestamp variables
	year = int(double_transpose(curr_pay[2:6]), 16)
	month = int(curr_pay[6:8], 16)
	day = int(curr_pay[8:10], 16)
	millisec = int(double_transpose(curr_pay[10:18]), 16)
	
	timestamp = [day, month, year, millisec]
	
	return timestamp
	
def millis(input):
#Receives a millisecond value and returns a timestamp string of hours, minutes, and seconds. 

	millis = input
	hours = int(millis/3600000)
	millis = millis-hours*3600000
	minutes = int(millis/60000)
	millis = millis - minutes*60000
	seconds = millis/1000

	return("{}:{}:{}".format(hours, minutes, seconds))

def parser_10bit(single_sample_set):
#Takes a single sample set and returns a list of samples from the hex-string values
	sample_list = []
	
	#If sample set does not have a set of 5 bytes, zeros are added to correctly run through the hex2sample parser.
	#The other samples are then removed.
	if len(single_sample_set)%10 != 0:
	
		remove_samples = int(4 - (((len(single_sample_set)%10)-2))/2)
		add0 = 10 - len(single_sample_set)%10
		edited_sample_set = single_sample_set + '0'*add0
	#Changes hex-string samples to actual samples, 5 bytes at a time, and removes samples
	for i in range(0, len(edited_sample_set), 10):
		curr_sample_hex = edited_sample_set[i:i+10]		#pulls 5 hexstr bytes
		sample_list = sample_list + hex2samples(curr_sample_hex)
		final_sample_list = sample_list[0:len(sample_list)-remove_samples]
		
	return final_sample_list

def parser_acc(single_sample_set):		
#Takes ACC data and produces the x, y, and z values 
	
	sample_list = []

	for i in range(0, len(single_sample_set), 30): 			
		curr_xyz = single_sample_set[i:i+30]				
		
		values = hex2samples(curr_xyz)
		
		set_1 = values[0:3]
		set_2 = values[3:6]
		set_3 = values[6:9]
		set_4 = values[9:12]
		
		sample_list = sample_list + [set_1] + [set_2] + [set_3] + [set_4]

		
	return sample_list

#Below are the tools used solely by the util scripts

def hex2samples(hex_values):
	
	transbin = ''
	sample_list = []
	
	#From a set of hex-string samples, creates a list of samples
	for i in range(0, len(hex_values), 2):
		byte2bin = bin(int(hex_values[i:i+2],16))[2:]
		if len(byte2bin) != 8:
			add0 = 8 - len(byte2bin)
			byte2bin = '0'*add0 + byte2bin
		transbin = transbin + transpose(byte2bin)
	for j in range(0, len(transbin), 10):
		binary_sample = transpose(transbin[j:j+10])
		sample_list = sample_list + [int(binary_sample, 2)]
	
	return sample_list

	#Tools used solely in the util program to change the order of data. Example below.
	#Transpose: ABCDEF --> Transpose --> F-E-D-C-B-A
	#Double Tranpose: ABCDEF --> DTranspose --> EF-CD-AB

def transpose(input):
	output = ''
	for i in range(len(input)):
		output = input[i] + output
	return output	

def double_transpose(input):
	output = ''
	for i in range(0, len(input), 2):
		output = input[i:i+2] + output
	return output
	
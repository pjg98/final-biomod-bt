
#Program to connect to the Zephyr BioModule and record data as a .dat file

import bluetooth
import csv
from time import sleep, time
from zephyr.protocol import create_message_frame as cmf


def connect_module(socket, MAC_Address):
#Connects to the specified BioModule MAC address.

	try: 
		socket.connect((str(MAC_Address), 1))
		print("Connected to module at specified MAC address.")
	except bluetooth.BluetoothError:
		raise


def initial(socket, type):
#Sends the proper initialization messages to the BioModule
#This causes the BioModule to begin sending the specified packets via Bluetooth

	print("Beginning initialization...")
	
	init_message_log = cmf(0x01, [1, 0, 0, 0, 0, 100])
	init_message_ecg = cmf(0x16, [1])
	init_message_res = cmf(0x15, [1])
	init_message_acc = cmf(0x1E, [1])
	init_message_sum = '\x02\xc2\x00\x00\x03'
	
	sending_message = []
	if type == 'ECG':
		socket.send(init_message_ecg)
	elif type == 'RES':
		socket.send(init_message_res)
	elif type == 'BOTH':
		socket.send(init_message_ecg)
		socket.send(init_message_res)
	elif type == 'LOG':
		socket.send(init_message_log)
	elif type == 'SUM':
		socket.send(init_message_sum)
		print('Requesting summary packet.')
	elif type == 'ACC':
		socket.send(init_message_acc)
	else:
		print("Error: invalid package type. Try 'ECG', 'RES', or 'BOTH'.")

	print("Initialization complete. Packets sending")

	
def get_filename_index(filename_index):
#Retreives the filename index such that multiple trials can be run and recorded. 
#This is stored in the separate .txt file and must be changed there. 
	
	file = open(filename_index, 'r')
	index = file.readline()
	if index == '':
		index = 0
	else:
		index = int(index)
	
	new_index = index + 1
	
	file = open(filename_index, 'w')
	file.write(str(new_index))
	
	return index
	
	
	
	
def collect_packages(socket, filename):
#Collects the packages and saves them collectively to the .dat file. 
	print('Collecting data...')
	
	try:
		while True:
			data = socket.recv(1024)
			decoded_data = data.hex()
			with open(filename, 'a') as f:
				writer = csv.writer(f)
				writer.writerow([decoded_data])
			print(decoded_data)
			socket.send('\x02#\x00\x00\x03')	#Prevents a connection timeout.
	except IOError:
		pass

def disconnect_module(socket):
#Disconnects the BioModule from the Pi
	try:
		socket.close()
		print('Module disconnected.')
	except:
		print('Error: socket cannot be closed.')


#Alter ONLY what is below to change connection and collection settings. 
#Below is the actual function to run to begin collecting data. 
def main():
	
	socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	
	mac_address = 'A0:E6:F8:FA:94:73'			#Insert MAC Address here.
	data_type = 'ACC'							#Insert data to be collected here.
	
	connect_module(socket, mac_address)
	initial(socket, data_type)						
	index_num = get_filename_index('filename_index.txt')
	save_file = 'zephyr_packet_file{}.dat'.format(index_num)	
	collect_packages(socket, save_file)
'''
	for i in range(10):
		connect_module(socket, mac_address)
		collect_packages(socket, save_file)
		print('Error occured: retrying...')
		print(i)
'''

	disconnect_module(socket) 	#Assumes to disconnect once the data stops sending (i.e. the BioModule is turned off)
		
	
	
	
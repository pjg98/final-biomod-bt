# Zephyr BioModule Bluetooth Connection - Tutorial

**Files needed:**
desktop_parser: csv_creator.py, util.py, main_parser.py, zephyr(folder with util + protocol)
raspberry_pi_collector: bluetooth_collector_pi.py, filename_index.txt

**Standard instructions to collect data via Bluetooth on the Raspberry Pi:**
 1. Open the ‘bluetooth_collector_pi’ program in a folder on the Raspberry Pi 3. 
 2. Change the MAC address, file index number, and data type variables.
  a. The MAC address is for the specific BioModule being collected from. Find this through the config tool while the BioModule is plugged in.
  
  b. The file index number changes the file number that the current recording session will be saved under. This can be changed in the ‘filename_index.txt’ file, and will increment by one after every trial, via the ‘get_filename_index’ function.
  c.The data type variable can be ‘ECG’, ‘RES’, ‘ACC’, or ‘BOTH’, written as a string. ‘BOTH’ will record both ECG and RES data and store them on the file. Whatever data is recorded will be the only data recorded. 
  
 3. Run the ‘main’ function in the ‘bluetooth_collector_pi’ program using Python3. The Raspberry Pi defaults to Python2, but Python3 is required. This should happen automatically when the bluetooth collector program is run.
 
  a. In a terminal, navigate to the appropriate directory and:
    ‘python3 bluetooth_collector_pi.py’
    
 4. Once complete, the file will be saved in the same directory as the program as ‘zephyr_packe_file##’ where ## is the file index. 

**Standard instructions to parse the data file from the Raspberry Pi on another computer:**
Have the three files in the same folder: ‘util’, ‘csv_creator’, and ‘main_parser’
‘util’ and ‘csv_creator’ are reference files for ‘main_parser’, which is the only file to be altered. 
Input/change the code of the ‘file_to_parse’ and ‘data_type’ variables. 
‘file_to_parse’ is the full name of the file, which is in the same directory as all this program. There should be an example file name, which would be replaced. 
‘data_type’ indicates the kind of data that you want from the file (‘ECG’, ‘RES’, ‘BOTH’, ‘ACC’). Indicate the type of data to retrieve here. 
Run ‘main_parser’ with Python3, which will be complete once the ‘Time taken: …’ is printed. The version of Python used when developing this program was 3.6.
The .csv files will be in the same directory as the program files. 
These will overwritten/appended to if they are not removed between files. 

Organization of the .dat file and Bluetooth packets
The .dat file is a list of hexadecimal-string, where each line is an individual packet. Each packet starts with 02, indicating the start of the message, then has the message ID (i.e. 21, 22, 23, etc.), then the length of the payload, the payload, and the end of the message as an 03. 

The payload contains a sequence number, the timestamp, and the set of encoded samples. The sequence number increments for each packet, to maintain the order of the packets (no kind of error system is implemented in this code, though). The timestamp separately stores the year, month, day, and milliseconds for the h/m/s/ms. 

For the ECG and RES sample sets, each individual sample is stored as a 10-bit binary number which are stored in a set of five bytes (5 bytes = 40 bits = 4 samples). The program is written, using the proprietary document as a guide, to pull out the samples in the sample set and save them to a csv file. 

Program Function Explanations:

util.py contains tools for the .dat file parser and csv file creator

payload_retv()
This function takes a .dat file and pulls each packet’s payload if the packet is for the specified data type. 
Since each bluetooth packet is on its own line, the function goes through the whole file, checks the message ID for each packet to see if it is the desired type, then pulls the payload to be parsed.
Returns a list of payload, in order, containing the sequence number, timestamp, and the set of samples. 

get_sample_set()
Takes a single payload (so the list of payloads would not process correctly) and pulls out the code for the sample set. 

get_timestamp()
From a payload, takes the timestamp code and returns the timestamp data to be formatted as a string. 	
The timestamp is coded in a 16 character sequence (characters 2 through 18 of the payload) with 2-6 being the year, 6-8 being the month, 8-10 being the day, and 10-18 being the milliseconds. 

millis()
Takes a millisecond input and produces a string in the format of hr/min/seconds. 

parser_10bit()
Takes the ECG and RES samples, since they are formatted the same way, and pulls out the samples formatted in 10-bit sequences. 
This function uses ‘hex2samples’ to convert 5 byte sequences of code into samples, then returning the samples. 
The ‘hex2samples’ function requires a 5 byte set of data, so this function also adds zeros to the end of the data as to make the sample set long enough, then goes back and removes the additional samples made due to the additional zeros. 
The correct samples from each payload are returned in a list. 

parser_acc()
The ACC data is formatted differently than the ECG/RES data, since there are three values to be recorded. This program accounts for these differences and returns sets of ACC data samples for each payload, which is then formatted into three separate data points for each timestamp. 
hex2string()
This is where the magic happens, and it is fairly complex. The function converts the hexadecimal string to a binary string, byte by byte, while also adding zeros since the internal python converter ignores starting-zeros (i.e. 00010101 is converted as 10101). 
The binary string is stored as transbin
The second loop goes through 10-bit segments of binary and converts them back to numerical data - the sample. It then saves each sample sequentially in a sample list, which is returned. 

transpose() and double_transpose() are explained in the code and used in the above functions

csv_creator.py has the functions to create a csv file from a .dat file

create_data_file()
Using the input filename and data type, this runs the appropriate data parser on the specified data types. These parsers/file creators are below.

ecg_file()
Sets save file for ECG data as ‘ecg_save_file.csv’. This can be changed.
Creates that file, and opens it for appending all the timestamps and samples.
The first loop collects all the timestamps and samples using the util.py functions.
The second loop writes each timestamp to the file and increments the timestamp milliseconds by 4ms (thus, 250Hz). This cannot be changed as it is programmed to increment this way. 

res_file()
Sets save file for RES data as ‘res_save_file.csv’. This can be changed.
Creates that file, and opens it for appending all the timestamps and samples.
The first loop collects all the timestamps and samples using the util.py functions.
The second loop writes each timestamp to the file and increments the timestamp milliseconds by 56ms (thus, ~18Hz). This cannot be changed as it is programmed to increment this way. 

ecg_file()
Sets save file for ECG data as ‘acc_save_file.csv’. This can be changed.
Creates that file, and opens it for appending all the timestamps and samples.
The first loop collects all the timestamps and samples using the util.py functions.
The second loop writes each timestamp to the file and increments the timestamp milliseconds by 20ms (thus, 50Hz). This cannot be changed as it is programmed to increment this way. It also save the x, y, and z data component in individual columns. 


On Raspberry Pi -  bluetooth_collector_pi.py

This program uses parts of another programer’s work to create the initialization messages to send to the Zephyr BioModule. His GitHub repository is linked below:

https://github.com/jpaalasm/zephyr-bt

This code was tested in an attempt to make work - the libraries it used are outdated and do not operate as they once did, hence the creation of an original code was implemented instead. While the specific files that are used are provided with this code set, the code was not well documented and not made for a Raspberry Pi. 

connect_module()
When run, this function connects the Raspberry Pi to the BioModule at the specified MAC Address. 

initial()
Initializes the BioModule to begin sending certain types of packets to store in the .dat file. 

get_filename_index()
Reads a separate file in order to get the filename index. This will be appended to the end of the filename for the .dat file so that several files can be taken. 

collect_packages()
Collects the data and stores it as a hexadecimal string, where each line is a packet of data from the BioModule. This also sends back a lifesign message to prevent a connection timeout. The hex-string is printed in the terminal to ensure the data is still being recorded. 

disconnect_module()
This ends the connection with the BioModule.

main()
Compiles all of the above code together with examples for the MAC address and the data type. There may be code commented out from attempts to fix a disconnection problem for longer periods of collection, but this depends on the finalized example of the code. 

Contact Information of Creator:
Patrick Gorman, Biomedical Engineering at UNC/NCSU
Most likely to respond through UNC email.

School email (anticipated to be good through Summer 2020): 
pjg98@live.unc.edu / pjgorman@ncsu.edu
Long term email: patrickjgorman@hotmail.com

There is an additional proprietary document that will not be included with this information and code, which contains the full bluetooth protocol for the Zephyr BioModule.

# imports
from pylogix import PLC
import argparse
import json
import time
from datetime import datetime
from time import localtime, strftime
import keyboard
import csv

# construct argument parser, parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True, help="path to JSON config file")
ap.add_argument("-f", "--file", required=True, help="path to output CSV file")
args = vars(ap.parse_args())

# load configuration
cfg = json.load(open(args["conf"]))

# get output filename
try:
    c_output_filename = args["file"]
    if c_output_filename[-3:] != 'csv':
        raise
except:
    print("output file must be csv - exiting...")
    exit()

# validate config
try:
    c_ip = cfg["ip"]
    c_tags = cfg["tags"]
    c_headers = cfg["headers"]
    c_trigger_type = cfg["trigger_type"]
    c_trigger_tag = cfg["trigger_tag"]
    c_period_time = cfg["period_time"]
    c_print_timestamp = cfg["print_timestamp"]
    if not(isinstance(c_ip, str)) or not(isinstance(c_period_time, (int, float))) or not(isinstance(c_print_timestamp, int)):
        raise
except:
    print("invalid config - exiting...")
    exit()

# utility function - return timestamp string
def GetTimestamp():
    return (datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))[:-3]

# utility function - parse string from PLC string tag
def ReadString(tag, comm):
    str_len = comm.Read(f'{tag}.LEN').Value
    value = ''
    if(str_len) > 0:
        data = comm.Read(f'{tag}.DATA[0]', int(str_len)).Value
        value = ''.join([chr(d) for d in data])
    return value

# utility function - update CSV by appending provided row
def UpdateCSV(row, filename):
    with open(filename, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(row)

# utility function - get row of data from PLC
def GetData(comm):
    results = []

    if(c_print_timestamp):
        results.append(GetTimestamp())

    for i in range(len(c_tags)):
        tagdata = comm.Read(c_tags[i])
        if tagdata.Status != 'Success':
            raise
        if isinstance(tagdata.Value, (bytes, bytearray, str)):
            results.append(ReadString(c_tags[i], comm))
        else:
            results.append(tagdata.Value)
    return results

# main function - open comms to PLC, record data until exit requested or error encountered
try:
    with PLC(c_ip) as comm:

        if c_print_timestamp:
            c_headers = ['Timestamp'] + c_headers

        UpdateCSV(c_headers, c_output_filename)     # start CSV with header row
        
        # define behavior based on trigger type chosen
        match c_trigger_type:

            # periodic trigger: 
            case "periodic":
                print("starting with periodic trigger - press q to quit logging")
                previous_time = 0
                while not keyboard.is_pressed('q'):
                    current_time = time.time()
                    if current_time - previous_time > c_period_time:
                        data = GetData(comm)
                        UpdateCSV(data, c_output_filename)
                        print('.', end='', flush=True)
                        previous_time = current_time

            # change trigger - update whenever trigger tag is changed
            case "change":
                print("starting with change trigger - press q to quit logging")
                previous_triggerdata = comm.Read(c_trigger_tag)
                if previous_triggerdata.Status != 'Success':
                    raise
                previous_val = previous_triggerdata.Value
                while not keyboard.is_pressed('q'):
                    current_triggerdata = comm.Read(c_trigger_tag)
                    if current_triggerdata.Status != 'Success':
                        raise
                    current_val = current_triggerdata.Value
                    if current_val != previous_val:
                        data = GetData(comm)
                        UpdateCSV(data, c_output_filename)
                        print('.', end='', flush=True)
                        previous_val = current_val

            # unknown trigger
            case _:
                print("unknown trigger type")

        print('\nexiting...')

except:
    print("\nerror encountered. exiting...")

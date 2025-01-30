# imports
from pylogix import PLC
import argparse
import json
import time
from datetime import datetime
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
    c_compare_condition = cfg["compare_condition"]
    c_compare_cutoff = cfg["compare_cutoff"]
    c_print_timestamp = cfg["print_timestamp"]
    c_live_update = cfg["live_update"]
    if not(isinstance(c_ip, str)) or not(isinstance(c_period_time, (int, float))) or not(isinstance(c_print_timestamp, int)) or not(isinstance(c_compare_condition, str)) or not(isinstance(c_compare_cutoff, (int, float))):
        raise
except:
    print("invalid config - exiting...")
    exit()

# custom exception for tag data not present
class TagError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

# utility function - return timestamp string
def GetTimestamp():
    return (datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))

# utility function - parse string from PLC string tag
def ReadString(tag, comm):
    str_len = comm.Read(f'{tag}.LEN').Value
    value = ''
    if(str_len) > 0:
        data = comm.Read(f'{tag}.DATA[0]', int(str_len)).Value
        value = ''.join([chr(d) for d in data])
    return value

# utility function - get row of data from PLC
def GetData(comm):
    results = []

    if(c_print_timestamp):
        results.append(GetTimestamp())

    tagdata = comm.Read(c_tags)
    for t in range(len(c_tags)):
        if tagdata[t].Status != 'Success':
            raise TagError(f"failed to read tag: {c_tags[t]}")
        if isinstance(tagdata[t].Value, (bytes, bytearray, str)):
            results.append(ReadString(c_tags[t], comm))
        else:
            results.append(tagdata[t].Value)
    return results

# utility function - update CSV by appending provided row. Only used with real-time updates; slower performance
def LiveUpdate(row, filename):
    with open(filename, 'a', newline='') as csv_file:
        realtime_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        realtime_writer.writerow(row)

# main function - open comms to PLC, record data until exit requested or error encountered
try:
    if not c_live_update:
        csv_file = open(c_output_filename, 'a', newline='')
        writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    with PLC(c_ip) as comm:

        if c_print_timestamp:
            c_headers = ['Timestamp'] + c_headers

        # start csv with header row
        if c_live_update:
            LiveUpdate(c_headers, c_output_filename)
        else:
            writer.writerow(c_headers)
        
        # define behavior based on trigger type chosen
        match c_trigger_type:

            # periodic trigger: 
            case "periodic":
                print("starting with periodic trigger - press ctrl + c to quit logging")
                previous_time = 0
                while True:
                    current_time = time.time()
                    if current_time - previous_time > c_period_time:
                        data = GetData(comm)
                        if c_live_update:
                            LiveUpdate(data, c_output_filename)
                        else:
                            writer.writerow(data)
                        print('.', end='', flush=True)
                        previous_time = current_time
                

            # change trigger - update whenever trigger tag is changed
            case "change":
                print("starting with change trigger - press ctrl + c to quit logging")
                previous_triggerdata = comm.Read(c_trigger_tag)
                if previous_triggerdata.Status != 'Success':
                    raise TagError(f"failed to read tag: {c_trigger_tag}")
                previous_val = previous_triggerdata.Value
                while True:
                    current_triggerdata = comm.Read(c_trigger_tag)
                    if current_triggerdata.Status != 'Success':
                        raise TagError(f"failed to read tag: {c_trigger_tag}")
                    current_val = current_triggerdata.Value
                    if current_val != previous_val:
                        data = GetData(comm)
                        if c_live_update:
                            LiveUpdate(data, c_output_filename)
                        else:
                            writer.writerow(data)
                        print('.', end='', flush=True)
                        previous_val = current_val

            # compare trigger - update whenever trigger tag fulfills specified conditions
            case "compare":
                print("starting with comparison trigger - press ctrl + c to quit logging")
                previous_triggerdata = comm.Read(c_trigger_tag)
                if previous_triggerdata.Status != 'Success':
                    raise TagError(f"failed to read tag: {c_trigger_tag}")
                while True:
                    current_triggerdata = comm.Read(c_trigger_tag).Value
                    
                    match c_compare_condition:
                        case "grt":
                            if current_triggerdata > c_compare_cutoff:
                                data = GetData(comm)
                                if c_live_update:
                                    LiveUpdate(data, c_output_filename)
                                else:
                                    writer.writerow(data)
                                print('.', end='', flush=True)

                        case "geq":
                            if current_triggerdata >= c_compare_cutoff:
                                data = GetData(comm)
                                if c_live_update:
                                    LiveUpdate(data, c_output_filename)
                                else:
                                    writer.writerow(data)
                                print('.', end='', flush=True)

                        case "les":
                            if current_triggerdata < c_compare_cutoff:
                                data = GetData(comm)
                                if c_live_update:
                                    LiveUpdate(data, c_output_filename)
                                else:
                                    writer.writerow(data)
                                print('.', end='', flush=True)

                        case "leq":
                            if current_triggerdata <= c_compare_cutoff:
                                data = GetData(comm)
                                if c_live_update:
                                    LiveUpdate(data, c_output_filename)
                                else:
                                    writer.writerow(data)
                                print('.', end='', flush=True) 

                        case "neq":
                            if current_triggerdata != c_compare_cutoff:
                                data = GetData(comm)
                                if c_live_update:
                                    LiveUpdate(data, c_output_filename)
                                else:
                                    writer.writerow(data)
                                print('.', end='', flush=True)

                        case "equ":
                            if current_triggerdata == c_compare_cutoff:
                                data = GetData(comm)
                                if c_live_update:
                                    LiveUpdate(data, c_output_filename)
                                else:
                                    writer.writerow(data)
                                print('.', end='', flush=True)

                        case _:
                            print("unknown comparison condition")
                            break


            # unknown trigger
            case _:
                print("unknown trigger type")

        print('\nexiting...')

except KeyboardInterrupt:
    print("\nexiting...")
except Exception as e:
    print(f"\nerror encountered: {type(e).__name__} - {e}. exiting...")

# cleanup
print(f"output stored here: {c_output_filename}")
if not c_live_update:
    csv_file.close()
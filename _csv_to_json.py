
import csv

# Convert CSV file to dictionary

def make(filename):
    with open(filename, 'r') as data:
        #create base dictonary used for data
        input_data = {}

        for line in csv.DictReader(data):
            # load values into temp variables to make
            # life easier!
            hostname = line['Hostname'].lower()
            interface = line['Interface'].lower()
            cost = int(line['Cost'])

            # if hostname already exists as object in
            # input dict, add interface to it, if it
            # doesnt, create it and add interface
            if hostname not in input_data:
                input_data[hostname] = {}
                input_data[hostname][interface]=cost
            else:
                input_data[hostname][interface]=cost

    return input_data



        

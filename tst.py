import csv

file_path = "/home/jack/Documents/data.txt"

with open(file_path, 'r') as datafile:
    raw_data = [row for row in csv.reader(datafile)]

print raw_data

header = dict((channel, []) for channel in raw_data[0])

max_lines = int(raw_data[-1][raw_data[0].index('a')]) + 1

line_index = (raw_data[0].index('a'))


for line in range(1, max_lines):
    for key in header:
        key_index = raw_data[0].index(key)
        header[key].append([row[key_index] for row in raw_data[1:] if int(row[line_index]) == line])

for key in header:
    print key + ":\t" + str(header[key])


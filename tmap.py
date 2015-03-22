__author__ = 'Jack Madden'

import csv


class TurbineMap(object):

    def __init__(self, path):
        """Class initialisation"""
        self.path = path
        self.rows = self.read_raw_data()
        self.line_index = self.get_line_index()
        self.max_lines = self.get_max_lines()
        self.channels = self.get_channels()
        self.test_type = self.rows[0][0]
        self.test_cell = self.rows[1][0]

    def read_raw_data(self):
        """Reads the csv file into an array"""
        try:  # to read the csv file
            with open(self.path, 'r') as datafile:
                raw_data = [row for row in csv.reader(datafile) if len(row) > 0]

                return raw_data

        except (IOError, csv.Error):
            print "Unable to open file: " + self.path
            exit(1)

    def get_line_index(self):
        """Return the index of the column that contains 'Line_no'
        as its value in row 2 of the raw data"""
        try:  # to get the index
            line_index = int((self.rows[2].index("Line_no")))
            return line_index
        except ValueError:
            print "'Line_no': is not in channel list - unable split data"
            exit(1)

    def get_max_lines(self):
        """return the highest value of all rows, with
        the index of 'Line_no' in row 2(headers)"""

        max_lines = None

        try:  # to get the value representing max number of lines
            for line_num in self.rows[5:]:
                if line_num[self.line_index] > max_lines:
                    max_lines = line_num[self.line_index]

            return int(float(max_lines))

        except ValueError:
            print "MAX LINES: Cannot read file"
            exit(1)

    def get_channels(self):
        """Build a dictionary of channels - [key] = channel name
        [value] = array of data points split by line number"""
        header = dict((channel_name, []) for channel_name in self.rows[2])

        for channel in header:  # Add the Unit as the first item
            key_index = self.rows[2].index(channel)
            header[channel].append(self.rows[3][key_index])

        for line in range(1, self.max_lines + 1):  # Add lists of data points, split according to Line_no
            for channel in header:
                key_index = self.rows[2].index(channel)
                header[channel].append([row[key_index] for row in self.rows[5:] if int(float(row[self.line_index])) == line])

        return header

    def sort_order(self, points):
        pass


# TESTING #############################################################################################################

if __name__ == "__main__":

    import matplotlib.pyplot as plt

    my_map = TurbineMap("testdata/15-0178-02-A")

    spd_lines = my_map.channels["Trb_spd"][1:]

    eff_lines = my_map.channels["Tur_eff"][1:]

    for i in spd_lines:
        order = [i.index(str(point)) for point in sorted(map(int, i))]

        x = [i[o] for o in order]
        y = [eff_lines[spd_lines.index(i)][o] for o in order]

        plt.title(my_map.test_cell + "\n" + my_map.test_type)
        plt.plot(x, y, label=spd_lines.index(i))
        plt.legend()

    plt.show()

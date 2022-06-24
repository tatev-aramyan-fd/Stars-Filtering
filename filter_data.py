import csv
from datetime import date


def header_from_tsv(filename):
    with open(filename, newline='') as f:
        f.readline()  # read first line is not needed
        header = f.readline().split("\t")

    return header[0], header[1], header[7], header[25][:-1]


def from_tsv_to_data_list():
    with open(filename, newline='') as f:
        f.readline()  # read first line not needed
        f.readline()  # header not needed
        csv_obj = csv.reader(f)
        data_list = []
        for i in csv_obj:
            row = i[0].split('\t')

            if float(row[0]) < fov_h and float(row[1]) < fov_v:
                data_list.append([float(row[0]), float(row[1]), float(row[7]), float(row[25])])
        return data_list






if __name__ == "__main__":
    # filename = "cleaned_stars.tsv"
    filename = "337.all.tsv"
    fov_h = 30
    fov_v = 30

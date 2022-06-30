import csv
from datetime import date
import time


def header_from_tsv(filename):
    with open(filename, newline='') as f:
        f.readline()  # read first line as it is not needed
        header = f.readline().strip().split("\t")
        ra, dec, id_, brightness = indexes_of_needed_fields(header)
        print(header[ra], header[dec], header[id_], header[brightness])

    return header[ra], header[dec], header[id_], header[brightness]


def indexes_of_needed_fields(header_list):
    ra_index = header_list.index('ra_ep2000')
    dec_index = header_list.index('dec_ep2000')
    id_index = header_list.index('source_id')
    b_index = header_list.index('b')
    return ra_index, dec_index, id_index, b_index


def from_tsv_to_data_list():
    data_list = []
    with open(filename) as f:
        f.readline()  # read first line / not needed
        header = f.readline().strip().split("\t")
        ra, dec, id_, brightness = indexes_of_needed_fields(header)
        csv_obj = csv.reader(f)

        for i in csv_obj:
            row = i[0].split('\t')
            store_stars_in_fov(float(row[ra]),
                               float(row[dec]),
                               float(row[id_]),
                               float(row[brightness]),
                               data_list)
        return data_list


def store_stars_in_fov(ra: float, dec: float,
                       id_: float, brightness: float,
                       storage: list):
    if id_ == '':
        raise Exception("ID of the star must be not null!!!")
    if not (ra == '' or dec == '' or id_ == '' or brightness == ''):

        if ((ra_dec[0] < ra) and (ra < fov_h + ra_dec[0])) \
                and (ra_dec[1] < fov_v and dec < fov_v + ra_dec[1]):
            storage.append([ra, dec, id_, brightness])
    else:
        raise Exception("Some data are null. With nullable data further work is impossible!!!!!!!")


def distance_between_two_points(ra_dec1: tuple, ra_dec2: tuple) -> float:
    ra1, dec1 = ra_dec1
    ra2, dec2 = ra_dec2
    distance = (ra1-ra2)**2 + (dec1-dec2)**2
    return distance


def sort_by_last_value_in_each_el(lst: list) -> list:   # 2d list/ matrix
    n = len(lst)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lst[j][-1] > lst[j + 1][-1]:  # needed value are the last one
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst


if __name__ == "__main__":
    # filename = "cleaned_stars.tsv"
    filename = "337.all.tsv"
    fov_h = 30
    fov_v = 30
    num = 15
    ra_dec = (45.0, 87.0)

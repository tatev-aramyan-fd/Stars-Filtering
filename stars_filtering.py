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
    try:
        if (ra_dec[0] < ra and (ra < (fov_h + ra_dec[0]))) \
                and ((ra_dec[1] < dec) and (dec < (fov_v + ra_dec[1]))):
            storage.append([ra, dec, id_, brightness])

        return storage
    except:
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


def update_data_with_distances() -> list:
    data_arr = n_bright_stars().copy()
    for i in data_arr:
        ra1, dec1 = ra_dec
        ra2 = i[0]
        dec2 = i[1]
        i.append(distance_between_two_points((ra1, dec1), (ra2, dec2)))
    return data_arr


def final_needed_data_sorted_by_distance() -> list:
    arr = update_data_with_distances()
    return sort_by_last_value_in_each_el(arr)


def n_bright_stars() -> list:
    data = from_tsv_to_data_list()
    sorted_by_brightness = sort_by_last_value_in_each_el(data)
    return sorted_by_brightness[:num]


def write_to_csv_file():
    current_timestamp = str(date.today()) + ".csv"
    with open(current_timestamp, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([*header_from_tsv(filename), 'distance'])
        for i in final_needed_data_sorted_by_distance():
            writer.writerow(i)


def run_application(ra_dec_coordinates: tuple,
                    fov_h_degree: float,
                    fov_v_degree: float,
                    num_of_stars: int):
    if (fov_h_degree<0 or fov_h_degree>360) \
            or (fov_v_degree > 90 or fov_v < -90)\
            or num_of_stars < 0\
            or ra_dec_coordinates[0]<0 or ra_dec_coordinates[0]>360 \
            or ra_dec_coordinates[1]>90 or ra_dec_coordinates[1]<-90:
        raise Exception("not valid input")
    try:
        if isinstance(ra_dec_coordinates, tuple) \
                and isinstance(fov_h_degree, (float, int)) \
                and isinstance(fov_v_degree, (float, int)) \
                and isinstance(num_of_stars, int):
            write_to_csv_file()
    except Exception:
        raise Exception("Something went wrong. Check given arguments!!!")


if __name__ == "__main__":
    # filename = "cleaned_stars.tsv"
    filename = "337.all.tsv"
    fov_h = 50.0
    fov_v = 45
    num = 10
    ra_dec = (45.0, 32.0)
    start = time.time()
    run_application(ra_dec, fov_h, fov_v, num)
    end = time.time()
    print(f"application runs in {end-start} seconds")


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


def distance_between_two_points(ra_dec1:tuple,ra_dec2:tuple)->float:
    ra1, dec1 = ra_dec1
    ra2, dec2 = ra_dec2
    distance = (ra1-ra2)**2 + (dec1-dec2)**2
    return distance


def sort_by_last_value_in_each_el(lst: list) -> list:   # 2d list/ matrix
    n = len(lst)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lst[j][-1] > lst[j + 1][-1]:  # needed value is the last one
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


def sort_needed_data_by_distance():
    arr = update_data_with_distances()
    return sort_by_last_value_in_each_el(arr)


def n_bright_stars() -> list:
    data = from_tsv_to_data_list()
    sorted_by_brightness = sort_by_last_value_in_each_el(data)
    return sorted_by_brightness[:num]


def write_to_csv_file():
    current_timestamp = str(date.today())+".csv"
    with open(current_timestamp, 'w',newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([*header_from_tsv(filename), 'distance'])
        for i in sort_needed_data_by_distance():
            writer.writerow(i)


def run_application(ra_dec_coordinates: tuple,
                    fov_h_degree: float,
                    fov_v_degree: float,
                    num_of_stars: int
                    ):

    # try:
    if isinstance(ra_dec_coordinates, tuple) \
            and isinstance(fov_h_degree, (float, int)) \
            and isinstance(fov_v_degree, (float, int)) \
            and isinstance(num_of_stars, int):

        write_to_csv_file()
    # except:
    #     raise Exception("Something went wrong. Check given arguments!!!")


if __name__ == "__main__":
    # filename = "cleaned_stars.tsv"
    filename = "337.all.tsv"
    fov_h = 30
    fov_v = 30
    num = 15
    ra_dec = (45.0, 87.0)

    run_application(ra_dec, fov_h, fov_v, num)

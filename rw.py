import csv


def csv_reader(filename):
    rows = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=' ')
        for row in reader:
            rows.append(row)
    return rows


def csv_writer(filename, rows):
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar=' ')
        writer.writerows(rows)


if __name__ == '__main__':
    csv_reader('input_filename.csv')
    csv_reader('output_filename.csv', rows=[('a', 1), ('b', 2)])

# -*- coding: utf-8 -*-

import sys
import csv


'''
    import sys
    import csv
    逐行输出demo
    writer = csv.writer(sys.stdout, delimiter=',')
    rows = _fetchall(sql, ())
    for a, b, c in rows:
        writer.writerow([a, b, c])
'''


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


def rows2csv(rows):
    writer = csv.writer(sys.stdout, delimiter=',')
    writer.writerows(rows)


def csv2rows(filename):
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            yield row


def csv2html(datas):
    l = []
    l.append(b'<table style="word-break: keep-all">\n')
    is_first_table = True
    for row in datas:
        if len(row) == 1:
            if not is_first_table:
                l.append(b'</table>\n')
                l.append(b'<table style="word-break: keep-all">\n')
            col = row[0]
            if isinstance(col, unicode):
                col = col.encode('U8')
            l.append(b'<h4>%s</h4>\n' % col)
            continue
        l.append(b'<tr>\n')
        if not row:
            l.append(b'<td>&nbsp;</td>\n')
        for col in row:
            if isinstance(col, unicode):
                col = col.encode('U8')
            l.append(b'<td>%s</td>\n' % col)
        l.append(b'</tr>\n')
        is_first_table = False
    l.append(b'</table>\n')
    return ''.join(l)


if __name__ == '__main__':
    csv_reader('input_filename.csv')
    csv_reader('output_filename.csv', rows=[('a', 1), ('b', 2)])

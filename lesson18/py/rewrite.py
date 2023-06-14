import csv

with open('./demographic.csv', 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)

    for i in range(1, len(rows)):
        if rows[i][0] == "1":
            continue
        rows[i][0] = str(int(rows[i - 1][0]) + 1)

with open('./demographic.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

import csv


def array_dict(results, filename):
    cols = [*results[0]].keys()
    headers = cols

    try:
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            [writer.writerow(d) for d in results]
    except IOError:
        print("I/O error")

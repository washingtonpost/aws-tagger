import csv


def array_dict(results, filename):
    cols = ['InstanceId', 'InstanceType', 'Tags']
    headers = cols

    try:
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(cols)
            for result in results:
                row = []
                row.append(result['InstanceId'] or "")
                row.append(result['InstanceType'] or "")
                row.append(result['Tags'] or [])
                writer.writerow(row)
    except IOError:
        print("I/O error")

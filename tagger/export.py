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


def cloudformation(stacks, filename):
    headers = ['StackId', 'StackName', 'Tags']
    _write_csv(filename, headers, stacks)


def _write_csv(filename, headers, records):
    try:
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|')
            writer.writerow(headers)
            for record in records:
                row = [(record[col] or '') for col in headers]
                writer.writerow(row)
    except IOError:
        print("I/O error")



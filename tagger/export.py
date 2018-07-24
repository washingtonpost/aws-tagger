import csv


def ec2(filename, instances):
    headers = ['InstanceId', 'InstanceType', 'Tags']
    _write_csv(filename, headers, instances)

def cloudformation(filename, stacks):
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



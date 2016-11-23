import os
import boto3
import botocore
from retrying import retry
import csv

def _format_dict(tags):
    output = []
    for key, value in tags.iteritems():
        output.append("%s:%s" % (key, value))

    return ", ".join(output)

def _dict_to_aws_tags(tags):
    return [{'Key': key, 'Value': value} for key, value in tags.iteritems() if not key.startswith('aws:') and not key.startswith('Name')]

def _aws_tags_to_dict(aws_tags):
    return {x['Key']: x['Value'] for x in aws_tags if not x['Key'].startswith('aws:')}

def _client(name):
    if os.environ.get('AWS_REGION'):
        return boto3.client(name, region_name=os.environ['AWS_REGION'])
    else:
        return boto3.client(name)

class SingleResourceTagger(object):
    def __init__(self, dryrun, verbose):
        self.ec2 = EC2Tagger(dryrun, verbose)

    def tag(self, resource_id, tags):
        if resource_id.startswith('i-'):
            self.ec2.tag_instance(resource_id, tags)
        elif resource_id == "":
            return
        else:
            print "Tagging is not supported for this resource %s" % resource_id

class MultipleResourceTagger(object):
    def __init__(self, dryrun, verbose):
        self.tagger = SingleResourceTagger(dryrun, verbose)

    def tag(self, resource_ids, tags):
        for resource_id in resource_ids:
            self.tagger.tag(resource_id, tags)

class CSVResourceTagger(object):
    def __init__(self, dryrun, verbose):
        self.tagger = SingleResourceTagger(dryrun, verbose)
        self.resource_id_column = 'Id'

    def tag(self, filename):
        with open(filename, 'rU') as csv_file:
            reader = csv.reader(csv_file)
            header_row = True
            tag_index = None

            for row in reader:
                if header_row:
                    header_row = False
                    tag_index = self._parse_header(row)
                else:
                    self._tag_resource(tag_index, row)

    def _parse_header(self, header_row):
        tag_index = {}
        for index, name in enumerate(header_row):
            tag_index[name] = index

        return tag_index

    def _tag_resource(self, tag_index, row):
        resource_id = row[tag_index[self.resource_id_column]]
        tags = {}
        for key, index in tag_index.iteritems():
            value = row[index]
            if key != self.resource_id_column and value != "":
                tags[key] = value

        self.tagger.tag(resource_id, tags)


class EC2Tagger(object):
    def __init__(self, dryrun, verbose):
        self.dryrun = dryrun
        self.verbose = verbose
        self.ec2 = _client('ec2')

    def tag_instance(self, instance_id, tags):
        aws_tags = _dict_to_aws_tags(tags)
        if self.verbose:
            print "tagging %s with %s" % (instance_id, _format_dict(tags))
        if not self.dryrun:
            self._ec2_create_tags(Resources=[instance_id], Tags=aws_tags)

    def _is_retryable_exception(exception):
        return not isinstance(exception, botocore.exceptions.ClientError) or \
            (exception.response["Error"]["Code"] in ['RequestLimitExceeded'])

    @retry(retry_on_exception=_is_retryable_exception, stop_max_delay=30000, wait_exponential_multiplier=1000)
    def _ec2_create_tags(self, **kwargs):
        return self.ec2.create_tags(**kwargs)

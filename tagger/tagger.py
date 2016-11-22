import os
import boto3
import botocore
from retrying import retry

def _dict_to_aws_tags(tags):
    return [{'Key': key, 'Value': value} for key, value in tags.iteritems() if not key.startswith('aws:') and not key.startswith('Name')]

def _aws_tags_to_dict(aws_tags):
    return {x['Key']: x['Value'] for x in aws_tags if not x['Key'].startswith('aws:')}

def _client(name):
    if os.environ.get('AWS_REGION'):
        return boto3.client(name, region_name=os.environ['AWS_REGION'])
    else:
        return boto3.client(name)

class ResourceTagger(object):
    def __init__(self):
        self.ec2 = EC2Tagger()

    def tag(self, resource_id, tags):
        if resource_id.startswith('i-'):
            self.ec2.tag_instance(resource_id, tags)

class EC2Tagger(object):
    def __init__(self):
        self.ec2 = _client('ec2')

    def tag_instance(self, instance_id, tags):
        aws_tags = _dict_to_aws_tags(tags)
        self._ec2_create_tags(Resources=[instance_id], Tags=aws_tags)

    def _is_retryable_exception(exception):
        return not isinstance(exception, botocore.exceptions.ClientError) or \
            (exception.response["Error"]["Code"] in ['RequestLimitExceeded'])

    @retry(retry_on_exception=_is_retryable_exception, stop_max_delay=5000, wait_exponential_multiplier=100)
    def _ec2_create_tags(self, **kwargs):
        return self.ec2.create_tags(**kwargs)

import boto3


def ec2_untagged(region_name='us-east-1'):
    """
    Fetch and find instances without __any__ tags
    """
    results = []
    response = _ec2_describe_instances(region_name)
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if len(instance['Tags']) == 0:
                results.append(instance)
    return results


def ec2_without_tag(region_name='us-east-1', tag_key='Name'):
    """
    Fetch and find instances without specified tag
    """
    results = []
    response = _ec2_describe_instances(region_name)
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if tag_key not in instance['Tags'].keys():
                result.append(instance)
    return intances


def _ec2_describe_instances(region_name):
    """
    Execute ec2 describe instances request
    """
    session = boto3.Session(region_name=region_name)
    ec2 = session.client('ec2')
    return ec2.describe_instances()


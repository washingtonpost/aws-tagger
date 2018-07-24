#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import sys
from pprint import pprint
from .tagger import MultipleResourceTagger, CSVResourceTagger
from . import fetch, export


@click.group()
def cli():
    pass


@cli.command()
@click.option('--dryrun/--no-dryrun', default=False, help='Verbose output.')
@click.option('--verbose/--no-verbose', default=False, help='Verbose output.')
@click.option('--region', help='AWS region.')
@click.option('--role', help='IAM role to use.')
@click.option('--resource', multiple=True, help='Resource ID to tag.')
@click.option('--tag', multiple=True,
    help='Tag to apply to resource in format "Key:Value".')
@click.option('--csv', help='CSV file to read data from.')
def tag(dryrun, verbose, region, role, resource, tag, csv):
    if csv and (len(resource) > 0 or len(tag) > 0):
        print("Cannot use --resource or --tag with --csv option")
        sys.exit(1)
    if csv:
        tagger = CSVResourceTagger(dryrun, verbose, role, region,
            tag_volumes=True)
        tagger.tag(csv)
    else:
        tagger = MultipleResourceTagger(dryrun, verbose, role, region,
            tag_volumes=True)
        tags = _tag_options_to_dict(tag)
        tagger.tag(resource, tags)


def _tag_options_to_dict(tag_options):
    tags = {}
    for tag_option in tag_options:
        key, value = tag_option.split(':')
        tags[key] = value
    return tags


@cli.command()
@click.option('--region-name', default="us-east-1")
@click.option('--tag-key', default=False)
def export_ec2_untagged(region_name, tag_key):
    instances = fetch.ec2_without_tag(region_name=region_name, tag_key=tag_key)
    count = len(instances)
    click.echo("... ec2: fetched ... {0}".format(count))
    filename = "ec2_untagged.csv"
    if count > 0:
        export.array_dict(instances, filename)
        click.echo("... ec2: exported to {}".format(filename))


@cli.command()
@click.option('--region-name', default="us-east-1")
@click.option('--tag-key', default=False)
def export_cf_untagged(region_name, tag_key):
    cfs = fetch.cf_without_tag(region_name=region_name, tag_key=tag_key)
    count = len(cfs)
    click.echo("... cf: fetched {0}".format(count))
    filename = "cf_untagged.csv"
    if count > 0:
        export.cloudformation(cfs, filename)
        click.echo("... cf: exported to {}".format(filename))


if __name__ == '__main__':
    cli()

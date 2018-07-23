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
@click.option('--tag', multiple=True, help='Tag to apply to resource in format "Key:Value".')
@click.option('--csv', help='CSV file to read data from.')
def tag(dryrun, verbose, region, role, resource, tag, csv):
    if csv and (len(resource) > 0 or len(tag) > 0):
        print("Cannot use --resource or --tag with --csv option")
        sys.exit(1)
    if csv:
        tagger = CSVResourceTagger(dryrun, verbose, role, region, tag_volumes=True)
        tagger.tag(csv)
    else:
        tagger = MultipleResourceTagger(dryrun, verbose, role, region, tag_volumes=True)
        tags = _tag_options_to_dict(tag)
        tagger.tag(resource, tags)


def _tag_options_to_dict(tag_options):
    tags = {}
    for tag_option in tag_options:
        key, value = tag_option.split(':')
        tags[key] = value
    return tags


@cli.command()
def export_ec2_untagged():
    instances = fetch.ec2_untagged()
    click.echo("fetched ... {0}".format(len(instances)))
    filename = "ec2_untagged.csv"
    export.array_dict(instances, filename)
    click.echo("exported")


if __name__ == '__main__':
    cli()

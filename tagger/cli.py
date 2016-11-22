#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import csv
@click.group()
def cli():
    pass

@cli.command()
@click.option('--resource', help='Resource ID.')
def tag(resource):
    print resource

if __name__ == '__main__':
    cli()

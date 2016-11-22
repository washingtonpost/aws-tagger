#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
from tagger import ResourceTagger

@click.command()
@click.option('--resource', help='Resource ID.')
def cli(resource):
    tags = {'Owner': 'Patrick Cullen'}
    tagger = ResourceTagger()
    tagger.tag(resource, tags)

if __name__ == '__main__':
    cli()

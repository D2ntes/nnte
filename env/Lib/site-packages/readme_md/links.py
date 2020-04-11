#!/usr/bin/env python
"""print README.md links"""
# -*- coding: utf-8 -*-
import click
import readme_md


MODULE_NAME = "readme_md.links"
PROG_NAME = 'python -m %s' % MODULE_NAME
USAGE = 'python -m %s path' % MODULE_NAME


@click.command()
@click.argument('path', required=True)
def _cli(path):
    string = open(path).read()
    links = readme_md.links(string)
    if links:
        print("\n".join(links))


if __name__ == '__main__':
    _cli(prog_name=PROG_NAME)

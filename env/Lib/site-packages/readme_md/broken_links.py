#!/usr/bin/env python
"""print README.md broken links"""
# -*- coding: utf-8 -*-
import click
import readme_md


MODULE_NAME = "readme_md.broken_links"
PROG_NAME = 'python -m %s' % MODULE_NAME
USAGE = 'python -m %s path [timeout]' % MODULE_NAME


@click.command()
@click.argument('path', required=True)
@click.argument('timeout', default=5, required=False)
def _cli(path, timeout):
    string = open(path).read()
    broken_links = readme_md.broken_links(string, timeout=timeout)
    if broken_links:
        print("\n".join(broken_links))


if __name__ == '__main__':
    _cli(prog_name=PROG_NAME)

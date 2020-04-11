#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""generate README.md"""
import sys
import readme_md

USAGE = 'python -m readme_md.create [path ...]'


def _cli():
    paths = sys.argv[1:]
    readme = readme_md.Readme()
    for path in paths:
        readme.load_sections(path)
    print(readme.render())


if __name__ == '__main__':
    _cli()

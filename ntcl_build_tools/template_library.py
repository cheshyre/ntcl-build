#!/usr/bin/env python3

from string import Template


def create_template_from_file(filename):
    with open(filename, 'r') as fh: template = Template(fh.read())
    return template

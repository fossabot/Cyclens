#!/usr/bin/env python
# coding: utf-8

"""
cyclens
~~~~~~~

Implements command-line-interface functions

This program comes with ABSOLUTELY NO WARRANTY; This is free software,
and you are welcome to redistribute it under certain conditions; See
file LICENSE, which is part of this source code package, for details.

:copyright: Copyright © 2019, The Cyclens Project
:license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals

import cv2
import json
import os
import click
import requests
import numpy as np

from PIL import Image


def get_response(image):
    url = 'http://localhost:5000/api/v1/demo/single'
    files = {'file': image}
    params = {'ap': 'true', 'er': 'true', 'fr': 'true', 'gp': 'true'}

    return requests.post(url, params = params, files = files)


def get_img(image):
    path = os.path.abspath(image)

    im = Image.open(path)

    arr = np.array(im)

    cvt = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

    _, res = cv2.imencode('.jpg', cvt)

    return res


@click.group()
def cli():
    pass


@cli.command()
@click.option("--image", type=click.Path(exists=True))
def hello(image):
    i = get_img(image)

    response = get_response(i)

    res = json.loads(response.text)

    click.echo(res)


if __name__ == '__main__':
    cli()

#!/usr/bin/env python
# coding: utf-8

"""
cyclens
~~~~~~~

Implements __init__.py used by Cyclens.

This program comes with ABSOLUTELY NO WARRANTY; This is free software,
and you are welcome to redistribute it under certain conditions; See
file LICENSE, which is part of this source code package, for details.

:copyright: Copyright © 2019, The Cyclens Project
:license: MIT, see LICENSE for more details.
"""


from .info import (
    __appname__,
    __version__,
    __license__,
    __url__,
    __author__,
    __authormail__,
    __maintainer__,
    __maintainermail__,
    __description__,
    __descriptionfull__,
    __copyright__,
    __licensefull__,
)

from .Cyclens import Cyclens

__all__ = ['main', 'Cyclens']

def main(argv=None):
    cyclens_main(argv)



def cyclens_main(argv=None):
    with Cyclens(None) as cyc:

        cyc.run()

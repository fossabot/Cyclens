#!/usr/bin/env python
# coding: utf-8

"""
cyclens
~~~~~~~

Implements utility functions.

This program comes with ABSOLUTELY NO WARRANTY; This is free software,
and you are welcome to redistribute it under certain conditions; See
file LICENSE, which is part of this source code package, for details.

:copyright: Copyright © 2019, The Cyclens Project
:license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals


class CyclensError(Exception):
    """Base exception for YoutubeDL errors."""
    pass


class PreProcessingError(CyclensError):
    """Pre-Processing exception."""

    def __init__(self, msg):
        super(PreProcessingError, self).__init__(msg)
        self.msg = msg


class ProcessingError(CyclensError):
    """Processing exception."""

    def __init__(self, msg):
        super(ProcessingError, self).__init__(msg)
        self.msg = msg


class PostProcessingError(CyclensError):
    """Post-Processing exception."""

    def __init__(self, msg):
        super(PostProcessingError, self).__init__(msg)
        self.msg = msg

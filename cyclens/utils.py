#!/usr/bin/env python
# coding: utf-8

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

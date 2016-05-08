#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from stupidlang.lang import main

__author__ = "Rahul Dave"
__copyright__ = "Rahul Dave"
__license__ = "mit"


def test_main():
    assert main(["tests/test2.sl"])=='7'

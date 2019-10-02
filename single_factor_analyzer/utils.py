#!/usr/bin/env python

import re
from typing import List


def get_forward_returns_columns(columns: List[str]):
    syntax = re.compile("^period_\\d+$")
    return columns[columns.astype("str").str.contains(syntax, regex=True)]

"""
Contains shared/common methods and functions.
"""

from typing import List
from string import Template


class DeltaTemplate(Template):
    delimiter = "%"


def camel_case_to_words(camel_case: str) -> str:
    
    pretty: List = []
    for char in camel_case:
        if char.isupper():
            pretty.append(' ')
            pretty.append(char.lower())
        else:
            pretty.append(char)
    return ''.join(map(str, pretty[1:]))


def camel_to_kebab_case(camel_case: str) -> str:
    
    kebab: List = []
    for char in camel_case:
        if char.isupper():
            kebab.append('-')
            kebab.append(char.lower())
        else:
            kebab.append(char)
    return ''.join(map(str, kebab[1:]))


def format_timedelta(timedelta, fmt):
    
    delta_format = {}
    milliseconds = timedelta.microseconds / 1000
    hours, rem = divmod(timedelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    delta_format["H"] = '{:02d}'.format(hours)
    delta_format["M"] = '{:02d}'.format(minutes)
    delta_format["S"] = '{:02d}'.format(seconds)
    delta_format["s"] = '{:.0f}'.format(milliseconds)
    template = DeltaTemplate(fmt)
    return template.substitute(**delta_format)

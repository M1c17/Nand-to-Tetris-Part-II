#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from helpers import valueSP_to_segmentValue

def handling_label(label):
    return '// label {}\n'.format(label) + \
           '({})\n'.format(label)
           
def handling_goto(label):
    return '// go {}\n'.format(label) + \
           '@{}\n'.format(label) + \
           '0; JMP\n'
           
def handling_if_goto(label):
    return '// goto {}\n'.format(label) + \
           valueSP_to_segmentValue() + \
           '@{}\n'.format(label) + \
           'D;JNE\n'


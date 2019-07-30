#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from helpers import valueSP_to_segmentValue, decrement_SP

"""

Stage I: Handling stack arithmetic commands: implement the nine 
aritmetic/logical commands of the VM language and VM command push 
constant x.
the first argument is constant and the second arg is some non-neg
integer x.

"""

label_counter = 0
           
def logical_command(operation):
    global label_counter
    
    true_label = 'TRUE_{}'.format(label_counter)
    false_label = 'FALSE_{}'.format(label_counter)
    continue_label = 'CONTINUE_{}'.format(label_counter)
    label_counter += 1
    
    return 'D=M-D\n' + \
           '@{}\n'.format(true_label) + \
           'D;{}\n'.format(operation) + \
           '@{}\n'.format(false_label) + \
           '0;JMP\n' + \
           '(' + true_label + ')\n' + \
           '@SP\n' + \
           'A=M-1\n' + \
           'M=-1\n' + \
           '@{}\n'.format(continue_label) + \
           '0;JMP\n' + \
           '(' + false_label + ')\n' + \
           '@SP\n' + \
           'A=M-1\n' + \
           'M=0\n' + \
           '@{}\n'.format(continue_label) + \
           '0;JMP\n' + \
           '(' + continue_label + ')\n'
           
    
def write_arithmetic(operation):
    
    if operation == 'add':
        return '//add\n' + \
               valueSP_to_segmentValue() + \
               decrement_SP() + \
               'M=D+M\n'
    elif operation == 'sub':
        return '//sub\n' + \
               valueSP_to_segmentValue() + \
               decrement_SP() + \
               'M=M-D\n'
    elif operation == 'neg':
        return '//neg\n' + \
               decrement_SP() + \
               'M=-M\n'
    elif operation == 'not':
        return '//not\n' + \
               decrement_SP() + \
               'M=!M\n'
    elif operation == 'or':
        return '//or\n' + \
               valueSP_to_segmentValue() + \
               decrement_SP() + \
               'M=D|M\n'
    elif operation == 'and':
        return '//and\n' + \
               valueSP_to_segmentValue() + \
               decrement_SP() + \
               'M=D&M\n'
    elif operation == 'eq':
        return '//eq\n' + \
               valueSP_to_segmentValue() + \
               decrement_SP() + \
               logical_command('JEQ')
    elif operation == 'lt':
        return '//lt\n' +\
               valueSP_to_segmentValue() + \
               decrement_SP() + \
               logical_command('JLT')
    else:
        return '//gt\n' + \
               valueSP_to_segmentValue() + \
               decrement_SP() + \
               logical_command('JGT')
    



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 14:31:50 2019

@author: MASTER
"""

def infinite_end():
    return '(END)\n' + \
           '@END\n' + \
           '0;JMP'
           
def push_segmentValue_to_stack():
    '''
    Take value store under segment *addr put it into stack 
    top most value 
    *SP = *addr
    SP++ incrementing by one the stack
    
    '''
    return '@SP\n' + \
           'M=M+1\n' + \
           'A=M-1\n' + \
           'M=D\n'

def decrement_SP():
    return '@SP\n' + \
           'A=M-1\n'

def valueSP_to_segmentValue():
    '''
    take value store under stack put it into address points it
    *addr=*SP
    
    '''
    return '@SP\n' + \
           'AM=M-1\n' + \
           'D=M\n' + \
           'M=0\n'


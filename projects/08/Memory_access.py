#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from helpers import push_segmentValue_to_stack, valueSP_to_segmentValue

#Implementing segment: constant

def push_constant_to_stack(constant):
    '''
    push constant to stack
    incrementing the stack by one
    
    '''
    return '//push constant {}\n'.format(constant) + \
           '@{}\n'.format(constant) + \
           'D=A\n' + \
           push_segmentValue_to_stack() 

#Implementing segments: local, argument, this, that

def push_segment_i(segment, index):
    '''
    1. compute target addr
    addr = segment pointer(base addr) + index
    2. push segment value to stack
    *SP=*addr
    3. incrementing stak by one
    SP++
    
    '''
    address = baseAddress_segment(segment)
    addr = address.get(segment)
    return '//push {} {}\n'.format(segment, index) + \
           '@{}\n'.format(index) + \
           'D=A\n' + \
           '@{}\n'.format(addr) + \
           'A=M+D\n' + \
           'D=M\n' + \
           push_segmentValue_to_stack()
           
def pop_segment_i(segment, index):
    '''
    1. compute target addr
    addr = segment pointer(base addr) + index
    2. decrement stack by one
    SP--
    3. take value store under *sp put it into address addr point it
    *addr=*SP
    
    '''
    address = baseAddress_segment(segment)
    addr = address.get(segment)
    return '//pop {} {}\n'.format(segment,index) + \
           '@{}\n'.format(index) + \
           'D=A\n' + \
           '@{}\n'.format(addr) + \
           'D=D+M\n' + \
           '@R13\n' + \
           'M=D\n' + \
           valueSP_to_segmentValue() + \
           '@R13\n' + \
           'A=M\n' + \
           'M=D\n'
         
##Implementing static 

def push_static_to_stack(file, index):
    file_name = file.replace('.vm', '').split('.vm')[0]
    segment_name = file_name.replace('Test', '').split('Test')[0]
    return '//push {} {}\n'.format(segment_name, index) + \
           '@{}.{}\n'.format(file_name, index) + \
           'D=M\n' + \
           push_segmentValue_to_stack()
           
def pop_static_to_stack(file, index):
    file_name = file.replace('.vm', '').split('.vm')[0]
    segment_name = file_name.replace('Test', '').split('Test')[0]
    return '//pop {} {}\n'.format(segment_name, index) + \
           valueSP_to_segmentValue() + \
           '@{}.{}\n'.format(file_name, index) + \
           'M=D\n'
           
##Implementing pointer & temp

def push_segmentAddr_to_stack(segment, index):
    '''
    temp: 
        addr = 5 + i, *SP=*addr, SP++
    pointer:
        *SP=THIS/THAT, SP++
    
    '''
    address = baseAddress_segment(segment)
    addr = address.get(segment)
    register = str(addr + int(index))
    return '//push {} {}\n'.format(segment, index) + \
           '@R{}\n'.format(register) + \
           'D=M\n' + \
           push_segmentValue_to_stack()
           
def pop_stack_to_segmentAddr(segment, index):
    '''
    temp:
        addr = 5 + i, SP--, *addr=*SP
    pointer:
        SP--, THIS/THAT = *SP
    ''' 
    address = baseAddress_segment(segment)
    addr = address.get(segment)
    register = str(addr + int(index))
    return '//pop {} {}\n'.format(segment, index) + \
           valueSP_to_segmentValue() + \
           '@R{}\n'.format(register) + \
           'M=D\n'

def baseAddress_segment(segment):
    return {
        'local': 'LCL',     #R1
        'argument': 'ARG',  #R2
        'this': 'THIS',     #R3
        'that': 'THAT',     #R4
        'pointer' : 3,      #0 THIS R3 - 1 THAT R4
        'temp' : 5,         #R5
        #R13 - R15 general purpose register
        'static' :16,       #R16 -> R255
        }

def command_push(segment, index, file):
    
    if segment in ['local', 'argument', 'this', 'that']:
        return push_segment_i(segment, index)
    elif segment in ['pointer', 'temp']:
        return push_segmentAddr_to_stack(segment, index)
    elif segment == 'static':
        return push_static_to_stack(file, index)
    elif segment == 'constant':
        constant = index
        return push_constant_to_stack(constant)
    else:
        raise Exception('Incorrect {}'.format(segment))

       
def command_pop(segment, index, file):
    if segment in ['local', 'argument', 'this', 'that']:
        return pop_segment_i(segment, index)
    elif segment in ['pointer', 'temp']:
        return pop_stack_to_segmentAddr(segment, index)
    elif segment == 'static':
        return pop_static_to_stack(file, index)
    else:
        raise Exception('Incorrect {}'.format(segment))

        
        
        
    




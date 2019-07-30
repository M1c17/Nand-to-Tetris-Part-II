#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Branching_command import handling_label, handling_goto
from helpers import saved_frame_of_the_caller, restores_frame_of_the_caller, push_segmentValue_to_stack
from Memory_access import push_constant_to_stack, pop_segment_i

        
def writeInit():
    '''
    When the VM implementation starts running or is reset, it starts
    executing the argument -less os function sys.init
    - register 256 store the value of stack pointer
    '''
    return '@256\n' + \
           'D=A\n' + \
           '@SP\n' + \
           'M=D\n' + \
           handling_call('Sys.init', 0)
          

def handling_call(functionName, nArgs):
    '''
    push returnAddress \\ Ussing the label declarated below
    Save frame of the caller \\ LCL, ARG, THIS, THAT
    ARG= SP -5 - nArgs \\ Repositions ARG
    LCL=SP             \\ Repositions LCL
    goto function Name \\ Transfers control to the called function
 (return Addres)       \\ Declares a label for the return - address
     '''
    call_counter = 0
    label_addr = '{}_{}'.format(functionName, str(call_counter))
    call_counter += 1
    return '// call {} locals: {}\n'.format(functionName, nArgs) + \
           '@{}\n'.format(label_addr) + \
           'D=A\n' + \
           push_segmentValue_to_stack() + \
           saved_frame_of_the_caller() + \
           '@SP\n' + \
           'D=M\n' + \
           '@5\n' + \
           'D=D-A\n' + \
           '@{}\n'.format(nArgs) + \
           'D=D-A\n' + \
           '@ARG\n' + \
           'M=D\n' + \
           '@SP\n' + \
           'D=M\n' + \
           '@LCL\n' + \
           'M=D\n' + \
           handling_goto(functionName) + \
           handling_label(label_addr)
           
def handling_function(functionName, nlocals):
    ''' 
    (function Name)     // declares a label for the function entry
    repeat nVars times  // nVars = number of local variables
    push 0              // initializes the local variables to 0 
    '''
    initialize_locals = ''
    for local in range(int(nlocals)):
        initialize_locals += push_constant_to_stack
        initialize_locals += pop_segment_i
                             
    return '// declare {} with locals {}\n'.format(functionName, nlocals) + \
            handling_label(functionName) + \
            initialize_locals

def handling_return():
    '''
    endFrame = LCL             // endFrame is a temporary variable
    retAddr = *(endFrame - 5)  // gets the return Address
    *ARG = pop()               // Repositions the return value for the caller
    (C_POP 'argument' 0)
    SP=ARG + 1                 // Repositions SP of the caller
    Restores segment frame of the caller  
    goto retAddr               // goes to return address in the caller's code
    '''
    endFrame = 'R13'
    retAddr = 'R14'
    return '// return\n' + \
           '@LCL\n' + \
           'D=M\n' + \
           '@{}\n'.format(endFrame) + \
           'M=D\n' + \
           '@5\n' + \
           'A=D-A\n' + \
           'D=M\n' + \
           '@{}\n'.format(retAddr) + \
           'M=D\n' + \
           '@SP\n' + \
           'A=M-1\n' + \
           'D=M\n' + \
           '@ARG\n' + \
           'A=M\n' + \
           'M=D\n' + \
           '@ARG\n' + \
           'D=M+1\n' + \
           '@SP\n' + \
           'M=D\n' + \
           restores_frame_of_the_caller() + \
           '@{}\n'.format(retAddr) + \
           'A=M\n' + \
           '0; JMP\n'
 
           
            
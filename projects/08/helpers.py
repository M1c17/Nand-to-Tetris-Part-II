#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

def saved_frame_of_the_caller():
    '''
    push LCL           \\ Saves LCL of the caller
    push ARG           \\ Saves ARG of the caller
    push THIS          \\ Saves THIS of the caller
    push THAT          \\ Saves THAT os the caller
    '''
    segment_pointer = ['LCL', 'ARG', 'THIS', 'THAT']
    saved_frame = ''
    for segment in segment_pointer:
        saved_segment = '@{}\n'.format(segment) + \
                        'D=M\n' + \
                        push_segmentValue_to_stack()
        saved_frame += saved_segment
    return saved_frame


def restores_frame_of_the_caller():
    '''
    THAT= *(endFrame -1)       // Restores THAT of the caller
    THIS= *(endFrame -2)       // Restores THIS of the caller
    ARG = *(endFrame -3)       // Restores ARG of the caller
    LCL = *(endFrame -4)       // Restores LCL of the caller 
    '''
    endFrame = 'R13'
    offset = 0
    restore_frame = ''
    segment_pointer = ['THAT', 'THIS', 'ARG', 'LCL']
    for segment in segment_pointer:
        offset +=1
        restore_segment = '@{}\n'.format(offset) + \
                          'D=A\n' + \
                          '@{}\n'.format(endFrame) + \
                          'A=M-D\n' + \
                          'D=M\n' + \
                          '@{}\n'.format(segment) + \
                          'M=D\n'

        restore_frame += restore_segment
    return restore_frame
                   
                          
               
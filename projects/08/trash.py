#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 15:51:37 2019

@author: MASTER
"""

def get_vm_files(mypath):
        
    files = []
    if os.path.isdir(mypath):
        glob_path = os.path.join('./', '**', '*.vm')
        for fileName in glob.glob(glob_path):
            files.append(fileName)
    elif os.path.isfile(mypath) and mypath.endswith('.vm'):
        files.append(mypath)
            
    return files


    return '// return\n' + \
           '@LCL\n' + \
           'D=M\n' + \
           '@{}\n'.format(endFrame) + \
           'M=D\n' + \
           '@5\n' + \
           'D=D-A\n' + \
           '@{}\n'.format(retAddr) + \
           'M=D\n' + \
           valueSP_to_segmentValue() + \
           '@ARG\n' + \
           'A=M\n' + \
           'M=D\n' + \
           'D=A+1\n'+ \
           '@SP\n' + \
           'M=D\n' + \
           
def restores_frame_of_the_caller():
    endFrame = 'R13'
    offset = 1
    restore_frame = ''
    segment_pointer = ['THAT', 'THIS', 'ARG', 'LCL']
    for segment in segment_pointer:
        if offset < 4:
            offset +=1
            restore_segment = 'D=M\n' + \
                              '@{}\n'.format(segment) + \
                              'M=D\n' + \
                              '@{}\n'.format(offset) + \
                              'D=A\n' + \
                              '@{}\n'.format(endFrame) + \
                              'D=M-D\n' + \
                              'A=D\n'
        else:
            restore_segment += 'D=M\n'+ \
                               '@{}\n'.format(segment) + \
                               'M=D\n'
                               
                               
def setFileName(fileName):
    '''
    Informs that the translation of anew VM file has started 
    '''
    file = fileName
    functionName = fileName
    if file == 'Sys':
        writeInit()            
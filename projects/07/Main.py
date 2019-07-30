#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Proposed design 
Parser: parser each VM command into its lexical elements
Code writer: writes the assembly code that implements the parsed
Main: drives the process (VMTranslator)

"""
from Parser import parse_generator
from Arithmetic_Commands import write_arithmetic
from Memory_access import command_push, command_pop
from helpers import infinite_end


def get_output_filename(vm_file):
    if '.vm' in vm_file:
        termination = vm_file.replace('.vm', '.asm')
        return termination

def translate_to_asm(vm_file):
    output_file = get_output_filename(vm_file)
    parser = parse_generator(vm_file)
    with open(output_file, 'w') as f:
        for command_type, arg_1, arg_2 in parser:
            if command_type == 'C_ARITHMETIC':
                f.write(write_arithmetic(arg_1))
            elif command_type == 'C_PUSH':
                f.write(command_push(arg_1, arg_2, vm_file))
            elif command_type == 'C_POP':
                f.write(command_pop(arg_1, arg_2, vm_file))  
        f.write(infinite_end())
                
#a = translate('StaticTest.vm')
#print(a) 


                      



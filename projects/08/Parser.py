#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parser
- Handles the parsing of a single .vm file
- Reads a VM command, parser the command into its lexical components
and provides convenient access to these components 
- Ignore all comments and white space to the begining and end of the line

"""
def ignore_comments(line):
    ignore_comments=line.split('/')[0]
    return ignore_comments.strip()
        
def command_type(split_command):
    '''
    Return: C_ARITHMETIC
            C_PUSH
            C_POP
            C_LABEL
            C_GOTO
            C_IF
            C_FUNCTION
            C_RETURN
            C_CALL
    Function: Returns a cosntant representing the type of 
    the current command.
    '''
    return {
            'add':     'C_ARITHMETIC',
            'sub':     'C_ARITHMETIC',
            'neg':     'C_ARITHMETIC',
            'eq' :     'C_ARITHMETIC',
            'gt' :     'C_ARITHMETIC',
            'lt' :     'C_ARITHMETIC',
            'and':     'C_ARITHMETIC',
            'or' :     'C_ARITHMETIC',
            'not':     'C_ARITHMETIC',
            'push':    'C_PUSH',
            'pop':     'C_POP',
            'label':   'C_LABEL',
            'goto':    'C_GOTO',
            'if-goto': 'C_IF',
            'function':'C_FUNCTION',
            'return':  'C_RETURN',
            'call':    'C_CALL',
            }[split_command[0]] 
    
def arg_1(split_command, command_type):
    '''
    Return: String
    Function: Return the first argument of the current command
    '''
    if command_type == 'C_RETURN':
        return None
    elif command_type == 'C_ARITHMETIC':
        #print(split_command[0])
        return split_command[0]
    else:
        #print(split_command[1])
        return split_command[1]


def arg_2(split_command, command_type):
    '''
    Return: int
    Function: Return the second argument of the current command
    '''
    if command_type in ['C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL']:
        #print(split_command[2])
        return split_command[2]
    
def parser_generator(file):
    '''
    Return: command_type , arg_1, arg_2
    Function: read the file and generate 3 outputs for each command.
    '''
    with open(file, 'r') as f:
    
        for line in f:
            command = ignore_comments(line)
            if not command:
                continue
            split_command = command.split(' ')
            #print(split_command)
            get_command_type = command_type(split_command)
            #print(get_command_type)
            get_arg_1 = arg_1(split_command, get_command_type)
            get_arg_2 = arg_2(split_command, get_command_type)
        
            yield get_command_type, get_arg_1, get_arg_2
     
#a=parser_generator('BasicTest.vm')
#print(a)

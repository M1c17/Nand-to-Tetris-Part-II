
"""
Proposed design 
Parser: parser each VM command into its lexical elements
Code writer: writes the assembly code that implements the parsed
Main: drives the process (VMTranslator)

"""
from Parser import parser_generator
from Arithmetic_Commands import write_arithmetic
from Memory_access import command_push, command_pop
from helpers import infinite_end
from Function_command import writeInit, handling_return, handling_call, handling_function
from Branching_command import handling_label, handling_goto, handling_if_goto


def get_output_fileName(vm_file):
    if '.vm' in vm_file:
        termination = vm_file.replace('.vm', '.asm')
        return termination
    
def translate(vm_file):
    output_file = get_output_fileName(vm_file)

    with open(output_file, 'w') as f: 
        f.write(writeInit() + '\n')
        parser = parser_generator(vm_file)
        file_name = vm_file.split('/')[-1]
        for command_type, arg_1, arg_2 in parser:
            if command_type == 'C_ARITHMETIC':
                f.write(write_arithmetic(arg_1))
            elif command_type == 'C_PUSH':
                f.write(command_push(arg_1, arg_2, file_name))
            elif command_type == 'C_POP':
                f.write(command_pop(arg_1, arg_2, file_name))
            elif command_type == 'C_LABEL':
                f.write(handling_label(arg_1))
            elif command_type == 'C_GOTO':
                f.write(handling_goto(arg_1))
            elif command_type == 'C_IF':
                f.write(handling_if_goto(arg_1))
            elif command_type == 'C_FUNCTION':
                f.write(handling_function(arg_1, arg_2))
            elif command_type == 'C_CALL':
                f.write(handling_call(arg_1, arg_2))
            elif command_type == 'C_RETURN':
                f.write(handling_return()) 
        f.write(infinite_end())

a = translate('Sys.vm')
print(a)





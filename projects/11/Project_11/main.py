import sys
import glob

from Compilation_Engine import compile_file


def _is_jack_file(file):
    return file.split('.')[1] == 'jack'


def _get_jack_files(arg):
    if '.' in arg:
        jack_files = [arg]
    else:
        pattern = '/**/*.jack'
        jack_files = glob.glob(pattern)

    return (file for file in jack_files if _is_jack_file(file))


def _get_output_filename(arg):
    return arg.replace('jack', 'vm')


if __name__ != '__main__':
    print('Please run as a self-contained program')

jack_files = _get_jack_files(sys.argv[1])

for file in jack_files:
    output_file = open(_get_output_filename(file), 'w')
    compile_file(output_file, file)
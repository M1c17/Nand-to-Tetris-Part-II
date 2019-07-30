#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 16:56:50 2019

@author: MASTER
"""
from Tokenizer import Tokenizer

stack_tokens = []
tokens = []


def _write(xml_file, line):
    xml_file.write('{}'.format(line))


def write_token(xml_file, token_type, token_value):
    _write(xml_file, '<{}> {} </{}>\n'.format(token_type, token_value, token_type))


def get_tokens(jack_file):
    token_generator = Tokenizer(jack_file)
    for token in token_generator:
        if not token:
            continue
        tokens.append(token)
    return tokens


def pop_token(stack):
    stack.pop(0)


def eat(xml_file, tokenType, tokenValue, token):
    token_type, token_val = token
    if tokenValue in ['static', 'field']:
        if token_type == tokenType:
            write_token(xml_file, token_type, token_val)
            pop_token(tokens)
    elif token_type == tokenType:
        if tokenValue == token_val:
            write_token(xml_file, token_type, token_val)
            pop_token(tokens)


def compile_Class(xml_file, jack_file):
    """
    compiles a complete class
    class 'class' className '{' classVarDec* subroutineDec* '}'
    """
    get_tokens(jack_file)
    token = tokens[0]
    token_type, token_val = token
    while token_type in ['keyword', 'identifier', 'symbol']:
        token = tokens[0]
        token_type, token_val = token
        if token_val == 'class':
            eat(xml_file, 'keyword', token_val, token)
            _write(xml_file, '<class>\n')
        elif token_type == 'identifier':
            eat(xml_file, 'identifier', token_val, token)
        elif token_val == '{':
            eat(xml_file, 'symbol', '{', token)
            compile_class_Var_Dec(xml_file)
            compile_class_Subroutine_Dec(xml_file)
        else:
            eat(xml_file, 'symbol', '}', token)
            _write(xml_file, '</class>\n')
            break


def compile_class_Var_Dec(xml_file):
    """
    compiles a static variable declaration, or a field declaration
    ('static' | 'field' ) type varName (',' varName)* ';'
    """
    token = tokens[0]
    token_type, token_val = token
    while token_type in ['keyword', 'identifier', 'symbol']:
        token = tokens[0]
        token_type, token_val = token
        if token_val in ['field', 'static']:
            _write(xml_file, '<classVarDec>\n')
            eat(xml_file, 'keyword', token_val, token)
        elif token_type == 'identifier':
            eat(xml_file, 'identifier', token_val, token)
        elif token_val in ['int', 'char', 'boolean']:
            eat(xml_file, 'keyword', token_val, token)
        elif token_val == ';':
            eat(xml_file, 'symbol', token_val, token)
            _write(xml_file, '</classVarDec>\n')
        elif token_val == ',':
            eat(xml_file, 'symbol', token_val, token)
        else:
            if token_val in ['constructor', 'function', 'method']:
                break


def compile_class_Subroutine_Dec(xml_file):
    """
    compile a complete method, function or constructor
    ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
    """
    token = tokens[0]
    token_type, token_val = token
    while token_type in ['keyword', 'identifier', 'symbol']:
        token = tokens[0]
        token_type, token_val = token
        if token_val in ['constructor', 'function', 'method']:
            _write(xml_file, '<Subroutine_Dec>\n')
            eat(xml_file, 'keyword', token_val, token)
        elif token_type == 'keyword':
            eat(xml_file, 'keyword', token_val, token)
        elif token_type == 'identifier':
            eat(xml_file, 'identifier', token_val, token)
        elif token_val == '(':
            eat(xml_file, 'symbol', token_val, token)
            compile_Parameter_List(xml_file)
        elif token_val == '{':
            compile_Subroutine_Body(xml_file)
            _write(xml_file, '</Subroutine_Dec>\n')
        else:
            break


def compile_Parameter_List(xml_file):
    """
    compile a (possibly empty) parameter list. does not handle
    the enclosing '()'
    ((type varName) (',' type varName)*)?
    """
    _write(xml_file, '<Parameter_List>\n')
    token = tokens[0]
    token_type, token_val = token
    while token_type in ['keyword', 'identifier', 'symbol']:
        token = tokens[0]
        token_type, token_val = token
        if token_val in ['int', 'char', 'boolean']:
            eat(xml_file, 'keyword', token_val, token)
        elif token_type == 'identifier':
            eat(xml_file, 'identifier', token_val, token)
        elif token_val == ',':
                eat(xml_file, 'symbol', token_val, token)
        else:
            if token_val == ')':
                _write(xml_file, '</Parameter_List>\n')
                eat(xml_file, 'symbol', token_val, token)
                break

def compile_Var_Dec(xml_file):
    """
    compile a var Declaration
    'var' type varName (',' varName)* ';'
    """
    token = tokens[0]
    token_type, token_val = token
    while token_type in ['keyword', 'identifier', 'symbol']:
        token = tokens[0]
        token_type, token_val = token
        if token_val in ['int', 'char', 'boolean']:
            eat(xml_file, 'keyword', token_val, token)
        elif token_val == 'var':
            _write(xml_file, '<varDec>\n')
            eat(xml_file, 'keyword', token_val, token)
        elif token_type == 'identifier':
            eat(xml_file, 'identifier', token_val, token)
        elif token_val == ',':
            eat(xml_file, 'symbol', token_val, token)
        else:
            if token_val == ';':
                eat(xml_file, 'symbol', token_val, token)
                _write(xml_file, '</varDec>\n')
                break


def compile_Subroutine_Body(xml_file):
    """
    compile a subroutines body
    '{' varDec* statements '}'
    """
    _write(xml_file, '<Subroutine_body>\n')
    token = tokens[0]
    token_type, token_val = token
    while token_type in ['keyword', 'identifier', 'symbol']:
        token = tokens[0]
        token_type, token_val = token
        if token_val == 'var':
            compile_Var_Dec(xml_file)
        elif token_val == '{':
            eat(xml_file, 'symbol', token_val, token)
        elif token_val in ['let', 'if', 'while', 'do', 'return']:
            compile_Statements(xml_file)
        else:
            if token_val == '}':
                eat(xml_file, 'symbol', token_val, token)
                break;

    _write(xml_file, '</Subroutine_body>\n')


def compile_Statements(xml_file):
    """
    compile a sequence of statements.
    does not handle the enclosing '{}'
    letStatement | ifStatement | whileStatement | doStatement | returnStatement
    """
    _write(xml_file, '<statements>\n')
    token = tokens[0]
    token_type, token_val = token
    while token_type == 'keyword':
        token = tokens[0]
        token_type, token_val = token
        if token_val == 'let':
            compile_let(xml_file)
        elif token_val == 'if':
            compile_if(xml_file)
        elif token_val == 'while':
            compile_while(xml_file)
        elif token_val == 'do':
            compile_do(xml_file)
        elif token_val == 'return':
            compile_return(xml_file)
        else:
            break
    _write(xml_file, '</statements>\n')


def compile_let(xml_file):
    """
    compile as if statement, possibly with a trailing
    else clause
    'let' varName '=' expression ';'
    or
    'let' varName '[' expression1 ']'? '=' expression2 ';'
    """
    token = tokens[0]
    token_type, token_val = token
    while token_type in ['keyword', 'identifier', 'symbol']:
        token = tokens[0]
        token_type, token_val = token
        if token_val == "let":
            _write(xml_file, '<let_Statement>\n')
            eat(xml_file, 'keyword', token_val, token)
        elif token_type == 'identifier':
            eat(xml_file, 'identifier', token_val, token)
        elif token_val == '[':
            eat(xml_file, 'symbol', token_val, token)
            compile_Expression(xml_file)
        elif token_val == ']':
            eat(xml_file, 'symbol', token_val, token)
        elif token_val == '=':
            eat(xml_file, 'symbol', token_val, token)
            compile_Expression(xml_file)
        else:
            if token_val in ';':
                eat(xml_file, 'symbol', token_val, token)
                _write(xml_file, '</let_Statement>\n')
                break


def compile_while(xml_file):
    """
    compile a while statement
    'while'(' expresion ')' '{' statements '}'
    """
    token = tokens[0]
    token_type, token_val = token
    while token_type in ['keyword', 'identifier', 'symbol']:
        token = tokens[0]
        token_type, token_val = token
        if token_val == "while":
            _write(xml_file, '<while_Statement>\n')
            eat(xml_file, 'keyword', token_val, token)
        elif token_val == '(':
            eat(xml_file, 'symbol', token_val, token)
            compile_Expression(xml_file)
        elif token_val == '{':
            eat(xml_file, 'symbol', token_val, token)
            compile_Statements(xml_file)
        else:
            if token_val == '}':
                eat(xml_file, 'symbol', token_val, token)
                _write(xml_file, '</while_Statement>\n')
                break


def compile_do(xml_file):
    """
    compile a do statement
    do function-or-method-call
    subroutineCall: subroutineName '(' expressionList ')' |
     '(' className | varName ')' '.' subroutineName '(' expressionList ')'
    """
    token = tokens[0]
    token_type, token_val = token
    while token_type in ['keyword', 'symbol', 'identifier']:
        token = tokens[0]
        token_type, token_val = token
        if token_val == "do":
            _write(xml_file, '<do_Statement>\n')
            eat(xml_file, 'keyword', token_val, token)
            compile_subroutine_call(xml_file)
        elif token_val == ')':
            eat(xml_file, 'symbol', token_val, token)
        else:
            if token_val == ';':
                eat(xml_file, 'symbol', token_val, token)
                _write(xml_file, '</do_Statement>\n')
                break


def compile_return(xml_file):
    """
    compile a return statement
    'return' expression? ';'
    or return ';'
    """

    token = tokens[0]
    token_type, token_val = token
    while token_type in ['keyword', 'symbol']:
        token = tokens[0]
        token_type, token_val = token
        if token_val == "return":
            _write(xml_file, '<return_Statement>\n')
            eat(xml_file, 'keyword', token_val, token)
        elif token_val != ';':
            compile_Expression(xml_file)
        else:
            if token_val == ';':
                eat(xml_file, 'symbol', token_val, token)
                _write(xml_file, '</return_Statement>\n')
                break


def compile_if(xml_file):
    """
    compile if statement
    'if' '(' expression ')' '{' statements1 '}' 'else' '{' statements2 '}' ?
    """
    token = tokens[0]
    token_type, token_val = token
    while token_type in ['keyword', 'identifier', 'symbol']:
        token = tokens[0]
        token_type, token_val = token
        if token_val == "if":
            _write(xml_file, '<if_Statement>\n')
            eat(xml_file, 'keyword', token_val, token)
        elif token_val == '(':
            eat(xml_file, 'symbol', token_val, token)
            compile_Expression(xml_file)
        elif token_val == '{':
            eat(xml_file, 'symbol', token_val, token)
            compile_Statements(xml_file)
        elif token_val == '}':
            eat(xml_file, 'symbol', token_val, token)
            token = tokens[0]
            token_type, token_val = token
            if token_val == "else":
                eat(xml_file, 'keyword', token_val, token)
            else:
                _write(xml_file, '</if_Statement>\n')
                break


def compile_Expression(xml_file):
    """
    compiles an expression
    term (op term)*
    """
    _write(xml_file, '<expression>\n')
    compile_term(xml_file)
    token = tokens[0]
    token_type, token_val = token
    while token_type == 'symbol':
        token = tokens[0]
        token_type, token_val = token
        if token_val in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            eat(xml_file, 'symbol', token_val, token)
            compile_term(xml_file)
        elif token_val == ')':
            eat(xml_file, 'symbol', token_val, token)
        else:
            break

    _write(xml_file, '</expression>\n')

def compile_subroutine_call(xml_file):
    token = tokens[0]
    token_type, token_val = token
    while token_type in ['identifier', 'symbol']:
        token = tokens[0]
        token_type, token_val = token
        if token_type == 'identifier':
            eat(xml_file, 'identifier', token_val, token)
        elif token_val == '.':
            eat(xml_file, 'symbol', token_val, token)
        elif token_val == '(':
            eat(xml_file, 'symbol', token_val, token)
            compile_Expression_List(xml_file)
        else:
            if token_val in [';', ')']:
                break


def compile_term(xml_file):
    """
    compile a term. if the current token is an identifier,
    the routine must distinguish between a variable, an array
    entry, or a subroutine call, a single look - ahead token
    which may be one of '[''(' or ',' '.', suffies to distinguish
    between the possibilities. Any other token is not part of this
    term & should not be advanced over.
    varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
    """

    _write(xml_file, '<term>\n')
    token = tokens[0]
    token_type, token_val = token
    while token_type in ['keyword', 'identifier', 'symbol', 'integer_constant', 'string_constant']:
        token = tokens[0]
        token_type, token_val = token
        if token_type == 'integer_constant':
            eat(xml_file, 'integer_constant', token_val, token)
        elif token_type == 'string_constant':
            eat(xml_file, 'string_constant', token_val, token)
        elif token_val in ['true', 'false', 'null', 'this']:
            eat(xml_file, 'keyword', token_val, token)
            break
        elif token_val == '(':
            eat(xml_file, 'symbol', token_val, token)
            compile_Expression(xml_file)
        elif token_val == '[':
            eat(xml_file, 'symbol', token_val, token)
            compile_Expression(xml_file)
        elif token_val == ']':
            break
        elif token_type == 'identifier':
            eat(xml_file, 'identifier', token_val, token)
            token = tokens[0]
            token_type, token_val = token
            if token_val == '.':
                compile_subroutine_call(xml_file)
        elif token_val in ['-', '~']:
            eat(xml_file, 'symbol', token_val, token)
            compile_term(xml_file)
        elif token_val in [',', ')', ';', ']', '{']:
            break
        else:
            if token_val in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
                break

    _write(xml_file, '</term>\n')


def compile_Expression_List(xml_file):
    """
    compiles a (possibly empty) comma separated list of expressions
    (expression (',' expression)* )?
    """
    _write(xml_file, '<expression_List>\n')
    token = tokens[0]
    token_type, token_val = token
    if token_val != ')':
        compile_Expression(xml_file)
        token = tokens[0]
        token_type, token_val = token
        while token_val == ',':
            eat(xml_file, 'symbol', token_val, token)
            compile_Expression(xml_file)
            token = tokens[0]
            token_type, token_val = token
            if token_val in [')', ';']:
                break

    _write(xml_file, '</expression_List>\n')


def compile_file(output_file, file):
    compile_Class(output_file, file)

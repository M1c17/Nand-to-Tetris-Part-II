from Tokenizer import Tokenizer
from Symbol_Table import define, _kind_Of, _Index_Of, start_subroutine
from VM_Writer import write_arithmetic, write_call, write_function, write_goto, \
  write_if, write_label, write_pop, write_push, write_return

tokens = []
while_num = 0


def get_tokens(jack_file):
  token_generator = Tokenizer(jack_file)
  for token in token_generator:
    if not token:
      continue
    tokens.append(token)
  return tokens


def pop_token(stack):
  stack.pop(0)


def eat(tokenType, tokenValue, token):
  token_type, token_val = token
  if tokenValue in ['static', 'field']:
    if token_type == tokenType:
      pop_token(tokens)
  elif token_type == tokenType:
    if tokenValue == token_val:
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
      eat('keyword', token_val, token)
    elif token_type == 'identifier':
      class_name = token_val
      eat('identifier', token_val, token)
    elif token_val == '{':
      eat('symbol', '{', token)
      compile_class_Var_Dec(xml_file)
      compile_class_Subroutine_Dec(xml_file, class_name)
    else:
      if token_val == '}':
        eat('symbol', '}', token)
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
      kind = token_val
      eat('keyword', token_val, token)
    elif token_val in ['int', 'char', 'boolean']:
      _type = token_val
      eat('keyword', token_val, token)
    elif token_type == 'identifier':
      name = token_val
      eat('identifier', token_val, token)
      import pdb;
      pdb.set_trace()
      define(name, _type, kind)
    elif token_val == ';':
      eat('symbol', token_val, token)
    elif token_val == ',':
      eat('symbol', token_val, token)
    else:
      if token_val in ['constructor', 'function', 'method']:
        break


def compile_class_Subroutine_Dec(xml_file, class_name=''):
  """
    compile a complete method, function or constructor
    ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
    """
  token = tokens[0]
  token_type, token_val = token
  start_subroutine()
  while token_type in ['keyword', 'identifier', 'symbol']:
    token = tokens[0]
    token_type, token_val = token

    if token_val in ['constructor', 'function', 'method']:
      subroutine_type = token_val
      eat('keyword', token_val, token)
    elif token_type == 'keyword':
      eat('keyword', token_val, token)
    elif token_type == 'identifier':
      if class_name:
        subroutine_name = '{}.{}'.format(class_name, token_val)
      else:
        subroutine_name = token_val
      eat('identifier', token_val, token)
    elif token_val == '(':
      eat('symbol', token_val, token)
      compile_Parameter_List(xml_file)
    elif token_val == '{':
      compile_Subroutine_Body(xml_file, subroutine_type, subroutine_name)
    else:
      break


def compile_Parameter_List(xml_file):
  """
    compile a (possibly empty) parameter list. does not handle
    the enclosing '()'
    ((type varName) (',' type varName)*)?
    """
  token = tokens[0]
  token_type, token_val = token
  while token_type in ['keyword', 'identifier', 'symbol']:
    token = tokens[0]
    token_type, token_val = token

    if token_val in ['int', 'char', 'boolean']:
      _type = token_val
      eat('keyword', token_val, token)
    elif token_type == 'identifier':
      name = token_val
      eat('identifier', token_val, token)
      define(name, _type, 'argument')
    elif token_val == ',':
      eat('symbol', token_val, token)
    else:
      if token_val == ')':
        eat('symbol', token_val, token)
        break


def compile_Var_Dec(xml_file):
  """
  compile a var Declaration
  'var' type varName (',' varName)* ';'
  """
  token = tokens[0]
  token_type, token_val = token
  if (token_type, token_val) != ('keyword', 'var'):
    return 0
  num_vars = 1
  while token_type in ['keyword', 'identifier', 'symbol']:
    token = tokens[0]
    token_type, token_val = token
    if token_val in ['int', 'char', 'boolean']:
      _type = token_val
      eat('keyword', token_val, token)
    elif token_val == 'var':
      eat('keyword', token_val, token)
    elif token_type == 'identifier':
      name = token_val
      eat('identifier', token_val, token)
      define(name, _type, 'local')
      num_vars += 1
    elif token_val == ',':
      eat('symbol', token_val, token)
    else:
      if token_val == ';':
        eat('symbol', token_val, token)
        break
  return num_vars


def compile_Subroutine_Body(xml_file, subroutine_type, subroutine_name):
  """
  compile a subroutines body
  '{' varDec* statements '}'
  """
  token = tokens[0]
  token_type, token_val = token
  while token_type in ['keyword', 'identifier', 'symbol']:
    token = tokens[0]
    token_type, token_val = token

    if token_val == 'var':
      compile_Var_Dec(xml_file)
    elif token_val == '{':
      num_locals = compile_Var_Dec(xml_file)
      if subroutine_type == 'method':
        num_locals += 1
      write_function(xml_file, subroutine_name, num_locals)
      if subroutine_type == 'constructor':
        write_push(xml_file, 'constant', num_locals)
        write_call(xml_file, 'Memory.alloc', 1)
      if subroutine_type == 'method':
        write_push(xml_file, 'argument', 0)
        write_pop(xml_file, 'pointer', 0)
      eat('symbol', token_val, token)
    elif token_val in ['let', 'if', 'while', 'do', 'return']:
      compile_Statements(xml_file)
    else:
      if token_val == '}':
        eat('symbol', token_val, token)
        break


def compile_Statements(xml_file):
  """
    compile a sequence of statements.
    does not handle the enclosing '{}'
    letStatement | ifStatement | whileStatement | doStatement | returnStatement
    """
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
      eat('keyword', token_val, token)
    elif token_type == 'identifier':
      symbol = token_val
      kind = _kind_Of(symbol)
      index = _Index_Of(symbol)
      eat('identifier', token_val, token)
    elif token_val == '[':
      eat('symbol', token_val, token)
      compile_Expression(xml_file)
      write_push(xml_file, kind, index)
    elif token_val == ']':
      eat('symbol', token_val, token)
      write_arithmetic(xml_file, 'add')
      token = tokens[0]
      token_type, token_val = token
      if token_val == '=':
        eat('symbol', token_val, token)
        compile_Expression(xml_file)
        write_pop(xml_file, 'temp', 0)
        write_pop(xml_file, 'pointer', 1)
        write_push(xml_file, 'temp', 0)
        write_pop(xml_file, 'that', 0)
    elif token_val == '=':
      eat('symbol', token_val, token)
      compile_Expression(xml_file)
      write_pop(xml_file, kind, index)

    else:
      if token_val in ';':
        eat('symbol', token_val, token)
        break


def compile_while(xml_file):
  """
  compile a while statement
  'while'(' expresion ')' '{' statements '}'
  """
  global while_num

  token = tokens[0]
  token_type, token_val = token
  while token_type in ['keyword', 'identifier', 'symbol']:
    token = tokens[0]
    token_type, token_val = token
    if token_val == "while":
      eat('keyword', token_val, token)
      while_expression_label = 'WHILE_{}'.format(while_num)
      while_continuation_label = 'WHILE_END_{}'.format(while_num)
      while_num += 1
      write_label(xml_file, while_expression_label)
    elif token_val == '(':
      eat('symbol', token_val, token)
      compile_Expression(xml_file)
      write_arithmetic(xml_file, 'not')
      write_if(xml_file, while_continuation_label)
    elif token_val == '{':
      eat('symbol', token_val, token)
      compile_Statements(xml_file)
    else:
      if token_val == '}':
        write_goto(xml_file, while_expression_label)
        write_label(xml_file, while_continuation_label)
        eat('symbol', token_val, token)
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
      eat('keyword', token_val, token)
      compile_subroutine_call(xml_file)
    elif token_val == ')':
      eat('symbol', token_val, token)
    else:
      if token_val == ';':
        write_pop(xml_file, 'temp', 0)
        eat('symbol', token_val, token)
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
      eat('keyword', token_val, token)
    elif token_val != ';':
      compile_Expression(xml_file)
    else:
      if token_val == ';':
        write_pop(xml_file, 'constant', 0)
        eat('symbol', token_val, token)
        write_return(xml_file)
        break


def compile_if(xml_file):
  """
  compile if statement
  'if' '(' expression ')' '{' statements1 '}' 'else' '{' statements2 '}' ?
  """
  global while_num
  label_if_true = 'IF_TRUE_{}'.format(while_num)
  label_if_false = 'IF_FALSE_{}'.format(while_num)
  label_if_continuation = 'IF_CONTINUATION_{}'.format(while_num)
  while_num += 1

  token = tokens[0]
  token_type, token_val = token
  while token_type in ['keyword', 'identifier', 'symbol']:
    token = tokens[0]
    token_type, token_val = token
    if token_val == "if":
      eat('keyword', token_val, token)
    elif token_val == '(':
      eat('symbol', token_val, token)
      compile_Expression(xml_file)
      write_if(xml_file, label_if_true)
      write_goto(xml_file, label_if_false)
      write_label(xml_file, label_if_true)
    elif token_val == '{':
      eat('symbol', token_val, token)
      compile_Statements(xml_file)
      write_goto(xml_file, label_if_continuation)
    elif token_val == '}':
      eat('symbol', token_val, token)
      token = tokens[0]
      token_type, token_val = token
      if token_val == "else":
        write_label(xml_file, label_if_false)
        eat('keyword', token_val, token)
        token = tokens[0]
        token_type, token_val = token
        if token_val == '{':
          eat('symbol', token_val, token)
          compile_Statements(xml_file)
      else:
        break
  write_label(xml_file, label_if_continuation)


# add = false - true ??
def compile_subroutine_call(xml_file):
  token = tokens[0]
  token_type, token_val = token
  while token_type in ['identifier', 'symbol']:
    token = tokens[0]
    token_type, token_val = token
    if token_type == 'identifier':
      eat('identifier', token_val, token)
      subroutine_name = token_val
    elif token_val == '.':
      subroutine_name += '.'
      eat('symbol', token_val, token)
      subroutine_name += token_val
    elif token_val == '(':
      eat('symbol', token_val, token)
      compile_Expression_List(xml_file)
      num_args = compile_Expression_List(xml_file)
      add_arg = True
      if add_arg:
        num_args += 1
      write_call(xml_file, subroutine_name, num_args)
    else:
      if token_val in [';', ')']:
        break


def compile_Expression(xml_file):
  """
  compiles an expression
  term (op term)*
  """
  compile_term(xml_file)
  token = tokens[0]
  token_type, token_val = token
  while token_type == 'symbol':
    token = tokens[0]
    token_type, token_val = token

    if token_val in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
      if token_val == '*':
        write_call(xml_file, 'Math.multiply', 2)
      elif token_val == '/':
        write_call(xml_file, 'Math.divide', 2)
      else:
        command = {
          '+': 'add',
          '-': 'sub',
          '&': 'and',
          '|': 'or',
          '<': 'lt',
          '>': 'gt',
          '=': 'eq'
        }[token_val]
        write_arithmetic(xml_file, command)
      eat('symbol', token_val, token)
      compile_term(xml_file)

    elif token_val == ')':
      eat('symbol', token_val, token)
    else:
      break


def _is_term(token_type, token_val):
  return token_type in ['true', 'false', 'null', 'this'] or \
         token_val in ['(', ')', '-', '~'] or \
         token_val in ['true', 'false', 'null', 'this']


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
  token = tokens[0]
  token_type, token_val = token

  if not _is_term(token_type, token_val):
    return

  while token_type in ['keyword', 'identifier', 'symbol', 'integer_constant', 'string_constant']:
    token = tokens[0]
    token_type, token_val = token
    if token_type == 'integer_constant':
      eat('integer_constant', token_val, token)
      write_push(xml_file, 'constant', token_val)
    elif token_type == 'string_constant':
      eat('string_constant', token_val, token)
      write_push(xml_file, 'constant', len(token_val))
      write_call(xml_file, 'String.new', 1)
      for letter in token_val:
        write_push(xml_file, 'constant', ord(letter))
        write_call(xml_file, 'string.appendChar', 2)
    elif token_val in ['true', 'false', 'null', 'this']:
      if token_val in ['false', 'null']:
        write_push(xml_file, 'constant', 0)
      elif token_val == 'true':
        write_push(xml_file, 'constant', 1)
      else:
        write_push(xml_file, 'pointer', 0)
      eat('keyword', token_val, token)
      break
    elif token_val == '(':
      eat('symbol', token_val, token)
      compile_Expression(xml_file)
    elif token_val == '[':
      kind = _kind_Of(token_val)
      index = _Index_Of(token_val)
      eat('symbol', token_val, token)
      compile_Expression(xml_file)
      write_push(xml_file, kind, index)
      write_arithmetic(xml_file, 'add')
      write_pop(xml_file, 'pointer', 1)
      write_push(xml_file, 'that', 0)
    elif token_val == ']':
      break
    elif token_type == 'identifier':
      kind = _kind_Of(token_val)
      index = _Index_Of(token_val)
      write_push(xml_file, kind, index)
      eat('identifier', token_val, token)
      token = tokens[0]
      token_type, token_val = token
      if token_val == '.':
        compile_subroutine_call(xml_file)
    elif token_val in ['-', '~']:
      eat('symbol', token_val, token)
      compile_term(xml_file)
      command = {'-': 'neg', '~': 'not'}[token_val]
      write_arithmetic(xml_file, command)
    elif token_val in [',', ')', ';', ']', '{']:
      break
    else:
      if token_val in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
        break


def compile_Expression_List(xml_file):
  """
  compiles a (possibly empty) comma separated list of expressions
  (expression (',' expression)* )?
  """
  num_args = 0
  token = tokens[0]
  token_type, token_val = token
  if token_val != ')':
    compile_Expression(xml_file)
    num_args += 1
    token = tokens[0]
    token_type, token_val = token
    while token_val == ',':
      eat('symbol', token_val, token)
      compile_Expression(xml_file)
      token = tokens[0]
      token_type, token_val = token
      num_args += 1
      if token_val in [')', ';']:
        break
  return num_args


def compile_file(output_file, file):
  compile_Class(output_file, file)

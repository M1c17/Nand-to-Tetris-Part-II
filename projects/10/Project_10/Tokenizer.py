import re

# &quot "
##&amp &
##&lt <
##&gt >


_keyword = ['class', 'constructor', 'function', 'method', \
            'field', 'static', 'var', 'int', 'char', 'boolean', \
            'void', 'true', 'false', 'null', 'this', 'let', 'do', \
            'if', 'else', 'while', 'return']

_symbol = ["{", "}", "[", "]", "(", ")", ".", ",", ";", "+", "-", "*", "/",
            "&", "|", "<", ">", "=", "~"]

keyword_pattern = 'class|method|function|constructor|int|boolean|char|void| \
                   var|static|field|let|do|if|else|while|return|true|false| \
                   null|this'

symbol_pattern = '{|}|\[|\]|\(|\)|\.|,|;|\+|-|\*|\/|&|\||<|>|=|~'

Integer_Constant_Pattern = '\d+'

String_Constant_Pattern = '\".*\"'

Identifier_Pattern = '[A-Za-z_]\w*'

Tokens_patterns = r'({}|{}|{}|{}|{})'.format(keyword_pattern, symbol_pattern,
                                             Integer_Constant_Pattern, String_Constant_Pattern,
                                             Identifier_Pattern)


def remove_comments(line):
    stripped_white_space = line.strip()
    remove_pattern = re.compile(r'(\/\/|\*\s*[a-zA-Z]|\*\/.|\/\*)\s?.*')
    without_comment = remove_pattern.sub('', stripped_white_space)
    return without_comment


def find_all_tokens(line):
    without_comments = remove_comments(line)
    return re.findall(Tokens_patterns, without_comments)


def get_token(word):
    if word in _keyword:
        return 'keyword', word

    elif word in _symbol:
        return 'symbol', word

    elif word == ''.join(re.findall(Integer_Constant_Pattern, word)):
        return 'integer_constant', word

    elif word == ''.join(re.findall(String_Constant_Pattern, word)):
        return 'string_constant', word.replace("\"", "")

    elif word == ''.join(re.findall(Identifier_Pattern, word)):
        return 'identifier', word
    else:
        return " Error. incorrect token"


def Tokenizer(jack_file):
    with open(jack_file, 'r') as f:
        for line in f:
            without_comments = remove_comments(line)
            tokens = find_all_tokens(without_comments)
            #            print(tokens)
            for token in tokens:
                if not token:
                    continue
                yield get_token(token)
                #print(get_token(token))

#a = Tokenizer('Main.jack')
#print(a)

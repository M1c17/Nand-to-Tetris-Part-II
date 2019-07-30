class_scope = {}
subroutine_scope = {}

class_kinds = ['static', 'field']
subroutine_kinds = ['argument', 'local']


def _get_scope(kind):
    """
    STATIC, & FIELD identifiers have a class scope,
    while ARG and VAR identifiers have a subroutine scope.
    """
    return {
        'static': class_scope,
        'field': class_scope,
        'argument': subroutine_scope,
        'local': subroutine_scope
    }[kind]


def define(name, _type, kind):
    """
    :param name: string
    :param _type: string
    :param kind: STATIC, FIELD, ARG or VAR
    :return: -
    function: Defines a new identifier of the given name, types & kind, and assigns it a
    running index.
    """
    _get_scope(kind)[name] = (_type, kind, _var_count(kind))


def _var_count(kind):
    """
    :param kind: STATIC, FIELD, ARG or VAR
    :return: int
    function: returns the number of variables of the given kind already defined in the current
    scope
    """

    return len(list(filter(lambda x: x[1] == kind, _get_scope(kind).values())))


def _kind_Of(name):
    """
    :param name: string
    :return: STATIC, FIELD, ARG, VAR, NONE
    function: returns the kind of the named identifier in the current scope.
    if the identifier is unknown in the current scope, returns NONE
    """
    return ((name in class_scope and class_scope[name][1] or
             name in subroutine_scope and subroutine_scope[name][1] or
             None))


def _Type_Of(name):
    """
    :param name: string
    :return: string
    function: returns the type of the named identifier in the current scope
    """
    return ((name in class_scope and class_scope[name][0]) or
            (name in subroutine_scope and subroutine_scope[name][0]) or
             None)


def _Index_Of(name):
    """
    :param name: string
    :return: int
    function: returns the index assigned to the named identifier
    """
    return ((name in class_scope and class_scope[name][2]) or
            (name in subroutine_scope and subroutine_scope[name][2]) or
            0)


def start_subroutine():
    global subroutine_scope
    subroutine_scope = {}
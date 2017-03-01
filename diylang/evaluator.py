# -*- coding: utf-8 -*-

from .types import Environment, DiyLangError, Closure, String
from .ast import is_boolean, is_atom, is_symbol, is_list, is_closure, is_integer, is_string
from .parser import unparse

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports,
making your work a bit easier. (We're supposed to get through this thing
in a day, after all.)
"""

def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""

    d('ast ' + str(ast))

    if ast == True \
            or ast == False \
            or is_integer(ast):
        return ast

    fn = ast[0]
    d('fn ' + str(fn))
    if fn == 'quote':
        return ast[1]

    if fn == 'atom':
        return not is_list(evaluate(ast[1], env))

    d('1 -> ' + str(ast[1]))
    d('2 -> ' + str(ast[2]))

    expr1 = []
    if len(ast) >= 1:
        expr1 = evaluate(ast[1], env)

    expr2 = []
    if len(ast) >= 2:
        expr2 = evaluate(ast[2], env)

    if fn == 'eq':
        return not is_list(expr1) and expr1 == expr2

    return math(fn, expr1, expr2)

    raise NotImplementedError("DIY")

def math(fn, expr1, expr2):
    print(expr1)
    print(expr2)

    if not is_integer(expr1) or not is_integer(expr2):
        raise DiyLangError

    if fn == '+':
        return expr1 + expr2

    if fn == '-':
        return expr1 - expr2

    if fn == '/':
        return expr1 / expr2

    if fn == '*':
        return expr1 * expr2

    if fn == 'mod':
        return expr1 % expr2

    if fn == '>':
        return expr1 > expr2


def d(s):
    #print(s)
    pass

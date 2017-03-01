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
        return is_atom(evaluate(ast[1], env))

    expr1 = expr(ast, 1, env)

    if fn == 'eq':
        expr2 = expr(ast, 2, env)
        return not is_list(expr1) and expr1 == expr2

    if fn == 'if':
        if expr1 == True:
            return expr(ast, 2, env)
        return expr(ast, 3, env)

    expr2 = expr(ast, 2, env)
    return math(fn, expr1, expr2)

    raise NotImplementedError("DIY")

def expr(ast, idx, env):
    if len(ast) <= idx:
        return []

    return evaluate(ast[idx], env)

def math(fn, expr1, expr2):
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

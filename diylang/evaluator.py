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

    print('---------- eval')
    print(ast)

    if is_symbol(ast):
        try:
            return env.lookup(ast)
        except:
            raise DiyLangError('my-var')

    d('ast ' + str(ast))

    if ast == True \
            or ast == False \
            or is_integer(ast):
        return ast

    if len(ast) == 0:
        raise DiyLangError

    fn = ast[0]
    d('fn ' + str(fn))

    if is_closure(fn):
        print('is closure')
        return eval_closure(fn, ast[1:], env)

    if fn == 'quote':
        return ast[1]

    if fn == 'atom':
        return is_atom(evaluate(ast[1], env))

    if fn == 'define':
        print('storing var: %s = %s' % ( ast[1], expr(ast, 2, env) ) )
        if len(ast) != 3:
            raise DiyLangError('Wrong number of arguments')
        env.set(ast[1], expr(ast, 2, env))
        return None

    if fn == 'lambda':
        print('parsing lambda')
        if not is_list(ast[1]):
            raise DiyLangError
        if len(ast) != 3:
            raise DiyLangError('number of arguments')
        return Closure(env, ast[1], ast[2])

    expr1 = expr(ast, 1, env)

    if fn == 'eq':
        expr2 = expr(ast, 2, env)
        return not is_list(expr1) and expr1 == expr2

    if fn == 'if':
        if expr1 == True:
            return expr(ast, 2, env)
        return expr(ast, 3, env)

    expr2 = expr(ast, 2, env)

    if fn == 'cons':
        return [ expr1 ] + expr2

    if fn == 'head':
        if not is_list(expr1):
            raise DiyLangError
        if len(expr1) == 0:
            raise DiyLangError
        return expr1[0]

    if fn == 'tail':
        if not is_list(expr1):
            raise DiyLangError
        if len(expr1) == 0:
            raise DiyLangError
        return expr1[1:]

    if fn == 'empty':
        if not is_list(expr1):
            raise DiyLangError
        return len(expr1) == 0

    result = math(fn, expr1, expr2)
    if not result is None:
        return result

    if is_symbol(fn):
        #print('is LAMBDA CALL')
        symbol = env.lookup(fn)
        print('got symbol: ' + str(symbol))
        return eval_closure(symbol, ast[1:], env)

    if is_list(fn):
        print('direct call')
        call = evaluate(fn, env)
        print('call: ' + str(call))
        # TODO recurse
        if is_closure(call):
            return eval_closure(call, ast[1:], env)
        raise DiyLangError

    print('*************')
    print(ast)
    print(fn)

    raise DiyLangError('not a function')

    raise NotImplementedError("DIY")

def expr(ast, idx, env):
    if len(ast) <= idx:
        return []

    return evaluate(ast[idx], env)

def math(fn, expr1, expr2):
    if fn == '+':
        assert_integer(expr1, expr2)
        return expr1 + expr2

    if fn == '-':
        assert_integer(expr1, expr2)
        return expr1 - expr2

    if fn == '/':
        assert_integer(expr1, expr2)
        return expr1 / expr2

    if fn == '*':
        assert_integer(expr1, expr2)
        return expr1 * expr2

    if fn == 'mod':
        assert_integer(expr1, expr2)
        return expr1 % expr2

    if fn == '>':
        assert_integer(expr1, expr2)
        return expr1 > expr2

    return None

def assert_integer(expr1, expr2):
    if not is_integer(expr1) or not is_integer(expr2):
        raise DiyLangError

def eval_closure(fn, args, env):
    if len(fn.params) != len(args):
        raise DiyLangError('wrong number of arguments, expected %d got %d' % (len(fn.params), len(args)))
    bound_params = zip(fn.params, [evaluate(arg, env) for arg in args])
    bound_env = fn.env.extend(dict(bound_params))
    return evaluate(fn.body, bound_env)

def d(s):
    #print(s)
    pass

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

    d('--- eval: ' + str(ast))

    if is_symbol(ast):
        try:
            return env.lookup(ast)
        except:
            raise DiyLangError('my-var')

    d('ast ' + str(ast))

    if ast == True \
            or ast == False \
            or is_integer(ast) \
            or is_string(ast):
        return ast

    if len(ast) == 0:
        raise DiyLangError

    fn = ast[0]
    d('fn ' + str(fn))

    if is_closure(fn):
        return eval_closure(fn, ast[1:], env)

    if fn == 'quote':
        return ast[1]

    if fn == 'atom':
        return is_atom(evaluate(ast[1], env))

    if fn == 'define':
        if len(ast) != 3:
            raise DiyLangError('Wrong number of arguments')
        ex = expr(ast, 2, env)
        print('storing var: %s = %s' % ( ast[1], ex ) )
        env.set(ast[1], ex)
        return None

    if fn == 'defn':
        #ex = expr(ast, 2, env)
        name = ast[1]
        args = ast[2]
        body = ast[3]
        print('storing func: %s :: %s => %s' % ( name, args, body) )
        closure = Closure(env, args, body)
        env.set(name, closure)
        return None

    if fn == 'lambda':
        #print('parsing lambda: ' + str(ast))
        if not is_list(ast[1]):
            raise DiyLangError
        if len(ast) != 3:
            raise DiyLangError('number of arguments')
        return Closure(env, ast[1], ast[2])

    if fn == 'cond':
        for case in ast[1]:
            if evaluate(case[0], env):
                return evaluate(case[1], env)
        return False

    if fn == 'let':
        letenv = Environment()
        letenv.extend(env.bindings)

        bindings = ast[1]

        for binding in bindings:
            letenv.set(binding[0], evaluate(binding[1], letenv))

        e = ast[2]

        return evaluate(e, letenv)

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
        if is_string(expr2):
            return String(expr1.val + expr2.val);

        print("cons'd : %s" % ([ expr1 ] + expr2))
        return [ expr1 ] + expr2

    if fn == 'head':
        if is_list(expr1):
            if len(expr1) == 0:
                raise DiyLangError
            return expr1[0]

        if is_string(expr1):
            if len(expr1.val) == 0:
                raise DiyLangError
            return String(expr1.val[0])

        raise DiyLangError

    if fn == 'tail':
        if is_list(expr1):
            if len(expr1) == 0:
                raise DiyLangError
            return expr1[1:]

        if is_string(expr1):
            if len(expr1.val) == 0:
                raise DiyLangError
            return String(expr1.val[1:])

        raise DiyLangError

        if not is_list(expr1):
            raise DiyLangError
        if len(expr1) == 0:
            raise DiyLangError

        return expr1[1:]

    if fn == 'empty':
        if is_list(expr1):
            return len(expr1) == 0

        if is_string(expr1):
            return len(expr1.val) == 0

        raise DiyLangError

    result = math(fn, expr1, expr2)
    if not result is None:
        return result

    if is_symbol(fn):
        #print('is LAMBDA CALL')
        symbol = env.lookup(fn)
        d('got symbol: ' + str(symbol))
        return eval_closure(symbol, ast[1:], env)

    if is_list(fn):
        call = evaluate(fn, env)
        print('call: ' + str(call))
        # TODO recurse
        if is_closure(call):
            return eval_closure(call, ast[1:], env)
        raise DiyLangError

    print('************* ERROR')
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

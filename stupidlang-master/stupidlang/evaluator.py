import math
import operator as op
from .parser import parse, Symbol

def global_env(envclass):
    "An environment with some Scheme standard procedures."
    env = envclass.empty()
    env.extend_many(vars(math))
    env.extend_many({
        '+':op.add, '-':op.sub, '*':op.mul, '/':op.truediv,
        'abs':     abs,
        'max':     max,
        'min':     min,
        'round':   round,
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '==':op.eq,
        'not':     op.not_
    })
    return env

class Function():
    def __init__(self, params, parsedbody, env):
        self.params = params
        self.code = parsedbody
        self.env = env
        self.envclass = env.__class__

    def __call__(self, *args):
        funcenv = self.envclass(outerenv = self.env)
        funcenv.extend_many(zip(self.params, args))
        return eval_ptree(self.code, funcenv)

def eval_ptree(x, env):
    fmap={'#t':True, '#f':False, 'nil':None}
    if x in ('#t', '#f', 'nil'):
        return fmap[x]
    elif isinstance(x, Symbol):
        # variable lookup
        return env.lookup(x)[0]
    elif not isinstance(x, list):  # constant
        return x
    elif len(x)==0: #noop
        return None
    elif x[0]=='if':
        (_, predicate, truexpr, falseexpr) = x
        if eval_ptree(predicate, env):
            expression = truexpr
        else:
            expression = falseexpr
        return eval_ptree(expression, env)
    elif x[0] == 'def':         # variable definition
        (_, var, expression) = x
        #postorder traversal by nested eval is needed below
        # your code here
        env.extend(var, eval_ptree(expression, env))
    elif x[0] == 'store':           # (set! var exp)
        (_, var, exp) = x
        env.lookup(var)[1].extend(var, eval_ptree(exp, env))
    elif x[0] == 'func':
        (_, parameters, parsedbody) = x
        return Function(parameters, parsedbody, env)
    else:                          # operator
        op = eval_ptree(x[0], env)
        #postorder traversal to get subexpressione before running the op
        args = [eval_ptree(arg, env) for arg in x[1:]]
        return op(*args)

class Program():
    """
    The representation of the program, and a mechanism for running it.

    Methods
    -------

    __init__
        Constructor takes an io stream and an env
    __iter__
        Yields the source code of the program line by line
    parse
        Yields the program list by list, with each list being the
        parse of a line
    run
        Yields the result of running each line.
    """

    def __init__(self, program, env):
        self.program = program
        self.env = env

    def __iter__(self):
        for line in self.program:
            yield line

    def parse(self):
        for l in iter(self):
            yield parse(l)

    def run(self):
        """
        a generator that runs the program, line by line

        Yields
        ------

        str, int, float, or None
            The result of running a single line of stupidlang code.
            The lines in the program are run from beginning to end.
        """
        for l in iter(self):
            yield eval_ptree(parse(l), self.env)

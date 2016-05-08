from .parser import parse
from .evaluator import eval_ptree, Program

def backtolang(exp):
    """
    Takes a expression list and converts it back into a
    stupidlang expression.

    Parameters
    ----------

    exp : list
        A list representing a parsed stupidlang expression

    Returns
    -------
    str
        A string with the corrsponding stupidlang code

    Examples
    --------

    >>> backtolang(None)
    nil
    >>> backtolang(True)
    #t
    >>> backtolang()
    """
    boolmap={True:'#t', False:'#f'}
    if  isinstance(exp, list):
        return '(' + ' '.join(map(backtolang, exp)) + ')'
    elif isinstance(exp, bool):
        return boolmap[exp]
    elif exp is None:
        return 'nil'
    else:
        return str(exp)

def repl(env, prompt='SL> '):
    """
    A REPL for the stupidlang language

    Parameters
    ----------

    env : Environment
        a concrete implementation instance of the Environment interface
    prompt : str, optional
        a string for the prompt, default SL>

    """
    try:
        import readline
    except:
        pass
    while True:
        try:
            val = eval_ptree(parse(input(prompt)), env)
        except (KeyboardInterrupt, EOFError):
            break
        if val is not None:
            print(backtolang(val))

def run_program_asif_repl(program, env):
    """
    Runs code with output as-if we were in a repl

    Parameters
    ----------

    program: str
        a multi-line string representing the stupidlang program
    env : Environment
        a concrete implementation instance of the Environment interface

    Returns
    -------

    str:
        The output of the program as if it were being run in a REPL
    """
    prog=Program(prpgram, env)
    for result in prog.run():
        print(backtolang(result))

def run_program(program, env):
    """
    Runs code without output until the last line where output is provided.

    Parameters
    ----------

    program: str
        a multi-line string representing the stupidlang program
    env : Environment
        a concrete implementation instance of the Environment interface

    Returns
    -------

    str:
        The last output of the program as if it were being run in a REPL

    """

    prog=Program(program, env)
    endit = None
    for result in prog.run():
        endit = result
    return backtolang(endit)

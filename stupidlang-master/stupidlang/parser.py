Symbol = str

def typer(token):
    if token == 'true':
        return True
    elif token == 'false':
        return False
    try:
        t = int(token)
        return t
    except ValueError:
        try:
            t = float(token)
            return t
        except ValueError:
            return Symbol(token)
        
def lex(loc):
    tokenlist =  loc.replace('(', ' ( ').replace(')', ' ) ').split()
    return [typer(t) for t in tokenlist]

def syn(tokens):
    if len(tokens) == 0:
        return []
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(syn(tokens))
        tokens.pop(0) # pop off ')'
        return L
    else:
        if token==')':
            assert 1, "should not have got here"
        return token
    
def parse(loc):
    return syn(lex(loc))
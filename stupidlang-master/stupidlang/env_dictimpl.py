
from .envinterface import Environment

class Env:
    """
    Absfun: the dicionary {k1:v1, k2:v2,...} represents the
    environment binding k1 to v1 and k2 to v2. There are no duplicates.

    The keys k must be strings, and the values v must be legitimate values
    in our environment.

    The empty dictionary represents the empty environment.

    Repinv: Newer bindings replace older bindings in the dictionary.
    This is guaranteed by using python dictionaries.
    """

    def __init__(self, outerenv=None):
        self.env = dict()
        self.outerenv = outerenv

    @classmethod
    def empty(cls):
        return cls()

    def extend(self, variable, value):
        self.env[variable] = value

    def extend_many(self, envdict):
        self.env.update(envdict)

    def lookup(self, key):
        try:
            found = self.env[key]
            env = self
        except KeyError:
            if self.outerenv is not None:
                found, env =self.outerenv.lookup(key)
            else:
                raise NameError("{} <<>> not found in Environment".format(key))
        return found, env

Environment.register(Env)
#print("Registered Env")

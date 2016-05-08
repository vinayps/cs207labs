import abc
class Environment(abc.ABC):
    """
    This is the interface for an Environment. The client for 
    this interface is a language intepreter. 
    """
    @classmethod
    @abc.abstractmethod
    def empty(cls):
        return cls()
    
    @abc.abstractmethod
    def extend(self, variable, value):
        """
        extend an existing environment by binding variable to value.
        The values must be an acceptable value in the language. If the
        same variable is used twice the newer value must be bound.
        """
    
    @abc.abstractmethod
    def extend_many(self, envdict):
        """
        extend the current environment by values in the dictionary
        envdict. If the dictionary contains variables already in the
        environment, the newer values from the dictionary are bound
        """
        
    @abc.abstractmethod
    def lookup(variable):
        """
        return the unique binding of the variable and the environment it was bound
        in as a tuple. If it is not found raise a NameError as below
        """
        raise NameError("{} not found in Environment".format(vaiable))
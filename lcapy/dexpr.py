"""This modules provides the dExpr class to provide common methods for
the discrete-time representations.

Copyright 2020 Michael Hayes, UCECE

"""

import numpy as np
from .expr import Expr

class dExpr(Expr):

    """Superclass of discrete-time, discrete-frequency, and z-domain
    expressions."""


    def __call__(self, arg, **assumptions):
        """Transform domain or substitute arg for variable. 
        
        Substitution is performed if arg is a tuple, list, numpy
        array, or constant.  If arg is a tuple or list return a list.
        If arg is an numpy array, return numpy array.

        Domain transformation is performed if arg is a domain variable
        or an expression of a domain variable.

        See also evaluate.

        """

        from .fexpr import f
        from .nexpr import n
        from .kexpr import k
        from .zexpr import z

        if isinstance(arg, (tuple, list)):
            return [self._subs1(self.var, arg1) for arg1 in arg]

        if isinstance(arg, np.ndarray):
            return np.array([self._subs1(self.var, arg1) for arg1 in arg])

        if id(arg) in (id(n), id(z), id(k), id(f)):
            return self.transform(arg, **assumptions)

        if arg in (n, k, z, f):
            return self.transform(arg, **assumptions)    

        # Do we really want to this?   
        return super(dExpr, self).__call__(arg, **assumptions)

    def transform(self, arg, **assumptions):

        from .nexpr import nExpr, n
        from .kexpr import kExpr, k
        from .zexpr import zExpr, z
        from .fexpr import f        

        # Is this wise?   It makes sense for Voltage and Impedance objects
        # but may cause too much confusion for other expressions
        if arg is n and isinstance(self, zExpr):
            return self.IZT(**assumptions)
        elif arg is n and isinstance(self, kExpr):
            return self.IDFT(**assumptions)        
        elif arg is z and isinstance(self, nExpr):
            return self.ZT(**assumptions)
        elif arg is z and isinstance(self, kExpr):
            return self.IDFT(**assumptions).ZT(**assumptions)
        elif arg is k and isinstance(self, nExpr):
            return self.DFT(**assumptions)
        elif arg is k and isinstance(self, zExpr):
            return self.IZT(**assumptions).DFT(**assumptions)
        elif arg is f and isinstance(self, nExpr):
            return self.DTFT(**assumptions)
        elif arg is f and isinstance(self, zExpr):
            return self.DTFT(**assumptions)                
        
        # Do we really want to this?   
        super(dExpr, self).transform(arg, **assumptions)            

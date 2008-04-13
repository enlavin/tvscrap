# -*- coding: utf-8 -*-
"""
func.py

Algunas utilidades funcionales
"""
def retry_n(func, niter):
    """ Reintenta una funcion N veces o devuelve una excepcion """
    def _inner(*args, **kwargs):
        _inner.__doc__ = func.__doc__
        for idx in range(niter):
            try:
                result = func(*args, **kwargs)
                if not result:
                    raise Exception()
                return result
            except Exception,exp:
                print "excepcion"
                if idx == niter - 1:
                    raise exp
    return _inner


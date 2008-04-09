def retry_n(func, n):
    """ Reintenta una funcion N veces o devuelve una excepcion """
    def _inner(*args, **kwargs):
        for i in range(n):
            try:
                result = func(*args, **kwargs)
                if not result:
                    raise Exception()
                return result
            except Exception,e:
                print "excepcion"
                if i == n-1:
                    raise e
    return _inner



from functools import wraps


def deco1(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("func.__doc__: %s, func.__name__: %s" % (func.__doc__, func.__name__))
        return func(*args, **kwargs)

    return wrapper


@deco1
def t1(a):
    print("in t1")


def deco2(func):
    print("in deco2")
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def t2(b):
    print("in t2")


t2 = deco2(t2)


if __name__ == '__main__':
    t1(a=1)
    print("t1.__doc__: %s, t1.__name__: %s" % (t1.__doc__, t1.__name__))
    # t2(b=2)


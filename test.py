# n = 7
# f0 = 0
# f1 = 1

# f2 = f0 + f1

def f(n):

    while n <= 1:
        fn = f(n)-2 + f(n)-1
        n = n+1
    print(fn)
    return fn




def fn(n):
    if n <= 2:
        return 1
    f = fn(n-1) + fn(n-2)
    return f


print(fn(7))

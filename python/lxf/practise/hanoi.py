def hanoi(n, a, b, c):
    if n == 1:
        print("%s --> %s" % (a, c))
        return
    hanoi(n - 1, a, c, b)
    print("%s --> %s" % (a, c))
    hanoi(n - 1, b, a, c)


hanoi(3, 'A', 'B', 'C')

MAX_RANGE = 1001


def bs():
    try:
        n = int(raw_input("count of need to sort: "))
        _list = []
        for x in range(n):
            i = int(raw_input("number %s: " % (x + 1)))
            if 0 <= i < MAX_RANGE:
                _list.append(i)
            else:
                print "wrong range"
                return
    except ValueError:
        print "need int"
        return
    _range = [0 for x in range(MAX_RANGE)]
    for i in _list:
        _range[i] += 1

    _b = MAX_RANGE
    while _b > 0:
        _b -= 1
        for i in range(_range[_b]):
            print _b


bs()

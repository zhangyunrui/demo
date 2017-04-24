MAX_RANGE = 1001


def bbs():
    try:
        m = int(raw_input("count of need to sort: "))
        _list = []
        for x in range(m):
            i = int(raw_input("number %s: " % (x + 1)))
            _list.append(i)
    except ValueError:
        print "need int"
        return

    while m > 1:
        n = 0
        m -= 1
        while n < m:
            if _list[n] < _list[n + 1]:
                _list[n], _list[n + 1] = _list[n + 1], _list[n]
            n += 1
    # i = 0
    # while i < m - 1:
    #     j = 0
    #     i += 1
    #     while j < m - i:
    #         if _list[j] < _list[j + 1]:
    #             _list[j], _list[j + 1] = _list[j + 1], _list[j]
    #         j += 1

    print _list


bbs()

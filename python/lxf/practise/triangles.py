def triangles():
    _list = [1]
    while True:
        _list = [x + y for x, y in zip(([0] + _list), (_list + [0]))]
        yield _list


triangles()

_tuple = ('ab', 'b', 'e', 'c', 'd', 'e', 'ab')

new_list = []

for i in _tuple:
    if _tuple.count(i) == 1:
        new_list.append(i)

_new_tuple = tuple(new_list)

print(_new_tuple)
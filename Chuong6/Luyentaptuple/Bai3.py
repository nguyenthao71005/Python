_tuple = ('ab', 'b', 'e', 'c', 'd', 'e', 'ab')

new_list = []

for i in _tuple:
    if i not in new_list:
        new_list.append(i)

_new_tuple = tuple(new_list)

print(_new_tuple)
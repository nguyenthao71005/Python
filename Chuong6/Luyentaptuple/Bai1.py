_tuple = ('a', 'b', 'd', 'e')

# Chuyển sang list
temp = list(_tuple)

# Thêm phần tử 'c' vào vị trí 2
temp.insert(2, 'c')

# Chuyển lại thành tuple
_new_tuple = tuple(temp)

print(_new_tuple)
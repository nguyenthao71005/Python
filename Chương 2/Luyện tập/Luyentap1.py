_a = int(16)
_b = int(3)
_c = int(5)
print(_a + _b + _c)
print(_a - _b - _c)
print(_a * _b * _c)
print(_a / _b / _c)
print(_a // _b // _c)
print(_a % _b % _c)
print(_a ** _b)

print(_a > _b)
print(_a < _b)
print(_a == _b)
print(_a != _b)

_a = 10
print(_a)
_a += 5
print(_a)
_a -= 3
print(_a)
_a *= 2
print(_a)
_a /= 4
print(_a)
_a //= 2
print(_a)
_a %= 3
print(_a)
_a **= 3
print(_a)

ketqua1 = _a > _b and _a < _c
ketqua2 = _a > _b or _a < _c    
ketqua3 = not (_a > _b)
print(ketqua1)
print(ketqua2)
print(ketqua3)

ketqua4 = _c & _b
ketqua5 = _c | _b
ketqua6 = _b ^ _b
ketqua7 = ~_b
ketqua8 = _c << 3
ketqua9 = _c >> 2
print(ketqua4)
print(ketqua5)
print(ketqua6)
print(ketqua7)
print(ketqua8)
print(ketqua9)

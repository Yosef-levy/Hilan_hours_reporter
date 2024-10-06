sep = '%'
hex1 = 'adf3cbe2'
hex2 = '7e6ba8dc4b5'


def encrypt(user_name, password):
    data = user_name + sep + password
    hexa = bytes(data, encoding='utf-8').hex()
    hexa = hexa + hex1
    hexa = hexa[::-1]
    tmp = ''
    for i, digit in enumerate(hexa):
        tmp += hex(15 - int(digit, 16)).split('x')[1]
    hexa = tmp
    hexa = hexa + hex2
    return (hex(int(hexa, 16) << 2)).split('x')[1]


def decrypt(s):
    res = s
    res = hex(int(res, 16) >> 2).split('x')[1]
    res = res.removesuffix(hex2)
    tmp = ''
    for i, digit in enumerate(res):
        tmp += hex(15 - int(digit, 16)).split('x')[1]
    res = tmp
    res = res[::-1]
    res = res.removesuffix(hex1)
    data_bytes = bytes.fromhex(res)
    return data_bytes.decode(encoding='utf-8').split(sep)


if __name__ == '__main__':
    user = "USER"
    password = "Password987654"
    res = decrypt(encrypt(user, password))
    if res != [user, password]:
        print('Fail')
    print('Pass')







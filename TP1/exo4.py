import math
from zipfile import ZipFile


def get_alphabet():
    alphabet = []
    for i in range(26):
        alphabet.append(chr(ord('a') + i))
    return alphabet


def get_passwords(size, pwd=""):
    if size != 1:
        for char in get_alphabet():
            yield from get_passwords(size-1, pwd+char)
    else:
        for char in get_alphabet():
            yield pwd+char




if __name__ == "__main__":
    fileName = 'archive.zip'
    with ZipFile(fileName) as fs:
        try:
            fs.extractall(pwd = bytes('', 'utf-8'))
        except RuntimeError as pwdRequired:
            pwd_size = 1
            pwd_found = False
            while not pwd_found:
                print(f"password trial size: {pwd_size}")
                for password in get_passwords(pwd_size):
                    try:
                        fs.extractall(pwd = bytes(password, 'utf-8'))
                    except Exception as wrongPwd:
                        continue
                    print(f"password is {password}")
                    pwd_found = True
                    break
                pwd_size += 1
                if pwd_size > 10:
                    print("password not found...")
                    pwd_found = True

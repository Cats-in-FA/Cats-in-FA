from pathlib import Path

from logic import encrypt, decrypt


def check_file(path_to_file: str) -> bool:
    p = Path(path_to_file)
    return p.exists() == True and p.is_dir() == False


def read_file_strings(file_name: str) -> str:
    with open(file_name, 'r', encoding="utf8") as ff:
        return ff.read()


def read_file_bytes(file_name: str) -> bytes:
    with open(file_name, 'rb') as ff:
        return ff.read()


def write_file_bytes(file_name: str, data: bytes) -> None:
    with open(file_name, 'wb') as ff:
        ff.write(data)


def encrypt_logic(read_file_name: str, write_file_name: str, key: str) -> str:
    data = read_file_bytes(read_file_name)

    crypted_data = []
    temp = []
    for byte in data:
        temp.append(byte)
        if len(temp) == 16:
            crypted_part = encrypt(temp, key)
            crypted_data.extend(crypted_part)
            del temp[:]
    else:

        if 0 < len(temp) < 16:
            empty_spaces = 16 - len(temp)
            for i in range(empty_spaces - 1):
                temp.append(0)
            temp.append(1)
            crypted_part = encrypt(temp, key)
            crypted_data.extend(crypted_part)

    write_file_bytes(write_file_name, bytes(crypted_data))
    return str(crypted_data)


def decrypt_logic(read_file_name: str, write_file_name: str, key: str) -> str:
    data = read_file_bytes(read_file_name)

    decrypted_data = []
    temp = []
    for byte in data:
        temp.append(byte)
        if len(temp) == 16:
            decrypted_part = decrypt(temp, key)
            decrypted_data.extend(decrypted_part)
            del temp[:]
    else:
        if 0 < len(temp) < 16:
            empty_spaces = 16 - len(temp)
            for i in range(empty_spaces - 1):
                temp.append(0)
            temp.append(1)
            decrypted_part = encrypt(temp, key)
            decrypted_data.extend(decrypted_part)

    write_file_bytes(write_file_name, bytes(decrypted_data))
    return read_file_strings(write_file_name)


from logic import encrypt, decrypt


def read_file(file_name: str) -> bytes:
    with open(file_name, 'rb') as ff:
        return ff.read()

def write_file(file_name: str, data: bytes):
    with open(file_name, 'wb') as ff:
        ff.write(data)

def main():


    command_input = input("Что вы хотите сделать?\n1. Зашифровать текст\n2. Расшифровать текст\n->")
    if command_input == "1":
        file_name = input("Введите путь к файлу для шифрования: ")
        data = read_file(file_name)
        key = input("Введите ключ: ")

        crypted_data = []
        temp = []
        for byte in data:
            temp.append(byte)
            if len(temp) == 16:
                crypted_part = encrypt(temp, key)
                crypted_data.extend(crypted_part)
                del temp[:]
        else:
            # padding v1
            # crypted_data.extend(temp)

            # padding v2
            if 0 < len(temp) < 16:
                empty_spaces = 16 - len(temp)
                for i in range(empty_spaces - 1):
                    temp.append(0)
                temp.append(1)
                crypted_part = encrypt(temp, key)
                crypted_data.extend(crypted_part)


        write_file(file_name, bytes(crypted_data))


    elif command_input == "2":
        text_input = input("Введите файл для расшифровки: ")

        data = read_file(text_input)

        key = input("Введите ключ: ")

        decrypted_data = []
        temp = []
        for byte in data:
            temp.append(byte)
            if len(temp) == 16:
                decrypted_part = decrypt(temp, key)
                decrypted_data.extend(decrypted_part)
                del temp[:]
        else:
            # padding v1
            # decrypted_data.extend(temp)

            # padding v2
            if 0 < len(temp) < 16:
                empty_spaces = 16 - len(temp)
                for i in range(empty_spaces - 1):
                    temp.append(0)
                temp.append(1)
                decrypted_part = encrypt(temp, key)
                decrypted_data.extend(decrypted_part)

        write_file(text_input, bytes(decrypted_data))




if __name__ == "__main__":
    main()
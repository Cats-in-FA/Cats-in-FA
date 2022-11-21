
from logic import encrypt, decrypt

def main():


    command_input = input("Что вы хотите сделать?\n1. Зашифровать текст\n2. Расшифровать текст\n->")
    if command_input == "1":
        text_input = input("Введите текст для шифрования: ")
        bytes_input = str.encode(text_input)

        key_input = input("Введите ключ: ")

        encrypted_text = encrypt(bytes_input, key_input)
        print("Зашифрованный текст: ", encrypted_text)

    elif command_input == "2":
        text_input = input("Введите текст для расшифрования: ")
        bytes_input = str.encode(text_input)

        key_input = input("Введите ключ: ")

        decrypted_text = decrypt(bytes_input, key_input)
        print("Расшифрованный текст: ", decrypted_text)



if __name__ == "__main__":
    main()
import tkinter as tk

from wrapper import decrypt_logic, encrypt_logic, check_file


def clear():
    for i, field in enumerate(fields):
        if i < len(fields) - 1:
            field.delete(0, tk.END)
        else:
            field.config(text="")


def encrypt_wrapper():
    file_name = fields[0].get()
    key = fields[1].get()
    if check_file(file_name):
        result = encrypt_logic(file_name, file_name, key)
    else:
        pass
    fields[2].config(text=result)


def decrypt_wrapper():
    file_name = fields[0].get()
    key = fields[1].get()
    if check_file(file_name):
        result = decrypt_logic(file_name, file_name, key)
    else:
        pass
    fields[2].config(text=result)


# Создается новое окно с заголовком "Введите домашний адрес".
window = tk.Tk()
window.title("AES")

# Создается новая рамка `frm_form` для ярлыков с текстом и
# Однострочных полей для ввода информации об адресе.
frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
# Помещает рамку на окно приложения.
frm_form.pack()

# Список ярлыков полей.
labels = [
    "Путь:",
    "Ключ:",
    "Результат:",
]
fields = []

# Цикл для списка ярлыков полей.
for i, text in enumerate(labels):
    # Создает ярлык с текстом из списка ярлыков.
    label = tk.Label(master=frm_form, text=text)
    # Создает текстовое поле которая соответствует ярлыку.
    if i < len(labels) - 1:
        entry = tk.Entry(master=frm_form, width=50)
    else:
        entry = tk.Label(master=frm_form, width=42)
    fields.append(entry)
    # Использует менеджер геометрии grid для размещения ярлыков и
    # текстовых полей в строку, чей индекс равен idx.
    label.grid(row=i, column=0, sticky="e")
    entry.grid(row=i, column=1)

# Создает новую рамку `frm_buttons` для размещения в ней
# кнопок "Отправить" и "Очистить". Данная рамка заполняет
# все окно в горизонтальном направлении с
# отступами в 5 пикселей горизонтально и вертикально.
frm_buttons = tk.Frame()
frm_buttons.pack()

# Создает кнопку "Отправить" и размещает ее
# справа от рамки `frm_buttons`.
btn_submit = tk.Button(master=frm_buttons, text="Clear", command=clear)
btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)

# Создает кнопку "Очистить" и размещает ее
# справа от рамки `frm_buttons`.
btn_clear = tk.Button(master=frm_buttons, text="Decrypt", command=decrypt_wrapper)
btn_clear.pack(side=tk.RIGHT)

# Создает кнопку "Очистить" и размещает ее
# справа от рамки `frm_buttons`.
btn_clear = tk.Button(master=frm_buttons, text="Encrypt", command=encrypt_wrapper)
btn_clear.pack(side=tk.RIGHT, padx=10, ipadx=10)

# Запуск приложения.
window.mainloop()

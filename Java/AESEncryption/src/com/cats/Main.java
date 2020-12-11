package com.cats;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Scanner;


class LocaleFileWriter {

    String fileName;
    byte[] data;

    public LocaleFileWriter(String fileName, byte[] data) {
        this.fileName = fileName;
        this.data = data;
        this.write();
    }

    void write() {
        try (FileOutputStream stream = new FileOutputStream(fileName)) {
            stream.write(this.data);
        } catch (IOException e) {
            e.printStackTrace();
        }

    }
}

class LocaleFileReader {
    String filename;

    public LocaleFileReader(String filename) {
        this.filename = filename;
    }

    public byte[] read() throws IOException {
        Path fileLocation = Paths.get(this.filename);
        return Files.readAllBytes(fileLocation);
    }
}

public class Main {

    public static void main(String[] args) throws IOException {

        System.out.println("Что вы хотите сделать?\n1. Зашифровать файл\n2. Расшифровать файл\n->");
        Scanner scanner = new Scanner(System.in);
        String commandInput = scanner.next();
        System.out.println(commandInput);

        //Шифрование файла
        if (commandInput.equals("1")) {
            System.out.println("Введите путь к файлу для его шифрования");

            String file2EncryptString = scanner.next();
            if (!IsFileExists(file2EncryptString)) {
                System.out.println("Введенного файла не существует");
                return;
            }
            LocaleFileReader inputFile = new LocaleFileReader(file2EncryptString);

            //Генерируем ключ шифрования
            byte[] keyBytes = KeyGenerator();
            AESClass obj = new AESClass(keyBytes);
            byte[] encrypt = obj.Encrypt(inputFile.read());

            //Запись ключа
            //TODO сохранять ключ в одну директорию с файлом + имя = файл_key.cat
            new LocaleFileWriter("./files/key.cat", keyBytes);
            //Запись зашифрованного файла на место предыдущего
            new LocaleFileWriter(file2EncryptString, encrypt);

            System.out.println("Успешно зашифровали файл " + file2EncryptString);
        }

        //Расшифровка файла
        else if (commandInput.equals("2")) {

            System.out.println("Введите путь к файлу для его расшифровки");
            String file2DecryptString = scanner.next();
            if (!IsFileExists(file2DecryptString)) {
                System.out.println("Введенного файла не существует");
                return;
            }
            System.out.println("Введите путь к файлу-ключу для расшифровки");
            String DecryptKeyString = scanner.next();
            if (!IsFileExists(DecryptKeyString)) {
                System.out.println("Введенного файла не существует");
                return;
            }

            LocaleFileReader inputKeyObj = new LocaleFileReader(DecryptKeyString);
            LocaleFileReader inputFileObj = new LocaleFileReader(file2DecryptString);

            AESClass obj = new AESClass(inputKeyObj.read());
            byte[] decrypt = obj.Decrypt(inputFileObj.read());

            new LocaleFileWriter(file2DecryptString, decrypt);

            System.out.println("Успешно расшифровали файл");

        }
        else
            System.out.println("Некорректный ввод данных..");
    }

    //Генерирует ключ для шифрования данных
    private static byte[] KeyGenerator() {
        StringBuilder key = new StringBuilder();
        for (int i = 0; i < 2; i++)
            key.append(Long.toHexString(Double.doubleToLongBits(Math.random())));
        return key.toString().getBytes();
    }

    //Проверка на существование файла из строки
    private static boolean IsFileExists(String Path) {
        File tempFile = new File(Path);
        return tempFile.exists();
    }
}

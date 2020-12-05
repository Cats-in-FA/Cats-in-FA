package com.cats;

import java.io.File;
import java.io.IOException;
import java.lang.reflect.Array;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) throws IOException {

        System.out.println("Что вы хотите сделать?\n1. Зашифровать файл\n2. Расшифровать файл\n->");
        Scanner scanner = new Scanner(System.in);
        String commandInput = scanner.next();
        System.out.println(commandInput);

        if (commandInput.equals("1")){
            System.out.println("Введите путь к файлу для его шифрования");

            //TODO проверка на существование файла
            String file2EncryptString = scanner.next();
            File fileToEncryptFile = new File(file2EncryptString);

            byte[] inputFileBytes = Files.readAllBytes(fileToEncryptFile.toPath());
            byte[] keyBytes = KeyGenerator();

            AESClass obj = new AESClass(keyBytes);
            byte[] encrypt = obj.Encrypt(inputFileBytes);

            //TODO запись ключа
            //TODO запись зашифрованного файла

            System.out.println("Успешно зашифровали файл");
        }
        else if (commandInput.equals("2")){
            System.out.println("Сча мы будем расшифровывать файл");
        }
        else
            System.out.println("Некорректный ввод данных..");


        //File fileToEncrypt = new File(this.filepath);


        String InputString = "Я кошка и у меня урчит живот";
        String KeyString = "3fed2c8817f0903a3fe007de83bac6dc";
        byte[] inputText = InputString.getBytes();
        byte[] key = KeyString.getBytes();

        AESClass obj = new AESClass(key);
        byte[] encrypt = obj.Encrypt(inputText);
        String CatResultEncrypt = new String(encrypt, StandardCharsets.UTF_8);
        System.out.println("Шифровка: " + CatResultEncrypt);

        byte[] decrypt = obj.Decrypt(encrypt);
        String CatResultDecrypt = new String(decrypt, StandardCharsets.UTF_8);
        System.out.println("Расшифровка: "+CatResultDecrypt);
    }

    private static byte[] KeyGenerator() {
        StringBuilder key = new StringBuilder();
        for (int i=0; i < 2; i++)
            key.append(Long.toHexString(Double.doubleToLongBits(Math.random())));
        return key.toString().getBytes();
    }
}

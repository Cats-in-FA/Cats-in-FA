package com.cats;

import java.lang.reflect.Array;
import java.nio.charset.StandardCharsets;

public class Main {

    public static void main(String[] args) {
        //TODO Тут сделать файлы

        String InputString = "MEOW";
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
}

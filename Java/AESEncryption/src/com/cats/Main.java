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

        String CatResultEncrypt = new String(obj.ECB_decrypt(obj.ECB_encrypt(inputText)), StandardCharsets.UTF_8);
        System.out.println("Шифровка: " + CatResultEncrypt);

        //String CatResultDecrypt = new String(obj.ECB_decrypt(CatResultEncrypt.getBytes()), StandardCharsets.UTF_8);
        //System.out.println("Расшифровка: "+CatResultDecrypt);

    }
}

package com.cats;

import java.lang.reflect.Array;

public class Main {

    public static void main(String[] args) {
        //TODO Тут сделать файлы
        String InputString = "MEOW";
        byte[] inputText = InputString.getBytes();

        for (int i = 0; i < inputText.length; i++) {
            System.out.println(inputText[i]);
        }

        byte[] iv = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15};
        byte[] key;

        // 128
        System.out.println("128 bit");
        //key = new byte[]{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15};
        //AESClass obj = new AESClass(key);
        //System.out.println("ECB result --> " + new String(obj.ECB_decrypt(obj.ECB_encrypt(inputText))));
        //obj = new AESClass(key, iv);
        //System.out.println("CBC result --> " + new String(obj.CBC_decrypt(obj.CBC_encrypt(inputText))));

    }
}

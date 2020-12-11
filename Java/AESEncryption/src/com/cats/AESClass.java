package com.cats;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.Arrays;

/*
Разработать программу шифровки-дешифровки по алгоритму AES-128.
Данные берутся из файла, зашифрованные данные сохраняются в указанный файл.

Использует режим электронной кодовой книги/Electronic Codebook/ECB
https://habr.com/ru/post/212235/
 */


public class AESClass {

    private final int Nb = 4; //число столбцов (32-х битных слов), составляющих State. Для стандарта регламентировано Nb = 4
    private final int Nr = 10;  //количество раундов шифрования. В зависимости от длины ключа, Nr = 10, 12 или 14
    private final int Nk = 4;  //длина ключа в 32-х битных словах. Для AES, Nk = 4, 6, 8. Мы уже определились, что будем использовать Nk = 4

    // Текущий раунд
    private int actual;

    // Состояние
    private int[][] state;

    //Вектор для преобразования ключа в ключ-матрицу в KeyExpansion
    private int[] RoundKey;
    // Ключ
    private int[] key;

    // Матрица для шифровки
    private final static int[] sBox = new int[]{
            //0     1    2      3     4    5     6     7      8    9     A      B    C     D     E     F
            0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
            0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
            0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
            0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
            0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
            0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
            0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
            0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
            0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
            0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
            0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
            0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
            0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
            0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
            0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
            0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16};

    //Матрица для дешифровки
    private final static int[] rsBox = new int[]{
            0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
            0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
            0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
            0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
            0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
            0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
            0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
            0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
            0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
            0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
            0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
            0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
            0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
            0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
            0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
            0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d};

    //Необходим для KeySchedule и заполнения её матрицы
    private final static int[] rCon = new int[]{
            0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
            0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39,
            0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a,
            0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8,
            0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef,
            0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc,
            0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b,
            0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
            0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94,
            0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20,
            0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35,
            0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f,
            0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04,
            0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63,
            0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd,
            0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d};

    //Это конструктор
    public AESClass(byte[] key) {

        //Ключ
        this.key = new int[key.length];

        //Выставление данных для ключа
        for (int i = 0; i < key.length; i++)
            this.key[i] = key[i];

        //Создание массива хранения для состояний
        //3-х мерный т.к. нам требуется хранить несколько состояний (2 номера состояния)
        state = new int[4][Nb];

        //Делает из ключа-строки ключ-матрицу
        KeyExpansion();
    }

    //Метод для преобразования ключа-строки в ключ-матрицу
    private int[] KeyExpansion() {

        int temp, i = 0;
        // Матрица на основе ключа
        RoundKey = new int[Nb * (Nr + 1)];

        while (i < Nk) {
            RoundKey[i] = 0x00000000;
            RoundKey[i] |= key[4 * i] << 24;
            RoundKey[i] |= key[4 * i + 1] << 16;
            RoundKey[i] |= key[4 * i + 2] << 8;
            RoundKey[i] |= key[4 * i + 3];
            i++;
        }
        i = Nk;
        while (i < Nb * (Nr + 1)) {
            temp = RoundKey[i - 1];
            if (i % Nk == 0) {
                // XOR с константами из rCon.
                temp = subWord(rotWord(temp)) ^ (rCon[i / Nk] << 24);
            }
            else if (Nk > 6 && (i % Nk == 4)) {
                temp = subWord(temp);
            }
            else {
            }
            RoundKey[i] = RoundKey[i - Nk] ^ temp;
            i++;
        }
        return RoundKey;
    }

    private static int rotWord(int word) {
        return (word << 8) | ((word & 0xFF000000) >>> 24);
    }


    //НАЧАЛО
    public byte[] Encrypt(byte[] text) {
        return Processing (text, true);
    }

    public byte[] Decrypt(byte[] text) {
        return Processing (text, false);
    }


    private byte[] Processing (byte[] text, boolean flag) {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        for (int i = 0; i < text.length; i+=16) {
            try {
                out.write(inputOutputProcessing(Arrays.copyOfRange(text, i, i + 16), flag));
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return out.toByteArray();
    }


    // Обработка входа и выхода, запуск шифрофки/дешифрофки в зависимости от флага
    private byte[] inputOutputProcessing (byte[] text, boolean flag) {

        byte[] out = new byte[text.length];

        // Заполняем массив State входными значениями по формуле
        for (int i = 0; i < Nb; i++) { // колонки
            for (int j = 0; j < 4; j++) { // строки
                state[j][i] = text[i * Nb + j] & 0xff;
            }
        }

        // Запуск основных преобразований
        if (flag) {
            cipher(state);
        }
        else {
            decipher(state);
        }

        // Составляем выходной массив зашифрованных байтов из State по формуле
        for (int i = 0; i < Nb; i++) {
            for (int j = 0; j < 4; j++) {
                out[i * Nb + j] = (byte) (state[j][i] & 0xff);
            }
        }
        return out;
    }


    // Запуск основных преобразований шифровки
    private void cipher(int[][] out) {
        actual = 0;
        AddRoundKey(out, actual);

        for (actual = 1; actual < Nr; actual++) {
            subBytes(out);
            shiftRows(out);
            mixColumns(out);
            AddRoundKey(out, actual);
        }
        subBytes(out);
        shiftRows(out);
        AddRoundKey(out, actual);

    }

    // Запуск основных преобразований дешифровки
    private void decipher(int[][] out) {
        actual = Nr;
        AddRoundKey(out, actual);

        for (actual = Nr - 1; actual > 0; actual--) {
            InvShiftRows(out);
            InvSubBytes(out);
            AddRoundKey(out, actual);
            invMixColumnas(out);
        }
        InvShiftRows(out);
        InvSubBytes(out);
        AddRoundKey(out, actual);

    }

    /* Блок основных преобразований для шифрования
    */

    //Трансформация производит побитовый XOR каждого элемента из State с
    //соответствующим элементом из RoundKey.
    //RoundKey — массив такого же размера, как и State, который строится для каждого
    //раунда на основе секретного ключа функцией KeyExpansion()
    private int[][] AddRoundKey(int[][] s, int round) {
        for (int c = 0; c < Nb; c++) {
            for (int r = 0; r < 4; r++) {
                s[r][c] = s[r][c] ^ ((RoundKey[round * Nb + c] << (r * 8)) >>> 24);
            }
        }
        return s;
    }


    // Замена каждого байта из State на соответствующий ему из константной таблицы Sbox
    private int[][] subBytes(int[][] state) {
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < Nb; j++) {
                state[i][j] = subWord(state[i][j]) & 0xFF;
            }
        }
        return state;
    }

    private static int subWord(int word) {
        int subWord = 0;
        for (int i = 24; i >= 0; i -= 8) {
            int in = word << i >>> 24;
            subWord |= sBox[in] << (24 - i);
        }
        return subWord;
    }

    // Циклический сдвиг влево построчно
    private int[][] shiftRows(int[][] state) {
        int temp1, temp2, temp3, i;

        // Строка 1 - сдвиг влево на 1
        temp1 = state[1][0];
        for (i = 0; i < Nb - 1; i++) {
            state[1][i] = state[1][(i + 1) % Nb];
        }
        state[1][Nb - 1] = temp1;

        // Строка 2 - сдвиг влево на 2
        temp1 = state[2][0];
        temp2 = state[2][1];
        for (i = 0; i < Nb - 2; i++) {
            state[2][i] = state[2][(i + 2) % Nb];
        }
        state[2][Nb - 2] = temp1;
        state[2][Nb - 1] = temp2;

        // Строка 3 - сдвиг влево на 3
        temp1 = state[3][0];
        temp2 = state[3][1];
        temp3 = state[3][2];
        for (i = 0; i < Nb - 3; i++) {
            state[3][i] = state[3][(i + 3) % Nb];
        }
        state[3][Nb - 3] = temp1;
        state[3][Nb - 2] = temp2;
        state[3][Nb - 1] = temp3;

        return state;
    }

    // Каждая колонка в State представляется в виде многочлена и перемножается в поле GF(2^8)
    // по модулю x4 + 1 с фиксированным многочленом 3x3 + x2 + x + 2
    private int[][] mixColumns(int[][] state) {
        int temp0, temp1, temp2, temp3;
        for (int c = 0; c < Nb; c++) {

            temp0 = mult(0x02, state[0][c]) ^ mult(0x03, state[1][c]) ^ state[2][c] ^ state[3][c];
            temp1 = state[0][c] ^ mult(0x02, state[1][c]) ^ mult(0x03, state[2][c]) ^ state[3][c];
            temp2 = state[0][c] ^ state[1][c] ^ mult(0x02, state[2][c]) ^ mult(0x03, state[3][c]);
            temp3 = mult(0x03, state[0][c]) ^ state[1][c] ^ state[2][c] ^ mult(0x02, state[3][c]);

            state[0][c] = temp0;
            state[1][c] = temp1;
            state[2][c] = temp2;
            state[3][c] = temp3;
        }

        return state;
    }


    private static int mult(int a, int b) {
        int sum = 0;
        while (a != 0) { // пока не 0
            if ((a & 1) != 0) { // проверка, является ли 1й бит 1
                sum = sum ^ b; // добавление b из младшего бита
            }
            b = xtime(b); // битовый сдвиг влево по модулю 0x11b при необходимости
            a = a >>> 1; // был использован младший бит "а", поэтому сдвиньте вправо
        }
        return sum;

    }

    private static int xtime(int b) {
        if ((b & 0x80) == 0) {
            return b << 1;
        }
        return (b << 1) ^ 0x11b;
    }


    // Блок основных преобразований для дешифрования (обратный порядок)
    private int[][] invMixColumnas(int[][] state) {
        int temp0, temp1, temp2, temp3;
        for (int c = 0; c < Nb; c++) {
            temp0 = mult(0x0e, state[0][c]) ^ mult(0x0b, state[1][c]) ^ mult(0x0d, state[2][c]) ^ mult(0x09, state[3][c]);
            temp1 = mult(0x09, state[0][c]) ^ mult(0x0e, state[1][c]) ^ mult(0x0b, state[2][c]) ^ mult(0x0d, state[3][c]);
            temp2 = mult(0x0d, state[0][c]) ^ mult(0x09, state[1][c]) ^ mult(0x0e, state[2][c]) ^ mult(0x0b, state[3][c]);
            temp3 = mult(0x0b, state[0][c]) ^ mult(0x0d, state[1][c]) ^ mult(0x09, state[2][c]) ^ mult(0x0e, state[3][c]);

            state[0][c] = temp0;
            state[1][c] = temp1;
            state[2][c] = temp2;
            state[3][c] = temp3;
        }
        return state;
    }

    private int[][] InvShiftRows(int[][] state) {
        int temp1, temp2, temp3, i;

        // row 1;
        temp1 = state[1][Nb - 1];
        for (i = Nb - 1; i > 0; i--) {
            state[1][i] = state[1][(i - 1) % Nb];
        }
        state[1][0] = temp1;
        // row 2
        temp1 = state[2][Nb - 1];
        temp2 = state[2][Nb - 2];

        for (i = Nb - 1; i > 1; i--) {
            state[2][i] = state[2][(i - 2) % Nb];
        }

        state[2][1] = temp1;
        state[2][0] = temp2;
        // row 3
        temp1 = state[3][Nb - 3];
        temp2 = state[3][Nb - 2];
        temp3 = state[3][Nb - 1];
        for (i = Nb - 1; i > 2; i--) {
            state[3][i] = state[3][(i - 3) % Nb];
        }
        state[3][0] = temp1;
        state[3][1] = temp2;
        state[3][2] = temp3;

        return state;
    }

    private int[][] InvSubBytes(int[][] state) {
        for (int i = 0; i < 4; i++)
            for (int j = 0; j < Nb; j++)
                state[i][j] = invSubWord(state[i][j]) & 0xFF;
        return state;
    }

    private static int invSubWord(int word) {
        int subWord = 0;
        for (int i = 24; i >= 0; i -= 8) {
            int in = word << i >>> 24;
            subWord |= rsBox[in] << (24 - i);
        }
        return subWord;
    }


}
package com.cats;

import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

// Класс для работы с файлами
public class FileProcessing {

    String fileName;

    public FileProcessing(String fileName) {
        this.fileName = fileName;
    }

    //Чтение
    public byte[] Read() throws IOException {
        Path fileLocation = Paths.get(this.fileName);
        return Files.readAllBytes(fileLocation);
    }

    //Запись
    public void Write(byte[] data) {
        try (FileOutputStream stream = new FileOutputStream(fileName)) {
            stream.write(data);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
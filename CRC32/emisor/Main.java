package CRC32.emisor;

import CRC32.emisor.vista;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        vista view = new vista();

        String mensaje = view.vista();
        
        crc crc = new crc(mensaje);

        view.MessageBin(crc.getMensaje());
        

        writeToFile(crc.getCrclst());

    
    }

    private static void writeToFile(ArrayList<String> data) {
        String directoryPath = "./CRC32/crc";
        String filePath = directoryPath + "/crc.txt";

        // Crear directorio si no existe
        File directory = new File(directoryPath);
        if (!directory.exists()) {
            if (directory.mkdirs()) {
                System.out.println("Directorio creado: " + directoryPath);
            } else {
                System.err.println("Error al crear el directorio: " + directoryPath);
                return;
            }
        }

        // Escribir en el archivo
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath))) {
            for (String line : data) {
                writer.write(line + "\n");
            }
            System.out.println("Datos escritos en el archivo " + filePath);
        } catch (IOException e) {
            System.err.println("Error al escribir en el archivo: " + e.getMessage());
        }
    }
}

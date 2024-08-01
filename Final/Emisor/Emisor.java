package Emisor;

import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;
import java.util.Random;
import java.util.ArrayList;
import java.io.FileWriter;
import java.io.PrintWriter;

public class Emisor {
    private static final String HOST = "127.0.0.1";
    private static final int PORT = 65432;

    public static void main(String[] args) {
        // Número de pruebas
        int[] numPruebas = {1000, 5000, 10000};

        try {
            for (int pruebas : numPruebas) {
                int exitos = 0;
                for (int i = 0; i < pruebas; i++) {
                    if (enviarDatos()) {
                        exitos++;
                    }
                }
                double tasaExito = (double) exitos / pruebas;
                guardarResultado(pruebas, tasaExito);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static boolean enviarDatos() {
        Random random = new Random();
        String word = generarPalabraAleatoria(10);  // Generar palabra de 10 caracteres
        String encodedData = encodeToHamming(word);
        double errorProbability = 0.01; // Probabilidad de error del 1%

        String noisyData = applyNoise(encodedData, errorProbability);
        return sendData("0 " + noisyData);
    }

    private static String generarPalabraAleatoria(int length) {
        String characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
        Random random = new Random();
        StringBuilder word = new StringBuilder(length);
        for (int i = 0; i < length; i++) {
            word.append(characters.charAt(random.nextInt(characters.length())));
        }
        return word.toString();
    }

    private static boolean sendData(String data) {
        try (Socket socket = new Socket(HOST, PORT);
             OutputStream outputStream = socket.getOutputStream()) {
            outputStream.write(data.getBytes());
            // Aquí debería verificarse la respuesta del receptor para determinar si fue exitoso
            return true;  // Suponer que fue exitoso por simplicidad
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }
    }

    private static void guardarResultado(int pruebas, double tasaExito) throws IOException {
        try (FileWriter fw = new FileWriter("resultados.txt", true);
             PrintWriter pw = new PrintWriter(fw)) {
            pw.println(pruebas + "," + tasaExito);
        }
    }

    private static String encodeToHamming(String word) {
        StringBuilder hammingString = new StringBuilder();
        for (char c : word.toCharArray()) {
            String binaryChar = String.format("%7s", Integer.toBinaryString(c)).replaceAll(" ", "0");
            String hammingChar = encodeHamming(binaryChar);
            hammingString.append(hammingChar).append(",");
        }
        if (hammingString.length() > 0) {
            hammingString.setLength(hammingString.length() - 1);
        }
        return hammingString.toString();
    }

    private static String encodeHamming(String binaryChar) {
        int[] data = new int[7];
        for (int i = 0; i < 7; i++) {
            data[i] = Character.getNumericValue(binaryChar.charAt(i));
        }

        int p1 = data[0] ^ data[1] ^ data[3] ^ data[4] ^ data[6];
        int p2 = data[0] ^ data[2] ^ data[3] ^ data[5] ^ data[6];
        int p4 = data[1] ^ data[2] ^ data[3];
        int p8 = data[4] ^ data[5] ^ data[6];

        return String.format("%d%d%d%d%d%d%d%d%d%d%d", p1, p2, data[0], p4, data[1], data[2], data[3], p8, data[4], data[5], data[6]);
    }

    private static String applyNoise(String data, double errorProbability) {
        Random random = new Random();
        StringBuilder noisyData = new StringBuilder();

        for (char bit : data.toCharArray()) {
            if (bit == ',' || bit == ' ') {
                noisyData.append(bit);
            } else {
                if (random.nextDouble() < errorProbability) {
                    noisyData.append(bit == '0' ? '1' : '0');
                } else {
                    noisyData.append(bit);
                }
            }
        }

        return noisyData.toString();
    }
}

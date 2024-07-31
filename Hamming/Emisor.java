import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;
import java.util.Scanner;
import java.util.Random;

public class Emisor {
    private static final String HOST = "127.0.0.1";
    private static final int PORT = 65432;

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Ingrese una palabra: ");
        String word = scanner.nextLine();

        String encodedData = encodeToHamming(word);
        double errorProbability = 0.01; // Probabilidad de error del 1%

        String noisyData = applyNoise(encodedData, errorProbability);
        System.out.println("Datos con ruido: " + noisyData);

        sendData(noisyData);
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

    private static void sendData(String data) {
        try (Socket socket = new Socket(HOST, PORT);
             OutputStream outputStream = socket.getOutputStream()) {
            outputStream.write(data.getBytes());
            System.out.println("Datos enviados");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

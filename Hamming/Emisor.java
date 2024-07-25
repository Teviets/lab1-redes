import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Emisor {

    public static int[] encodeHamming117(int[] data) {
        if (data.length != 7) {
            throw new IllegalArgumentException("La entrada debe ser de 7 bits");
        }

        int[] code = new int[11];

        code[2] = data[0];
        code[4] = data[1];
        code[5] = data[2];
        code[6] = data[3];
        code[8] = data[4];
        code[9] = data[5];
        code[10] = data[6];

        code[0] = code[2] ^ code[4] ^ code[6] ^ code[8] ^ code[10];  // Paridad 1
        code[1] = code[2] ^ code[5] ^ code[6] ^ code[9] ^ code[10];  // Paridad 2
        code[3] = code[4] ^ code[5] ^ code[6];  // Paridad 4
        code[7] = code[8] ^ code[9] ^ code[10];  // Paridad 8

        return code;
    }

    public static List<String> encodeMessage(String message) {
        List<String> encoded = new ArrayList<>();
        for (char c : message.toCharArray()) {
            String binary = String.format("%7s", Integer.toBinaryString(c)).replace(' ', '0');
            int[] data = new int[7];
            for (int i = 0; i < 7; i++) {
                data[i] = Character.getNumericValue(binary.charAt(i));
            }
            int[] hamming = encodeHamming117(data);
            StringBuilder sb = new StringBuilder();
            for (int bit : hamming) {
                sb.append(bit);
            }
            encoded.add(sb.toString());
        }
        return encoded;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Introduce un mensaje a codificar: ");
        String message = scanner.nextLine();
        List<String> encodedMessage = encodeMessage(message);

        System.out.println("Mensaje original: " + message);
        System.out.println("Mensaje codificado en Hamming:");
        System.out.println(String.join(",", encodedMessage));

        scanner.close();
    }
}
package emisor;

import java.util.ArrayList;

public class crc {

    private static final int POLYNOMIAL = 0x04C11DB7;
    private static final int CRC32_MASK = 0xFFFFFFFF;
    private static final int[] CRC32_TABLE = new int[256];
    
    private String data = "";
    private ArrayList<String> mensaje = new ArrayList<>();
    private ArrayList<String> crc = new ArrayList<>();

    static {
        // Inicializar la tabla CRC-32
        for (int i = 0; i < 256; i++) {
            int crc = i;
            for (int j = 8; j > 0; j--) {
                if ((crc & 1) != 0) {
                    crc = (crc >>> 1) ^ POLYNOMIAL;
                } else {
                    crc = crc >>> 1;
                }
            }
            CRC32_TABLE[i] = crc;
        }
    }

    public crc(String data) {
        this.data = data;

        // Convertir cada carácter a su representación binaria de 8 bits
        for (int i = 0; i < data.length(); i++) {
            mensaje.add(String.format("%8s", Integer.toBinaryString(data.charAt(i))).replace(' ', '0'));
        }

        // Calcular CRC-32 para cada mensaje binario
        for (String m : mensaje) {
            String crcValue = calculateCRC32(m);
            crc.add(crcValue);
        }
    }

    private String calculateCRC32(String binaryString) {
        int crc = CRC32_MASK;
        int length = binaryString.length();
        
        for (int i = 0; i < length; i++) {
            int bit = binaryString.charAt(i) - '0'; // Convertir char a int (0 o 1)
            int tableIndex = ((crc >>> 24) ^ bit) & 0xFF;
            crc = (crc << 8) ^ CRC32_TABLE[tableIndex];
        }

        // XOR final con CRC_MASK
        crc ^= CRC32_MASK;

        // Convertir CRC a cadena binaria
        return String.format("%32s", Integer.toBinaryString(crc)).replace(' ', '0');
    }

    public ArrayList<String> getCRC() {
        return crc;
    }

    public ArrayList<String> getMensaje() {
        return mensaje;
    }

}

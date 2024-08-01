package CRC32.emisor;

import java.util.ArrayList;

public class crc {

    private static final int POLYNOMIAL = 0xEDB88320;
    private static final int CRC32_MASK = 0xFFFFFFFF;
    private static final int[] CRC32_TABLE = new int[256];


    private String data;
    private ArrayList<String> mensaje = new ArrayList<>();
    private ArrayList<String> crclst = new ArrayList<>();  // Inicializa crclst
    private String crc;


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


        // Convertir cada carácter a su representación binaria de 8 bits y añadir a mensaje
        for (int i = 0; i < data.length(); i++) {
            mensaje.add(String.format("%8s", Integer.toBinaryString(data.charAt(i) & 0xFF)).replace(' ', '0'));
        }

        // Calcular CRC-32 para cada cadena en mensaje y añadir a crclst
        for (int i = 0; i < mensaje.size(); i++) {
            System.out.println(mensaje.get(i));
            crclst.add(calculateCRC32(mensaje.get(i)));
        }

        // Calcular CRC-32 para la cadena completa
        this.crc = calculateCRC32(data);

    }

    private String calculateCRC32(String data) {
        int crc = CRC32_MASK;

        // Calcular CRC-32 para cada byte del mensaje
        for (int i = 0; i < data.length(); i++) {
            int byteValue = data.charAt(i) & 0xFF;
            int tableIndex = (crc ^ byteValue) & 0xFF;
            crc = (crc >>> 8) ^ CRC32_TABLE[tableIndex];
        }

        // XOR final con CRC_MASK
        crc ^= CRC32_MASK;

        // Convertir CRC a cadena binaria de 32 bits
        return String.format("%32s", Integer.toBinaryString(crc)).replace(' ', '0');
    }


    public ArrayList<String> getMensaje() {
        return mensaje;
    }

    public ArrayList<String> getCrclst() {
        return crclst;
    }

    public String getCRC() {
        return crc;
    }

    public ArrayList<String> getFinalCRC(){
        
        ArrayList<String> fnl = new ArrayList<>();

        for (int i = 0; i<mensaje.size(); i++){
            fnl.add(mensaje.get(i)+crclst.get(i));
        }
        return fnl;
    }

}

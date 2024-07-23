package emisor;

import emisor.vista;
import emisor.crc;

public class Main {
    public static void main(String[] args) {
        vista view = new vista();

        String mensaje = view.vista();
        
        crc crc = new crc(mensaje);

        view.MessageBin(crc.getMensaje());

        view.MessageCRC(crc.getCRC());
    }
}
package CRC32.emisor;

import java.util.Scanner;
import java.util.ArrayList;

public class vista {
    
    public static String vista(){
        System.out.println("Por favor ingrese el mensaje a enviar: ");

        Scanner scanner = new Scanner(System.in);
        String mensaje = scanner.nextLine();

        return mensaje;
    }

    public static void MessageBin(ArrayList<String> mensaje){
        System.out.println("Mensaje en binario: ");
        for (int i = 0; i < mensaje.size(); i++) {
            System.out.print(mensaje.get(i) + "\n");

        }
        System.out.println();
    }

    public static void MessageCRC(String mensaje){
        System.out.println("Mensaje con CRC: ");
        System.out.println(mensaje);
        
        System.out.println();
    }
}
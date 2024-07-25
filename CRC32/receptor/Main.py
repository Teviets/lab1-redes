
import os

POLYNOMIAL = 0xEDB88320
CRC32_MASK = 0xFFFFFFFF

# Crear la tabla CRC-32
CRC32_TABLE = [0] * 256
for i in range(256):
    crc = i
    for j in range(8):
        if (crc & 1) != 0:
            crc = (crc >> 1) ^ POLYNOMIAL
        else:
            crc = crc >> 1
    CRC32_TABLE[i] = crc

def calculate_crc32(data):
    crc = CRC32_MASK
    for byte in data:
        table_index = (crc ^ byte) & 0xFF
        crc = (crc >> 8) ^ CRC32_TABLE[table_index]
    crc ^= CRC32_MASK
    return format(crc, '032b')

def read_file(file_path):
    # Obtener la ruta absoluta a partir de la ruta relativa
    absolute_path = os.path.abspath(file_path)
    print(f"Intentando abrir el archivo en: {absolute_path}")
    
    try:
        with open(absolute_path, 'r') as file:
            lines = file.readline()
        return lines.split('[')[1].split(']')[0]
    except FileNotFoundError:
        print(f"Error: El archivo '{absolute_path}' no se encontró.")
        raise

def interpret_message_and_crc(file_path):
    lines = read_file(file_path)
    if len(lines) < 2:
        raise ValueError("El archivo debe contener al menos dos líneas: mensaje y CRC.")

    message_binary = lines[0].strip()
    crc_received = lines[1].strip()

    # Convertir el mensaje binario a una cadena de texto
    message = ''.join(chr(int(message_binary[i:i+8], 2)) for i in range(0, len(message_binary), 8))

    # Calcular CRC del mensaje recibido
    crc_calculated = calculate_crc32(message.encode('utf-8'))

    # Comparar CRC calculado con el CRC recibido
    if crc_calculated == crc_received:
        print("El mensaje es válido.")
        print("Mensaje recibido:", message)
    else:
        print("Error en el mensaje. CRC calculado:", crc_calculated)

# Uso
if __name__ == "__main__":
    # Ruta relativa del archivo con el mensaje y CRC
    file_path = "msj/mensaje.txt"
    interpret_message_and_crc(file_path)


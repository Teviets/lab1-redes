# Tabla de polinomios para CRC-32
CRC32_POLY = 0xEDB88320
CRC32_INIT = 0xFFFFFFFF

def crc32(data):
    crc = CRC32_INIT
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ CRC32_POLY
            else:
                crc >>= 1
    return crc ^ 0xFFFFFFFF

def parse_message_with_crc(binary_message):
    # Verificar si la longitud del mensaje es suficiente
    if len(binary_message) < 33:
        raise ValueError("Mensaje demasiado corto para contener CRC-32")

    # Extraer el CRC de los últimos 32 bits
    message_data = binary_message[:-32]
    received_crc = int(binary_message[-32:], 2)

    # Convertir el mensaje a una lista de bytes
    message_bytes = [int(message_data[i:i+8], 2) for i in range(0, len(message_data), 8)]

    # Calcular el CRC del mensaje
    calculated_crc = crc32(message_bytes)

    return message_data

def read_message_from_file(filepath):
    with open(filepath, 'r') as file:
        binary_message = file.readlines()

    for i in range(len(binary_message)):
        binary_message[i] = binary_message[i].strip()
    
    
    return binary_message

def main():
    # Ruta del archivo
    filepath = 'CRC32/crc/crc.txt'

    try:
        # Leer el mensaje desde el archivo
        binary_message = read_message_from_file(filepath)
        for cadena in binary_message:
            # Asegúrate de que el mensaje es una cadena binaria válida
            if not all(bit in '01' for bit in cadena):
                raise ValueError("El mensaje en el archivo no es una cadena binaria válida.")

        # Procesar el mensaje con CRC
        message = []

        for i in range(len(binary_message)):
            message.append(parse_message_with_crc(binary_message[i]))

        finalMessage = ""
        for i in range(len(message)):
            finalMessage += ''.join(chr(int(message[i][j:j+8], 2)) for j in range(0, len(message[i]), 8))
            if message[i] is not None:
                print("Mensaje recibido:", ''.join(chr(int(message[i][j:j+8], 2)) for j in range(0, len(message[i]), 8)))
            else:
                print("El mensaje contiene errores.")

        print("Mensaje final:", finalMessage)
    except FileNotFoundError:
        print("El archivo no se encuentra en la ruta especificada.")
    except ValueError as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
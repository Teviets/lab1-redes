import socket

def calculate_parity(bits, positions):
    return sum(bits[pos-1] for pos in positions) % 2

def correct_and_decode(block):
    parity_positions = {
        1: [1, 3, 5, 7, 9, 11],
        2: [2, 3, 6, 7, 10, 11],
        4: [4, 5, 6, 7],
        8: [8, 9, 10, 11]
    }

    hamming_code = [int(bit) for bit in block]

    syndrome = sum(p for p, positions in parity_positions.items()
                   if calculate_parity(hamming_code, positions) != 0)

    if syndrome != 0:
        hamming_code[syndrome-1] ^= 1 

    data_positions = [3, 5, 6, 7, 9, 10, 11]
    data_bits = [hamming_code[pos-1] for pos in data_positions]

    return data_bits, syndrome

def decode_message(encoded_message):
    blocks = encoded_message.split(',')

    decoded_message_bits = []
    for block in blocks:
        if len(block) == 11:
            data_bits, syndrome = correct_and_decode(block)
            if syndrome != 0:
                print(f"Error encontrado y corregido en el bloque: {block} (Síndrome: {syndrome})")
            else:
                print(f"Bloque sin errores detectados: {block}")
            decoded_message_bits.extend(data_bits)
        else:
            print(f"Bloque inválido: {block}")

    ascii_chars = []
    for i in range(0, len(decoded_message_bits), 7):
        if i + 7 > len(decoded_message_bits):
            break
        char_bits = decoded_message_bits[i:i+7]
        char_value = sum(bit << (6 - j) for j, bit in enumerate(char_bits))
        ascii_chars.append(chr(char_value))

    return ''.join(ascii_chars)

def verify_message(message, crc):
    calculated_crc = calculate_crc32(binary_to_text(message))
    return calculated_crc == int(crc, 2)

def binary_to_text(binary):
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))

# Inicializar la tabla CRC-32
CRC32_TABLE = []
POLYNOMIAL = 0xEDB88320
for i in range(256):
    crc = i
    for _ in range(8):
        if crc & 1:
            crc = (crc >> 1) ^ POLYNOMIAL
        else:
            crc >>= 1
    CRC32_TABLE.append(crc)

def calculate_crc32(data):
    crc = 0xFFFFFFFF
    for char in data:
        byte_value = ord(char) & 0xFF
        table_index = (crc ^ byte_value) & 0xFF
        crc = (crc >> 8) ^ CRC32_TABLE[table_index]
    return crc ^ 0xFFFFFFFF

import socket

def verificar_datos(data):
    tipo, datos = data.split(' ', 1)
    if tipo == '0':
        return verificar_hamming(datos)
    elif tipo == '1':
        return verificar_crc(datos)
    return False

def verificar_hamming(data):
    palabras = data.split(',')
    for palabra in palabras:
        if not verificar_hamming_palabra(palabra):
            return False
    return True

def verificar_hamming_palabra(palabra):
    bits = [int(bit) for bit in palabra]
    p1 = bits[0] ^ bits[2] ^ bits[4] ^ bits[6] ^ bits[8] ^ bits[10]
    p2 = bits[1] ^ bits[2] ^ bits[5] ^ bits[6] ^ bits[9] ^ bits[10]
    p4 = bits[3] ^ bits[4] ^ bits[5] ^ bits[6]
    p8 = bits[7] ^ bits[8] ^ bits[9] ^ bits[10]
    sindrome = p1 * 1 + p2 * 2 + p4 * 4 + p8 * 8
    return sindrome == 0

def verificar_crc(data):
    mensaje, crc_recibido = data.split(' ')
    crc_calculado = calculate_crc32(mensaje)
    return crc_recibido == crc_calculado

def main():
    HOST = '127.0.0.1'
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                data = conn.recv(1024)
                if not data:
                    continue
                print("Received data:", data.decode())
                if verificar_datos(data.decode()):
                    print("Datos correctos")
                else:
                    print("Datos incorrectos")

if __name__ == "__main__":
    main()


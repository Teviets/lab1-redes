import re

def calculate_parity(bits, positions):
    return sum(bits[pos-1] for pos in positions) % 2

def correct_and_decode(block):
    parity_positions = {
        1: [1, 3, 5, 7, 9, 11],
        2: [2, 3, 6, 7, 10, 11],
        3: [4, 5, 6, 7],
        4: [8, 9, 10, 11]
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
        data_bits, syndrome = correct_and_decode(block)
        if syndrome != 0:
            print(f"Error encontrado y corregido en el bloque: {block} (Síndrome: {syndrome})")
        else:
            print(f"Bloque sin errores detectados: {block}")
        decoded_message_bits.extend(data_bits)

    ascii_chars = []
    for i in range(0, len(decoded_message_bits), 7):
        if i + 7 > len(decoded_message_bits):
            break
        char_bits = decoded_message_bits[i:i+7]
        char_value = sum(bit << (6 - j) for j, bit in enumerate(char_bits))
        ascii_chars.append(chr(char_value))

    return ''.join(ascii_chars)

def main():
    print("Introduce la cadena de caracteres codificados en Hamming (11,7) separados por comas:")
    input_string = input().strip()

    decoded_message = decode_message(input_string)
    print(f"Mensaje decodificado: {decoded_message}")

if __name__ == "__main__":
    main()
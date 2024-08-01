def read_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

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

def verify_message(message, crc):
    calculated_crc = calculate_crc32(binary_to_text(message))
    return calculated_crc == int(crc, 2)

def main():
    filename = "./CRC32/crc/crc.txt"
    lines = read_file(filename)
    
    for line in lines:
        message, crc = line.split()
        text = binary_to_text(message)
        is_valid = verify_message(message, crc)
        
        print(f"Mensaje recibido: {text}")
        print(f"Mensaje en binario: {message}")
        print(f"CRC32 recibido: {crc}")
        print(f"CRC32 calculado: {calculate_crc32(text):032b}")
        print(f"¿El mensaje es válido?: {'Sí' if is_valid else 'No'}")
        print("-" * 50)

if __name__ == "__main__":
    main()
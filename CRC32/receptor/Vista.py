class CRC32:
    def __init__(self):
        self.crc32 = 0xFFFFFFFF
        self.table = self.generate_crc32_table()
        self.binary_message = ""

    @staticmethod
    def generate_crc32_table():
        # Genera la tabla CRC-32
        polynomial = 0xEDB88320
        table = []
        for i in range(256):
            crc = i
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ polynomial
                else:
                    crc >>= 1
            table.append(crc)
        return table

    def update(self, binary_data):
        # Asegurarse de que los datos sean una cadena binaria
        if isinstance(binary_data, str) and all(c in '01' for c in binary_data):
            self.binary_message = binary_data
            # Convertir la cadena binaria a bytes
            data = int(binary_data, 2).to_bytes((len(binary_data) + 7) // 8, byteorder='big')
        else:
            raise ValueError("Input must be a binary string containing only '0' and '1'")

        for byte in data:
            self.crc32 = (self.crc32 >> 8) ^ self.table[(self.crc32 & 0xFF) ^ byte]

    def digest(self):
        return self.crc32 ^ 0xFFFFFFFF

    def hexdigest(self):
        return '%08x' % self.digest()

    def get_message(self):
        # Convertir la cadena binaria a caracteres
        chars = [chr(int(self.binary_message[i:i+8], 2)) for i in range(0, len(self.binary_message), 8)]
        return ''.join(chars)

# Ejemplo de uso
if __name__ == "__main__":
    crc32 = CRC32()
    binary_message = '11101000101101111011111001000011'  # Ejemplo de binario recibido

    crc32.update(binary_message)
    print("Mensaje en caracteres:", crc32.get_message())
    print("CRC-32:", crc32.hexdigest())

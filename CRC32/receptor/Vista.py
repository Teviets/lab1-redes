class CRC32:
    def __init__(self):
        self.crc32 = 0xFFFFFFFF
        self.table = self.generate_crc32_table()

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
        if isinstance(binary_data, str):
            data = int(binary_data, 2).to_bytes((len(binary_data) + 7) // 8, byteorder='big')
        else:
            raise ValueError("Input must be a binary string")

        for byte in data:
            self.crc32 = (self.crc32 >> 8) ^ self.table[(self.crc32 & 0xFF) ^ byte]

    def digest(self):
        return self.crc32 ^ 0xFFFFFFFF

    def hexdigest(self):
        return '%08x' % self.digest()

# Ejemplo de uso
if __name__ == "__main__":
    crc32 = CRC32()
    binary_message = '01001000011011110110110001100001001000000110111101101110011001000110110000100001'  # 'Hola, mundo!' en binario

    crc32.update(binary_message)
    print("CRC-32:", crc32.hexdigest())

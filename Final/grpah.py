import matplotlib.pyplot as plt

# Leer los resultados del archivo
pruebas = []
tasa_exito = []

with open('resultados.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        num_pruebas, tasa = line.strip().split(',')
        pruebas.append(int(num_pruebas))
        tasa_exito.append(float(tasa))

# Calcular tasas de error
tasa_error = [1 - tasa for tasa in tasa_exito]

# Crear el gráfico
plt.figure(figsize=(10, 6))
plt.plot(pruebas, tasa_exito, label='Tasa de Éxito', marker='o')
plt.plot(pruebas, tasa_error, label='Tasa de Error', marker='x')

# Añadir títulos y etiquetas
plt.title('Tasas de Éxito y Error para Diferentes Cantidades de Pruebas')
plt.xlabel('Número de Pruebas')
plt.ylabel('Tasa')
plt.legend()
plt.grid(True)

# Mostrar el gráfico
plt.show()

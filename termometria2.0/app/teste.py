from database import MysqlConnector

import matplotlib.pyplot as plt
import numpy as np

import json

db = MysqlConnector()

dados = db.get_query("SELECT * FROM registro_instalacao WHERE codigo = 703;")
#AQUI CONTEM TODOS OS DADOS QUE VEM DO BANCO DE DADOS EM FORMATO DICIONARIO
dados_temp = {chave:valor for chave , valor in dados[0].items()}
#print(f'DADOS_TEMPERATURAS: {dados_temp}')
print()

#AQUI EU FILTRO SO O CAMPO QUE CONTEM AS TEMPERATURAS COM SUAS CHAVES E VALORES, EM FORMATO DICT
temperaturas = json.loads(dados_temp['temperaturas'])
print(f'TEMPERATURAS: {temperaturas.__class__}')
#print()

#AQUI EU OBTENHO SÓ AS CHAVES DO DOCINARIO 'TEMPERATURAS'
lista_sensores = [chave for chave , valor in temperaturas.items()]
print(f'VALORES_SENSORES: {lista_sensores}')
#print()

#AQUI EU OBTENHO SÓ OS VALORES DO DICIONARIO 'TEMPERATURAS'
lista_temperaturas = [int(float(valor)) for chave , valor in temperaturas.items()]
print(f'VALORES_TEMPERATUAS: {lista_temperaturas}')


#AQUI EU FILTRO AS TEMPERATURAS VALIDAS, CASO VENHA TEMPERATURAS ERRADAS EXEM:399 OU MENOR DOQUE 0
lista_temperaturas_validas = [temp for temp in lista_temperaturas if temp > 0 and temp != 399]
#print(f'temperaturas_validas: {lista_temperaturas_validas}')


#---------------------------------------------------------------------------------------------------------------------------------------#
variance= np.var(lista_temperaturas_validas)
print(f'VARIANCE: {variance}')

desvio_padrao_amostral = f'{np.std(lista_temperaturas_validas, ddof=1):.0f}'
print(f'DESVIO PADRÃO: {desvio_padrao_amostral}')

mean_value = np.mean(lista_temperaturas_validas)
median_value = np.median(lista_temperaturas_validas)
std_dev = np.std(lista_temperaturas_validas)
print(f'Media: {mean_value}, Mediana: {median_value}, Desviação Padrão: {std_dev:.0f}')


grouped_channels_temperatures = {}

# Iterar sobre los elementos del diccionario original
for key, value in temperaturas.items():
    # Extraer el número de canal
    channel_number = key[2:4]
    
    # Crear una lista para almacenar las temperaturas si el número de canal no existe en el diccionario agrupado
    if channel_number not in grouped_channels_temperatures:
        grouped_channels_temperatures[channel_number] = []
    
    # Agregar la temperatura a la lista
    grouped_channels_temperatures[channel_number].append(value)

# Imprimir el resultado
for channel, temperatures in grouped_channels_temperatures.items():
    print(f'{channel}: {temperatures}')






























































# # Exemplo de dados de temperatura (substitua isso pelos seus dados reais)
# lista_temperaturas = np.random.rand(len(lista_sensores))
# print(lista_temperaturas)


# # Agrupamento por canal
# canais = set(sensor[2] for sensor in lista_sensores)
# plt.scatter(canais, lista_temperaturas,c='k')

# plt.xlabel('Sensores')
# plt.ylabel('Temperaturas')
# plt.show()

# # Exemplo de dados de temperatura (substitua isso pelos seus dados reais)
# lista_temperaturas = np.random.rand(len(lista_sensores))

# # Ordena os sensores alfanumericamente
# lista_sensores.sort()

# # Cria o gráfico de barras
# plt.scatter(lista_sensores, lista_temperaturas, color='blue', alpha=0.7)
# plt.xlabel('Sensores')
# plt.ylabel('Temperaturas')
# plt.xticks(rotation=45, ha='right')  # Rotação para melhor legibilidade

# plt.tight_layout()  # Ajusta automaticamente o layout para evitar cortes

# # fig, ax = plt.subplots()
# # ax.plot(lista_sensores, lista_temperaturas)
# # plt.show()            


# # plt.plot(lista_sensores, lista_temperaturas)
# plt.xlabel('tempo')
# plt.ylabel('Valor')
# plt.title('Visualización de Datos')
# plt.show()

# plt.bar(lista_sensores, lista_temperaturas)
# plt.xlabel('Sensores')
# plt.ylabel('Temperaturas')
# plt.title('Temperaturas por Sensor')
# plt.show()

# plt.scatter(lista_sensores,lista_sensores)
# plt.ylabel('Temperaturas')
# plt.xlabel('Sensores')
# plt.title('Relación entre Sensores y Temperaturas')
# plt.show()


# plt.pie(lista_temperaturas, labels=lista_sensores, autopct='%1.1f%%')
# plt.title('Distribución de Temperaturas por Sensor')
# plt.show()


# plt.boxplot(lista_temperaturas)
# plt.xticks([1], ['Temperaturas'])
# plt.title('Boxplot de Temperaturas')
# plt.show()
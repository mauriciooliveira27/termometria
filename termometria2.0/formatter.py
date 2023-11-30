import json 

class Formatter:
    #método formata os dados da temperatura
    def dados_temperatura(self, temperaturas):
        self.temperaturas = temperaturas
        temperatura = []

        for item in temperaturas:
            #deixando data.time em formato de strings
            data_string = item['data'].strftime("%Y-%m-%d %H:%M:%S")
            #formato para chave/valor
            dados_temperatura = {
                'Temperaturas': json.loads(item['temperaturas']),
                'Nome_Silo' : item['nome'],
                'Data': data_string,
                'Config_fisica':json.loads(item['config_fisica'])
            }

            dados_json = json.dumps(dados_temperatura)
            dados_json2 = json.loads(dados_json)
            temperatura.append(dados_json2)
        return temperatura
        
    #método formata os dados do cliente
    def dados_cliente(self, dados_cliente):
        for item in dados_cliente:
            dados_cliente = {
                'ID_cliente': item['id_cliente'],
                'ID_planta':item['id_planta'],
                'ID_equipamento':item['id_equipamento'],
                'ID_placa':item['id_placa'],
                'superaquecimento':     100,
                'nivel_percentual_silo': 100,
                'total_armazenado_ton': 1000000,
                'Total_armazenado_sacas': 18.750
            }

            dados_json = json.dumps(dados_cliente)
            dados_json2 = json.loads(dados_json)
            return dados_json2
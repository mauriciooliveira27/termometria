import json 

class Formatter:
    sensores = {}
    print(sensores)
    #método formata os dados da temperatura
    def dados_temperatura(self, temperaturas):
        
        self.temperaturas = temperaturas
        print(self.sensores)
        temperatura = []
        

        for item in temperaturas:
            self.sensores = item['temperaturas']
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
        total_armazenamento = 300.000
        self.sensores = json.loads(self.sensores)
        print(self.sensores.__class__)
        #chaves_desejadas = [chave for chave,valor in self.sensores.items() if chave.startswith("Ch1S")]
        filtrado = {chave: valor for chave,valor in self.sensores.items() if chave.startswith("Ch1S")}
        total_sensores = len(filtrado)
        print(total_sensores)
        #valores_desejados = 
        chaves_desejadas = {chave: valor for chave , valor in filtrado.items() if valor < '29.00'}
        tem_produto = len(chaves_desejadas)

        percentual_saca = (total_armazenamento *  tem_produto) / 100

        tonKG = 1000
        sacaKG = 60
        saca_por_ton  =  (sacaKG * percentual_saca) / 1000
        

        print(f'TOTAL_TON: {saca_por_ton:.0f} TONELADAS')
        print(f'PERCENTUAL_SACA: {percentual_saca:.0f} MIL')
        print(f'total_armazenamento: {total_armazenamento:.0f} MIL')
        for item in dados_cliente:
            dados_cliente = {
                'ID_cliente': item['id_cliente'],
                'ID_planta':item['id_planta'],
                'ID_equipamento':item['id_equipamento'],
                'ID_placa':item['id_placa'],
                'superaquecimento':     100,
                'nivel_percentual_silo': percentual_saca,
                'total_armazenado_ton': saca_por_ton,
                'Total_armazenado_sacas': total_armazenamento
            }

            dados_json = json.dumps(dados_cliente)
            dados_json2 = json.loads(dados_json)
            return dados_json2
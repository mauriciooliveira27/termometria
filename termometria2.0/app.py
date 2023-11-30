from typing import Type
import json
import time
import http.client
from formatter import Formatter
from query import *
from database import MysqlConnector

class SearchData:
    
    def search(self):
        global db
        db = MysqlConnector()
        formatter = Formatter()
        temperatura = db.get_query(get_temperatura())
        cliente = db.get_query(get_cliente())
        result_temperatura = formatter.dados_temperatura(temperatura)
        result_cliente = formatter.dados_cliente(cliente)

        return result_temperatura , result_cliente

class Request:
    def __init__(self,host,endpoint):
        self.host = host
        self.endpoint = endpoint

    def Post(self, dados):
        global conn
        conn = http.client.HTTPSConnection(self.host)
        dados_enviar = json.dumps(dados)
        conn.request('POST', self.endpoint, dados_enviar, headers={'Content-Type':'application/json'})

        return conn.getresponse()

class Response:
    def treat_response(self,response, datas):
        global erros

        if response.status == 202:
            self.datas = datas
            print(response.status, response.reason)
            objeto_resposta = json.loads(response.read().decode('utf-8'))
            data_formatada = [' '.join(item) for item in objeto_resposta]
            datas = [data for data in datas if data in data_formatada]
            datas_atualizar = str(datas)[1:-1]

            if len(datas_atualizar) != 0:
                db.set_query(update(datas_atualizar))
            else:
                time.sleep(30)
                print("possivel falha na gravação da integração no endpoint!")
                db.set_query(failure_record_integration())
                erros += 1
        
        elif response.status == 500:
            time.sleep(30)
            print("Erro 500 encontrado . Obtendo o conteúdo do erro...")
            content = response.read()
            print(content)
            db.set_query(error_status500())
            erros += 1
            
        elif response.status == 404:
            time.sleep(30)
            db.set_query(error_status404())
            print("Erro 404: recurso não encontrado . Verifique se a URL ou a rota está corre.")
            erros += 1

class Main:

    def __init__(self):
        self.search_data = SearchData()
        self.request = Request('api.tisinapse.com.br','/publico/integracao/unidade-armazenamento/leitura-temperaturas')
        self.response = Response()
        self.erros = 0
        

    def process_sending_data(self):
        global dados_temperatura, datas,erros
        dados_temperatura , dados_cliente = self.search_data.search()
        tentativas = 5
        db = MysqlConnector()
        if len(dados_temperatura) != 0:
            dados_enviar = [{'Leituras': dados_temperatura},{'Dados_cliente':dados_cliente}]
            datas = [item['Data'] for item in dados_enviar[0]["Leituras"]]
            print(dados_enviar)
            if dados_temperatura is not None:
                while self.erros < tentativas:
                    try:
                        response = self.request.Post(dados_enviar)
                        self.response.treat_response(response,datas)
                        break 
                    except http.client.HTTPException as e :
                        time.sleep(30)
                        db.set_query(error_http_exception())
                        erros += 1
                    except ConnectionError as e:
                        time.sleep(30)
                        db.set_query(error_connection())
                        erros += 1
                    except TimeoutError as e:
                        time.sleep(30)
                        db.set_query(error_timeout())
                        erros += 1
                    except json.JSONDecodeError as e:
                        time.sleep(30)
                        db.set_query(error_json_decode())
                        erros +=1
                    except Exception as e:
                        time.sleep(30)
                        self.erros += 1
                if self.erros == tentativas:
                    self.erros = 0
                    time.sleep(30)
            elif len(dados_temperatura) == 0:
                print("nenhum registro")
    
    def run(self):
        while True:
    
            self.process_sending_data()
            if self.process_sending_data is None or len(dados_temperatura) != 0:
                return True
            else:
                return False 
    
app = Main()
while True:
    if app.run():
        app.run()
    else:
        print("sem registro aguardando a proxima leitura")
        time.sleep(10)
        app.run()

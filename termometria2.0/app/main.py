from typing import Type
import json
import time
import http.client
from .formatter_json import Formatter
from .query_database import *
from .database import MysqlConnector





class SearchData:

    def search(self):
                    
                    global db
                    db                      =       MysqlConnector()
                    formatter               =       Formatter()
                    temperatura             =       db.get_query(get_temperatura())
                    cliente                 =       db.get_query(get_cliente())
                    result_temperatura      =       formatter.dados_temperatura(temperatura)
                    result_cliente          =       formatter.dados_cliente(cliente)

                    return result_temperatura , result_cliente



class Request:

    def __init__(self,host,endpoint):
                    self.host           =       host
                    self.endpoint       =       endpoint



    def Post(self, dados):
                    global conn
                    conn                =       http.client.HTTPSConnection(self.host)
                    dados_enviar        =       json.dumps(dados)
                    conn.request('POST', self.endpoint, dados_enviar, headers={'Content-Type':'application/json'})
                    return conn.getresponse()




class Response:
   
    def treat_response(self, response, date):
        tentativas = 2
        self.erros_response = 0
        while self.erros_response <= tentativas:
            self.date = date
            self.response = response
            if response.status == 202:
                use_date_if_error = str(date)[1:-1]
                objeto_resposta = json.loads(self.response.read().decode('utf-8'))
                data_formatada = [' '.join(item) for item in objeto_resposta]
                dates = [data for data in self.date if data in data_formatada]
                dates_update = str(dates)[1:-1]

                if len(dates_update) != 0:
                    db.set_query(update(dates_update))
                    break
                else:
                    resp_empty = []
                    self.erros_response

            elif response.status == 500:
                time.sleep(30)
                print("Erro 500 encontrado. Obtendo o conteúdo do erro...")
                content = response.read()
                print(content)
                db.set_query(error_status500())
                print("erro 2")

            elif response.status == 404:
                print("erro 3")
                time.sleep(30)
                db.set_query(error_status404())
                print("Erro 404: recurso não encontrado. Verifique se a URL ou a rota está correta.")
                self.erros_response +=1

            elif self.erros_response == tentativas and len(resp_empty) == 0:
                print()
                db.set_query(update(use_date_if_error))
                break

            elif self.erros_response == tentativas:
                self.erros_response = 0
                break




error_mapping = {
     
                    http.client.HTTPException: error_http_exception(),
                    ConnectionError: error_connection(),
                    TimeoutError: error_timeout(),
                    json.JSONDecodeError: error_json_decode(),
                    # Add more mappings as needed
                }



class Main:

    
    def __init__(self):
                        self.search_data        =    SearchData()
                        self.request            =    Request('api.sinapsesolucoes.com', '/publico/integracao/unidade-armazenamento/leitura-temperaturas')
                        self.response           =    Response()
                        
                        self.dados_temperatura  =    []
                        self.datas              =    []
                        self.erros              =    0
                        #print("selferro = 0")


    def process_sending_data(self): 
        tentativas = 5
        self.erros = 0
        db                                  =       MysqlConnector()
        tentativas                          =       5
        dados_temperatura, dados_cliente    =       self.search_data.search()

        if len(dados_temperatura) != 0:
                dados_enviar                =       [{'Leituras': dados_temperatura}, {'Dados_cliente': dados_cliente}]
                self.datas                  =       [item['Data'] for item in dados_enviar[0]["Leituras"]]
                print(self.datas)
                if dados_temperatura is not None:
                    while self.erros < tentativas:
                        try:
                            response        =           self.request.Post(dados_enviar)
                            result          =           self.response.treat_response(response, self.datas)
  
                            break

                        except ( 
                                http.client.HTTPException, 
                                ConnectionError, TimeoutError, 
                                json.JSONDecodeError
                                ) as e:
                            
                            # time.sleep(30)
                            db.set_query(error_mapping.get(type(e)))
                            self.erros += 1

                        except Exception as e:
                            db.set_query(error_except_exception())
                            #print('erros 4')
                            # time.sleep(30)
                            self.erros += 1
                            # Log the exception or handle it appropriately

                    if self.erros == tentativas:
                        self.erros = 0
                        #print('limite de erros')
                        # time.sleep(30)

        elif len(dados_temperatura) == 0:
            print("nenhum registro")


    def run(self):
        while True:
            print("break")
            self.process_sending_data()
            time.sleep(1)




class App:
    def __init__(self) -> None:
        self.app = Main()

    @classmethod
    def execute(cls):
        cls().app.run()


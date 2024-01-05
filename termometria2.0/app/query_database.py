
def get_temperatura():
    return "SELECT * FROM registro_instalacao WHERE integracao is null order by codigo desc limit 1;"

def get_cliente():
    return "SELECT ConfigInstalacao.id_cliente, ConfigInstalacao.id_planta, ConfigInstalacao.id_equipamento, ConfigInstalacao.id_placa FROM ConfigInstalacao;" 

def update(data):
    return f"UPDATE registro_instalacao SET integracao = NOW() WHERE data IN ({data});"

#erro de solicitação

def error_status404():
    return "INSERT INTO log_erros (TIPO_ERRO, MSG_ERRO,ID_ERRO) VALUES ('falha ao enviar dados termometria.', 'Erro 404: Recurso não encontrado. Verifique se a URL ou a rota está correta.',1);"

def error_http_exception():
     return "INSERT INTO log_erros (TIPO_ERRO, MSG_ERRO,ID_ERRO) VALUES ('falha ao enviar dados termometria.', 'ERRO: Ocorreu um erro de HTTP',2);"

def error_connection():
    return "INSERT INTO log_erros (TIPO_ERRO, MSG_ERRO,ID_ERRO) VALUES ('falha ao enviar dados termometria.', 'ERRO: falha na conexão.',3);"
#erro de timeout

def error_timeout():
    return "INSERT INTO  log_erros (TIPO_ERRO, MSG_ERRO,ID_ERRO) VALUES ('falha ao enviar dados da termometria.', 'ERROR:500 Houve um erro de tempo limite.',4);"
#erro decodificação do Json

def error_json_decode():
    return "INSERT INTO log_erros (TIPO_ERRO, MSG_ERRO, ID_ERRO) VALUES ('falha ao enviar dados da termometria.', 'ERROR: Houve um erro na decodificação do Json no corpo na requisição.',5)"
#erro indefino trata erros de maneira genérica

def error():
     return "INSERT INTO log_erros (TIPO_ERRO, MSG_ERRO,ID_ERRO) VALUES ('falha ao enviar dados termometria.','ERROR: Houve um erro.',6);"

def error_status500():
    return "INSERT INTO log_erros (TIPO_ERRO, MSG_ERRO, ID_ERRO) VALUES ('Falha ao enviar dados termometria.', 'ERROR: Erro 500 encontrado, possivel erro no JSON.', 7);"

def failure_record_integration():
    return "INSERT INTO log_erros (TIPO_ERRO, MSG_ERRO , ID_ERRO) VALUES ('Falha ao enviar dados termometria', 'FALHA: essa menssagem é para quando o endpoint retorna um Json vazio indicando uma possivel falha , proxima tentativa em 1 minuto!', 8)"
def error_except_exception():
    return "INSERT INTO log_erros (TIPO_ERRO, MSG_ERRO , ID_ERRO) VALUES ('Falha ao enviar dados termometria', 'FALHA: essa menssagem é para quando o endpoint retorna um Json vazio indicando uma possivel falha , proxima tentativa em 1 minuto!', 9)"

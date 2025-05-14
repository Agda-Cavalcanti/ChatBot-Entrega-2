import openai, json, logging
from flask import Flask, request, jsonify
from flask_cors import CORS

# Criação de logger personalizado
logger = logging.getLogger("meu_chatbot")
logger.setLevel(logging.DEBUG)  # Aceita tudo de DEBUG até CRITICAL

# Handler para gravar em arquivo
file_handler = logging.FileHandler("Logs.log")
file_handler.setLevel(logging.DEBUG)  

# Formatação dos logs
formatter = logging.Formatter(
    "%(asctime)s::%(levelname)s::%(filename)s::%(lineno)d::%(message)s"
)
file_handler.setFormatter(formatter)

# Adiciona o handler ao logger
logger.addHandler(file_handler)


# Chaves da API e Assistente 
openai.api_key = "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"
ASSISTANT_ID= "asst_TuuMZ9M9gJzzqKhuj1u4DdnV"

# Criando a aplicação no Flask
app = Flask(__name__)
CORS(app)

# ROTAS
#A função view index()é vinculada à rota /usando o app.routedecorador.
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    pergunta = data.get('pergunta')
    logger.info("Pergunta recebida: %s", pergunta)

    try:
        # Cria uma thread
        thread = openai.beta.threads.create()

        # Adiciona a mensagem do usuário
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=pergunta
        )

        # Inicia execução
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        # Aguarda execução terminar
        while True:
            run_status = openai.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == 'completed':
                break

        #Resposta final
        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        resposta_json = messages.data[0].content[0].text.value
        logger.info("Resposta bruta recebida: %s", resposta_json)

        try:
            resposta_formatada = json.loads(resposta_json)  # Se veio JSON serializado
        except:
            resposta_formatada = {"resposta": resposta_json}  # Se veio como texto

        return jsonify(resposta_formatada)

    except Exception as e:
        print("Erro:", str(e))
        return jsonify({"erro": str(e)}), 500





# Executar aplicação
if __name__ == '__main__':
    app.run(debug=True)

Esta plataforma é um Agente de Inteligência Artificial dedicado à análise de dados.
O Agente está diretamente conectado à base de dados e responde às perguntas utilizando exclusivamente as informações nela armazenadas.

As interações são feitas em linguagem natural: o usuário faz a pergunta, o Agente processa uma query SQL no backend e devolve a resposta novamente em linguagem natural.

Notas sobre o código:

* O ficheiro .env contém as informações de conexão com a base de dados (neste caso, foi utilizado o Oracle SQL Developer).
* É necessário também possuir uma chave de API da OpenAI.
* O ficheiro application.py contém o código do frontend e pode ser executado com o comando: streamlit run application.py
* O ficheiro main.py é o executável do backend.
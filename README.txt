This platform is an Artificial Intelligence Agent dedicated to data analysis.
The Agent is directly connected to the database and answers questions using exclusively the information stored within it.

Interactions are conducted in natural language: the user asks a question, the Agent processes an SQL query in the backend, and returns the answer again in natural language.

Notes about the code:

* The .env file contains the database connection information (in this case, Oracle SQL Developer was used).
* You also need to have an OpenAI API key.
* The application.py file contains the frontend code and can be executed with the command: streamlit run application.py
* The main.py file is the backend executable.

-------------------------------------------------------------------------------------------------------------------------------

Esta plataforma é um Agente de Inteligência Artificial dedicado à análise de dados.
O Agente está diretamente conectado à base de dados e responde às perguntas utilizando exclusivamente as informações nela armazenadas.

As interações são feitas em linguagem natural: o usuário faz a pergunta, o Agente processa uma query SQL no backend e devolve a resposta novamente em linguagem natural.

Notas sobre o código:

* O ficheiro .env contém as informações de conexão com a base de dados (neste caso, foi utilizado o Oracle SQL Developer).
* É necessário também possuir uma chave de API da OpenAI.
* O ficheiro application.py contém o código do frontend e pode ser executado com o comando: streamlit run application.py
* O ficheiro main.py é o executável do backend.

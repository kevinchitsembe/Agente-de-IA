#openai_api.py
import os
import openai
import json
import re
import logging
from dotenv import load_dotenv
from database_explorer import DatabaseExplorer

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()
client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

def clean_query(query: str) -> str:
    """
    Remove blocos de código markdown e espaços desnecessários da query SQL.
    """
    query = query.strip()
    query = re.sub(r"^```sql", "", query, flags=re.MULTILINE)  # Remove início do bloco
    query = re.sub(r"```$", "", query, flags=re.MULTILINE)     # Remove final do bloco
    return query.strip()

def generate_sql_query(user_input: str, context_history: list = None):
    """
    Gera uma query SQL baseada na entrada do usuário e contexto anterior usando OpenAI.
    """
    try:
        db_explorer = DatabaseExplorer()
        base_prompt = db_explorer.generate_schema_prompt()

        context_text = ""
        if context_history:
            for i, (q, a) in enumerate(context_history):
                context_text += f"\nPergunta anterior {i+1}: {q}\nResposta anterior {i+1}: {a}"

        full_prompt = f"""
        {base_prompt}
        {context_text}

        Agora, baseado em tudo acima, gere uma query SQL para responder à seguinte pergunta atual:
        {user_input}

        Responda no seguinte formato:
        QUERY: <sua query SQL aqui>
        PARAMS: {{"param1": "value1"}} (ou {{}} se não houver)
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": full_prompt}],
            temperature=0
        )

        content = response.choices[0].message.content

        if "QUERY:" not in content or "PARAMS:" not in content:
            raise ValueError("Resposta da API não está no formato esperado")

        query_part = content.split("QUERY:")[1].split("PARAMS:")[0].strip()
        params_part = content.split("PARAMS:")[1].strip()

        query_part = clean_query(query_part)

        try:
            params = json.loads(params_part)
        except json.JSONDecodeError:
            params = {}

        return query_part, params

    except Exception as e:
        raise Exception(f"Erro ao gerar query SQL: {str(e)}")


def generate_natural_response(user_input: str, query: str, results: list):
    """
    Converte os resultados da query em uma explicação clara e natural em português de Portugal, 
    garantindo que o GPT utilize os dados corretamente.
    """
    try:
        logger.debug(f"Query recebida: {query}")
        logger.debug(f"Número de resultados: {len(results)}")

        if not results:
            return "Infelizmente, não encontrei informações sobre esse assunto na base de dados. Se precisar de algo mais específico, posso ajudar!"

        # Converter os resultados para um formato JSON legível para o modelo
        results_json = json.dumps(results, ensure_ascii=False, indent=2)

        # Criar um prompt mais inteligente
        prompt = f"""
        Tu és um assistente conversacional que responde de forma clara e objetiva às perguntas do utilizador,
        utilizando os dados extraídos da base de dados.

        **Pergunta do utilizador:** {user_input}

        **Query executada:** {query}

        **Resultados obtidos:** 
        {results_json}

        **Instruções para gerar a resposta:**
        - Explica os resultados de forma natural e envolvente.
        - Mantém a resposta objetiva e sem informações inventadas.
        - Se os dados contiverem um número (exemplo: COUNT), responde de forma quantitativa.
        - Se os dados contiverem nomes ou descrições, organiza-os numa frase fluida e estruturada.
        - Não menciona a query SQL na resposta.
        - Escreve sempre em português de Portugal.

        **Exemplo de resposta esperada:**
        - "O departamento de IT tem 8 colaboradores."
        - "Os funcionários do departamento de IT são João Silva, Marta Rocha e Pedro Lima."
        - "Atualmente, 5 colaboradores fazem parte da equipa de suporte técnico."

        Gere a resposta:
        """

        logger.debug("Enviando requisição para a API OpenAI")

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=300
        )

        natural_response = response.choices[0].message.content.strip()
        logger.info("Resposta natural gerada com sucesso")
        logger.debug(f"Resposta gerada: {natural_response}")

        return natural_response

    except Exception as e:
        logger.error(f"Erro ao gerar resposta natural: {str(e)}")
        return "Houve um problema ao gerar a resposta. Por favor, tente novamente."

#routes.py
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from utils import execute_query, convert_to_excel
from openai_api import generate_sql_query, generate_natural_response
import logging
import os
from collections import deque

logger = logging.getLogger(__name__)
router = APIRouter()

user_memory = {}  # chave = IP, valor = deque de (pergunta, resposta)

MAX_MEMORY = 5

@router.post("/query")
async def process_natural_language_query(request: Request, payload: dict):
    try:
        user_input = payload.get("user_input")
        client_ip = request.client.host

        if not user_input:
            return JSONResponse(status_code=400, content={"detail": "Input não fornecido", "success": False})

        # Inicializar memória do utilizador
        if client_ip not in user_memory:
            user_memory[client_ip] = deque(maxlen=MAX_MEMORY)

        # Recuperar histórico recente para este utilizador
        context_history = list(user_memory[client_ip])  # lista de (pergunta, resposta)

        # Gerar SQL Query com base no contexto
        query, params = generate_sql_query(user_input, context_history)
        df = execute_query(query, params=params)

        if df.empty:
            return JSONResponse(content={"natural_response": "Não encontrei resultados para essa busca.", "success": True})

        results_list = df.to_dict(orient="records")
        natural_response = generate_natural_response(user_input, query, results_list)

        # Atualizar a memória
        user_memory[client_ip].append((user_input, natural_response))

        # Excel
        file_path = convert_to_excel(df, query, "query_results")

        return JSONResponse(content={
            "natural_response": natural_response,
            "success": True,
            "file_name": "query_results.xlsx"
        })

    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": f"Erro interno: {str(e)}", "success": False})

@router.get("/download/{file_name}")
async def download_excel(file_name: str):
    """
    Permite que o usuário baixe o arquivo Excel com os resultados da query.
    """
    from tempfile import gettempdir
    file_path = os.path.join(gettempdir(), file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")

    return FileResponse(file_path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=file_name)

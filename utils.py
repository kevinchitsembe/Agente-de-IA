#utils.py
import pandas as pd
import os
import tempfile
from fastapi import HTTPException
from database import get_oracle_engine
import logging
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import pandas as pd

logger = logging.getLogger(__name__)


def execute_query(query: str, params: dict = None) -> pd.DataFrame:
    """Executa a query no Oracle Database com parâmetros opcionais e retorna os resultados como DataFrame."""
    try:
        engine = get_oracle_engine()
        
        logger.info(f"Query original: {query}")
        logger.info(f"Parâmetros originais: {params}")
        
        with engine.connect() as conn:
            df = pd.read_sql_query(query, conn, params=params if params else {})

        return df

    except Exception as e:
        logger.error(f"Erro na execução da query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao executar a query: {str(e)}")

def convert_to_excel(df: pd.DataFrame, query: str, file_name: str) -> str:
    """Converte um DataFrame para um arquivo Excel e salva num diretório temporário."""
    try:
        temp_dir = tempfile.gettempdir()  # Diretório temporário do sistema
        output_file = os.path.join(temp_dir, f"{file_name}.xlsx")

        with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Resultados", index=False)
            pd.DataFrame({"Query Executada": [query]}).to_excel(writer, sheet_name="Query", index=False)
        
        logger.info(f"Arquivo Excel gerado: {output_file}")
        return output_file  # Retorna o caminho completo do arquivo

    except Exception as e:
        logger.error(f"Erro na conversão para Excel: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao converter para Excel: {str(e)}")

#database_explorer.py
from typing import Dict, List, Tuple
import logging
from sqlalchemy import inspect, MetaData, create_engine
from database import get_oracle_engine

logger = logging.getLogger(__name__)

class DatabaseExplorer:
    def __init__(self):
        self.engine = get_oracle_engine()
        self.schema_cache = None
        
    def get_schema_info(self) -> Dict:
        """
        Explora a base de dados e retorna informações sobre todas as tabelas,
        colunas, chaves primárias e relacionamentos.
        """
        if self.schema_cache:
            return self.schema_cache
            
        try:
            inspector = inspect(self.engine)
            metadata = MetaData()
            metadata.reflect(bind=self.engine)
            
            schema_info = {}
            
            # Coletar informações de cada tabela
            for table_name in inspector.get_table_names():
                table_info = {
                    'columns': {},
                    'primary_keys': inspector.get_pk_constraint(table_name)['constrained_columns'],
                    'foreign_keys': [],
                    'relationships': []
                }
                
                # Informações das colunas
                for column in inspector.get_columns(table_name):
                    table_info['columns'][column['name']] = {
                        'type': str(column['type']),
                        'nullable': column.get('nullable', True),
                    }
                
                # Chaves estrangeiras e relacionamentos
                for fk in inspector.get_foreign_keys(table_name):
                    table_info['foreign_keys'].append({
                        'constrained_columns': fk['constrained_columns'],
                        'referred_table': fk['referred_table'],
                        'referred_columns': fk['referred_columns']
                    })
                    
                schema_info[table_name] = table_info
            
            self.schema_cache = schema_info
            return schema_info
            
        except Exception as e:
            logger.error(f"Erro ao explorar schema da base de dados: {str(e)}")
            raise

    def generate_schema_prompt(self) -> str:
        """
        Gera um prompt dinâmico baseado na estrutura atual da base de dados.
        """
        schema_info = self.get_schema_info()
        
        prompt = """
        Você é um assistente especializado em banco de dados Oracle.
        Analise a estrutura da base de dados abaixo e gere uma query SQL apropriada para a pergunta do usuário.
        
        Estrutura da Base de Dados:
        """
        
        # Adiciona informações de cada tabela ao prompt
        for table_name, info in schema_info.items():
            prompt += f"\nTabela: {table_name}\n"
            prompt += "Colunas:\n"
            
            # Adiciona colunas e seus tipos
            for col_name, col_info in info['columns'].items():
                pk_marker = "PK" if col_name in info['primary_keys'] else ""
                prompt += f"- {col_name} ({col_info['type']}) {pk_marker}\n"
            
            # Adiciona relacionamentos
            if info['foreign_keys']:
                prompt += "Relacionamentos:\n"
                for fk in info['foreign_keys']:
                    cols = ', '.join(fk['constrained_columns'])
                    ref_cols = ', '.join(fk['referred_columns'])
                    prompt += f"- {cols} -> {fk['referred_table']}({ref_cols})\n"
        
        prompt += """
        Instruções:
        1. Use JOINs apropriados quando precisar relacionar tabelas
        2. Use aliases para as tabelas quando usar JOINs
        3. Adicione ordenação apropriada ao contexto
        4. Otimize a query para melhor performance
        
        Retorne EXATAMENTE neste formato:
        QUERY: [sua query SQL com WHERE e condições apropriadas]
        PARAMS: [dicionário vazio {} se não usar parâmetros]
        """
        
        return prompt

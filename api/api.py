from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from DataFrameInput import DataFrameInput
from ListingResponse import ListingResponse
from typing import List
import pandas as pd

app_description = """
Esta API interage com a base de dados do projeto "Pra Onde Ir?" permitindo a inclusão e o retorno de dados.
"""

app = FastAPI(
    title="Pra Onde Ir?",
    description=app_description,
)

# Carregar dados da planilha CSV
data = pd.read_csv("../data/airbnb_data.csv", dtype={"Listing ID": "string"})


# Endpoint GET para consultar os dados
@app.get(
    "/get_listings/",
    tags=["hospedagens"],
    response_model=List[ListingResponse],
    responses={
        204: {
            "description": "Empty Response",
            "content": {
                "application/json": {"example": "Nenhum dado encontrado para a região 'XYZ'"}
            },
        },
        422: {},
        500: {
            "description": "Server Error",
            "content": {
                "application/json": {"example": "Erro ao ler os dados: Exception ..."}
            },
        }
    },
)
def obter_hospedagens(
    region: str = Query(None, description="Nome da região para filtrar os dados")
):
    """
    Endpoint para obter as hospedagens da base dados, com possibilidades de filtro.

    Uso:
    ```python
    response = requests.get(url)
    data = pd.DataFrame(response.json())
    ```
    """
    try:
        data_clean = data.where(pd.notnull(data), "")

        # Se o parâmetro `region` for fornecido, filtra os resultados
        if region:
            data_filtered = data_clean[data_clean["Region"] == region]
            # Se o filtro retornar uma tabela vazia, retorna status 204 (No Content)
            if data_filtered.empty:
                return JSONResponse(
                    status_code=204,
                    content={
                        "message": f"Nenhum dado encontrado para a região '{region}'"
                    },
                )
            data_clean = data_filtered

        return data_clean.to_dict(
            orient="records"
        )  # Retorna os dados como uma lista de dicionários
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler os dados: {str(e)}")


def has_empty_or_null_values(data, column):
    """
    Checa se uma coluna em um dataframe possui algum valor vazio ou nulo.
    """
    return data[column].isna().sum() + (data[column].values == "").sum() > 0


# Endpoint POST para adicionar novos dados
@app.post(
    "/append_listings/",
    tags=["hospedagens"],
    responses={
        200: {
            "content": {
                "application/json": {"example": "Dados adicionados com sucesso"}
            },
        },
        422: {
            "content": {
                "application/json": {"example": "Erro ao adicionar dados com colunas inválidas: ['Coluna Inválida']"}
            },
        },
        500: {
            "description": "Server Error",
            "content": {
                "application/json": {"example": "Erro ao adicionar dados: Exception ..."}
            },
        },
    },
)
def adicionar_hospedagens(novo_dado: DataFrameInput):
    """
    Endpoint para adicionar novas hospedagens na base dados.
    É possível enviar a partir de um Pandas DataFrame.

    Uso:
    ```python
    data = df.where(pd.notnull(df), '').to_dict(orient='split')
    response = requests.post(url, json=data)
    ```
    """
    try:
        global data
        # Converter o input para DataFrame
        novo_df = pd.DataFrame(data=novo_dado.data, columns=novo_dado.columns)
        # Colunas inválidas
        invalid_columns = [c for c in novo_df.columns if c not in data.columns]
        if len(invalid_columns) > 0:
            raise HTTPException(
                status_code=422,
                detail=f"Erro ao adicionar dados com colunas inválidas: {str(invalid_columns)}",
            )
        # Colunas obrigatórias
        required_columns = ["Listing ID", "Region", "Room Type", "Rating"]
        missing_columns = [
            c
            for c in required_columns
            if c not in novo_df.columns or has_empty_or_null_values(novo_df, c)
        ]
        if len(missing_columns) > 0:
            raise HTTPException(
                status_code=422,
                detail=f"Erro ao adicionar dados com valores inválidos/faltantes nas colunas: {str(missing_columns)}",
            )
        # Juntar dados
        data = pd.concat([data, novo_df], ignore_index=True).drop_duplicates(
            subset="Listing ID", keep="first"
        )
        return {"message": "Dados adicionados com sucesso"}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar dados: {str(e)}")

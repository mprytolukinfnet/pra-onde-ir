from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from DataFrameInput import DataFrameInput
from ListingResponse import ListingResponse
from typing import List
import pandas as pd
import sys
sys.path.append('../scraper')
from AirbnbScraper import AirbnbScraper

app_description = """
Esta API interage com a base de dados do projeto "Pra Onde Ir?" permitindo a inclusão e o retorno de dados.
"""

app = FastAPI(
    title="Pra Onde Ir?",
    description=app_description,
)

# Carregar dados da planilha CSV
data = pd.read_csv("../data/airbnb_data.csv", dtype={"Listing ID": "string"})

# Carregar Scraper do Airbnb
airbnb = AirbnbScraper()

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

# Endpoint GET para buscar as imagens de uma hospedagem do Airbnb
@app.get(
    "/get_airbnb_pictures/",
    tags=["hospedagens"],
    response_model=List[str],
    responses={
        200: {
            "description": "Uma lista de URLs de imagens",
            "content": {
                "application/json": {
                    "example": [
                        "https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6NTYzNTMxNTQwOTA4MzY2ODU5/original/14c5c8df-01f9-459e-9c27-372b7a5b5a73.jpeg?im_w=960&im_format=avif",
                        "https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6NTYzNTMxNTQwOTA4MzY2ODU5/original/ff948dc4-0b28-41c2-808e-8f6d2a346207.jpeg?im_w=480&im_format=avif",
                        "https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6NTYzNTMxNTQwOTA4MzY2ODU5/original/4fe405ff-74ce-4ca5-aa5e-d52885632316.jpeg?im_w=480&im_format=avif",
                        "https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6NTYzNTMxNTQwOTA4MzY2ODU5/original/28d289e9-cea8-406e-b84f-6bad7c43f2a9.jpeg?im_w=480&im_format=avif",
                        "https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6NTYzNTMxNTQwOTA4MzY2ODU5/original/24fcc289-b69d-4839-adb2-fdc364a2a0d6.jpeg?im_w=480&im_format=avif"
                    ]
                }
            }
        },
        400: {
            "description": "User Error",
            "content": {
                "application/json": {"example": "Erro: Número de listagem inválido"}
            },
        },
        422: {},
        500: {
            "description": "Server Error",
            "content": {
                "application/json": {"example": "Erro ao buscar as imagens da hospedagem: Exception ..."}
            },
        }
    },
)
def obter_imagens_airbnb(
    listing_id: str = Query(None, description="Id da hospedagem do Airbnb para obter as imagens")
):
    """
    Endpoint para obter as imagens de uma hospedagem do Airbnb.

    Uso:
    ```python
    response = requests.get(url)
    pictures = response.json()
    ```
    """
    print(listing_id)
    try:
        int(listing_id)
    except TypeError:
        raise HTTPException(status_code=400, detail=f"Número de listagem não fornecido")
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Número de listagem não é um número inteiro")
    try:
        pictures = airbnb.get_stay_pictures(listing_id)
        return pictures
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar as imagens da hospedagem: {str(e)}")


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

from pydantic import BaseModel
from typing import List, Any

# Modelo que representa o DataFrame no formato 'split'
class DataFrameInput(BaseModel):
    index: List[int]
    columns: List[str]
    data: List[List[Any]]

    model_config = {
        "json_schema_extra": {
            "example": {
                "index": [0, 1],
                "columns": [
                    "Region",
                    "Listing ID",
                    "Name",
                    "Title",
                    "Room Type",
                    "Person Capacity",
                    "Price per Night (R$)",
                    "Rating",
                    "Reviews",
                    "Latitude",
                    "Longitude",
                    "Badge",
                    "Description",
                    "Amenities",
                    "Pictures",
                ],
                "data": [
                    [
                        "Acre",
                        725194536276378133,
                        "Kitnet mobiliado  Super Encantador 101",
                        "Quarto privativo em loft em Rio Branco, Brasil",
                        "Quarto privativo em loft",
                        3,
                        115,
                        4.95,
                        42,
                        -9.9685,
                        -67.8336,
                        "Preferido dos hóspedes",
                        "Abrace a simplicidade neste lugar tranquilo e bem-localizado.",
                        "['Vista para o pátio', 'Produtos de limpeza', 'Sabonete para o corpo']",
                        "['https://a0.muscache.com/im/ml/photo_enhancement/pictures/22f9ab68-a805-4f1c-bb50-bf95025e46b9.jpg', 'https://a0.muscache.com/im/pictures/aa6bc3a2-bb39-4e69-bb6b-e0bda7ed959a.jpg']",
                    ],
                    [
                        "Acre",
                        1189755903813718306,
                        "apartamento completo com banheiro  para 6 pessoas",
                        "Espaço inteiro: apartamento em Rio Branco, Brasil",
                        "Espaço inteiro: apartamento",
                        6,
                        200,
                        5.0,
                        9,
                        -9.9709,
                        -67.8159,
                        "Preferido dos hóspedes",
                        "apartamento ideal para quem esta buscando conforto, boa acomodacao, e qualidade, moveis todos novos, localizado no centro de rio branco, perto dos principais pontos turisticos de rio branco, apartamaneto com duas camas casal muito confortaveis, uma bi cama de molas, banheiro, geladeira, fogao 4 bocas, microondas, televisao, ar condicionado, guarda roupa, com seguranca, portao eletronico, estacionamento aberto para 4 carros , cerca eletrica, quarto amplo e arejado",
                        "['Máquina de Lavar', 'TV', 'Ar-condicionado']",
                        "['https://a0.muscache.com/im/pictures/miso/Hosting-1189755903813718306/original/78485c05-9d76-4022-bec4-1db9fa2681e2.jpeg']",
                    ],
                ],
            }
        }
    }
from pydantic import BaseModel, Field
from typing import Optional


# Modelo para a resposta de uma hospedagem
class ListingResponse(BaseModel):
    Region: str
    Listing_ID: str = Field(alias="Listing ID")
    Name: str
    Title: str
    Room_Type: str = Field(alias="Room Type")
    Person_Capacity: int = Field(alias="Person Capacity")
    Price_per_Night: int = Field(alias="Price per Night (R$)")
    Rating: float
    Reviews: int
    Latitude: float
    Longitude: float
    Badge: Optional[str]
    Description: str
    Amenities: str
    Pictures: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "Region": "Acre",
                "Listing ID": "725194536276378133",
                "Name": "Kitnet mobiliado Super Encantador 101",
                "Title": "Quarto privativo em loft em Rio Branco, Brasil",
                "Room Type": "Quarto privativo em loft",
                "Person Capacity": 3,
                "Price per Night (R$)": 115,
                "Rating": 4.95,
                "Reviews": 42,
                "Latitude": -9.9685,
                "Longitude": -67.8336,
                "Badge": "Preferido dos hóspedes",
                "Description": "Abrace a simplicidade neste lugar tranquilo e bem-localizado.",
                "Amenities": "['Vista para o pátio', 'Produtos de limpeza', 'Sabonete para o corpo']",
                "Pictures": "['https://a0.muscache.com/im/ml/photo_enhancement/pictures/22f9ab68-a805-4f1c-bb50-bf95025e46b9.jpg','https://a0.muscache.com/im/pictures/aa6bc3a2-bb39-4e69-bb6b-e0bda7ed959a.jpg']",
            }
        }
    }

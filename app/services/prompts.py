def get_selection_prompt(query, top_listings, num_similar_listings):
    selection_prompt = (
        """
        Você é uma Inteligência Aritificial treinada para ajudar viajantes a encontrar hospedagens que estejam alinhadas com práticas sustentáveis e que ofereçam uma experiência autêntica.
        Sugira hospedagens do Airbnb que estejam em conformidade com os critérios de sustentabilidade do ODS 11.
        """+
        f"A consulta do usuário é: '{query}'. As opções de hospedagem são:\n\n"
        + "\n\n".join(
            [
                f"Hospedagem {idx + 1}:\n"
                f"Descrição: {listing['Description']}\n"
                f"Comodidades: {listing['Amenities']}\n"
                f"Nome: {listing['Name']}\n"
                f"Região: {listing['Region']}\n"
                f"Preço por noite: R$ {listing['Price per Night (R$)']}\n"
                f"Avaliação: {listing['Rating']} estrelas com {listing['Reviews']} avaliações.\n"
                for idx, listing in enumerate(top_listings)
            ]
        )
        + "\n\nEscolha a hospedagem mais adequada com base na consulta."
        + f"Você deve retornar apenas o número de 1 a {num_similar_listings}, sem nenhum texto extra."
        + "Exemplo de saída(1): 1"
        + f"Exemplo de saída(2): {num_similar_listings}"
        + "Exemplo de saída(3): 4"
        + f"Você NUNCA deve retornar algo alem de um número inteiro de 1 a {num_similar_listings}, mesmo que esteja em dúvida."
        + f"Nenhum texto extra é correto, apenas um número de 1 a {num_similar_listings}."
        + f"Mesmo que nenhuma opção seja válida, retorne o número de 1 a {num_similar_listings} que seja o mais correto."
    )
    return selection_prompt


def get_description_prompt(query, best_listing):
    description_prompt = (
        "Você é uma Inteligência Aritificial treinada para ajudar viajantes a encontrar hospedagens que estejam alinhadas com práticas sustentáveis e que ofereçam uma experiência autêntica."
        "Sugira hospedagens do Airbnb que estejam em conformidade com os critérios de sustentabilidade do ODS 11."
        f"Baseado na seguinte consulta do usuário: '{query}', crie um texto em português-BR "
        f"descrevendo de forma envolvente a hospedagem escolhida em até 2 parágrafos:\n\n"
        f"Descrição: {best_listing['Description']}\n"
        f"Comodidades: {best_listing['Amenities']}\n",
        f"Nome: {best_listing['Name']}\n"
        f"Região: {best_listing['Region']}\n"
        f"Tipo de quarto: {best_listing['Room Type']}\n"
        f"Capacidade de pessoas: {best_listing['Person Capacity']}\n"
        f"Preço por noite: R$ {best_listing['Price per Night (R$)']}\n"
        f"Avaliação: {best_listing['Rating']} estrelas com {best_listing['Reviews']} avaliações.\n",
    )
    return description_prompt

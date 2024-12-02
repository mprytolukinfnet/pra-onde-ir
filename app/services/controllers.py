import streamlit as st
import asyncio
import httpx
import pandas as pd
import re
from urllib.parse import urljoin
from app.services.prompts import get_selection_prompt, get_description_prompt
from app.services.call_llm import call_llm, call_llm_stream
from streamlit_carousel import carousel

# Initialize session state
state = st.session_state
try:
    API_URL = st.secrets.APP_API_URL
except:
    import os
    from dotenv import load_dotenv
    from pathlib import Path

    # Load environment variables
    load_dotenv(dotenv_path=Path('../../.env'))
    API_URL = os.environ.get('APP_API_URL')

# Change query handler
def change_query():
    state._query = state.query
    for key in ['similar_listings', 'selected_idx', 'best_listing', 'pictures', 'descriptive_text', 'description_complete']:
        if key in state:
            del state[key]
    state.description_complete = False

# Select next listing handler
def select_next_listing(NUM_SIMILAR_LISTINGS):
    if 'selected_idx' in state:
        state.selected_idx = (state.selected_idx + 1) % NUM_SIMILAR_LISTINGS
        for key in ['best_listing', 'pictures', 'descriptive_text', 'description_complete']:
            if key in state:
                del state[key]
        state.description_complete = False

# Fetch data async
async def get_data_async():
    async with httpx.AsyncClient() as client:
        url = urljoin(API_URL, "/get_listings/")
        response = await client.get(url)
        return pd.DataFrame(response.json())

# Get data from API
@st.cache_data 
def get_data():
    url = urljoin(API_URL, "/get_listings/")
    response = httpx.get(url, timeout=30.0)
    return pd.DataFrame(response.json())
    
# Fetch listing images async
async def get_listing_images_async(listing_id):
    async with httpx.AsyncClient() as client:
        url = urljoin(API_URL, f"/get_airbnb_pictures/?listing_id={listing_id}")
        response = await client.get(url)
        return response.json()

# Update listing description
async def update_description(text_placeholder):
    if not state.description_complete:
        description_prompt = get_description_prompt(state.query, state.best_listing)
        state.descriptive_text = ""  # Initialize text incrementally
        async for text_chunk in call_llm_stream(description_prompt):
            state.descriptive_text += text_chunk
            text_placeholder.write(state.descriptive_text)  # Real-time update
        state.description_complete = True

# Load pictures
async def load_pictures(img_placeholders):
    if 'pictures' not in state:
        try:
            state.pictures = await get_listing_images_async(state.best_listing['Listing ID'])
            img_placeholders['cover_placeholder'].image(state.pictures[0], use_column_width=True)
            carousel_items = [dict(title="", text="", img=pic) for pic in state.pictures[1:]]
            img_placeholders['carousel_placeholder'].write("### Outras fotos:")
            img_placeholders['carousel_container'].empty()
            with img_placeholders['carousel_container'].container():
                carousel(items=carousel_items, key=f"carousel_async")
        except:
            img_placeholders.write('Não foi possível carregar as imagens do Airbnb.')


# Run both async tasks
async def get_description_and_pictures_parallel(text_placeholder, img_placeholders):
    await asyncio.gather(update_description(text_placeholder), load_pictures(img_placeholders))


def get_description_and_pictures(text_placeholder, img_placeholders):
    asyncio.run(get_description_and_pictures_parallel(text_placeholder, img_placeholders))

# Select best listing according to the user query
def select_best_listing(data, NUM_SIMILAR_LISTINGS=5, select_with_llm = True):
    top_listings = data[data["Listing ID"].isin(state.similar_listings)].to_dict(orient="records")

    if 'best_listing' not in state:
        if select_with_llm:
            if 'selected_idx' not in state:
                try:
                    # Call Gemini to select the best listing
                    selection_prompt = get_selection_prompt(state.query, top_listings, NUM_SIMILAR_LISTINGS)
                    best_listing_response = call_llm(selection_prompt)
                    # Filter response
                    filtered_response = re.sub('[^0-9]','', best_listing_response)
                    state.selected_idx = (int(best_listing_response) - 1) % NUM_SIMILAR_LISTINGS  # Assuming Gemini returns a 1-based index
                except (ValueError, IndexError):
                    # If error, select first result
                    state.selected_idx = 0
        else:
            state.selected_idx = state.selected_idx if 'selected_idx' in state else 0
        state.best_listing = top_listings[state.selected_idx]

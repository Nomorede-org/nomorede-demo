import openai
import json
import streamlit as st

OPENAI_KEY = st.secrets['general']['OPENAI_API_KEY']

client = openai.OpenAI(api_key=OPENAI_KEY)

def count_tokens(text):
    return len(text.split())

def generate_lookbook(client_data):
    print(f"AI analyst working on {client_data['name']}")
    essential_data = {
        "name": client_data['name'],
        "gender": client_data['gender'],
        "face_shape":client_data['face_shape'],
        "eyewere_suggestion":client_data['eyewere_suggestion'],
        "hair_suggestion":client_data['hair_suggestion'],        
        "clothing_suggestion":client_data['clothing_suggestion'],
        "beard_suggestion":client_data['beard_suggestion'] if client_data['gender'] == "Male" else None,
        "accessory_suggestion":client_data['accessory_suggestion'] if client_data['gender'] == "Female" else None,
        "unit_height": client_data['unit_height'],

        "weight": client_data['weight'],
        "height": client_data['height'],
        "bust_size": client_data['bust_size'] if client_data['gender'] == "Female" else None,
        "shoulder_width": client_data['shoulder_width'],
        "hip_size": client_data['hip_size'],
        "body_shape":client_data['body_shape'],
        "body_shape_suggestion":client_data['body_shape_suggestion'],
        "waist_size": client_data['waist_size'],
        "veins_color": client_data['veins_color'],
        "cloth_prefered": client_data['fabric_like'],
        "features_highlight": client_data['features_highlight'],
        "area_camoflage": client_data['area_camoflage'],
        "season":client_data['season'],
        "tone":client_data['tone'],
        "flow":client_data['flow'],
        "color_pallet":client_data['color_pallet']
    }
    print(essential_data['eyewere_suggestion'])
    prompt = f"""
    You are an expert fashion stylist dedicated to curating personalized lookbooks for clients, leveraging their unique body measurements, face shape, and color analysis to suggest styles that elevate their individual aesthetic. Your role is to provide detailed explanations about suitable styles, necklines, sleeve types, patterns, and colors without suggesting specific products or pricing.
    Client Information:
    Name: {essential_data['name']}
    Height: {essential_data['unit_height']} ({essential_data['height']})
    Weight: {essential_data['weight']}
    Bust Size: {essential_data['bust_size']if not None else "Not acclicable"} (if applicable)
    Shoulder Width: {essential_data['shoulder_width']}
    Hip Size: {essential_data['hip_size']}
    Body Shape: {essential_data['body_shape']}
    Waist Size: {essential_data['waist_size']}
    Vein Color: {essential_data['veins_color']} (to determine undertones)
    Face Shape Analysis:
    Gender: {essential_data['gender']}
    Face Shape: {essential_data['face_shape']}

    Eyewear Suggestions:
    Recommended:{essential_data['eyewere_suggestion']['Recommended']}.
    Avoid: {essential_data['eyewere_suggestion']['Avoid']}.

    Hair Suggestions:
    Recommended: {essential_data['hair_suggestion']['recommended']}.
    Avoid: {essential_data['hair_suggestion']['avoid']}.

    Clothing Suggestions:
    
    Color Analysis:
    Explain the significance of there color analysis and explain in depth about there Season, Tone and Flow
    Season: {essential_data['season']}
    Tone: {essential_data['tone']}
    Flow: {essential_data['flow']}
    
    Recommendations:
    Explain the stlyes that go well with the body shape based on these suggestions {essential_data['body_shape_suggestion']}
    Your explanations should empower the client with knowledge and confidence in their style choices, ensuring they understand the reasoning behind each recommendation. Aim to make the client feel valued and excited about their personal style journey.
    """

    # Check token count and truncate if necessary
    if count_tokens(prompt) > 3500:
        raise ValueError("The prompt is too long and may exceed the token limit for GPT-4.")

    # Call the OpenAI API to generate the lookbook
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert fashion stylist."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the generated text from the response
    lookbook = response.choices[0].message.content
    print("OpenAI Assistant Running")
    return lookbook
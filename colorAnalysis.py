import cv2
import numpy as np
from colorthief import ColorThief
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import streamlit as st

def extract_colors(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    color_thief = ColorThief(image_path)
    dominant_color = color_thief.get_color(quality=1)
    return dominant_color

def get_dominant_colors(image, k=3):
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixels = img_rgb.reshape(-1, 3)
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_
    return colors.astype(int)

def plot_colors(colors):
    bar = np.zeros((50, 300, 3), dtype='uint8')
    start_x = 0
    for color in colors:
        end_x = start_x + 300 // len(colors)
        cv2.rectangle(bar, (start_x, 0), (end_x, 50), color.tolist(), -1)
        start_x = end_x
    return bar

def classify_color(color):
    r, g, b = color
    if r > 200 and g > 200 and b > 200:
        return 'Light'
    elif r < 50 and g < 50 and b < 50:
        return 'Dark'
    elif (r > g) and (r > b):
        return 'Warm'
    elif (b > g) and (b > r):
        return 'Cool'
    else:
        return 'Neutral'

def determine_season_and_flow(skin_color, hair_color, eye_color):
    skin_tone = classify_color(skin_color)
    hair_tone = classify_color(hair_color)
    eye_tone = classify_color(eye_color)

    if skin_tone == 'Cool' or eye_tone == 'Cool':
        if hair_tone == 'Dark' or skin_tone == 'Dark':
            season = 'Winter'
            if hair_tone == 'Bright' or skin_tone == 'Bright':
                tone = 'Bright Winter'
            elif eye_tone == 'Bright' or skin_tone == 'Bright':
                tone = 'Bright Winter'
            else:
                tone = 'Dark Winter'
        else:
            season = 'Summer'
            if skin_tone == 'Light' or hair_tone == 'Light':
                tone = 'Light Summer'
            elif hair_tone == 'Muted' or eye_tone == 'Muted':
                tone = 'Soft Summer'
            else:
                tone = 'True Summer'
    else:
        if hair_tone == 'Light' or skin_tone == 'Light':
            season = 'Spring'
            if hair_tone == 'Bright' or eye_tone == 'Bright':
                tone = 'Bright Spring'
            elif skin_tone == 'Warm':
                tone = 'True Spring'
            else:
                tone = 'Light Spring'
        else:
            season = 'Autumn'
            if skin_tone == 'Dark' or hair_tone == 'Dark':
                tone = 'Dark Autumn'
            elif hair_tone == 'Muted' or eye_tone == 'Muted':
                tone = 'Soft Autumn'
            else:
                tone = 'True Autumn'

    flow = None
    if season == 'Winter':
        flow = 'Flow into Summer'
    elif season == 'Summer':
        flow = 'Flow into Winter'
    elif season == 'Autumn':
        flow = 'Flow into Spring'
    elif season == 'Spring':
        flow = 'Flow into Autumn'

    return season, tone, flow

# Streamlit UI
st.title('Image Color Analysis and Season Determination')

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display uploaded image
    image = np.array(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # st.image(image, caption='Uploaded Image', use_column_width=True)
    # Analyze and display dominant colors
    colors = get_dominant_colors(image, k=3)
    color_bar = plot_colors(colors)
    st.image(color_bar, caption='Dominant Colors', use_column_width=True)

    # Determine season and flow
    skin_color = colors[0]
    hair_color = colors[1]
    eye_color = colors[2]
    season, tone, flow = determine_season_and_flow(skin_color, hair_color, eye_color)

    st.write(f'Season: {season}, Tone: {tone}, Flow: {flow}')
else:
    st.write('Upload an image to begin analysis.')

import requests
import cv2
import numpy as np
from colorthief import ColorThief
from sklearn.cluster import KMeans
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.patches as patches


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
color_palettes = {
    "Bright Spring": ["#FF6F61", "#FFD700", "#FFA07A", "#00FF00", "#40E0D0", "#FF69B4", "#FFA500", "#8A2BE2"],
    "Warm Spring": ["#FF4500", "#FFD700", "#FFA500", "#ADFF2F", "#00FA9A", "#FF69B4", "#DA70D6", "#8B4513"],
    "Light Spring": ["#FFB6C1", "#FFD700", "#98FB98", "#ADFF2F", "#00CED1", "#FF69B4", "#F0E68C", "#DDA0DD"],
    "Light Summer": ["#E6E6FA", "#B0E0E6", "#98FB98", "#ADD8E6", "#FFB6C1", "#FFDAB9", "#E0FFFF", "#FAFAD2"],
    "Cool Summer": ["#8A2BE2", "#4682B4", "#00CED1", "#5F9EA0", "#6A5ACD", "#48D1CC", "#7B68EE", "#87CEFA"],
    "Muted Summer": ["#D8BFD8", "#C0C0C0", "#A9A9A9", "#778899", "#B0C4DE", "#AFEEEE", "#D3D3D3", "#DDA0DD"],
    "Muted Autumn": ["#8B4513", "#A0522D", "#D2691E", "#F4A460", "#DAA520", "#CD853F", "#D2B48C", "#BC8F8F"],
    "Warm Autumn": ["#A52A2A", "#D2691E", "#B8860B", "#CD853F", "#DAA520", "#8B4513", "#D2B48C", "#FFD700"],
    "Dark Autumn": ["#8B4513", "#654321", "#D2691E", "#8B0000", "#A52A2A", "#800000", "#D2B48C", "#8B4513"],
    "Dark Winter": ["#000080", "#2F4F4F", "#8B0000", "#800000", "#4B0082", "#483D8B", "#191970", "#2F4F4F"],
    "Cool Winter": ["#00008B", "#000080", "#483D8B", "#4B0082", "#4682B4", "#5F9EA0", "#4682B4", "#00008B"],
    "Bright Winter": ["#FF1493", "#1E90FF", "#00CED1", "#32CD32", "#FFA07A", "#8A2BE2", "#DA70D6", "#00BFFF"],
}

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
                tone = 'Cool Winter'
            else:
                tone = 'Dark Winter'
        else:
            season = 'Summer'
            if skin_tone == 'Light' or hair_tone == 'Light':
                tone = 'Light Summer'
            elif hair_tone == 'Muted' or eye_tone == 'Muted':
                tone = 'Cool Summer'
            else:
                tone = 'Muted Summer'
    else:
        if hair_tone == 'Light' or skin_tone == 'Light':
            season = 'Spring'
            if hair_tone == 'Bright' or eye_tone == 'Bright':
                tone = 'Bright Spring'
            elif skin_tone == 'Warm':
                tone = 'Warm Spring'
            else:
                tone = 'Light Spring'
        else:
            season = 'Autumn'
            if skin_tone == 'Dark' or hair_tone == 'Dark':
                tone = 'Dark Autumn'
            elif hair_tone == 'Muted' or eye_tone == 'Muted':
                tone = 'Muted Autumn'
            else:
                tone = 'Warm Autumn'

    flow = None
    if season == 'Winter':
        flow = 'Flow into Summer'
    elif season == 'Summer':
        flow = 'Flow into Winter'
    elif season == 'Autumn':
        flow = 'Flow into Spring'
    elif season == 'Spring':
        flow = 'Flow into Autumn'

    return season, tone, flow,color_palettes[tone]


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def overlay_color_strip(image, color, compliment_color):
    # Ensure the image has an alpha channel
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    # Get the size of the original image
    width, height = image.size

    # Define the height of each color block (10% each for two blocks, so total 20%)
    block_height = int(height * 0.1)  # Each block will be 10% of the image height

    # Create a new image with extra space for the color blocks
    new_image = Image.new('RGBA', (width, height + 2 * block_height), (255, 255, 255, 0))

    # Paste the original image onto the new image
    new_image.paste(image, (0, 0))

    # Create the color blocks using ImageDraw
    draw = ImageDraw.Draw(new_image)

    # Draw the first color block (original color) at the bottom of the image
    draw.rectangle([(0, height), (width, height + block_height)], fill=color + (255,))

    # Draw the second color block (complementary color) below the first one
    # draw.rectangle([(0, height + block_height), (width, height + 2 * block_height)], fill=compliment_color + (255,))

    return new_image

def create_color_plot(color_pallet):
    colors = color_pallet['color']
    compliment_colors = color_pallet['compliment_color']

    # Ensure we have the same number of colors and compliments
    assert len(colors) == len(compliment_colors), "Colors and compliment colors must have the same length"

    # Set the figure size
    fig, ax = plt.subplots(figsize=(12, 6))

    # Number of rows and columns
    num_cols = 5  # We'll have 5 pairs per row
    num_rows = len(colors) // num_cols + (1 if len(colors) % num_cols != 0 else 0)

    # Set up the plot
    ax.set_xlim(0, num_cols * 2)  # Double the width for pairs
    ax.set_ylim(0, num_rows)
    ax.set_aspect('equal')
    ax.axis('off')

    # Plot color pairs
    for idx, (color, compliment) in enumerate(zip(colors, compliment_colors)):
        row = idx // num_cols
        col = idx % num_cols

        # Main color circle
        main_circle = patches.Circle((col * 2 + 0.5, num_rows - row - 0.5), 0.4, color=color)
        ax.add_patch(main_circle)

        # Complementary color circle
        comp_circle = patches.Circle((col * 2 + 1.5, num_rows - row - 0.5), 0.4, color=compliment)
        ax.add_patch(comp_circle)

        # Add color codes as text
        ax.text(col * 2 + 0.5, num_rows - row - 1, color, ha='center', va='center', fontsize=8)
        ax.text(col * 2 + 1.5, num_rows - row - 1, compliment, ha='center', va='center', fontsize=8)

    plt.title("Color Palette with Complementary Colors")
    return fig

def GetColorName(hex):
    url = f"https://www.thecolorapi.com/id?hex={hex[1:]}"
    response = requests.get(url)
    data = response.json()
    return data['name']['value']
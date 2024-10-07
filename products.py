import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO


backend_url = st.secrets['general']['BACKEND_URL']

# Endpoint URL
endpoint = f"{backend_url}/customer/search/66ec18c26fcff589f0960ede"

# Fetch products from the API
def fetch_products():
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()["products"]
    else:
        st.error(f"Error fetching products: {response.status_code}")
        return []

# Main function to display product cards
def GetPersonalProduct():
    st.warning('This section is not yet live', icon="⚠️")
    # products = fetch_products()
    
    # num_columns = 3
    # if products:
    #     for i in range(0, len(products), num_columns):
    #         # Create a row with the defined number of columns
    #         cols = st.columns(num_columns)
            
    #         # Loop over each product in the current row
    #         for idx, col in enumerate(cols):
    #             if i + idx < len(products):
    #                 product = products[i + idx]
                    
    #                 with col:
    #                     # Product Information
    #                     st.subheader(f"{product['name']}")
    #                     st.markdown(f"Price: **{product['price']} {product['price_unit']}**")
    #                     st.text(f"Category: {product['category']}")
    #                     st.text(f"Gender: {product['gender']}")
    #                     st.text(f"Sizes: {[size['size'] for size in product['sizes']]}")
    #                     st.markdown(f"*:red[Available Quantity:{product['quantity']}]* ")
                        
    #                     # Display first image of the product
    #                     first_variant = product['varient'][0]
    #                     first_image_url = first_variant['images'][0]
    #                     try:
    #                         response = requests.get(first_image_url)
    #                         response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    #                         img = Image.open(BytesIO(response.content))
    #                         st.image(img, caption=f"Color: {first_variant['color_name']}", width=200)
    #                     except requests.RequestException as e:
    #                         st.error(f"Error fetching image: {e}")
    #                     except UnidentifiedImageError:
    #                         st.error("Unable to open image. The image might be corrupted or in an unsupported format.")
    #                     except Exception as e:
    #                         st.error(f"An unexpected error occurred: {e}")
                        
    #                     st.text(f"Tags: {', '.join(product['tags'])}")
    #                     st.markdown("---")  # Separator line

    # else:
    #     st.text("No products found.")

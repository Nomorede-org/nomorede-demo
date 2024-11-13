
from products import GetPersonalProduct
import streamlit as st
from PIL import Image
import json
import requests
from io import BytesIO
import cv2
import numpy as np
from PIL import Image
from aihelper import generate_lookbook
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from helper import GetColorName, create_color_plot, determine_season_and_flow, get_dominant_colors, hex_to_rgb, overlay_color_strip, plot_colors,color_palettes
from streamlit_option_menu import option_menu
from waitlist import add_to_waitlist
# Streamlit Page Configuration

backend_url = st.secrets['general']['BACKEND_URL']
body_shape_url= st.secrets['general']['BODY_SHAPE_URL']

st.set_page_config(
    page_title="Nomorede",
    page_icon="5.ico",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.nomorede.com/contactUs',
        'Report a bug': "https://www.nomorede.com/contactUs",
        'About': "One Stop Science Backed styling aggregator platform"
    }
)
clothing_styles = [
    "T-shirts",
    "Dress Shirts",
    "Polo Shirts",
    "Jeans",
    "Chinos",
    "Suit Pants",
    "Blazers",
    "Hoodies",
    "Sweaters",
    "Leather Jackets",
    "Blouses",
    "Tops",
    "Dresses",
    "Skirts",
    "Jeans",
    "Leggings",
    "Cardigans",
    "Blazers",
    "Jumpsuits",
    "Maxi Dresses"
]

cloth_material=[ "Cotton",
    "Linen",
    "Wool",
    "Silk",
    "Denim",
    "Leather",
    "Polyester",
    "Velvet",
    "Satin",
    "Chiffon",
    "Khadi",
    "Rayon",
    "Viscose",
    "Georgette"]

body_features=[
    "Neck",
    "Shoulders",
    "Bust / Chest",
    "Arms",
    "Back",
    "Stomach",
    "Waist",
    "Hips",
    "Thighs"
    ]

with st.sidebar:
    selected = option_menu("Menu",["Home", 'LookBook','Products','Contact Us','About us',], 
        icons=['bi-house-door-fill', 'bi-person-fill',"bi bi-boxes",'bi bi-people-fill','bi-info-circle-fill'],menu_icon="bi-list", default_index=0)
    
    # selected
if 'status' not in st.session_state:
    st.session_state.status = False
if selected == "Home":
    st.title("Personal Styling 🧢👟👖🎧")
    st.markdown("**Personal Details**")
    
    name=st.text_input("Hey, We’re curious to know your Name?")
    gender = st.radio("Gender", ["Male", "Female", "Prefer not to say"])
    st.markdown("**Body Measurements**")
    unit_height = st.radio(
        "What Unit are you measuring in?",
        ["Meter"]
    )
    # foot_size = st.number_input("Foot Size", min_value=1, max_value=15)
    weight = st.number_input("Weight (in kg)", min_value=1)
    height = st.number_input("Height (in units)", min_value=1.0, format="%.2f")
    # if gender == "Female":
    #     bust_size = st.number_input("Bust size (in Inches)", min_value=0)
    
    # shoulder_width = st.number_input("Shoulder width (in Inches)", min_value=0)
    # hip_size = st.number_input("Hip size (in Inches)", min_value=0)
    # # high_hip = st.number_input("High hip", min_value=0)
    # waist_size = st.number_input("Waist size (in Inches)", min_value=0)
    # st.markdown("**------OR------**")
    st.image('body-shape-reference.jpg', width=500, caption="*Please share your image in this pose*")
    body_image = st.file_uploader('Upload a full body image', type=['png', 'jpeg', 'jpg'])
    face_image = st.file_uploader('Upload a selfie', type=['png', 'jpeg', 'jpg'])
    st.warning("For optimal results, please upload an image with a clearly visible face taken in natural sunlight ☀️.")
    # hand_veins = st.file_uploader('Upload an image of veins on hand', type=['png', 'jpeg', 'jpg'])
    if face_image is not None:
        st.session_state.face_image = face_image
    if body_image is not None:
        st.session_state.body_image = body_image
    st.markdown("**Color Theory**")
    
    st.image('color_analysis.jpg', width=500, caption="Veins Color")

    veins_color = st.radio(
        "What is your veins color?",
        ["cool", "warm", "neutral"]
    )

    st.markdown("**Style Preferences and Goals**")
    cloth_prefered_input = st.multiselect("If you could live in these fabrics forever, which would you choose?",cloth_material)
    
    st.markdown("**Body Comfort:**")
    features_highlight = st.multiselect("What body features do you love to show off?",body_features)
    area_camoflage = st.multiselect("Are there any body features you like to keep subtle?",body_features)
    
    # Collect all the data in a dictionary
    data = {
        "name":name,
        "gender": gender,
        "unit_height": unit_height,
        # "foot_size": foot_size,
        "weight": weight,
        "height": height*100,
        # "bust_size": bust_size if gender == "Female" else None,
        # "shoulder_width": shoulder_width,
        # "hip_size": hip_size,
        # "waist_size": waist_size,
        "veins_color": veins_color,
        "fabric_like": cloth_prefered_input,
        "features_highlight": features_highlight,
        "area_camoflage": area_camoflage
    }

    # body_shape_post = {
    #     "gender": gender,
    #     "unit": "inche",
    #     "bust_size": bust_size if gender == "Female" else 0,
    #     "shoulder_width": shoulder_width if gender == "Male" else 0,
    #     "hip_size": hip_size,
    #     "waist_size": waist_size
    # }

    # Button to submit the form
    if st.button("Submit"):
        with st.spinner("Analyzing data..."):
            st.write("Calculating Body Shape...")
            try:
                image_body=Image.open(body_image)
                image_bytes = BytesIO()
                image_bytes.seek(0)
                image_body.save(image_bytes, format="JPEG")
                image_bytes = image_bytes.getvalue()
                files = {"file": ("filename", image_bytes, body_image.type)}
                headers = {
                "accept": "application/json",
                "Content-Type": "multipart/form-data"
                }
                body_shape_analysis_response=requests.post(body_shape_url,
                                                           files=files,
                                                           params={
                                                           "height":data['height']
                                                            })
                print(f"Status Code: {body_shape_analysis_response.status_code}")
                print("Response BODY SHAPE ANALYSIS JSON:", body_shape_analysis_response.json())
                # if body_shape_analysis_response.status_code != 200:
                body_shape_image_response=body_shape_analysis_response.json()
                data['bust_size']=body_shape_image_response['processed_image']['chest']
                data['shoulder_width']=body_shape_image_response['processed_image']['shoulder width']
                data['hip_size']=body_shape_image_response['processed_image']['hips']
                data['waist_size']=body_shape_image_response['processed_image']['waist']
                body_shape = requests.post(f"{backend_url}/tools/bodyShape", json={
                                                                                "gender": gender,
                                                                                "unit": "inche",
                                                                                "bust_size":body_shape_image_response['processed_image']['chest'],
                                                                                "shoulder_width": body_shape_image_response['processed_image']['shoulder width'],
                                                                                "hip_size": body_shape_image_response['processed_image']['hips'],
                                                                                "waist_size": body_shape_image_response['processed_image']['waist']
                                                                            })
                if body_shape.status_code != 200:
                    st.error("Failed to submit data. Please try again.")
                body_shape = body_shape.json()
                print(f"body shape response::{body_shape}")
                data['body_shape'] = body_shape['body_shape']
                data['body_shape_suggestion'] = body_shape['body_shape_suggestion']
                # else:
                #     st.error("Please retry with different image")
            except Exception as e:
                st.error(f"An error occurred: {e}")
            
            st.write("Identifying Face Shape and Performing Color Analysis...")
            try:
                if face_image is not None:
                    image = Image.open(face_image)
                    # Convert image to bytes for face shape analysis
                    image_bytes = BytesIO()
                    image.save(image_bytes, format="JPEG")
                    image_bytes = image_bytes.getvalue()
                    files = {"file": ("filename", image_bytes, face_image.type)}
                    data_post = {
                        'gender': gender,
                    }
                    face_shape_analysis = requests.post(f"{backend_url}/tools/faceAnalysis?gender={gender}", files=files)
                    if face_shape_analysis.status_code != 200:
                        st.error("Failed to submit face image for analysis. Please try again.")
                    face_shape_analysis = face_shape_analysis.json()
                    print(face_shape_analysis)
                    data['face_shape'] = face_shape_analysis['body_measurements.face_shape']
                    data['eyewere_suggestion'] = face_shape_analysis['eyewere_suggestion']
                    data['hair_suggestion'] = face_shape_analysis['hair_suggestion']
                    data['clothing_suggestion'] = face_shape_analysis['clothing_suggestion']
                    if gender == "Male":
                        data['beard_suggestion'] = face_shape_analysis['beard_suggestion']
                    elif gender == "Female":
                        data['accessory_suggestion'] = face_shape_analysis['accessory_suggestion']
                    
                    # Color analysis
                    files_color = {"image": ("filename", image_bytes, face_image.type)}
                    color_analysis = requests.post(f"{backend_url}/tools/colorAnalysis?vain_color={veins_color}", files=files_color)
                    
                    if color_analysis.status_code!=200:
                        st.error("Failed to submit face image for color analysis. Please try again.")
                    color_analysis=color_analysis.json()
                    print(f"Color Analysis results: {color_analysis}")
                    data['season'] = color_analysis['season']
                    data['tone'] = color_analysis['tone']
                    data['flow'] = color_analysis['flow']
                    data['color_pallet']=color_analysis['color_pallet']
                    # st.text(f"face predicted: {prediction}")
                else:
                    st.error("Please upload an image with clear face visibility")
            except Exception as e:
                st.error(f"Error in face shape and color analysis: {e}")
            # fig = create_color_plot(data['color_pallet'])
            # st.pyplot(fig)
            st.write("Generating lookbook...")
            try:
                lookbook_data= generate_lookbook(data)
                st.session_state.summary = lookbook_data
                st.success("Lookbook generated successfully.")
            except Exception as e:
                st.error(f"Error generating lookbook: {e}")

            # Save data to session state
            st.session_state.data = data
            st.session_state.face_image = face_image
            st.session_state.status = True

            st.success("Profile is ready!")

elif selected == 'LookBook':
    if st.session_state.status == False:
        st.warning("Please fill the form and submit before viewing the lookbook.")
    else:
        st.warning("This is not ideally how a customer views our platform, Imagin all products that fit directly as per these suggestions in one place if still not satisfied they can view the entire marketplace.", icon="⚠️")
        if 'summary' in st.session_state:
            st.markdown(st.session_state.summary)
        else:
            st.warning("Lookbook summary is not available.")

        if 'face_image' in st.session_state:
            st.session_state.face_image.seek(0)
            image = Image.open(st.session_state.face_image)
            
            if 'color_pallet' in st.session_state.data:
                hex_list = st.session_state.data['color_pallet']['color']+st.session_state.data['color_pallet']['compliment_color']
                colors = {GetColorName(hex_code): hex_code for hex_code in hex_list}
                print(colors)
                cols = st.columns(4)  # Create 4 columns for the grid
                for index, (color_name, color_hex) in enumerate(colors.items()):
                    with cols[index % 4]:  # Use modulo to cycle through columns
                        st.markdown(
                            f"<div style='background-color: {color_hex}; width: 100%; height: 80px; border-radius: 5px;'></div>", 
                            unsafe_allow_html=True
                        )
                        st.write(color_name)
            else:
                st.warning("Color palette data is not available for image overlay.")
        else:
            st.warning("Face image is not available.")

if selected =='Products':
    GetPersonalProduct()
    # if st.session_state.status == False:
    #     st.markdown("Please fill the form and submit.")
    # else:
if selected =='Contact Us':
    st.markdown("""
    **Contact Us:**

    If you have any questions or feedback, please don't hesitate to reach out to us. You can contact us through the following channels:

    - Email: [kaushik@nomorede.com](mailto:kaushik@nomorede.com)
    - Phone: [+91 7816093181](tel:+91 7816093181)

    We value your input and look forward to hearing from you!
    """)
    name=st.text_input("Name",placeholder="Ralph")
    email=st.text_input("Email",placeholder="info@nomorede.com")
    mobile=st.text_input("Mobile",placeholder="+91 7816093181")
    message=st.text_area("Message",placeholder="I found this app really useful and it made me look better. Could you make it even better?")
    if st.button("Submit"):
        response=add_to_waitlist(name=name,email=email,mobile=mobile,message=message,backend_url=backend_url)
        if response==200:
            st.success("Your message has been submitted successfully.")
        else:
            st.error(f"Failed to submit your message. Please try again later.")
if selected =='About us':
    st.markdown("""

**About Us:**

Nomorede is your one-stop destination for all things fashion. From head-to-toe styling to wardrobe organization, our platform simplifies the process of looking your best, so you can focus on feeling great in your own skin.

**Manifesto:**

At Nomorede, we're redefining personal style with a seamless blend of innovation and individuality. Our cutting-edge technology offers virtual consultations and personalized shopping, ensuring a high-quality, effortless experience. Discover the future of fashion with us, where the art of styling meets the science of technology.

**Where Fashion Meets Technology**

Founded by a tech enthusiast and a fashion aficionado, Nomorede is your canvas to boldly showcase your unique style. With cutting-edge tech and visionary creators, fashion becomes exhilarating, accessible, and captivating. Join our revolution, rewrite the rules, and radiate confidence every step of the way.

**Our Values:**

**Future-Proof Fashion**
At Nomorede, we push boundaries and embrace the new, setting trends on fire with fresh ideas and cutting-edge tech. We're leading the fashion revolution one killer outfit at a time.

**Power in Partnership**
We're all about building a fashion family, collaborating with fierce brands and stylists. Together, we push boundaries, creating a space where everyone shines.

**Human-Centric Fashion**
We're fueled by real people rocking real styles. With cutting-edge tech, we make fashion fun, accessible, and totally you. Join our community of fashion enthusiasts and unleash your unique style with Nomorede.
""")
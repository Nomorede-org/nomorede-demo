import streamlit as st

# Title of the app
st.title("Color Palette and Color Picker")

st.subheader("Static Color Palette")
colors = {
    "Red": "#FF5733",
    "Green": "#33FF57",
    "Blue": "#3357FF",
    "Yellow": "#FFFF33",
    "Purple": "#5733FF",
    "Orange": "#FF8C00",
    "Cyan": "#00FFFF",
    "Magenta": "#FF00FF",
}


cols = st.columns(4)  # Create 4 columns for the grid
for index, (color_name, color_hex) in enumerate(colors.items()):
    with cols[index % 4]:  # Use modulo to cycle through columns
        st.markdown(
            f"<div style='background-color: {color_hex}; width: 100%; height: 80px; border-radius: 5px;'></div>", 
            unsafe_allow_html=True
        )
        st.write(color_name)
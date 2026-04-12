import streamlit as st
from PIL import ImageEnhance, ImageFilter, Image
import io

st.title("Image Resizer Tool v2")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

style = st.selectbox(
    "Choose style",
    ["Art (A4 Portrait)", "Art Horizontal (A4 Landscape)", "YouTube"]
)

if uploaded_file:
    img = Image.open(uploaded_file)

    if style == "Art (A4 Portrait)":
        size = (2480, 3508)
    elif style == "Art Horizontal (A4 Landscape)":
        size = (3508, 2480)
    else:
        size = (4608, 3072)

    img = img.resize(size, Image.Resampling.LANCZOS)

    # Improve clarity
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    # Slight color/contrast pop
    img = ImageEnhance.Color(img).enhance(1.05)
    img = ImageEnhance.Contrast(img).enhance(1.1)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG", dpi=(300, 300))
    buffer.seek(0)

    st.image(img, caption="Preview", use_column_width=True)

    filename = st.text_input("Enter file name (without extension)", value="processed")

    st.download_button(
        label="Download Image",
        data=buffer,
        file_name=f"{filename}.png",
        mime="image/png"
    )
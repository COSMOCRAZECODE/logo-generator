import streamlit as st
import requests
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import os

# Load API keys from Streamlit secrets
HUGGINGFACE_TOKEN = st.secrets["HUGGINGFACE_TOKEN"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-pro")

# Hugging Face endpoint
HF_API_URL = "https://api-inference.huggingface.co/models/thepowerfulde/logo-diffusion"
headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}

def query_huggingface(prompt):
    payload = {"inputs": prompt}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    return response.content

def generate_prompt(company, style, colors, mood):
    full_prompt = f"""
Generate a creative prompt for a tech logo using the following details:

Company Name: {company}
Design Style: {style}
Color Preferences: {colors}
Mood or Theme: {mood}

The prompt should be clear, detailed, and suitable for AI-based logo generation.
    """
    response = gemini_model.generate_content(full_prompt)
    return response.text.strip()

# Streamlit UI
st.set_page_config(page_title="AI Logo Generator", page_icon="🤖")
st.title("🎨 AI-Powered Logo Generator")
st.markdown("Generate stunning tech logos using **Gemini + Stable Diffusion**")

with st.form("logo_form"):
    company = st.text_input("Company Name")
    style = st.text_input("Design Style", value="Minimalist, flat, vector")
    colors = st.text_input("Color Preferences", value="Blues, greys, or gradients")
    mood = st.text_input("Mood/Theme", value="Futuristic, professional, techy")
    submitted = st.form_submit_button("Generate Logo")

if submitted:
    with st.spinner("🤖 Generating prompt using Gemini..."):
        logo_prompt = generate_prompt(company, style, colors, mood)

    st.subheader("✨ Gemini-Generated Prompt:")
    st.markdown(f"```{logo_prompt}```")

    with st.spinner("🎨 Generating logo with Stable Diffusion..."):
        image_bytes = query_huggingface(logo_prompt)

    try:
        image = Image.open(BytesIO(image_bytes))
        st.image(image, caption="Generated Logo", use_column_width=True)

        buf = BytesIO()
        image.save(buf, format="PNG")
        st.download_button(
            label="⬇️ Download Logo",
            data=buf.getvalue(),
            file_name=f"{company.lower().replace(' ', '_')}_logo.png",
            mime="image/png",
        )
    except Exception as e:
        st.error("❌ Error generating image. Please try again.")
        st.text(str(e))


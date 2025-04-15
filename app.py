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
gemini_model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

# Hugging Face endpoint
HF_API_URL = "https://api-inference.huggingface.co/models/thepowerfulde/logo-diffusion"
headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}

def query_huggingface(prompt):
   def query_huggingface(prompt):
    payload = {"inputs": prompt}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    
    # Check if it's JSON (likely an error or loading)
    if "application/json" in response.headers["Content-Type"]:
        err_json = response.json()
        raise ValueError(err_json.get("error", "Unknown error from Hugging Face API"))
    
    return response.content

def generate_prompt(company_name, industry, brand_values, target_audience, design_style, color_palette, typography, icon_type, mandatory_elements, mood):
    full_prompt = f"""
    You are a branding expert and AI logo designer. Based on the following design brief, generate a unique logo concept and a clear image prompt for an AI image generation model like Stable Diffusion.

    Company Name: {company_name}
    Industry: {industry}
    Brand Values: {brand_values}
    Target Audience: {target_audience}
    Design Style: {design_style}
    Color Palette and Meaning: {color_palette}
    Typography: {typography}
    Icon Type: {icon_type}
    Mandatory Elements: {mandatory_elements}
    Mood: {mood}

    1. Describe the logo concept clearly.
    2. Then, write a detailed prompt in one line to generate the logo using an image model like Stable Diffusion.
    """
    response = gemini_model.generate_content(full_prompt)
    return response.text.strip()

# Streamlit UI
st.set_page_config(page_title="AI Logo Generator", page_icon="🤖")
st.title("🎨 AI-Powered Logo Generator")
st.markdown("Generate stunning tech logos using **Gemini + Stable Diffusion**")

with st.form("logo_form"):
    company_name = st.text_input("What's the name of your company?")
    industry = st.text_input("What's your industry type?")
    brand_values = st.text_input("What are your country's brand values?")
    target_audience = st.text_input("What are your target audience?")
    design_style = st.text_input("Design Style", value="Minimalist, flat, vector")
    color_palette = st.text_input("Color Preferences", value="Blues, greys, or gradients")
    typography = st.text_input("suggest some typography")
    icon_type = st.text_input("What are the icon types you want?")
    mood = st.text_input("Mood/Theme", value="Futuristic, professional, techy")
    mandatory_elements = st.text_input("What are some suggestions and mandatory elements you want?")
    submitted = st.form_submit_button("Generate Logo")

if submitted:
    with st.spinner("🤖 Generating prompt using Gemini..."):
        logo_prompt = generate_prompt(company_name, industry, brand_values, target_audience, design_style, color_palette, typography, icon_type, mandatory_elements, mood)

    st.subheader("✨ Gemini-Generated Prompt:")
    st.markdown(f"```{logo_prompt}```")

    with st.spinner("🎨 Generating logo with Stable Diffusion..."):
       try:
          image_bytes = query_huggingface(logo_prompt)
          image = Image.open(BytesIO(image_bytes))
          st.image(image, caption="Generated Logo", use_column_width=True)

          buf = BytesIO()
          image.save(buf, format="PNG")
          st.download_button(
             label="⬇️ Download Logo",
             data=buf.getvalue(),
             file_name=f"{company_name.lower().replace(' ', '_')}_logo.png",
             mime="image/png",
          )
          
       except Exception as e:
            st.error("❌ Error generating image. Please try again.")
            st.code(str(e))

            # Check if the model is cold starting
            if "loading" in str(e).lower() or "currently loading" in str(e).lower():
                st.info("⏳ The Hugging Face model is warming up. Please wait 30–60 seconds and try again.")



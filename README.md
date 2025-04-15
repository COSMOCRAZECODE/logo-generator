# AI Logo Generator 🎨

This Streamlit web app uses Gemini (Google AI) and Hugging Face's Stable Diffusion to generate custom tech logos based on user input.

## Features

- Gemini (LLM) generates a creative prompt from your logo preferences.
- Logo Diffusion (Stable Diffusion model) converts the prompt into a beautiful image.
- Simple UI for non-tech users.
- Downloadable PNG logo.

## How to Use

1. Enter details like company name, style, color, and mood.
2. Gemini creates a prompt for the logo.
3. The app generates and displays the logo.
4. Click to download it!

## Deploy Your Own

Add the following to Streamlit secrets:
- `HUGGINGFACE_TOKEN`
- `GEMINI_API_KEY`


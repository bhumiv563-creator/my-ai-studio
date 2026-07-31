import asyncio
import os
import streamlit as st
import edge_tts
import requests
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title="AI Animation Studio",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 AI Animated Video & Storyboard Studio")
st.markdown("Create multi-scene animated video concepts, render scene styles, and generate voiceover audio seamlessly!")

# Sidebar controls
st.sidebar.header("Studio Controls")
animation_style = st.sidebar.selectbox(
    "Select Art Style",
    ["3D Pixar/Disney", "Studio Ghibli Anime", "Cyberpunk", "Claymation", "Comic Book"]
)

user_prompt = st.text_area(
    "Enter your animation concept or nursery rhyme:",
    value="A stylish cartoon horse wearing sunglasses and a colorful Indian turban dancing to a Bollywood beat."
)

if st.button("🚀 Generate Studio Storyboard"):
    if not user_prompt:
        st.warning("Please enter a concept prompt first.")
    else:
        with st.spinner("Drafting multi-scene animation storyboard..."):
            # Mocking scene breakdown based on user input
            scenes = [
                {
                    "scene": 1,
                    "title": "The Grand Hook",
                    "description": f"Wide shot in {animation_style} style: {user_prompt}",
                    "dialogue": "What if tradition had a brand new beat drop?",
                    "voice": "en-US-AriaNeural"
                },
                {
                    "scene": 2,
                    "title": "The Village Journey",
                    "description": f"Close-up tracking shot in {animation_style} style: The character moves through a bustling vibrant street.",
                    "dialogue": "Bringing energy straight to the heart of the village!",
                    "voice": "en-US-GuyNeural"
                },
                {
                    "scene": 3,
                    "title": "The Grand Finale",
                    "description": f"Cinematic group celebration shot in {animation_style} style with confetti.",
                    "dialogue": "Keep the energy looping and never stop dancing!",
                    "voice": "en-US-AriaNeural"
                }
            ]

            st.session_state['scenes'] = scenes
            st.success("Storyboard generated successfully!")

# Display Scenes if available
if 'scenes' in st.session_state:
    st.markdown("---")
    st.header("📋 Scene Storyboard & Production Hub")

    async def generate_audio(text, voice_name, output_file):
        communicate = edge_tts.Communicate(text, voice_name)
        await communicate.save(output_file)

    for idx, s in enumerate(st.session_state['scenes']):
        with st.container():
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader(f"Scene {s['scene']}: {s['title']}")
                st.write(f"**Visual Prompt:** {s['description']}")
                st.write(f"**Voiceover Dialogue:** _{s['dialogue']}_")
            
            with col2:
                audio_path = f"scene_{s['scene']}.mp3"
                if st.button(f"Generate Audio {s['scene']}", key=f"audio_btn_{idx}"):
                    with st.spinner("Synthesizing voice..."):
                        try:
                            asyncio.run(generate_audio(s['dialogue'], s['voice'], audio_path))
                            st.audio(audio_path)
                        except Exception as e:
                            st.error(f"Audio generation error: {e}")
            st.markdown("---")

import os
import time
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="ComicCraft",
    page_icon="🎨"
)

st.title("🎨 ComicCraft")
st.subheader("AI Comic Story Creator using Gemini")

story_idea = st.text_area(
    "Enter your comic story idea",
    placeholder="Example: A student discovers a mysterious robot in his college..."
)

characters = st.text_area(
    "Enter the characters",
    placeholder="Example: Arun - student, Robo - friendly robot"
)

if st.button("✨ Generate Comic Story"):

    if not story_idea.strip():
        st.warning("Please enter a story idea.")

    elif not API_KEY:
        st.error("Gemini API key not found in .env file.")

    else:
        with st.spinner("Creating your comic story..."):

            client = genai.Client(api_key=API_KEY)

            prompt = f"""
Create a creative comic story based on the following information.

Story Idea:
{story_idea}

Characters:
{characters}

Requirements:
1. Give the comic a title.
2. Divide the story into 6 comic panels.
3. For each panel include:
   - Scene
   - Character dialogue
   - Short narration
4. Use simple and engaging language.
5. Return only the comic story.
"""


        try:
            response = None

            for attempt in range(3):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )
                    break

                except Exception as error:
                    if "503" in str(error) and attempt < 2:
                        time.sleep(3 * (attempt + 1))
                    else:
                        raise error

            st.success("Comic story generated successfully!")
            st.subheader("📖 Your Comic Story")
            st.write(response.text)

        except Exception as e:
            st.error(f"Error: {e}")
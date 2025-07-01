import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai # New import for Google Gemini

# --- Configuration for Environment Variables ---
# Load environment variables from .env file for secure API key handling
load_dotenv()

# Retrieve Google Gemini API Key from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Google Gemini Model Configuration ---
gemini_model = None # Initialize to None

if not GOOGLE_API_KEY:
    st.error("Google Gemini API Key not found. Please check your .env file.")
    st.info("You need to create a '.env' file in this folder and add your Google API Key.")
    st.info("Example .env content:\nGOOGLE_API_KEY=\"YOUR_ACTUAL_GOOGLE_GEMINI_API_KEY_HERE\"")
else:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        # Initialize the Gemini model here, AFTER genai.configure()
        # We'll try 'gemini-1.5-flash' as it's often broadly available.
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        st.success("Google Gemini API Key loaded and model initialized successfully. Ready to connect!")
    except Exception as e:
        st.error(f"Failed to configure Google Gemini API or initialize model: {e}")
        st.info("Please double-check your GOOGLE_API_KEY in the .env file and your internet connection.")


# --- Streamlit UI Setup ---
st.set_page_config(layout="wide") # Makes the app use more screen width
st.title("HealthAI: Intelligent Healthcare Assistant")

st.write("Welcome to HealthAI! How can I assist you today?")

# Placeholder for user input for Patient Chat
user_input = st.text_input("Ask me a health question:", key="chat_input")

# --- Patient Chat Section (Scenario 4) using Google Gemini ---
if user_input:
    st.write(f"You asked: {user_input}")
    with st.spinner("HealthAI is thinking..."): # Show a spinner while AI processes
        ai_response = "Error: AI model not initialized. Please ensure your GOOGLE_API_KEY is correct in .env and try again."

        if gemini_model: # Only proceed if the Gemini model was successfully initialized
            try:
                # Constructing a prompt for health questions
                prompt_template = f"""
                You are HealthAI, a helpful and empathetic healthcare assistant.
                Your primary goal is to provide general health information and clarify medical concepts.
                You must NEVER provide medical advice, diagnose conditions, or prescribe treatments.
                Always encourage the user to consult a qualified healthcare professional for any medical concerns.

                User: {user_input}
                HealthAI:
                """
                # Generate response from Gemini model
                response = gemini_model.generate_content(prompt_template)
                ai_response = response.text

                # A final safety check/addition to the response
                # This ensures a medical disclaimer is almost always present in health-related responses
                if "consult a doctor" not in ai_response.lower() and \
                   "medical advice" not in ai_response.lower() and \
                   "healthcare professional" not in ai_response.lower() and \
                   "qualified medical professional" not in ai_response.lower():
                    ai_response += "\n\n*Important:* Please consult a qualified healthcare professional for any medical concerns or before making health decisions. This information is for general knowledge only."

            except Exception as e:
                st.error(f"An error occurred while communicating with the Google Gemini model: {e}")
                ai_response = "I'm sorry, I encountered an issue while trying to get an answer. Please try again later."
        else:
            # This else block is for when gemini_model is None (due to API key error)
            st.error("Google Gemini model is not configured. Please check your .env file and ensure the GOOGLE_API_KEY is correct.")

    st.write(f"HealthAI says: {ai_response}")

st.markdown("---")
st.subheader("Disclaimer")
st.warning("HealthAI provides general information and is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional for any medical concerns.")

# You will add more sections for Disease Prediction, Treatment Plans, Health Analytics later.
# For now, this basic structure confirms your setup

import streamlit as st 
import google.generativeai as ai
from environs import Env
from streamlit.components.v1 import html

env = Env()
env.read_env()  # Reads .env file
api_key = env('API_KEY')

if api_key is None:
    st.error("Please provide the api key for accessing AI model.")
    st.stop()

ai.configure(api_key=api_key)


sys_prompt = """You are a helpful Python programming language expert. 
                People will provide you with their python code. If they entered python code then, 
                You will provide :
                1. **Bugs Report** : find bugs, syntax or any other errors in the submitted python code.
                2. **Corrected Code** : provide corrected python code with explanation for each line.
                3. **Suggestions** : Analyse the corrected python code(which you created) and suggest where the code can be further improved for readability, resuability, speed,etc. to make a better python code.
                If the code is not in python politely remind the user that you are a python code review assistant. """
model = ai.GenerativeModel(model_name="models/gemini-1.5-flash", system_instruction=sys_prompt)

st.set_page_config(
    page_title="Python Code Reviewer",
    layout="wide",
)

st.markdown(
    """
    <style>
    body {
        background-color: #D3D3D3; /* Light grey background */
        color: #000; /* Dark text color for readability */
    }
    h1, h2, h3, h4, h5, h6 {
        color: #d50000; /* A darker shade for headings */
    }
    .stButton>button {
        background-color: #003366; /* Button background color */
        color: white; /* Button text color */
        border-radius: 8px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #b00000; /* Darker red on hover */
        color: white;
    }
    .footer {
    position: fixed; /* Fixed position */
    left: 100;
    bottom: 0;
    width: 100%; /* Full width */
    background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent background */
    color: black; /* Text color */
    text-align: center; /* Centered text */
    padding: 10px; /* Padding */
    z-index: 1000; /* High z-index to overlay above other elements */
    }
    .stSidebar {
        background-color: #ffe0b2; /* Light sidebar background */
        color: #333; /* Dark text in sidebar */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Page Header
st.markdown("""
    <div style="text-align: right; padding: 1px;">
        <p>Created by Ritik Raturi<p>
    </div>
    <div style="text-align: center; padding: 20px;">
        <h1> <span style="color: var(--primaryColor)">Python Code Reviewer🕵️</span></h1>
        <p>Some bugs 🐛 in your python code 💻 ? Enter code below and we will make it bugs free ✨</p>
    </div>
""", unsafe_allow_html=True)

# Page Footer
st.markdown("""
    <div class="footer" style="position: fixed; bottom: 0; width: 100%; background-color: #1E1E1E; color: #e0e0e0; text-align: center; padding: 9px; font-size: 12px;">
        Powered by Google Gemini AI & Streamlit
    </div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown("""
    <h2 style="text-align: center; color: var(--primaryColor)">Useful Links</h2>
    <hr style="border: 2px solid #ddd;">
""", unsafe_allow_html=True)

# Sidebar Buttons
if st.sidebar.button("Home"):
    st.session_state.page = "Home"
if st.sidebar.button("Python Documentation"):
    js = f"window.open('{'https://docs.python.org/3/'}', '_blank')"
    html(f"<script>{js}</script>")  
if st.sidebar.button("Learn Python"):
    js = f"window.open('{'https://docs.python-guide.org/intro/learning/'}', '_blank')"
    html(f"<script>{js}</script>")

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Content for Each Page
if st.session_state.page == "Home":
    st.markdown("""
    #### Features:
    - Identifies bugs and suggests corrections
    - Provides complete corrected code (with explanation)
    - Provides suggestions on further improving the corrected code & improved code example based on these suggestions
    """)
    
    st.markdown("All with the help of **AI**. _Hard to believe? just try it!_")

    # Code Input
    user_prompt = st.text_area("Enter your Python Code :", placeholder="Type/paste your python code here...",height = 400)
    
    btn_clicked = st.button("Find bugs")

    if btn_clicked:
        st.write("Finding answer, kindly wait")
        try:
            response = model.generate_content(user_prompt)
            st.write(response.text)

        except Exception as e:
            st.error(f"An error occurred: {e}")

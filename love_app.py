# love_app.py
import streamlit as st
import requests
from streamlit.components.v1 import html

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'main'

# DeepSeek API configuration
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {st.secrets['DEEPSEEK_KEY']}",
    "Content-Type": "application/json"
}

def generate_love_quote():
    """Generate AI love quote using DeepSeek's API"""
    prompt = """Generate a unique, romantic love quote. Follow these rules:
    1. Maximum 15 words
    2. Include a metaphor about nature
    3. Use passionate but elegant language
    4. No clichés like 'heart of gold'"""
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a romantic poet."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 50
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, json=data, headers=HEADERS)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"Error generating quote: {str(e)}")
        return "Your love is my eternal sunrise, forever painting my world with warmth."

# Load HTML content from Love.html
with open("Love.html", "r") as f:
    heart_html = f.read()

def main_page():
    """Display the heart animation with button"""
    # Display heart animation by passing HTML string to the component
    html(heart_html, height=800)
    
    if st.button("💝 Generate Special Love Message 💝", key="main_button"):
        st.session_state.page = 'quotes'

def quotes_page():
    """Display AI-generated love quotes"""
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style='color: #ff6b6b;'>For My Beloved Maurine</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate and display quote
    if 'current_quote' not in st.session_state:
        st.session_state.current_quote = generate_love_quote()
    
    # Quote display styling
    st.markdown(f"""
    <div style='
        padding: 30px;
        border-radius: 15px;
        background: #fff3f3;
        margin: 20px auto;
        max-width: 600px;
        color: #333;
        font-size: 1.4em;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        min-height: 150px;
        display: flex;
        align-items: center;
        justify-content: center;
    '>
        💖 {st.session_state.current_quote} 💖
    </div>
    """, unsafe_allow_html=True)
    
    # Control buttons
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("✨ New Love Message ✨"):
            st.session_state.current_quote = generate_love_quote()
            st.rerun()
    with col2:
        if st.button("🔙 Back to Heart"):
            st.session_state.page = 'main'
            st.rerun()

# Page routing
if st.session_state.page == 'main':
    main_page()
else:
    quotes_page()
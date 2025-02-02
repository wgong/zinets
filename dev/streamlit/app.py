import streamlit as st
import json
from typing import Dict, Any
import re

# Set page config
st.set_page_config(
    page_title="Chinese Character Explorer",
    page_icon="🈶",
    layout="wide"
)

# Custom CSS for cards with enhanced hover effects
st.markdown("""
<style>
    .stCard {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .stCard:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
        cursor: pointer;
    }
    
    .meaning-card {
        background-color: #E3F2FD;
        border: 1px solid #BBDEFB;
    }
    .meaning-card:hover {
        background-color: #BBDEFB;
    }
    
    .structure-card {
        background-color: #F3E5F5;
        border: 1px solid #E1BEE7;
    }
    .structure-card:hover {
        background-color: #E1BEE7;
    }
    
    .pronunciation-card {
        background-color: #E8F5E9;
        border: 1px solid #C8E6C9;
    }
    .pronunciation-card:hover {
        background-color: #C8E6C9;
    }
    
    .etymology-card {
        background-color: #FFF3E0;
        border: 1px solid #FFE0B2;
    }
    .etymology-card:hover {
        background-color: #FFE0B2;
    }
    
    .characters-card {
        background-color: #F1F8E9;
        border: 1px solid #DCEDC8;
    }
    .characters-card:hover {
        background-color: #DCEDC8;
    }
    
    .homophonic-card {
        background-color: #E0F7FA;
        border: 1px solid #B2EBF2;
    }
    .homophonic-card:hover {
        background-color: #B2EBF2;
    }
    
    .phrases-card {
        background-color: #FBE9E7;
        border: 1px solid #FFCCBC;
    }
    .phrases-card:hover {
        background-color: #FFCCBC;
    }
    
    .idioms-card {
        background-color: #E8EAF6;
        border: 1px solid #C5CAE9;
    }
    .idioms-card:hover {
        background-color: #C5CAE9;
    }
    
    .sentences-card {
        background-color: #F9FBE7;
        border: 1px solid #F0F4C3;
    }
    .sentences-card:hover {
        background-color: #F0F4C3;
    }
    
    .stories-card {
        background-color: #E0F2F1;
        border: 1px solid #B2DFDB;
    }
    .stories-card:hover {
        background-color: #B2DFDB;
    }
    
    .poetry-card {
        background-color: #FCE4EC;
        border: 1px solid #F8BBD0;
    }
    .poetry-card:hover {
        background-color: #F8BBD0;
    }
    
    .card-title {
        color: #1f77b4;
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .card-content {
        color: #2c3e50;
        font-size: 1em;
    }
    
    .chat-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
    }
    
    .chat-message {
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 5px;
    }
    
    .user-message {
        background-color: #e3f2fd;
        margin-left: 20px;
    }
    
    .bot-message {
        background-color: #f5f5f5;
        margin-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

def extract_character_from_filename(filename: str) -> str:
    """Extract character from filename pattern <character>-1.json"""
    match = re.match(r"([^-]+)-\d+\.json", filename)
    return match.group(1) if match else "Unknown Character"

def create_card(title: str, content: Any, card_type: str) -> None:
    """Create a styled card with title and content."""
    st.markdown(f"""
        <div class="stCard {card_type}-card">
            <div class="card-title">{title}</div>
            <div class="card-content">
                {content if isinstance(content, str) else '<br>'.join(content)}
            </div>
        </div>
    """, unsafe_allow_html=True)

def initialize_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat():
    """Display the chatbot interface in the sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.header("Chat Assistant")
    
    # Initialize chat history
    initialize_chat_history()
    
    # Display chat history
    for message in st.session_state.messages:
        with st.sidebar.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.sidebar.chat_input("Ask about the character..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Add assistant response
        response = f"Here's what I know about your question: '{prompt}'\n\nLet me help you understand more about this character based on the available data."
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        st.sidebar.rerun()

def main():
    st.title("Chinese Character Explorer")
    
    # File upload section
    st.sidebar.header("Upload Data")
    uploaded_file = st.sidebar.file_uploader("Upload JSON file", type=['json'])
    
    # Load data
    if uploaded_file is not None:
        try:
            character_data = json.load(uploaded_file)
            st.sidebar.success("File uploaded successfully!")
            
            # Extract character from filename
            character = extract_character_from_filename(uploaded_file.name)
            st.markdown(f"## {character}")
            
        except json.JSONDecodeError:
            st.sidebar.error("Error: Invalid JSON file")
            character_data = load_default_data()
            character = "东"
    else:
        character_data = load_default_data()
        character = "东"
    
    st.markdown(f"# {character} (Character)")
    st.markdown("---")

    # Create 4x3 grid layout
    col1, col2, col3, col4 = st.columns(4)
    
    # Distribute cards across columns
    columns = [col1, col2, col3, col4]
    card_data = [
        ("Meaning (含义)", character_data["含义"], "meaning"),
        ("Structure (字形)", character_data["字形"], "structure"),
        ("Pronunciation (读音)", character_data["读音"], "pronunciation"),
        ("Etymology (字源)", character_data["字源"], "etymology"),
        ("Characters with 东 (含此字的字)", character_data["含此字的字"], "characters"),
        ("Homophonic Characters (同音字)", character_data["同音字"], "homophonic"),
        ("Common Phrases (常用词组)", character_data["常用词组"], "phrases"),
        ("Idioms (成语)", character_data["成语"], "idioms"),
        ("Example Sentences (例句)", character_data["例句"], "sentences"),
        ("Stories (短故事)", character_data["短故事"], "stories"),
        ("Poetry (诗词)", character_data["诗词"], "poetry")
    ]
    
    # Distribute cards evenly across columns
    for idx, (title, content, card_type) in enumerate(card_data):
        with columns[idx % 4]:
            create_card(title, content, card_type)
    
    # Display chat interface in sidebar
    display_chat()
    
    # Footer
    st.markdown("---")
    st.markdown("*Upload your own character data JSON file using the sidebar, or explore the default character.*")

def load_default_data():
    """Load the default character data."""
    return {
        "含义": "The character '东' means 'east'. It represents the direction of the sunrise and is often associated with beginnings, renewal, and the source of light and life.",
        "字形": "The character '东' is composed of two parts: the left part is a simplified form of '木' (tree), and the right part is a simplified form of '日' (sun). Together, they symbolize the sun rising through the trees, indicating the east.",
        "读音": "The pronunciation of '东' is 'dōng' in Mandarin Chinese, with the first tone.",
        "字源": "The character '东' originates from ancient pictographs depicting the sun rising behind a tree. Over time, it evolved into its current simplified form.",
        "含此字的字": [
            "陈 (chén)", "冻 (dòng)", "栋 (dòng)", "鸫 (dōng)", "岽 (dōng)"
        ],
        "同音字": [
            "冬 (dōng)", "咚 (dōng)", "氡 (dōng)"
        ],
        "常用词组": [
            "东方 (dōng fāng) - East",
            "东西 (dōng xi) - Thing",
            "东北 (dōng běi) - Northeast",
            "东南 (dōng nán) - Southeast",
            "东风 (dōng fēng) - East wind"
        ],
        "成语": [
            "东山再起 (dōng shān zài qǐ) - To stage a comeback",
            "东张西望 (dōng zhāng xī wàng) - To look around in all directions",
            "东施效颦 (dōng shī xiào pín) - Blind imitation with ludicrous effect",
            "东窗事发 (dōng chuāng shì fā) - The secret is out"
        ],
        "例句": [
            "太阳从东方升起。 (Tài yáng cóng dōng fāng shēng qǐ.) - The sun rises from the east.",
            "他来自东北。 (Tā lái zì dōng běi.) - He comes from the northeast."
        ],
        "短故事": [
            "In ancient China, the east was considered the most auspicious direction. Emperors would face east during important ceremonies to symbolize their connection to the rising sun and the renewal of life.",
            "There is a famous story about a man who moved to the east to start a new life. He built a house facing east, believing it would bring him good fortune and success."
        ],
        "诗词": [
            "《登鹳雀楼》 - 王之涣 (Dēng Guàn Què Lóu - Wáng Zhī Huàn)\n白日依山尽，黄河入海流。\n欲穷千里目，更上一层楼。\n(The sun sets behind the mountains, the Yellow River flows into the sea.\nTo see a thousand miles further, climb one more floor.)",
            "《静夜思》 - 李白 (Jìng Yè Sī - Lǐ Bái)\n床前明月光，疑是地上霜。\n举头望明月，低头思故乡。\n(Bright moonlight before my bed, I suspect it's frost on the ground.\nI raise my head to gaze at the moon, then lower it, thinking of home.)"
        ]
    }

if __name__ == "__main__":
    main()
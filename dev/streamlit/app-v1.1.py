import streamlit as st
import json
from typing import Dict, Any

# Set page config
st.set_page_config(
    page_title="Chinese Character Explorer",
    page_icon="🈶",
    layout="wide"
)

# Custom CSS for cards
st.markdown("""
<style>
    .stCard {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e6e6e6;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
</style>
""", unsafe_allow_html=True)

def create_card(title: str, content: Any) -> None:
    """Create a styled card with title and content."""
    st.markdown(f"""
        <div class="stCard">
            <div class="card-title">{title}</div>
            <div class="card-content">
                {content if isinstance(content, str) else '<br>'.join(content)}
            </div>
        </div>
    """, unsafe_allow_html=True)

def load_default_data() -> Dict:
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
            "《登鹳雀楼》 - 王之涣 (Dēng Guàn Què Lóu - Wáng Zhī Huàn)<br>白日依山尽，黄河入海流。<br>欲穷千里目，更上一层楼。<br>(The sun sets behind the mountains, the Yellow River flows into the sea.<br>To see a thousand miles further, climb one more floor.)",
            "《静夜思》 - 李白 (Jìng Yè Sī - Lǐ Bái)<br>床前明月光，疑是地上霜。<br>举头望明月，低头思故乡。<br>(Bright moonlight before my bed, I suspect it's frost on the ground.<br>I raise my head to gaze at the moon, then lower it, thinking of home.)"
        ]
    }

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
        except json.JSONDecodeError:
            st.sidebar.error("Error: Invalid JSON file")
            character_data = load_default_data()
    else:
        character_data = load_default_data()
    
    # Display character title
    st.markdown(f"## 东 (East)")
    st.markdown("---")

    # Create 4x3 grid layout
    col1, col2, col3, col4 = st.columns(4)
    
    # Distribute cards across columns
    columns = [col1, col2, col3, col4]
    card_data = [
        ("Meaning (含义)", character_data["含义"]),
        ("Structure (字形)", character_data["字形"]),
        ("Pronunciation (读音)", character_data["读音"]),
        ("Etymology (字源)", character_data["字源"]),
        ("Characters with 东 (含此字的字)", character_data["含此字的字"]),
        ("Homophonic Characters (同音字)", character_data["同音字"]),
        ("Common Phrases (常用词组)", character_data["常用词组"]),
        ("Idioms (成语)", character_data["成语"]),
        ("Example Sentences (例句)", character_data["例句"]),
        ("Stories (短故事)", character_data["短故事"]),
        ("Poetry (诗词)", character_data["诗词"])
    ]
    
    # Distribute cards evenly across columns
    for idx, (title, content) in enumerate(card_data):
        with columns[idx % 4]:
            create_card(title, content)
    
    # Footer
    st.markdown("---")
    st.markdown("*Upload your own character data JSON file using the sidebar, or explore the default '东' character.*")

if __name__ == "__main__":
    main()
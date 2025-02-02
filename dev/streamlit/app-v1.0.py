import streamlit as st
import json

# Set page config
st.set_page_config(
    page_title="Chinese Character Explorer",
    page_icon="🈶",
    layout="wide"
)

# Load data
character_data = {
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

# Title and introduction
st.title("东 (East) - Chinese Character Explorer")
st.markdown("---")

# Create two columns for the main layout
col1, col2 = st.columns([1, 1])

with col1:
    # Basic information section
    st.header("Basic Information")
    st.subheader("Meaning (含义)")
    st.write(character_data["含义"])
    
    st.subheader("Character Structure (字形)")
    st.write(character_data["字形"])
    
    st.subheader("Pronunciation (读音)")
    st.write(character_data["读音"])
    
    st.subheader("Etymology (字源)")
    st.write(character_data["字源"])

    # Characters containing this component
    st.header("Related Characters")
    col1_1, col1_2 = st.columns(2)
    
    with col1_1:
        st.subheader("Characters with 东 (含此字的字)")
        for char in character_data["含此字的字"]:
            st.write(char)
    
    with col1_2:
        st.subheader("Homophonic Characters (同音字)")
        for char in character_data["同音字"]:
            st.write(char)

with col2:
    # Common words and phrases
    st.header("Usage")
    st.subheader("Common Phrases (常用词组)")
    for phrase in character_data["常用词组"]:
        st.write(phrase)
    
    st.subheader("Idioms (成语)")
    for idiom in character_data["成语"]:
        st.write(idiom)
    
    st.subheader("Example Sentences (例句)")
    for sentence in character_data["例句"]:
        st.write(sentence)

# Create an expander for additional content
with st.expander("Stories and Poetry"):
    # Stories section
    st.subheader("Stories (短故事)")
    for story in character_data["短故事"]:
        st.write(story)
        st.write("---")
    
    # Poetry section
    st.subheader("Poetry (诗词)")
    for poem in character_data["诗词"]:
        st.write(poem)
        st.write("---")

# Footer
st.markdown("---")
st.markdown("*This app provides comprehensive information about the Chinese character '东' (East).*")
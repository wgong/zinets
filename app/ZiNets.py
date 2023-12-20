"""
# TODO
[2023-08-26]
- compile and build ZiNets app - multimodal/multilingual Chinese dictionary powered by AI
- 


"""

from utils import *

st.set_page_config(
     page_title='ZiNets',
     layout="wide",
     initial_sidebar_state="expanded",
)

readme_md = open("README.md", encoding="utf-8").read()
st.markdown(readme_md, unsafe_allow_html=True)

# load config params into memory
# st.session_state["TABLE_CHATS"] = CFG["TABLE_CHATS"]

# detect table's existence, if no, create it

with DBConn() as _conn:
    for table_name in CFG["TABLES"].keys():
        db_create_table(table_name, _conn, drop_table=False)


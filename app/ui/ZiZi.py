"""
ZiZi app prototype in streamlit

#=======
# TODO
#=======

[2024-01-29]
- Visualize Zi in tree structures
- Design Zi app for end-user
- Integrate with AI for pronounciation, Chinese-to-English translation, text-to-image
- create a new page to log activities
- prepare AI app proposal (deadline 2024-03-01)

[2024-01-04]
- incorporate work at https://github.com/kfcd/chaizi 


[2023-12-23]
- build an emoji lookup tool 
    - scrape and parse 2000 emojis into CSV (https://unicode.org/emoji/charts/full-emoji-list.html)
    - seq_num, unicodes, sample, browser, category, CLDR Short Name
- add unicode as id for Zi
- refine t_part table based on https://unicode.org/charts/nameslist/
    - Kangxi Radicals
    - CJK Radicals Supplement
    - CJK Strokes


[2023-12-20]
- build Zi-Editor UI
- refine Zi-Manager UI
- leverage AI assistants like Bard, Claude for this project

#=======
# DONE
#=======

[2024-01-28]
- completed decomposing  HSK2000 Zi's

[2024-01-18]
- bulk-update in SQLite, see zizi\devs\sql\parts_count-20240118.csv

[2023-08-26]
- compile and build ZiNets app - multimodal/multilingual Chinese dictionary powered by AI


"""

from utils import *

st.set_page_config(
     page_title='ZiZi 字子',
     layout="wide",
     initial_sidebar_state="expanded",
)

readme_md = open("README.md", encoding="utf-8").read()
st.markdown(readme_md, unsafe_allow_html=True)

# load config params into memory
# st.session_state["TABLE_CHATS"] = CFG["TABLE_CHATS"]

# detect table's existence, if no, create it

# with DBConn() as _conn:
#     for table_name in CFG["TABLES"].keys():
#         db_create_table(table_name, _conn, drop_table=False)


from utils import *

from datetime import datetime

st.set_page_config(layout="wide")
st.subheader("字网 Editor")

ZI_PARTS = [
    "zi_left_up", "zi_up", "zi_right_up",
    "zi_left", "zi_mid", "zi_right",
    "zi_left_down", "zi_down", "zi_right_down",
    "zi_mid_back", "zi_mid_front"]

def main():
    col_left, col_right = st.columns([3,6])

    with col_left:
        with st.form(key="zi_parts"):
            c1_1,c1_2,c1_3 = st.columns(3)
            with c1_1:
                zi_left_up = st.text_input('左上', value="",  key="zi_left_up")
            with c1_2:
                zi_up = st.text_input('上', value="",  key="zi_up")
            with c1_3:
                zi_right_up = st.text_input("右上", value="",  key="zi_right_up")

            c2_1,c2_2,c2_3 = st.columns(3)
            with c2_1:
                zi_left = st.text_input('左', value="",  key="zi_left")
            with c2_2:
                zi_mid = st.text_input('中', value="",  key="zi_mid")
            with c2_3:
                zi_right = st.text_input("右", value="",  key="zi_right")

            c3_1,c3_2,c3_3 = st.columns(3)
            with c3_1:
                zi_left_down = st.text_input('左下', value="",  key="zi_left_down")
            with c3_2:
                zi_down = st.text_input('下', value="",  key="zi_down")
            with c3_3:
                zi_right_down = st.text_input("右下", value="",  key="zi_right_down")

            _,c4_1,_,c4_2,_ = st.columns([1,2,1,2,1])
            with c4_1:
                zi_mid_back = st.text_input('中后', value="",  key="zi_mid_back")
            with c4_2:
                zi_mid_front = st.text_input('中前', value="",  key="zi_mid_front")

            st.form_submit_button('Save', on_click=_submit_zi_parts, use_container_width=True)

def _submit_zi_parts():
    msg = []
    for p in ZI_PARTS:
        zp = st.session_state.get(p,"")
        if zp:
            msg.append(f"{p} : {zp}")
    
    st.info(",  ".join(msg))



if __name__ == '__main__':
    main()
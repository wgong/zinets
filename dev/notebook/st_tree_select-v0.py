import streamlit as st
from streamlit_tree_select import tree_select

if "selected" not in st.session_state:
    st.session_state.selected = []
if "expanded" not in st.session_state:
    st.session_state.expanded = []


st.title("🐙 Streamlit-tree-select")
st.subheader("A simple and elegant checkbox tree for Streamlit.")

# Create nodes to display
nodes = [
    {
        "label": "藻", "value": "藻",
        "children": [
            {"label": "艹", "value": "艹"},
            {
                "label": "喿", "value": "喿",
                "children": [
                    {
                        "label": "品", "value": "品",
                        "children": [
                            {"label": "口", "value": "口-1"},
                            {"label": "口", "value": "口-2"},
                            {"label": "口", "value": "口-3"},
                        ], 
                    }, 
                    {"label": "木", "value": "木"},
                ],
            },
        ],
    },
]

selected = tree_select(nodes, 
                    checked=st.session_state.selected, 
                    expanded=st.session_state.expanded,
                    # only_leaf_checkboxes=True, 
                    no_cascade=True,
                )
                    
                    
if len(selected["checked"]) > 1:
    st.session_state.selected = [x for x in selected["checked"] if x != st.session_state.selected[0]][0:1]
    st.session_state.expanded = selected["expanded"]
    # st.experimental_rerun()
    st.rerun()
    
else:
    st.session_state.selected = selected["checked"]
    st.session_state.expanded = selected["expanded"]  
    
st.write(selected)